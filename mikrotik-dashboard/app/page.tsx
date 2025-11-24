'use client';

import {
    Activity,
    Clock,
    Cpu,
    HardDrive,
    Network,
    RefreshCw,
    Server,
    Shield,
    TrendingDown,
    TrendingUp,
    Users
} from 'lucide-react';
import { useEffect, useState } from 'react';

interface SystemInfo {
    uptime: string;
    version: string;
    cpu: string;
    memory: string;
    connections: number;
}

interface Device {
    ip: string;
    mac: string;
    hostname: string;
    status: string;
}

interface InterfaceStats {
    name: string;
    rxByte: string;
    txByte: string;
    running: boolean;
}

export default function Home() {
    const [systemInfo, setSystemInfo] = useState<SystemInfo>({
        uptime: '...',
        version: '...',
        cpu: '...',
        memory: '...',
        connections: 0
    });

    const [devices, setDevices] = useState<Device[]>([]);
    const [interfaces, setInterfaces] = useState<InterfaceStats[]>([]);
    const [loading, setLoading] = useState(false);
    const [activeTab, setActiveTab] = useState('dashboard');
    const [autoRefresh, setAutoRefresh] = useState(false);

    useEffect(() => {
        loadData();
    }, []);

    useEffect(() => {
        if (autoRefresh) {
            const interval = setInterval(loadData, 30000);
            return () => clearInterval(interval);
        }
    }, [autoRefresh]);

    const loadData = async () => {
        setLoading(true);
        try {
            const response = await fetch('/api/router/status');
            if (response.ok) {
                const data = await response.json();
                setSystemInfo(data.system || systemInfo);
                setDevices(data.devices || []);
                setInterfaces(data.interfaces || []);
            }
        } catch (error) {
            console.error('Failed to load data:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
            {/* Header */}
            <header className="bg-slate-900/50 backdrop-blur-sm border-b border-slate-700">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                            <Server className="h-8 w-8 text-blue-500" />
                            <div>
                                <h1 className="text-2xl font-bold text-white">MikroTik Dashboard</h1>
                                <p className="text-sm text-slate-400">SKS Router - 202.84.44.49</p>
                            </div>
                        </div>
                        <div className="flex items-center space-x-4">
                            <label className="flex items-center space-x-2 text-white">
                                <input
                                    type="checkbox"
                                    checked={autoRefresh}
                                    onChange={(e) => setAutoRefresh(e.target.checked)}
                                    className="rounded"
                                />
                                <span className="text-sm">Auto-refresh</span>
                            </label>
                            <button
                                onClick={loadData}
                                disabled={loading}
                                className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition disabled:opacity-50"
                            >
                                <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
                                <span>Refresh</span>
                            </button>
                        </div>
                    </div>
                </div>
            </header>

            {/* Navigation Tabs */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6">
                <div className="flex space-x-2 border-b border-slate-700">
                    {[
                        { id: 'dashboard', label: 'Dashboard', icon: Activity },
                        { id: 'devices', label: 'Devices', icon: Users },
                        { id: 'interfaces', label: 'Interfaces', icon: Network },
                        { id: 'firewall', label: 'Firewall', icon: Shield },
                    ].map(tab => (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`flex items-center space-x-2 px-4 py-3 border-b-2 transition ${activeTab === tab.id
                                    ? 'border-blue-500 text-blue-500'
                                    : 'border-transparent text-slate-400 hover:text-white'
                                }`}
                        >
                            <tab.icon className="h-4 w-4" />
                            <span>{tab.label}</span>
                        </button>
                    ))}
                </div>
            </div>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {activeTab === 'dashboard' && (
                    <div className="space-y-6">
                        {/* Stats Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                            <StatCard
                                title="Uptime"
                                value={systemInfo.uptime}
                                icon={Clock}
                                color="blue"
                            />
                            <StatCard
                                title="CPU Load"
                                value={systemInfo.cpu}
                                icon={Cpu}
                                color="purple"
                            />
                            <StatCard
                                title="Memory"
                                value={systemInfo.memory}
                                icon={HardDrive}
                                color="green"
                            />
                            <StatCard
                                title="Connections"
                                value={systemInfo.connections.toString()}
                                icon={Network}
                                color="orange"
                            />
                        </div>

                        {/* System Info */}
                        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                            <h2 className="text-xl font-semibold text-white mb-4 flex items-center">
                                <Server className="h-5 w-5 mr-2 text-blue-500" />
                                System Information
                            </h2>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <InfoRow label="RouterOS Version" value={systemInfo.version} />
                                <InfoRow label="Uptime" value={systemInfo.uptime} />
                                <InfoRow label="Active Connections" value={systemInfo.connections.toString()} />
                                <InfoRow label="CPU Usage" value={systemInfo.cpu} />
                            </div>
                        </div>

                        {/* Interface Traffic */}
                        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                            <h2 className="text-xl font-semibold text-white mb-4 flex items-center">
                                <Activity className="h-5 w-5 mr-2 text-blue-500" />
                                Interface Traffic
                            </h2>
                            <div className="overflow-x-auto">
                                <table className="w-full">
                                    <thead>
                                        <tr className="text-left border-b border-slate-700">
                                            <th className="pb-3 text-slate-400 font-medium">Interface</th>
                                            <th className="pb-3 text-slate-400 font-medium">Status</th>
                                            <th className="pb-3 text-slate-400 font-medium">RX</th>
                                            <th className="pb-3 text-slate-400 font-medium">TX</th>
                                        </tr>
                                    </thead>
                                    <tbody className="text-white">
                                        {interfaces.map((iface, idx) => (
                                            <tr key={idx} className="border-b border-slate-700/50">
                                                <td className="py-3">{iface.name}</td>
                                                <td className="py-3">
                                                    <span className={`inline-flex items-center px-2 py-1 rounded text-xs ${iface.running
                                                            ? 'bg-green-500/20 text-green-400'
                                                            : 'bg-red-500/20 text-red-400'
                                                        }`}>
                                                        {iface.running ? 'Running' : 'Stopped'}
                                                    </span>
                                                </td>
                                                <td className="py-3 flex items-center">
                                                    <TrendingDown className="h-4 w-4 mr-1 text-blue-400" />
                                                    {iface.rxByte}
                                                </td>
                                                <td className="py-3">
                                                    <span className="flex items-center">
                                                        <TrendingUp className="h-4 w-4 mr-1 text-green-400" />
                                                        {iface.txByte}
                                                    </span>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                )}

                {activeTab === 'devices' && (
                    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                        <h2 className="text-xl font-semibold text-white mb-4 flex items-center">
                            <Users className="h-5 w-5 mr-2 text-blue-500" />
                            Connected Devices ({devices.length})
                        </h2>
                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead>
                                    <tr className="text-left border-b border-slate-700">
                                        <th className="pb-3 text-slate-400 font-medium">Hostname</th>
                                        <th className="pb-3 text-slate-400 font-medium">IP Address</th>
                                        <th className="pb-3 text-slate-400 font-medium">MAC Address</th>
                                        <th className="pb-3 text-slate-400 font-medium">Status</th>
                                    </tr>
                                </thead>
                                <tbody className="text-white">
                                    {devices.map((device, idx) => (
                                        <tr key={idx} className="border-b border-slate-700/50">
                                            <td className="py-3">{device.hostname || 'Unknown'}</td>
                                            <td className="py-3 font-mono text-sm">{device.ip}</td>
                                            <td className="py-3 font-mono text-sm text-slate-400">{device.mac}</td>
                                            <td className="py-3">
                                                <span className="inline-flex items-center px-2 py-1 rounded text-xs bg-green-500/20 text-green-400">
                                                    {device.status}
                                                </span>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                )}

                {activeTab === 'interfaces' && (
                    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                        <h2 className="text-xl font-semibold text-white mb-4 flex items-center">
                            <Network className="h-5 w-5 mr-2 text-blue-500" />
                            Network Interfaces
                        </h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {interfaces.map((iface, idx) => (
                                <div key={idx} className="bg-slate-900/50 rounded-lg p-4 border border-slate-700">
                                    <div className="flex items-center justify-between mb-3">
                                        <h3 className="text-lg font-semibold text-white">{iface.name}</h3>
                                        <span className={`px-2 py-1 rounded text-xs ${iface.running
                                                ? 'bg-green-500/20 text-green-400'
                                                : 'bg-red-500/20 text-red-400'
                                            }`}>
                                            {iface.running ? 'Active' : 'Inactive'}
                                        </span>
                                    </div>
                                    <div className="space-y-2 text-sm">
                                        <div className="flex justify-between text-slate-400">
                                            <span>RX (Download):</span>
                                            <span className="text-white">{iface.rxByte}</span>
                                        </div>
                                        <div className="flex justify-between text-slate-400">
                                            <span>TX (Upload):</span>
                                            <span className="text-white">{iface.txByte}</span>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {activeTab === 'firewall' && (
                    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                        <h2 className="text-xl font-semibold text-white mb-4 flex items-center">
                            <Shield className="h-5 w-5 mr-2 text-blue-500" />
                            Firewall Status
                        </h2>
                        <div className="text-center py-12">
                            <Shield className="h-16 w-16 mx-auto text-slate-600 mb-4" />
                            <p className="text-slate-400">Firewall rules will be displayed here</p>
                            <p className="text-sm text-slate-500 mt-2">Connect to API to view firewall configuration</p>
                        </div>
                    </div>
                )}
            </main>

            {/* Footer */}
            <footer className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 mt-12 border-t border-slate-700">
                <div className="text-center text-slate-400 text-sm">
                    <p>MikroTik Dashboard • SKS Router Management Panel</p>
                    <p className="mt-1">Built with Next.js & Tailwind CSS</p>
                </div>
            </footer>
        </div>
    );
}

function StatCard({ title, value, icon: Icon, color }: {
    title: string;
    value: string;
    icon: any;
    color: string;
}) {
    const colorClasses = {
        blue: 'bg-blue-500/20 text-blue-400',
        purple: 'bg-purple-500/20 text-purple-400',
        green: 'bg-green-500/20 text-green-400',
        orange: 'bg-orange-500/20 text-orange-400',
    }[color];

    return (
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
            <div className="flex items-center justify-between">
                <div>
                    <p className="text-slate-400 text-sm">{title}</p>
                    <p className="text-2xl font-bold text-white mt-2">{value}</p>
                </div>
                <div className={`p-3 rounded-lg ${colorClasses}`}>
                    <Icon className="h-6 w-6" />
                </div>
            </div>
        </div>
    );
}

function InfoRow({ label, value }: { label: string; value: string }) {
    return (
        <div className="flex justify-between py-2 border-b border-slate-700/50">
            <span className="text-slate-400">{label}:</span>
            <span className="text-white font-medium">{value}</span>
        </div>
    );
}
