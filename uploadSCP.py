import paramiko
from paramiko import SSHClient
from scp import SCPClient
from tqdm import tqdm
import os

# Custom progress bar callback
def progress_callback(filename, current, total):
    # Ensure filename is a string (some SCP implementations might provide bytes)
    filename = filename.decode() if isinstance(filename, bytes) else filename
    if filename not in progress_bars:
        # Create a new progress bar for each file
        progress_bars[filename] = tqdm(total=total, unit='B', unit_scale=True, unit_divisor=1024, desc=filename)
    progress_bars[filename].update(current - progress_bars[filename].n)

    # Close the progress bar when done
    if current == total:
        progress_bars[filename].close()
        del progress_bars[filename]

# Server details
hostname = '10.10.10.96'
username = 'ludwig'
password = 'ludwig123'

# Connect to the server
ssh = SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password)

# Create a dictionary to store progress bars for each file
progress_bars = {}

# Create an SCP client
with SCPClient(ssh.get_transport(), progress=progress_callback) as scp:
    # Define the local and remote paths
    local_folder = '/Users/ludwig.cho/Desktop/Ludwig/AsConvSR'
    remote_folder = '/home/ludwig/'

    # Recursively upload the folder with progress bar
    scp.put(local_folder, remote_folder, recursive=True)

# Close the connection
ssh.close()
