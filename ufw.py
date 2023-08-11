import copy
import time
import torch
import argparse
import bittensor as bt
import subprocess

# Function to resynchronize with the Bittensor metagraph
def resync_metagraph():
    bt.logging.info("resync_metagraph()")
    
    # Make a deep copy of the current metagraph
    previous_metagraph = copy.deepcopy(metagraph)
    
    # Sync the local metagraph with the remote metagraph
    metagraph.sync(subtensor=subtensor)
    
    # Check if the metagraph's axon info has changed since the last sync
    metagraph_axon_info_updated = previous_metagraph.axons != metagraph.axons
    
    # Log a message if the metagraph has been updated
    if metagraph_axon_info_updated:
        bt.logging.info("Metagraph updated, re-syncing hotkeys")
    
    bt.logging.info("Metagraph synced!")

# Function to check the top 50 UIDs in the metagraph and extract their IPs
def check_metagraph():
    bt.logging.info("check_metagraph()")
    
    # Extract the indices of the top 50 stakes
    indices = torch.topk(metagraph.stake, 50).indices
    
    # Extract the corresponding UIDs
    uids_with_highest_stake = metagraph.uids[indices].tolist()
    
    # Extract the corresponding axons
    axons = [metagraph.axons[uid] for uid in uids_with_highest_stake]
    
    # Extract the corresponding IPs
    ips = [axon.ip for axon in axons]
    
    # Pair the UIDs with their IPs and remove duplicates
    unique_ip_to_uid = {ip: uid for ip, uid in zip(ips, uids_with_highest_stake)}
    ips = list(unique_ip_to_uid.keys())
    
    bt.logging.info(f"Top 50 uids: {uids_with_highest_stake}")
    
    return ips

# Function to whitelist IPs in UFW (Uncomplicated Firewall)
def whitelist_ips_in_ufw(ips):
    # Disable UFW
    stop_cmd = "sudo ufw disable"
    # Reset UFW
    reset_cmd = "echo y | sudo ufw reset"
    
    subprocess.run(stop_cmd, shell=True)
    subprocess.run(reset_cmd, shell=True)
    
    # Allow SSH connections
    ssh_cmd = "sudo ufw allow ssh"
    subprocess.run(ssh_cmd, shell=True)
    
    # Whitelist the provided IPs for TCP connections
    for ip in ips:
        cmd = f"sudo ufw allow proto tcp from {ip}/16"
        subprocess.run(cmd, shell=True)
        bt.logging.info(f"Whitelisted IP {ip} for bittensor")
    
    # Enable UFW
    start_cmd = "echo y | sudo ufw enable"
    subprocess.run(start_cmd, shell=True)

# Function to parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Run firewall")
    parser.add_argument('--netuid', help='Machine to connect to', choices=[1, 11, 21], default=1)
    
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    # Parse command line arguments
    args = parse_arguments()
    # Connect to Bittensor network
    subtensor = bt.subtensor(network="finney")
    # Initialize metagraph with netuid
    metagraph = subtensor.metagraph(netuid=args.netuid)

    # Infinite loop to keep the metagraph synced and firewall updated
    while True:
        # Resync the metagraph
        resync_metagraph()
        
        # Get the IPs of the top 50 validators
        ips = check_metagraph()
        
        # Transform the IPs to a specific format
        ips = [ip.split(".")[0] + "." + ip.split(".")[1] + ".0.0" for ip in ips]
        
        # Whitelist the IPs in UFW
        whitelist_ips_in_ufw(ips)
        
        # Wait for 100 blocks (approximately 1200 seconds or 20 minutes)
        bt.logging.info("Waiting for 100 blocks, sleeping")
        time.sleep(1200)
