import pandas as pd
import numpy as np
import pickle
import smtplib
from email.message import EmailMessage
import time
import subprocess
from datetime import datetime
import schedule

# Load the ML model
with open('ml_model.pkl', 'rb') as file:
    model = pickle.load(file)

alert_sent_flag = False

# Define threshold and blacklist dictionary for IP blocking
threshold_seconds = 60  # Threshold for blocking in seconds
blacklist = {}

# Calculate time difference
def calc_time_diff(packet_time):
    current_time = datetime.now()
    return (current_time - packet_time).total_seconds()

# Block an IP and add to blacklist
def block_ip(ip_address, packet_time):
    time_diff = calc_time_diff(packet_time)
    if time_diff < threshold_seconds and ip_address not in blacklist:
        blacklist[ip_address] = packet_time
        subprocess.run(f"iptables -A INPUT -s {ip_address} -j DROP", shell=True)
        print(f"IP {ip_address} is blocked due to suspicious activity")

# Unblock IPs exceeding threshold time
def unblock_ips():
    current_time = datetime.now()
    unblocked_ips = [ip for ip, pkt_time in list(blacklist.items()) 
                     if (current_time - pkt_time).total_seconds() > threshold_seconds]
    for ip in unblocked_ips:
        subprocess.run(f"iptables -D INPUT -s {ip} -j DROP", shell=True)
        del blacklist[ip]
        print(f"IP {ip} unblocked")

# Parse packet for DDoS detection
def parse_packet(line):
    # Example packet: "1 0.000000000 105.213.0.247 → 192.168.1.4 UDP 60 48347 → 0 Len=0"
    parts = line.split()
    timestamp = float(parts[1])  # Timestamp
    src_port = int(parts[7])  # Source Port
    dest_port = int(parts[9])  # Destination Port
    header_len = int(parts[6])  # Header length after "UDP"
    payload_len = int(parts[10].split('=')[1])  # Extract payload length from "Len=..."
    pkt_len = header_len + payload_len  # Total packet length
    return timestamp, src_port, dest_port, pkt_len

# ML prediction for DDoS detection
def ml_predict(content):
    global alert_sent_flag
    pkt_lens = []
    timestamps = []
    ip_addresses = []

    #print("Starting ML prediction...")
    for line in content:
        try:
            parts = line.split()
            ip_address = parts[2]  # Source IP address
            ip_addresses.append(ip_address)
            timestamp, src_port, dest_port, pkt_len = parse_packet(line)
            timestamps.append(timestamp)
            pkt_lens.append(pkt_len)
        except ValueError:
            #print("Skipping malformed line")
            continue  # Skip malformed lines

    # Ensure there are enough packets for flow duration calculation
    if len(timestamps) < 2:
        #print("Not enough packets for flow duration calculation. Exiting.")
        return

    # Calculate flow duration (difference between max and min timestamps)
    flow_duration = max(timestamps) - min(timestamps)

    total_pkt_len = sum(pkt_lens)
    avg_pkt_len = np.mean(pkt_lens) if pkt_lens else 0
    min_pkt_len = min(pkt_lens) if pkt_lens else 0
    packets_per_sec = len(pkt_lens) / (flow_duration + 1e-5)

    # Prepare data for prediction
    flow_data = np.array([src_port, dest_port, flow_duration, 
                          min_pkt_len, avg_pkt_len, total_pkt_len, packets_per_sec]).reshape(1, -1)

    # Model prediction
    y_pred = model.predict(flow_data)

    # If an attack is detected
    if y_pred == 1:
        # Block the detected source IPs
        for ip in ip_addresses:
            block_ip(ip, datetime.now())

    if alert_sent_flag == False:
            alert_sent_flag = True
            send_email_alert(
                subject="DDoS Detected",
                body="A UDP DDoS attack has started on the target server.",
                to="harini100.venky@gmail.com"
            )

# Email alert function
def send_email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = "pes2202100499@pesu.pes.edu"
    password = "owkztpvsneuzgtcy"

    msg['from'] = user
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()
  
# Schedule unblocking every 2 minutes
schedule.every(1).minutes.do(unblock_ips)

# Main Loop
while True:
    try:
        #print("Reading out.csv...")
        with open("out.csv", "r") as f:
            content = f.readlines()
            ml_predict(content)
        
        # Clear file content after processing
        #print("Clearing out.csv content...")
        with open("out.csv", "w"):
            pass

        # Run scheduled tasks
        schedule.run_pending()
    except FileNotFoundError:
    	pass
        #print("out.csv not found. Waiting for file...")
    except Exception as e:
    	pass
        #print(f"Error: {e}")
    time.sleep(1)


