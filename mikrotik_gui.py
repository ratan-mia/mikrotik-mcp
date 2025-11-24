#!/usr/bin/env python3
"""MikroTik Router Control Panel - GUI Dashboard"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from ttkthemes import ThemedTk
import paramiko
import socket
import threading
import time
from datetime import datetime
import json

class MikroTikControlPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("MikroTik Control Panel - SKS Router")
        self.root.geometry("1200x800")
        
        # Connection settings
        self.host = "202.84.44.49"
        self.port = 22
        self.username = "Admin115"
        self.password = "@dminAhL#"
        
        # Connection status
        self.connected = False
        self.auto_refresh = False
        
        # Create main layout
        self.create_widgets()
        
        # Auto-connect on startup
        self.root.after(500, self.connect_router)
    
    def create_widgets(self):
        # Top Frame - Connection Status
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        ttk.Label(top_frame, text="🖥️ MikroTik Control Panel", 
                 font=('Arial', 16, 'bold')).pack(side=tk.LEFT)
        
        self.status_label = ttk.Label(top_frame, text="● Disconnected", 
                                     foreground="red", font=('Arial', 10))
        self.status_label.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(top_frame, text="Connect", command=self.connect_router).pack(side=tk.RIGHT, padx=5)
        ttk.Button(top_frame, text="Refresh", command=self.refresh_all).pack(side=tk.RIGHT, padx=5)
        
        self.auto_refresh_var = tk.BooleanVar()
        ttk.Checkbutton(top_frame, text="Auto-Refresh (30s)", 
                       variable=self.auto_refresh_var,
                       command=self.toggle_auto_refresh).pack(side=tk.RIGHT, padx=5)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_devices_tab()
        self.create_interfaces_tab()
        self.create_firewall_tab()
        self.create_dhcp_tab()
        self.create_system_tab()
        self.create_terminal_tab()
        
    def create_dashboard_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📊 Dashboard")
        
        # System Info Frame
        info_frame = ttk.LabelFrame(frame, text="System Information", padding="10")
        info_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        info_grid = ttk.Frame(info_frame)
        info_grid.pack(fill=tk.BOTH, expand=True)
        
        # Create info labels
        labels = ["Uptime:", "Version:", "CPU:", "Memory:", "Connections:"]
        self.info_values = {}
        
        for i, label in enumerate(labels):
            ttk.Label(info_grid, text=label, font=('Arial', 10, 'bold')).grid(row=i, column=0, sticky=tk.W, padx=5, pady=3)
            value_label = ttk.Label(info_grid, text="...", font=('Arial', 10))
            value_label.grid(row=i, column=1, sticky=tk.W, padx=5, pady=3)
            self.info_values[label] = value_label
        
        # Traffic Frame
        traffic_frame = ttk.LabelFrame(frame, text="Interface Traffic", padding="10")
        traffic_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.traffic_text = scrolledtext.ScrolledText(traffic_frame, height=15, wrap=tk.WORD, font=('Consolas', 9))
        self.traffic_text.pack(fill=tk.BOTH, expand=True)
        
    def create_devices_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🖥️ Devices")
        
        # Controls
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(control_frame, text="🔄 Refresh Devices", 
                  command=self.load_devices).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="📋 Export List", 
                  command=self.export_devices).pack(side=tk.LEFT, padx=5)
        
        # Device Tree
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.device_tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set,
                                       columns=("IP", "MAC", "Status", "Server"),
                                       show='tree headings')
        self.device_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.device_tree.yview)
        
        # Configure columns
        self.device_tree.heading("#0", text="Device")
        self.device_tree.heading("IP", text="IP Address")
        self.device_tree.heading("MAC", text="MAC Address")
        self.device_tree.heading("Status", text="Status")
        self.device_tree.heading("Server", text="DHCP Server")
        
        self.device_tree.column("#0", width=150)
        self.device_tree.column("IP", width=150)
        self.device_tree.column("MAC", width=150)
        self.device_tree.column("Status", width=100)
        self.device_tree.column("Server", width=150)
        
    def create_interfaces_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔌 Interfaces")
        
        # Controls
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(control_frame, text="🔄 Refresh", 
                  command=self.load_interfaces).pack(side=tk.LEFT, padx=5)
        
        # Interface display
        self.interface_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=('Consolas', 9))
        self.interface_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
    def create_firewall_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔥 Firewall")
        
        # Controls
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(control_frame, text="🔄 Load Rules", 
                  command=self.load_firewall).pack(side=tk.LEFT, padx=5)
        ttk.Label(control_frame, text="Filter:").pack(side=tk.LEFT, padx=5)
        
        self.fw_filter = ttk.Combobox(control_frame, values=["All", "Input", "Forward", "Output"], 
                                     state="readonly", width=15)
        self.fw_filter.set("All")
        self.fw_filter.pack(side=tk.LEFT, padx=5)
        self.fw_filter.bind('<<ComboboxSelected>>', lambda e: self.load_firewall())
        
        # Firewall display
        self.firewall_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=('Consolas', 9))
        self.firewall_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
    def create_dhcp_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📡 DHCP")
        
        # Controls
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(control_frame, text="🔄 Refresh", 
                  command=self.load_dhcp).pack(side=tk.LEFT, padx=5)
        
        # DHCP display
        self.dhcp_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=('Consolas', 9))
        self.dhcp_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
    def create_system_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="⚙️ System")
        
        # Controls
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(control_frame, text="📊 Resources", 
                  command=self.load_system_resources).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="📝 Logs", 
                  command=self.load_logs).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="💾 Backup", 
                  command=self.create_backup).pack(side=tk.LEFT, padx=5)
        
        # System display
        self.system_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=('Consolas', 9))
        self.system_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
    def create_terminal_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="💻 Terminal")
        
        # Output area
        self.terminal_output = scrolledtext.ScrolledText(frame, wrap=tk.WORD, 
                                                         font=('Consolas', 9),
                                                         bg='black', fg='white')
        self.terminal_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Input area
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Command:").pack(side=tk.LEFT, padx=5)
        self.terminal_input = ttk.Entry(input_frame)
        self.terminal_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.terminal_input.bind('<Return>', lambda e: self.execute_command())
        
        ttk.Button(input_frame, text="Execute", 
                  command=self.execute_command).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="Clear", 
                  command=lambda: self.terminal_output.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
        
    def execute_ssh_command(self, command):
        """Execute SSH command and return output"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((self.host, self.port))
            
            transport = paramiko.Transport(sock)
            transport.banner_timeout = 60
            transport.connect(username=self.username, password=self.password)
            
            channel = transport.open_session()
            channel.settimeout(10)
            channel.exec_command(command)
            output = channel.recv(65535).decode('utf-8', errors='ignore')
            channel.close()
            transport.close()
            
            return output
        except Exception as e:
            return f"Error: {str(e)}"
    
    def connect_router(self):
        """Test connection to router"""
        def connect_thread():
            try:
                self.status_label.config(text="● Connecting...", foreground="orange")
                output = self.execute_ssh_command('/system identity print')
                if output and "Error" not in output:
                    self.connected = True
                    self.status_label.config(text="● Connected", foreground="green")
                    messagebox.showinfo("Success", "Connected to MikroTik router successfully!")
                    self.refresh_all()
                else:
                    self.connected = False
                    self.status_label.config(text="● Connection Failed", foreground="red")
                    messagebox.showerror("Error", "Failed to connect to router")
            except Exception as e:
                self.connected = False
                self.status_label.config(text="● Connection Failed", foreground="red")
                messagebox.showerror("Error", f"Connection error: {str(e)}")
        
        threading.Thread(target=connect_thread, daemon=True).start()
    
    def refresh_all(self):
        """Refresh all data"""
        self.load_dashboard()
        self.load_devices()
        self.load_interfaces()
    
    def load_dashboard(self):
        """Load dashboard data"""
        def load_thread():
            # System resources
            output = self.execute_ssh_command('/system resource print')
            if output and "Error" not in output:
                for line in output.split('\n'):
                    if 'uptime:' in line:
                        self.info_values["Uptime:"].config(text=line.split('uptime:')[1].strip())
                    elif 'version:' in line:
                        self.info_values["Version:"].config(text=line.split('version:')[1].strip())
                    elif 'free-memory:' in line:
                        mem_free = line.split('free-memory:')[1].strip()
                        total_output = self.execute_ssh_command('/system resource print')
                        for tline in total_output.split('\n'):
                            if 'total-memory:' in tline:
                                mem_total = tline.split('total-memory:')[1].strip()
                                self.info_values["Memory:"].config(text=f"{mem_free} / {mem_total}")
            
            # CPU
            cpu_output = self.execute_ssh_command('/system resource cpu print')
            if cpu_output and "Error" not in cpu_output:
                lines = [l for l in cpu_output.split('\n') if l.strip()]
                avg_cpu = "N/A"
                if len(lines) > 1:
                    self.info_values["CPU:"].config(text=f"Multi-core (see System tab)")
            
            # Connections
            conn_output = self.execute_ssh_command('/ip firewall connection print count-only')
            if conn_output and "Error" not in conn_output:
                self.info_values["Connections:"].config(text=conn_output.strip())
            
            # Traffic
            traffic_output = self.execute_ssh_command('/interface print stats')
            self.traffic_text.delete(1.0, tk.END)
            self.traffic_text.insert(1.0, traffic_output)
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def load_devices(self):
        """Load connected devices"""
        def load_thread():
            self.device_tree.delete(*self.device_tree.get_children())
            
            # DHCP Leases
            output = self.execute_ssh_command('/ip dhcp-server lease print detail')
            if output and "Error" not in output:
                device_num = 0
                current_device = {}
                
                for line in output.split('\n'):
                    line = line.strip()
                    if line.startswith('Flags:') or not line:
                        if current_device:
                            device_num += 1
                            ip = current_device.get('address', 'N/A')
                            mac = current_device.get('mac-address', 'N/A')
                            status = current_device.get('status', 'N/A')
                            server = current_device.get('server', 'N/A')
                            hostname = current_device.get('host-name', f'Device {device_num}')
                            
                            self.device_tree.insert('', 'end', text=hostname,
                                                   values=(ip, mac, status, server))
                            current_device = {}
                        continue
                    
                    if 'address=' in line:
                        parts = line.split()
                        for part in parts:
                            if '=' in part:
                                key, val = part.split('=', 1)
                                current_device[key] = val
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def load_interfaces(self):
        """Load interface information"""
        def load_thread():
            output = self.execute_ssh_command('/interface print detail stats')
            self.interface_text.delete(1.0, tk.END)
            self.interface_text.insert(1.0, output)
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def load_firewall(self):
        """Load firewall rules"""
        def load_thread():
            filter_chain = self.fw_filter.get().lower()
            if filter_chain == "all":
                cmd = '/ip firewall filter print detail'
            else:
                cmd = f'/ip firewall filter print detail where chain={filter_chain}'
            
            output = self.execute_ssh_command(cmd)
            self.firewall_text.delete(1.0, tk.END)
            self.firewall_text.insert(1.0, output)
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def load_dhcp(self):
        """Load DHCP configuration"""
        def load_thread():
            output = self.execute_ssh_command('/ip dhcp-server print detail')
            output += "\n\n" + "="*80 + "\nDHCP Networks:\n" + "="*80 + "\n"
            output += self.execute_ssh_command('/ip dhcp-server network print detail')
            
            self.dhcp_text.delete(1.0, tk.END)
            self.dhcp_text.insert(1.0, output)
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def load_system_resources(self):
        """Load system resources"""
        def load_thread():
            output = "SYSTEM RESOURCES\n" + "="*80 + "\n"
            output += self.execute_ssh_command('/system resource print')
            output += "\n\nCPU LOAD\n" + "="*80 + "\n"
            output += self.execute_ssh_command('/system resource cpu print')
            
            self.system_text.delete(1.0, tk.END)
            self.system_text.insert(1.0, output)
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def load_logs(self):
        """Load system logs"""
        def load_thread():
            output = self.execute_ssh_command('/log print')
            self.system_text.delete(1.0, tk.END)
            self.system_text.insert(1.0, output)
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def create_backup(self):
        """Create system backup"""
        def backup_thread():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output = self.execute_ssh_command(f'/system backup save name=backup_{timestamp}')
            messagebox.showinfo("Backup", f"Backup created: backup_{timestamp}\n{output}")
        
        threading.Thread(target=backup_thread, daemon=True).start()
    
    def execute_command(self):
        """Execute terminal command"""
        command = self.terminal_input.get()
        if not command:
            return
        
        self.terminal_output.insert(tk.END, f"\n> {command}\n", "command")
        self.terminal_output.tag_config("command", foreground="yellow")
        
        def exec_thread():
            output = self.execute_ssh_command(command)
            self.terminal_output.insert(tk.END, output + "\n", "output")
            self.terminal_output.tag_config("output", foreground="white")
            self.terminal_output.see(tk.END)
        
        threading.Thread(target=exec_thread, daemon=True).start()
        self.terminal_input.delete(0, tk.END)
    
    def export_devices(self):
        """Export device list to JSON"""
        try:
            devices = []
            for item in self.device_tree.get_children():
                values = self.device_tree.item(item)
                device = {
                    'hostname': values['text'],
                    'ip': values['values'][0],
                    'mac': values['values'][1],
                    'status': values['values'][2],
                    'server': values['values'][3]
                }
                devices.append(device)
            
            filename = f"devices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(devices, f, indent=2)
            
            messagebox.showinfo("Export", f"Devices exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def toggle_auto_refresh(self):
        """Toggle auto-refresh"""
        self.auto_refresh = self.auto_refresh_var.get()
        if self.auto_refresh:
            self.auto_refresh_loop()
    
    def auto_refresh_loop(self):
        """Auto-refresh loop"""
        if self.auto_refresh:
            self.refresh_all()
            self.root.after(30000, self.auto_refresh_loop)  # 30 seconds

def main():
    root = ThemedTk(theme="arc")  # Modern theme
    app = MikroTikControlPanel(root)
    root.mainloop()

if __name__ == "__main__":
    main()
