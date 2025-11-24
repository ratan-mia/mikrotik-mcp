#!/usr/bin/env python3
"""Simple SSH test to MikroTik"""

import paramiko
import socket

def test_ssh():
    host = "202.84.44.49"
    port = 22  # Standard SSH port
    username = "Admin115"
    password = "@dminAhL#"
    
    print(f"Connecting to {host}:{port}...")
    
    try:
        # Create SSH client with minimal settings
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Create a socket first
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((host, port))
        print("✓ TCP connection established")
        
        # Connect SSH over the socket
        transport = paramiko.Transport(sock)
        transport.banner_timeout = 60
        transport.connect(username=username, password=password)
        print("✓ SSH authentication successful")
        
        # Open a session
        channel = transport.open_session()
        channel.settimeout(10)
        
        # Execute command to get DHCP leases
        print("\n" + "=" * 80)
        print("DHCP LEASES")
        print("=" * 80)
        channel.exec_command('/ip dhcp-server lease print detail where status=bound')
        output = channel.recv(65535).decode('utf-8', errors='ignore')
        print(output)
        channel.close()
        
        # New channel for ARP
        channel = transport.open_session()
        channel.settimeout(10)
        print("\n" + "=" * 80)
        print("ARP TABLE")
        print("=" * 80)
        channel.exec_command('/ip arp print detail')
        output = channel.recv(65535).decode('utf-8', errors='ignore')
        print(output)
        channel.close()
        
        # New channel for interfaces
        channel = transport.open_session()
        channel.settimeout(10)
        print("\n" + "=" * 80)
        print("INTERFACES")
        print("=" * 80)
        channel.exec_command('/interface print stats')
        output = channel.recv(65535).decode('utf-8', errors='ignore')
        print(output)
        channel.close()
        
        transport.close()
        print("\n✓ Connection closed")
        
    except socket.timeout:
        print("✗ Connection timeout")
    except socket.error as e:
        print(f"✗ Socket error: {e}")
    except paramiko.AuthenticationException:
        print("✗ Authentication failed - check username/password")
    except paramiko.SSHException as e:
        print(f"✗ SSH error: {e}")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ssh()
