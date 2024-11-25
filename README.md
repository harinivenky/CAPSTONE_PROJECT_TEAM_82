# CAPSTONE_PROJECT_TEAM_82
DDoS Detection and Prevention using ML and Blockchain

List of commands used : 
1) For UDP Flood Attack Simulation :
=> sudo hping3 --udp --flood --rand-source 192.168.1.9
2) For simulating legitimate udp traffic as a UDP Client :
=> sudo hping3 --udp -a 192.168.1.5 -i u990000 -p 12345 192.168.1.9
3) watch -n 10 "tshark -i eth0 -f 'udp and host 192.168.1.9' -a duration:2 -E separator=, >> out.csv" :
=> Command to monitor only udp traffic to victim vm [192.168.1.9] every 10s for a duration of 2s and save the Wireshark traffic as a csv file to out.csv.
4) netsh interface ip set address name = "Ethernet" 192.168.1.9 255.255.255.0 192.168.1.4
=> Command to set up kali Linux analytics vm as the default gateway of Windows vm, so that all the traffic that is being sent to victim vm [Windows] compulsorily passes through the analytics vm, on which a code checks if it is legitimate and only then forwards traffic to Windows. 

Explanation of purpose of each code file : 
1) Capstone_DDoS_ML.ipynb : ML Model Training Code
2) DDoS_dataset : CICDDoS2019 which can be found on Kaggle : https://www.kaggle.com/datasets/rodrigorosasilva/cic-ddos2019-30gb-full-dataset-csv-files
[ONLY DrDoS_UDP.csv HAS BEEN TAKEN AND USED FOR TRAINING]
3) ml_model.pkl : Pickle file containing the model, so, it can be loaded anywhere to make predictions
4) out.csv : Contains udp packets monitored by watch command for collecting Attack Summary required for incident analysis
5) ddos_ml_predict.py : The main code in which packets are flagged as malicious(1) or legitimate(0) by the ML Model and only if legitimate, forwarded to victim Windows vm, else, if predicted malicious, Gmail alert is sent to admin, IP addresses are extracted from the malicious packets and traffic from there is blocked. After a threshold set number of seconds, (2 minutes, here) the blocked IPs are slowly unblocked as we can't permanently block IP of legitimate machines infected by the attacker.
6) udpserver.ps1 : The code for creating & running a UDP Server listening and replying to requests from UDP Clients on the victim Windows vm.
7) bcDDoS.sol : Solidity smart contract code to store and retrieve calculated attack data to and from blockchain.
8) index.html : Design for webpage where the attack data retrieved from blockchain is displayed.
9) BC_Web3.py : Code for collecting and calculating attack data for incident analysis, its interaction/integration with blockchain and webpage using ngrok and web3.js. 
10) Cyber+Incident+Response+-+Generic+Denial+of+Service+Playbook+v2.3.pdf : A DDoS incident response playbook written by the organisation, NCC group, according to which attack information required for investigation is calculated.   
11) DDoS_Stats.png : Image of a pie graph showing 2023 Q2 Statistics for types of DDoS attack incidents that have occurred during the second quarter of 2023, according to medium.com. Full source reference : https://qratorlabs.medium.com/q2-2023-ddos-attacks-statistics-and-overview-698682abf508
12) output.pdf : Output screenshots of the project.

NOTE : PROJECT FILES ARE PROVIDED AS A ZIP FILE. DOWNLOAD AND UNZIP.
