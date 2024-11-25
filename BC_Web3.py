# Install web3.py if not already installed
!pip install web3

from web3 import Web3

# Use the ngrok URL to connect to Ganache
ganache_url = "https://ed5c-122-172-84-134.ngrok-free.app"  # Replace with your actual ngrok URL
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check if the connection is successful
if web3.is_connected():
    print("Connected to Ganache via ngrok")
else:
    print("Failed to connect")
# Contract address from Remix (after deployment)
contract_address = "0xb86246ad2e70b23aB9C586051167122Bac0bDdE3"  # Replace with your actual contract address

# ABI from Remix (after compilation)
contract_abi = [
	{
		"constant": False,
		"inputs": [
			{
				"name": "_targetIP",
				"type": "string"
			},
			{
				"name": "_packetCount",
				"type": "string"
			},
			{
				"name": "_bandwidthImpact",
				"type": "string"
			},
			{
				"name": "_attackPattern",
				"type": "string"
			},
			{
				"name": "_spreadPattern",
				"type": "string"
			},
			{
				"name": "_detectionStartTime",
				"type": "string"
			},
			{
				"name": "_detectionEndTime",
				"type": "string"
			}
		],
		"name": "logAttackSummary",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "getAttackSummary",
		"outputs": [
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "summary",
		"outputs": [
			{
				"name": "targetIP",
				"type": "string"
			},
			{
				"name": "packetCount",
				"type": "string"
			},
			{
				"name": "bandwidthImpact",
				"type": "string"
			},
			{
				"name": "attackPattern",
				"type": "string"
			},
			{
				"name": "spreadPattern",
				"type": "string"
			},
			{
				"name": "detectionStartTime",
				"type": "string"
			},
			{
				"name": "detectionEndTime",
				"type": "string"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	}
]

# Interact with the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Set the sender address (using the first account from Ganache)
sender_address = web3.eth.accounts[0]

# Function to store calculated attack data on blockchain
def logAttackSummary(targetIP, packetCount, bandwidthImpact, attackPattern, spreadPattern, detectionStartTime, detectionEndTime):
    # Send the transaction directly
    tx_hash = contract.functions.logAttackSummary(targetIP, packetCount, bandwidthImpact, attackPattern, spreadPattern, detectionStartTime, detectionEndTime).transact({'from': sender_address})
    web3.eth.wait_for_transaction_receipt(tx_hash)  # Wait for the transaction to be mined
    print("Attack info logged!")

# Function to get attack data from blockchain
def getAttackSummary():
    summary = contract.functions.getAttackSummary().call()

from datetime import datetime
# 1. Calculate targetIP (most frequently targeted IP)
targetIP = df_BC['DestinationIP'].mode()[0]

# 2. Calculate packetCount (total forward + backward packets)
packetCount = str(df_BC[' Total Fwd Packets'].sum() + df_BC[' Total Backward Packets'].sum())

# 3. Calculate bandwidthImpact (total forward + backward packet lengths)
bandwidthImpact = str(df_BC['Total Length of Fwd Packets'].sum() + df_BC[' Total Length of Bwd Packets'].sum())

# 4. Calculate attackPattern (check if packets per second are increasing)
df_BC['Timestamp'] = pd.to_datetime(df_BC[' Timestamp'])
df_BC = df_BC.sort_values(by='Timestamp')
df_BC['packets_per_second'] = df_BC[' Total Fwd Packets'] + df_BC[' Total Backward Packets']
attackPattern = "increasing" if df_BC['packets_per_second'].is_monotonic_increasing else "stable"

# 5. Determine spreadPattern (confined or spreading based on unique DestinationIP)
spreadPattern = "spreading" if df_BC['DestinationIP'].nunique() > 1 else "confined"

# 6. Detection start and end times
detectionStartTime = df_BC['Timestamp'].min().timestamp()
detectionEndTime = df_BC['Timestamp'].max().timestamp()
detection_Start_Time = datetime.fromtimestamp(detectionStartTime).strftime('%d-%m-%Y %H:%M:%S.%f')
detection_End_Time = datetime.fromtimestamp(detectionEndTime).strftime('%d-%m-%Y %H:%M:%S.%f')

# Make function calls to store actual calculated info on blockchain & retrieve from bc
logAttackSummary(targetIP, packetCount, bandwidthImpact, attackPattern, spreadPattern, detection_Start_Time, detection_End_Time)
getAttackSummary()