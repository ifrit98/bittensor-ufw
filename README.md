# Bittensor UFW Configuration Tutorial
Howdy folks, this is a quick update to mitigate naive DDOS attacks. 

This guide will walk you through how to set up a firewall configuration for your Bittensor miner or validator using the provided script and PM2. This will help you keep your system secure while only allowing authorized connections. 

This helps maintain a nicely firewalled network that does not allow anyone to query it unless they are querying from a validator registered and recorded on the metagraph. 

By implementing firewall rules we all create a protected network that can only be accessed from the endpoints that we have recorded in the metagraph (miners and validators). This should also help stop random IPs from doing bad things, and ensure all things done are done via IPs recorded on the network. 

>> Note:
Having said this, validator owners should be careful now as you are the front facing entity, so you need to ensure you have rate limitations and proper firewalls (perhaps only accessible through your APIs) to stop attackers from DDOS-ing you. Miners should also stay vigilant. As the network grows, so will the number of people trying to break it.


If you encounter any issues, please refer to the official [Bittensor documentation](https://github.com/opentensor/docs) or reach out to the community support at the [Discord](https://discord.com/channels/799672011265015819/1096187495667998790).



## Prerequisites

1. **Python**: Make sure Python 3.x is installed.
2. **UFW (Uncomplicated Firewall)**: Ensure UFW is installed on your system.
3. **PM2**: You'll need PM2 for managing the process. You can install it globally using `npm install pm2 -g`.
4. **Bittensor**: Make sure you have Bittensor installed and properly configured.

## Steps

### 1. Clone the Repository

First, clone the repository containing the script.

```bash
git clone https://github.com/ifrit98/bittensor-ufw.git
cd bittensor-ufw
```

### 2. Install the Required Libraries

Before running the script, you must install the required libraries:

```bash
sudo apt update        # Update the package lists
sudo apt install ufw   # Install UFW
pip install bittensor  # Install bittensor
pip install validators # Install openvalidators (if running a validator)
```

### 3. Configure and Start the Script with PM2

Start the script using PM2:

```bash
pm2 start ufw.py --name ufw
```

This will start the UFW configuration script in the background, and PM2 will make sure it stays running.

### 4. Check the Status

You can check the status of the script using:

```bash
pm2 status ufw
```

### 5. Start Your Bittensor Miner/Validator

You can now start your Bittensor miner or validator as usual. The UFW script will automatically update the firewall rules to allow connections from the top 50 validators in the Bittensor network.

### 6. Additional PM2 Commands

- To view the logs:

  ```bash
  pm2 logs ufw
  ```

- To stop the script:

  ```bash
  pm2 stop ufw
  ```

- To restart the script:

  ```bash
  pm2 restart ufw
  ```

