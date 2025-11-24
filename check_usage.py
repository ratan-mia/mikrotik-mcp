#!/usr/bin/env python3
"""Check current usage on MikroTik router"""

import paramiko
import socket

def check_usage():
    host = "202.84.44.49"
    port = 22
    username = "Admin115"
    password = "@dminAhL#"
    
    print(f"Connecting to {host}:{port}...")
    
    try:
        # Create socket and transport
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((host, port))
        
        transport = paramiko.Transport(sock)
        transport.banner_timeout = 60
        transport.connect(username=username, password=password)
        print("✓ Connected\n")
        
        # System Resources
        channel = transport.open_session()
        channel.settimeout(10)
        print("=" * 80)
        print("SYSTEM RESOURCES")
        print("=" * 80)
        channel.exec_command('/system resource print')
        output = channel.recv(65535).decode('utf-8', errors='ignore')
        print(output)
        channel.close()
        
        # Interface Traffic
        channel = transport.open_session()
        channel.settimeout(10)
        print("\n" + "=" * 80)
        print("INTERFACE TRAFFIC (Real-time)")
        print("=" * 80)
        channel.exec_command('/interface monitor-traffic ether1,ether3 once')
        output = channel.recv(65535).decode('utf-8', errors='ignore')
        print(output)
        channel.close()
        
        # Interface Statistics
        channel = transport.open_session()
        channel.settimeout(10)
        print("\n" + "=" * 80)
        print("INTERFACE STATISTICS (Total)")
        print("=" * 80)
        channel.exec_command('/interface print stats')
        output = channel.recv(65535).decode('utf-8', errors='ignore')
        print(output)
        channel.close()
        
        # CPU Load
        channel = transport.open_session()
        channel.settimeout(10)
        print("\n" + "=" * 80)
        print("CPU LOAD")
        print("=" * 80)
        channel.exec_command('/system resource cpu print')
        output = channel.recv(65535).decode('utf-8', errors='ignore')
        print(output)
        channel.close()
        
        # Active Connections
        channel = transport.open_session()
        channel.settimeout(10)
        print("\n" + "=" * 80)
        print("ACTIVE CONNECTIONS (Sample)")
        print("=" * 80)
        channel.exec_command('/ip firewall connection print count-only')
        output = channel.recv(65535).decode('utf-8', errors='ignore')
        print(f"Total Connections: {output.strip()}")
        channel.close()
        
        # Top connections by protocol
        channel = transport.open_session()
        channel.settimeout(10)
        channel.exec_command('/ip firewall connection print stats')
        output = channel.recv(65535).decode('utf-8', errors='ignore')
        print(output[:2000] if len(output) > 2000 else output)  # Limit output
        channel.close()
        
        # Memory usage
        channel = transport.open_session()
        channel.settimeout(10)
        print("\n" + "=" * 80)
        print("MEMORY USAGE")
        print("=" * 80)
        channel.exec_command('/system resource print')
        output = channel.recv(65535).decode('utf-8', errors='ignore')
        # Extract memory info
        for line in output.split('\n'):
            if 'memory' in line.lower() or 'free' in line.lower():
                print(line)
        channel.close()
        
        # Uptime
        channel = transport.open_session()
        channel.settimeout(10)
        print("\n" + "=" * 80)
        print("SYSTEM UPTIME")
        print("=" * 80)
        channel.exec_command('/system resource print')
        output = channel.recv(65535).decode('utf-8', errors='ignore')
        for line in output.split('\n'):
            if 'uptime' in line.lower() or 'version' in line.lower():
                print(line)
        channel.close()
        
        transport.close()
        print("\n✓ Connection closed")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_usage()
