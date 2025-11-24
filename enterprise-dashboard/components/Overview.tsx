'use client';

import { apiService } from '@/lib/api';
import { Activity, AlertTriangle, Cpu, HardDrive, Server, TrendingUp, Users } from 'lucide-react';
import { useEffect, useState } from 'react';

interface Stats {
    total_routers: number;
    active_routers: number;
    total_devices: number;
    active_alerts: number;
    critical_alerts: number;
}

export default function Overview() {
    const [stats, setStats] = useState<Stats | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadStats();
        const interval = setInterval(loadStats, 30000);
        return () => clearInterval(interval);
    }, []);

    const loadStats = async () => {
        try {
            const data = await apiService.getDashboardStats();
            setStats(data);
        } catch (error) {
            console.error('Failed to load stats:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return <div className="text-white">Loading...</div>;
    }

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-white mb-2">Dashboard Overview</h2>
                <p className="text-slate-400">Monitor all your MikroTik routers from one place</p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                    icon={<Server className="h-8 w-8" />}
                    title="Total Routers"
                    value={stats?.total_routers || 0}
                    subtitle={`${stats?.active_routers || 0} active`}
                    color="blue"
                />
                <StatCard
                    icon={<Users className="h-8 w-8" />}
                    title="Connected Devices"
                    value={stats?.total_devices || 0}
                    subtitle="Across all networks"
                    color="green"
                />
                <StatCard
                    icon={<AlertTriangle className="h-8 w-8" />}
                    title="Active Alerts"
                    value={stats?.active_alerts || 0}
                    subtitle={`${stats?.critical_alerts || 0} critical`}
                    color="yellow"
                />
                <StatCard
                    icon={<Activity className="h-8 w-8" />}
                    title="System Health"
                    value="98%"
                    subtitle="All systems operational"
                    color="green"
                />
            </div>

            {/* Quick Actions */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                <h3 className="text-xl font-semibold text-white mb-4">Quick Actions</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition flex items-center justify-center space-x-2">
                        <Server className="h-5 w-5" />
                        <span>Add Router</span>
                    </button>
                    <button className="bg-slate-700 hover:bg-slate-600 text-white font-semibold py-3 px-6 rounded-lg transition flex items-center justify-center space-x-2">
                        <Activity className="h-5 w-5" />
                        <span>Run Diagnostics</span>
                    </button>
                    <button className="bg-slate-700 hover:bg-slate-600 text-white font-semibold py-3 px-6 rounded-lg transition flex items-center justify-center space-x-2">
                        <TrendingUp className="h-5 w-5" />
                        <span>View Analytics</span>
                    </button>
                </div>
            </div>

            {/* Recent Activity */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                    <h3 className="text-xl font-semibold text-white mb-4">System Performance</h3>
                    <div className="space-y-4">
                        <PerformanceBar label="CPU Usage" value={45} color="blue" icon={<Cpu className="h-5 w-5" />} />
                        <PerformanceBar label="Memory Usage" value={62} color="green" icon={<HardDrive className="h-5 w-5" />} />
                        <PerformanceBar label="Network Load" value={38} color="purple" icon={<Activity className="h-5 w-5" />} />
                    </div>
                </div>

                <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                    <h3 className="text-xl font-semibold text-white mb-4">Recent Alerts</h3>
                    <div className="space-y-3">
                        <AlertItem severity="warning" message="High CPU usage on Router-1" time="5 min ago" />
                        <AlertItem severity="info" message="New device connected to Router-2" time="15 min ago" />
                        <AlertItem severity="critical" message="Connection timeout on Router-3" time="1 hour ago" />
                    </div>
                </div>
            </div>
        </div>
    );
}

function StatCard({ icon, title, value, subtitle, color }: any) {
    const colors = {
        blue: 'from-blue-600 to-blue-700',
        green: 'from-green-600 to-green-700',
        yellow: 'from-yellow-600 to-yellow-700',
        purple: 'from-purple-600 to-purple-700',
    };

    return (
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
            <div className={`bg-gradient-to-br ${colors[color as keyof typeof colors]} text-white p-3 rounded-lg w-fit mb-4`}>
                {icon}
            </div>
            <div className="text-3xl font-bold text-white mb-1">{value}</div>
            <div className="text-sm font-medium text-slate-300 mb-1">{title}</div>
            <div className="text-xs text-slate-500">{subtitle}</div>
        </div>
    );
}

function PerformanceBar({ label, value, color, icon }: any) {
    const colors = {
        blue: 'bg-blue-600',
        green: 'bg-green-600',
        purple: 'bg-purple-600',
    };

    return (
        <div>
            <div className="flex items-center justify-between mb-2">
                <div className="flex items-center space-x-2 text-slate-300">
                    {icon}
                    <span className="text-sm font-medium">{label}</span>
                </div>
                <span className="text-sm font-semibold text-white">{value}%</span>
            </div>
            <div className="w-full bg-slate-700 rounded-full h-2">
                <div className={`${colors[color as keyof typeof colors]} h-2 rounded-full transition-all duration-500`} style={{ width: `${value}%` }}></div>
            </div>
        </div>
    );
}

function AlertItem({ severity, message, time }: any) {
    const colors = {
        critical: 'bg-red-500/10 border-red-500 text-red-500',
        warning: 'bg-yellow-500/10 border-yellow-500 text-yellow-500',
        info: 'bg-blue-500/10 border-blue-500 text-blue-500',
    };

    return (
        <div className={`flex items-start space-x-3 p-3 rounded-lg border ${colors[severity as keyof typeof colors]}`}>
            <AlertTriangle className="h-5 w-5 mt-0.5 flex-shrink-0" />
            <div className="flex-1 min-w-0">
                <p className="text-sm font-medium">{message}</p>
                <p className="text-xs opacity-75 mt-1">{time}</p>
            </div>
        </div>
    );
}
