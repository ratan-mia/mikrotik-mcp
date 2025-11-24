'use client';

import { apiService, Router } from '@/lib/api';
import { Activity, ExternalLink, Plus, Server, Settings, Wifi, WifiOff } from 'lucide-react';
import { useEffect, useState } from 'react';

export default function RoutersPage() {
    const [routers, setRouters] = useState<Router[]>([]);
    const [loading, setLoading] = useState(true);
    const [showAddModal, setShowAddModal] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        // Only load routers if we have a token
        const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
        if (token) {
            loadRouters();
        } else {
            setError('No authentication token found');
            setLoading(false);
        }
    }, []);

    const loadRouters = async () => {
        try {
            setError(null);
            const data = await apiService.getRouters();
            setRouters(data);
        } catch (error: any) {
            console.error('Failed to load routers:', error);
            const errorMsg = error.response?.status === 401
                ? 'Session expired. Please log in again.'
                : 'Failed to load routers. Please try again.';
            setError(errorMsg);
        } finally {
            setLoading(false);
        }
    };

    const handleCollectMetrics = async (routerId: number) => {
        try {
            await apiService.collectMetrics(routerId);
            alert('Metrics collection started successfully');
        } catch (error) {
            console.error('Failed to collect metrics:', error);
            alert('Failed to collect metrics');
        }
    };

    if (loading) {
        return <div className="text-white">Loading routers...</div>;
    }

    if (error) {
        return (
            <div className="bg-red-500/20 border border-red-500 rounded-xl p-6 text-center">
                <p className="text-red-400 text-lg mb-4">{error}</p>
                <div className="flex gap-3 justify-center">
                    <button
                        onClick={loadRouters}
                        className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg transition"
                    >
                        Retry
                    </button>
                    {error.includes('Session expired') || error.includes('authentication') ? (
                        <button
                            onClick={() => {
                                localStorage.clear();
                                window.location.href = '/';
                            }}
                            className="bg-slate-600 hover:bg-slate-700 text-white font-semibold py-2 px-6 rounded-lg transition"
                        >
                            Go to Login
                        </button>
                    ) : null}
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-white mb-2">MikroTik Routers</h2>
                    <p className="text-slate-400">Manage and monitor your network devices</p>
                </div>
                <button
                    onClick={() => setShowAddModal(true)}
                    className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition flex items-center space-x-2"
                >
                    <Plus className="h-5 w-5" />
                    <span>Add Router</span>
                </button>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-slate-400 text-sm">Total Routers</p>
                            <p className="text-3xl font-bold text-white mt-1">{routers.length}</p>
                        </div>
                        <Server className="h-12 w-12 text-blue-500" />
                    </div>
                </div>
                <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-slate-400 text-sm">Active</p>
                            <p className="text-3xl font-bold text-green-400 mt-1">
                                {routers.filter(r => r.is_active).length}
                            </p>
                        </div>
                        <Wifi className="h-12 w-12 text-green-500" />
                    </div>
                </div>
                <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-slate-400 text-sm">Offline</p>
                            <p className="text-3xl font-bold text-slate-400 mt-1">
                                {routers.filter(r => !r.is_active).length}
                            </p>
                        </div>
                        <WifiOff className="h-12 w-12 text-slate-500" />
                    </div>
                </div>
            </div>

            {/* Routers List */}
            <div className="space-y-4">
                {routers.length === 0 ? (
                    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-12 border border-slate-700 text-center">
                        <Server className="h-16 w-16 text-slate-600 mx-auto mb-4" />
                        <h3 className="text-xl font-semibold text-white mb-2">No routers yet</h3>
                        <p className="text-slate-400 mb-6">Add your first MikroTik router to get started</p>
                        <button
                            onClick={() => setShowAddModal(true)}
                            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg transition inline-flex items-center space-x-2"
                        >
                            <Plus className="h-5 w-5" />
                            <span>Add Router</span>
                        </button>
                    </div>
                ) : (
                    routers.map((router) => (
                        <RouterCard
                            key={router.id}
                            router={router}
                            onCollectMetrics={handleCollectMetrics}
                            onRefresh={loadRouters}
                        />
                    ))
                )}
            </div>

            {/* Add Router Modal */}
            {showAddModal && (
                <AddRouterModal
                    onClose={() => setShowAddModal(false)}
                    onSuccess={() => {
                        setShowAddModal(false);
                        loadRouters();
                    }}
                />
            )}
        </div>
    );
}

