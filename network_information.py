import speedtest 
import wifi
from pythonping import ping
import socket 
import struct

# Function to get download and upload speeds using speedtest-cli
def get_speed_test():
    st = speedtest.Speedtest()
    download_speed = st.download()
    upload_speed = st.upload()
    return download_speed, upload_speed

# Function to get information about all wifi signals picked up by the network card
def get_wifi_info():
    
    # Use the wifi library to retreieve information about available wifi signals
    cells = wifi.Cell.all('wlan0')
    
    # Create a list of dictionaries containing SSID and Signal Strength for each wifi signal
    wifi_info = [{'SSID' : cell.ssid, 'Signal Strength' : cell.signal} for cell in cells]
    
    return wifi_info

# Function to get local and public IP addresses
def get_ip_addresses():
    
    # Get the local hostname of the device
    hostname = socket.gethostname()
    
    # Resolve the local IP address
    local_ip = socket.gethostbyname(hostname)

    # Resolve the public IP address by querying an external server (google)
    public_ip = socket.gethostbyname('www.google.com')

    return local_ip, public_ip

# Function to get routing info 
def get_routing_info():
    
    # Initalise an empty list to store routing information
    routing_info = []

    # Open the '/proc/net/route' file to read routing information
    with open('/proc/net/route') as route_file:

        #Skip the header and iterate over the remaining lines
        for line in route_file.readlines()[1:]:
            
            # Split the line into fields
            fields = line.strip().split()

            # Extract the interface and gateway information
            interface = fields[0]

            # Convert the hex gateway value to an IP address
            gateway = socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

            # Append a dictionary with interface and gateway information to the routing_info list
            routing_info.append({'Interface' : interface, 'Gateway' : gateway})
    
    return routing_info

# Function to ping specified domains and get round-trip times
def ping_domains(domains):

    # Use the pythonping library to ping each specified domain and calculate round-trip times
    ping_results = {domain: ping(domain, count=3).rtt_avg for domain in domains}

    return ping_results

if __name__ == "__main__":

    # Get download and upload speeds
    download_speed, upload_speed = get_speed_test()
    print(f"Download Speed: {download_speed / 1024 / 1024:.2f} Mbps")
    print(f"Upload Speed: {upload_speed / 1024 / 1024:.2f} Mbps")

    # Get wifi information
    wifi_info = get_wifi_info()
    print("\n WiFi Information:")
    for info in wifi_info:
        print(f"SSID: {info['SSID']}, Signal Strength: {info['Signal Strength']} dBm")

    # Get local and public IP addresses
    local_ip, public_ip = get_ip_addresses()
    print(f"\nLocal IP Address: {local_ip}")
    print(f"Public IP Address: {public_ip}")

    # Get routing information
    routing_info = get_routing_info()
    print("\nRouting Information")
    for info in routing_info:
        print(f"Interface: {info['Interface']}, Gateway: {info['Gateway']}")

    # Ping specified domains and display results
    domains = ['reddit.com', 'bbc.com', 'youtube.com']
    ping_results = ping_domains(domains)
    print("\nPing Results:")
    for domain, rtt in ping_results.items():
        print(f"{domain}: {rtt:.2f} ms")

