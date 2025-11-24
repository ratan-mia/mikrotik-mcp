'use client';

import { apiService, Metric, Router } from '@/lib/api';
import { Activity, AlertCircle, CheckCircle, Cpu, HardDrive, Network, RefreshCw, Wifi } from 'lucide-react';
import { useEffect, useState } from 'react';

interface RouterWithMetrics extends Router {
    latestMetrics?: Metric;
    status?: 'online' | 'offline' | 'warning';
}

export default function MonitoringPage() {
    const [routers, setRouters] = useState<RouterWithMetrics[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [refreshing, setRefreshing] = useState(false);

    useEffect(() => {
        loadMonitoringData();
        const interval = setInterval(loadMonitoringData, 30000); // Refresh every 30 seconds
        return () => clearInterval(interval);
    }, []);

    const loadMonitoringData = async () => {
        try {
            setError(null);
            const routersList = await apiService.getRouters();

            // Fetch latest metrics for each router
            const routersWithMetrics = await Promise.all(
                routersList.map(async (router) => {
                    try {
                        const status = await apiService.getRouterStatus(router.id);
                        const hasMetrics = status.latest_metric !== null;
                        return {
                            ...router,
                            latestMetrics: status.latest_metric,
                            status: hasMetrics ? 'online' : 'offline',
                        } as RouterWithMetrics;
                    } catch (error) {
                        return {
                            ...router,
                            status: 'offline',
                        } as RouterWithMetrics;
                    }
                })
            );

            setRouters(routersWithMetrics);
        } catch (error: any) {
            console.error('Failed to load monitoring data:', error);
            setError('Failed to load monitoring data');
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    };

    const handleRefresh = () => {
        setRefreshing(true);
        loadMonitoringData();
    };

    const handleCollectMetrics = async (routerId: number) => {
        try {
            await apiService.collectMetrics(routerId);
            setTimeout(loadMonitoringData, 2000); // Reload after 2 seconds
        } catch (error) {
            console.error('Failed to collect metrics:', error);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center h-96">
                <div className="text-gray-400">Loading monitoring data...</div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-red-500/10 border border-red-500 text-red-500 px-6 py-4 rounded-lg">
                <div className="flex items-center">
                    <AlertCircle className="h-5 w-5 mr-2" />
                    <span>{error}</span>
                </div>
                <button
                    onClick={loadMonitoringData}
                    className="mt-4 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg text-sm"
                >
                    Retry
                </button>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-white">Real-Time Monitoring</h1>
                    <p className="text-gray-400 mt-1">Monitor your MikroTik routers in real-time</p>
                </div>
                <button
                    onClick={handleRefresh}
                    disabled={refreshing}
                    className="flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white rounded-lg transition-colors"
                >
                    <RefreshCw className={`h-4 w-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
                    {refreshing ? 'Refreshing...' : 'Refresh'}
                </button>
            </div>

            {routers.length === 0 ? (
                <div className="bg-slate-800 rounded-lg p-12 text-center">
                    <Wifi className="h-16 w-16 text-gray-600 mx-auto mb-4" />
                    <h3 className="text-xl font-semibold text-white mb-2">No Routers Found</h3>
                    <p className="text-gray-400">Add a router to start monitoring</p>
                </div>
            ) : (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {routers.map((router) => (
                        <div key={router.id} className="bg-slate-800 rounded-lg p-6 border border-slate-700">
                            <div className="flex items-start justify-between mb-6">
                                <div className="flex items-center">
                                    <div className={`p-3 rounded-lg mr-4 ${router.status === 'online' ? 'bg-green-500/20' :
                                            router.status === 'warning' ? 'bg-yellow-500/20' : 'bg-red-500/20'
                                        }`}>
                                        {router.status === 'online' ? (
                                            <CheckCircle className="h-6 w-6 text-green-500" />
                                        ) : router.status === 'warning' ? (
                                            <AlertCircle className="h-6 w-6 text-yellow-500" />
                                        ) : (
                                            <AlertCircle className="h-6 w-6 text-red-500" />
                                        )}
                                    </div>
                                    <div>
                                        <h3 className="text-lg font-semibold text-white">{router.name}</h3>
                                        <p className="text-sm text-gray-400">{router.hostname}:{router.port}</p>
                                    </div>
                                </div>
                                <div className="flex items-center space-x-2">
                                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${router.status === 'online' ? 'bg-green-500/20 text-green-400' :
                                            router.status === 'warning' ? 'bg-yellow-500/20 text-yellow-400' : 'bg-red-500/20 text-red-400'
                                        }`}>
                                        {router.status === 'online' ? 'Online' :
                                            router.status === 'warning' ? 'Warning' : 'Offline'}
                                    </span>
                                </div>
                            </div>

                            {router.latestMetrics ? (
                                <div className="grid grid-cols-2 gap-4 mb-4">
                                    <div className="bg-slate-900/50 rounded-lg p-4">
                                        <div className="flex items-center text-blue-400 mb-2">
                                            <Cpu className="h-4 w-4 mr-2" />
                                            <span className="text-sm font-medium">CPU Load</span>
                                        </div>
                                        <div className="text-2xl font-bold text-white">
                                            {router.latestMetrics.cpu_load?.toFixed(1) || '0'}%
                                        </div>
                                        <div className="mt-2 w-full bg-slate-700 rounded-full h-2">
                                            <div
                                                className={`h-2 rounded-full transition-all ${(router.latestMetrics.cpu_load || 0) > 80 ? 'bg-red-500' :
                                                        (router.latestMetrics.cpu_load || 0) > 60 ? 'bg-yellow-500' : 'bg-green-500'
                                                    }`}
                                                style={{ width: `${Math.min(router.latestMetrics.cpu_load || 0, 100)}%` }}
                                            />
                                        </div>
                                    </div>

                                    <div className="bg-slate-900/50 rounded-lg p-4">
                                        <div className="flex items-center text-purple-400 mb-2">
                                            <HardDrive className="h-4 w-4 mr-2" />
                                            <span className="text-sm font-medium">Memory</span>
                                        </div>
                                        <div className="text-2xl font-bold text-white">
                                            {router.latestMetrics.memory_used && router.latestMetrics.memory_total
                                                ? ((router.latestMetrics.memory_used / router.latestMetrics.memory_total) * 100).toFixed(1)
                                                : '0'}%
                                        </div>
                                        <div className="text-xs text-gray-400 mt-1">
                                            {formatBytes(router.latestMetrics.memory_used || 0)} / {formatBytes(router.latestMetrics.memory_total || 0)}
                                        </div>
                                    </div>

                                    <div className="bg-slate-900/50 rounded-lg p-4">
                                        <div className="flex items-center text-green-400 mb-2">
                                            <Network className="h-4 w-4 mr-2" />
                                            <span className="text-sm font-medium">Connections</span>
                                        </div>
                                        <div className="text-2xl font-bold text-white">
                                            {router.latestMetrics.active_connections || 0}
                                        </div>
                                        <div className="text-xs text-gray-400 mt-1">Active</div>
                                    </div>

                                    <div className="bg-slate-900/50 rounded-lg p-4">
                                        <div className="flex items-center text-yellow-400 mb-2">
                                            <Activity className="h-4 w-4 mr-2" />
                                            <span className="text-sm font-medium">Traffic</span>
                                        </div>
                                        <div className="text-sm text-white">
                                            <div>↓ {formatBytes(router.latestMetrics.total_rx_bytes || 0)}</div>
                                            <div>↑ {formatBytes(router.latestMetrics.total_tx_bytes || 0)}</div>
                                        </div>
                                    </div>
                                </div>
                            ) : (
                                <div className="bg-slate-900/50 rounded-lg p-6 text-center mb-4">
                                    <p className="text-gray-400 text-sm">No metrics available</p>
                                </div>
                            )}

                            <div className="flex items-center justify-between pt-4 border-t border-slate-700">
                                <div className="text-xs text-gray-400">
                                    {router.last_seen ? `Last seen: ${new Date(router.last_seen).toLocaleString()}` : 'Never connected'}
                                </div>
                                <button
                                    onClick={() => handleCollectMetrics(router.id)}
                                    className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded text-sm transition-colors"
                                >
                                    Collect Now
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

function formatBytes(bytes: number): string {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}