function RouterCard({
    router,
    onCollectMetrics,
    onRefresh
}: {
    router: Router;
    onCollectMetrics: (id: number) => void;
    onRefresh: () => void;
}) {
    const [status, setStatus] = useState<any>(null);
    const [loadingStatus, setLoadingStatus] = useState(false);

    const checkStatus = async () => {
        setLoadingStatus(true);
        try {
            const data = await apiService.getRouterStatus(router.id);
            setStatus(data);
        } catch (error) {
            console.error('Failed to get status:', error);
        } finally {
            setLoadingStatus(false);
        }
    };

    useEffect(() => {
        if (router.is_active) {
            checkStatus();
        }
    }, [router.id, router.is_active]);

    return (
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700 hover:border-slate-600 transition">
            <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-4">
                    <div className={`p-3 rounded-lg ${router.is_active ? 'bg-green-500/20' : 'bg-slate-700'}`}>
                        <Server className={`h-8 w-8 ${router.is_active ? 'text-green-400' : 'text-slate-400'}`} />
                    </div>
                    <div>
                        <h3 className="text-xl font-semibold text-white">{router.name}</h3>
                        <p className="text-slate-400 text-sm">{router.hostname}:{router.port}</p>
                        {router.location && (
                            <p className="text-slate-500 text-sm mt-1">📍 {router.location}</p>
                        )}
                    </div>
                </div>
                <div className="flex items-center space-x-2">
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${router.is_active
                        ? 'bg-green-500/20 text-green-400'
                        : 'bg-slate-700 text-slate-400'
                        }`}>
                        {router.is_active ? 'Active' : 'Inactive'}
                    </span>
                </div>
            </div>

            {router.description && (
                <p className="text-slate-300 mb-4">{router.description}</p>
            )}

            {/* Status Info */}
            {status && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4 p-4 bg-slate-900/50 rounded-lg">
                    <div>
                        <p className="text-slate-500 text-xs">Router OS</p>
                        <p className="text-white font-semibold">{status.routeros_version || 'N/A'}</p>
                    </div>
                    <div>
                        <p className="text-slate-500 text-xs">Board</p>
                        <p className="text-white font-semibold">{status.board_name || 'N/A'}</p>
                    </div>
                    <div>
                        <p className="text-slate-500 text-xs">Uptime</p>
                        <p className="text-white font-semibold">{status.uptime || 'N/A'}</p>
                    </div>
                    <div>
                        <p className="text-slate-500 text-xs">CPU Load</p>
                        <p className="text-white font-semibold">{status.cpu_load || '0'}%</p>
                    </div>
                </div>
            )}

            {/* Actions */}
            <div className="flex flex-wrap gap-2">
                <button
                    onClick={checkStatus}
                    disabled={loadingStatus}
                    className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 text-white text-sm font-semibold py-2 px-4 rounded-lg transition flex items-center space-x-2"
                >
                    <Activity className="h-4 w-4" />
                    <span>{loadingStatus ? 'Checking...' : 'Check Status'}</span>
                </button>
                <button
                    onClick={() => onCollectMetrics(router.id)}
                    className="bg-slate-700 hover:bg-slate-600 text-white text-sm font-semibold py-2 px-4 rounded-lg transition flex items-center space-x-2"
                >
                    <Settings className="h-4 w-4" />
                    <span>Collect Metrics</span>
                </button>
                <a
                    href={`http://${router.hostname}:${router.port === 22 ? 80 : router.port}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="bg-slate-700 hover:bg-slate-600 text-white text-sm font-semibold py-2 px-4 rounded-lg transition flex items-center space-x-2"
                >
                    <ExternalLink className="h-4 w-4" />
                    <span>Web UI</span>
                </a>
            </div>

            {router.last_seen && (
                <p className="text-slate-500 text-xs mt-4">
                    Last seen: {new Date(router.last_seen).toLocaleString()}
                </p>
            )}
        </div>
    );
}

function AddRouterModal({
    onClose,
    onSuccess
}: {
    onClose: () => void;
    onSuccess: () => void;
}) {
    const [formData, setFormData] = useState({
        name: '',
        hostname: '',
        port: 22,
        username: '',
        password: '',
        description: '',
        location: ''
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const response = await fetch('/api/v1/routers', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                },
                body: JSON.stringify({
                    ...formData,
                    port: parseInt(formData.port.toString()),
                    is_active: true
                })
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.detail || 'Failed to add router');
            }

            onSuccess();
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
            <div className="bg-slate-800 rounded-xl p-6 max-w-2xl w-full border border-slate-700 max-h-[90vh] overflow-y-auto">
                <h3 className="text-2xl font-bold text-white mb-6">Add New Router</h3>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-slate-300 mb-2">
                                Router Name *
                            </label>
                            <input
                                type="text"
                                required
                                value={formData.name}
                                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                                placeholder="Main Office Router"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-slate-300 mb-2">
                                Hostname/IP *
                            </label>
                            <input
                                type="text"
                                required
                                value={formData.hostname}
                                onChange={(e) => setFormData({ ...formData, hostname: e.target.value })}
                                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                                placeholder="192.168.1.1"
                            />
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-slate-300 mb-2">
                                SSH Port *
                            </label>
                            <input
                                type="number"
                                required
                                value={formData.port}
                                onChange={(e) => setFormData({ ...formData, port: parseInt(e.target.value) })}
                                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                                placeholder="22"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-slate-300 mb-2">
                                Location
                            </label>
                            <input
                                type="text"
                                value={formData.location}
                                onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                                placeholder="Main Office"
                            />
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-slate-300 mb-2">
                                Username *
                            </label>
                            <input
                                type="text"
                                required
                                value={formData.username}
                                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                                placeholder="admin"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-slate-300 mb-2">
                                Password *
                            </label>
                            <input
                                type="password"
                                required
                                value={formData.password}
                                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                            />
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">
                            Description
                        </label>
                        <textarea
                            value={formData.description}
                            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                            rows={3}
                            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                            placeholder="Primary network router..."
                        />
                    </div>

                    {error && (
                        <div className="bg-red-500/20 border border-red-500 rounded-lg p-3 text-red-400 text-sm">
                            {error}
                        </div>
                    )}

                    <div className="flex justify-end space-x-3 pt-4">
                        <button
                            type="button"
                            onClick={onClose}
                            className="bg-slate-700 hover:bg-slate-600 text-white font-semibold py-2 px-6 rounded-lg transition"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            disabled={loading}
                            className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 text-white font-semibold py-2 px-6 rounded-lg transition"
                        >
                            {loading ? 'Adding...' : 'Add Router'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
