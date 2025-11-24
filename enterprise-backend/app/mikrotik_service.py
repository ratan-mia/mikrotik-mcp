import paramiko
import socket
from typing import Dict, List, Optional
from datetime import datetime
from app.models import Router


class MikroTikSSHClient:
    """SSH client for MikroTik RouterOS"""
    
    def __init__(self, router: Router):
        self.router = router
        self.client: Optional[paramiko.SSHClient] = None
    
    def connect(self) -> bool:
        """Establish SSH connection to router"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((self.router.hostname, self.router.port))
            
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                self.router.hostname,
                port=self.router.port,
                username=self.router.username,
                password=self.router.password,
                timeout=10,
                sock=sock
            )
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def disconnect(self):
        """Close SSH connection"""
        if self.client:
            self.client.close()
    
    def execute_command(self, command: str) -> str:
        """Execute a command on the router"""
        if not self.client:
            raise Exception("Not connected to router")
        
        try:
            stdin, stdout, stderr = self.client.exec_command(command, timeout=30)
            output = stdout.read().decode('utf-8', errors='ignore')
            error = stderr.read().decode('utf-8', errors='ignore')
            
            if error and 'warning' not in error.lower():
                raise Exception(f"Command error: {error}")
            
            return output
        except Exception as e:
            raise Exception(f"Command execution failed: {e}")
    
    def get_system_resource(self) -> Dict:
        """Get system resource information"""
        output = self.execute_command("/system resource print")
        
        result = {
            "uptime": "",
            "version": "",
            "cpu": "",
            "memory_used": 0,
            "memory_total": 0,
            "cpu_load": 0
        }
        
        for line in output.split('\n'):
            line = line.strip()
            if "uptime:" in line:
                result["uptime"] = line.split("uptime:", 1)[1].strip()
            elif "version:" in line:
                result["version"] = line.split("version:", 1)[1].strip()
            elif "cpu:" in line or "cpu-count:" in line:
                result["cpu"] = line.split(":", 1)[1].strip()
            elif "total-memory:" in line:
                mem_str = line.split(":", 1)[1].strip().replace("MiB", "").strip()
                result["memory_total"] = float(mem_str) if mem_str else 0
            elif "free-memory:" in line:
                mem_str = line.split(":", 1)[1].strip().replace("MiB", "").strip()
                free_mem = float(mem_str) if mem_str else 0
                result["memory_used"] = result["memory_total"] - free_mem
            elif "cpu-load:" in line:
                cpu_str = line.split(":", 1)[1].strip().replace("%", "").strip()
                result["cpu_load"] = float(cpu_str) if cpu_str else 0
        
        return result
    
    def get_connections(self) -> int:
        """Get number of active connections"""
        output = self.execute_command("/ip firewall connection print count-only")
        try:
            return int(output.strip())
        except:
            return 0
    
    def get_dhcp_leases(self) -> List[Dict]:
        """Get DHCP lease information"""
        output = self.execute_command("/ip dhcp-server lease print detail")
        
        devices = []
        current_device = {}
        
        for line in output.split('\n'):
            line = line.strip()
            if not line or line.startswith('Flags:'):
                continue
            
            if line and not line.startswith(' '):
                if current_device:
                    devices.append(current_device)
                current_device = {}
            
            if "address=" in line:
                current_device["ip"] = line.split("address=", 1)[1].split()[0]
            elif "mac-address=" in line:
                current_device["mac"] = line.split("mac-address=", 1)[1].split()[0]
            elif "host-name=" in line:
                current_device["hostname"] = line.split("host-name=", 1)[1].split()[0].strip('"')
            elif "status=" in line:
                current_device["status"] = line.split("status=", 1)[1].split()[0]
        
        if current_device:
            devices.append(current_device)
        
        return devices
    
    def get_interfaces(self) -> List[Dict]:
        """Get network interface statistics"""
        output = self.execute_command("/interface print stats")
        
        interfaces = []
        current_iface = {}
        
        for line in output.split('\n'):
            line = line.strip()
            if not line or line.startswith('Flags:'):
                continue
            
            if line and not line.startswith(' '):
                if current_iface:
                    interfaces.append(current_iface)
                current_iface = {}
            
            if "name=" in line:
                current_iface["name"] = line.split("name=", 1)[1].split()[0].strip('"')
            elif "rx-byte=" in line:
                current_iface["rx_bytes"] = self._parse_bytes(line.split("rx-byte=", 1)[1].split()[0])
            elif "tx-byte=" in line:
                current_iface["tx_bytes"] = self._parse_bytes(line.split("tx-byte=", 1)[1].split()[0])
            elif "rx-packet=" in line:
                current_iface["rx_packets"] = int(line.split("rx-packet=", 1)[1].split()[0])
            elif "tx-packet=" in line:
                current_iface["tx_packets"] = int(line.split("tx-packet=", 1)[1].split()[0])
            elif "running=" in line:
                current_iface["running"] = "true" in line.lower()
        
        if current_iface:
            interfaces.append(current_iface)
        
        return interfaces
    
    def get_firewall_rules(self) -> List[Dict]:
        """Get firewall filter rules"""
        output = self.execute_command("/ip firewall filter print detail")
        
        rules = []
        current_rule = {}
        
        for line in output.split('\n'):
            line = line.strip()
            if not line or line.startswith('Flags:'):
                continue
            
            if line and not line.startswith(' '):
                if current_rule:
                    rules.append(current_rule)
                current_rule = {}
            
            if "chain=" in line:
                current_rule["chain"] = line.split("chain=", 1)[1].split()[0]
            elif "action=" in line:
                current_rule["action"] = line.split("action=", 1)[1].split()[0]
            elif "protocol=" in line:
                current_rule["protocol"] = line.split("protocol=", 1)[1].split()[0]
        
        if current_rule:
            rules.append(current_rule)
        
        return rules
    
    def create_backup(self) -> str:
        """Create a backup of router configuration"""
        backup_name = f"backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.execute_command(f"/system backup save name={backup_name}")
        return backup_name
    
    def _parse_bytes(self, byte_str: str) -> float:
        """Parse byte string to float"""
        multipliers = {
            'KiB': 1024,
            'MiB': 1024**2,
            'GiB': 1024**3,
            'TiB': 1024**4
        }
        
        for suffix, multiplier in multipliers.items():
            if suffix in byte_str:
                return float(byte_str.replace(suffix, '').strip()) * multiplier
        
        try:
            return float(byte_str)
        except:
            return 0.0


def get_mikrotik_client(router: Router) -> MikroTikSSHClient:
    """Factory function to create MikroTik client"""
    client = MikroTikSSHClient(router)
    if not client.connect():
        raise Exception(f"Failed to connect to router {router.name}")
    return client
