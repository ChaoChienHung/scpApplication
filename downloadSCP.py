import paramiko
from paramiko import SSHClient
from scp import SCPClient
from tqdm import tqdm


csv = "csv"
json = "json"
water_army = "test_set_for_water_amy"

csv_files = "2024-07-05.csv"
json_files = "2024-07-05.json"
water_army_files = "sampled_0720_10000_th.csv"

# hostname = '10.11.12.100'
# username = 'ulink'
# password = '7777777'

hostname = '10.90.66.201'
username = 'ludwig'
password = 'ludwig123'

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
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password)

progress_bars = {}

# # Download a file
# with SCPClient(ssh.get_transport()) as scp:
#     scp.get(f'/home/ulink/chat_room_data/data/{csv}/{csv_files}', '/Users/ludwig.cho/Desktop/Ludwig')

# Download a folder
with SCPClient(ssh.get_transport(), progress=progress_callback) as scp:
    path: str = "/home/ludwig/AsConvSR"
    scp.get(path, '/Users/ludwig.cho/Desktop/Ludwig/', recursive=True)
    # scp.get(f'/home/ulink/chat_room_data/data/{water_army}/', '/Users/ludwig.cho/Desktop/Ludwig/', recursive=True)

# Close the connection
ssh.close()
