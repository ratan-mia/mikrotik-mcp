import { NextResponse } from 'next/server';
import { Client } from 'ssh2';

const ROUTER_CONFIG = {
  host: '202.84.44.49',
  port: 22,
  username: 'Admin115',
  password: '@dminAhL#',
};

async function executeCommand(command: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const conn = new Client();
    let output = '';

    conn.on('ready', () => {
      conn.exec(command, (err, stream) => {
        if (err) {
          conn.end();
          reject(err);
          return;
        }

        stream.on('close', () => {
          conn.end();
          resolve(output);
        }).on('data', (data: Buffer) => {
          output += data.toString();
        }).stderr.on('data', (data) => {
          console.error('STDERR: ' + data);
        });
      });
    }).connect(ROUTER_CONFIG);

    conn.on('error', (err) => {
      reject(err);
    });

    setTimeout(() => {
      conn.end();
      reject(new Error('Connection timeout'));
    }, 10000);
  });
}

function parseSystemInfo(output: string) {
  const info: any = {};
  const lines = output.split('\n');
  
  for (const line of lines) {
    if (line.includes('uptime:')) {
      info.uptime = line.split('uptime:')[1].trim();
    }
    if (line.includes('version:')) {
      info.version = line.split('version:')[1].trim();
    }
    if (line.includes('free-memory:')) {
      info.freeMemory = line.split('free-memory:')[1].trim();
    }
    if (line.includes('total-memory:')) {
      info.totalMemory = line.split('total-memory:')[1].trim();
    }
  }
  
  return info;
}

function parseDevices(output: string) {
  const devices: any[] = [];
  const lines = output.split('\n');
  let currentDevice: any = {};
  
  for (const line of lines) {
    if (line.trim().startsWith('Flags:') || !line.trim()) {
      if (Object.keys(currentDevice).length > 0) {
        devices.push(currentDevice);
        currentDevice = {};
      }
      continue;
    }
    
    const parts = line.trim().split(/\s+/);
    for (const part of parts) {
      if (part.includes('=')) {
        const [key, value] = part.split('=');
        currentDevice[key] = value;
      }
    }
  }
  
  if (Object.keys(currentDevice).length > 0) {
    devices.push(currentDevice);
  }
  
  return devices.map(d => ({
    ip: d.address || 'N/A',
    mac: d['mac-address'] || 'N/A',
    hostname: d['host-name'] || 'Unknown',
    status: d.status || 'N/A'
  }));
}

function parseInterfaces(output: string) {
  const interfaces: any[] = [];
  const lines = output.split('\n');
  
  for (const line of lines) {
    if (line.includes('ether') || line.includes('wlan')) {
      const parts = line.trim().split(/\s+/);
      if (parts.length >= 4) {
        interfaces.push({
          name: parts[1] || parts[0],
          rxByte: formatBytes(parts[2]),
          txByte: formatBytes(parts[3]),
          running: line.includes('R')
        });
      }
    }
  }
  
  return interfaces;
}

function formatBytes(bytes: string): string {
  const num = parseInt(bytes?.replace(/[^\d]/g, '') || '0');
  if (num === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(num) / Math.log(k));
  return Math.round((num / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

export async function GET() {
  try {
    // Get system resources
    const sysOutput = await executeCommand('/system resource print');
    const systemInfo = parseSystemInfo(sysOutput);
    
    // Get CPU info
    const cpuOutput = await executeCommand('/system resource cpu print');
    const cpuLines = cpuOutput.split('\n').filter(l => l.trim());
    systemInfo.cpu = cpuLines.length > 2 ? `${cpuLines.length - 1} cores` : '1 core';
    
    // Get connection count
    const connOutput = await executeCommand('/ip firewall connection print count-only');
    const connections = parseInt(connOutput.trim()) || 0;
    
    // Get DHCP leases
    const dhcpOutput = await executeCommand('/ip dhcp-server lease print detail where status=bound');
    const devices = parseDevices(dhcpOutput);
    
    // Get interfaces
    const ifaceOutput = await executeCommand('/interface print stats');
    const interfaces = parseInterfaces(ifaceOutput);
    
    return NextResponse.json({
      system: {
        uptime: systemInfo.uptime || 'N/A',
        version: systemInfo.version || 'N/A',
        cpu: systemInfo.cpu,
        memory: `${systemInfo.freeMemory || 'N/A'} / ${systemInfo.totalMemory || 'N/A'}`,
        connections
      },
      devices,
      interfaces
    });
  } catch (error: any) {
    console.error('Router API Error:', error);
    return NextResponse.json(
      { 
        error: 'Failed to connect to router',
        message: error.message,
        system: {
          uptime: 'Error',
          version: 'Error',
          cpu: 'Error',
          memory: 'Error',
          connections: 0
        },
        devices: [],
        interfaces: []
      },
      { status: 500 }
    );
  }
}
