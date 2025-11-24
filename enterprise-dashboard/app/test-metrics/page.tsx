'use client';

import { useState } from 'react';

export default function TestMetrics() {
    const [result, setResult] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    const testCollect = async () => {
        setLoading(true);
        setResult(null);
        try {
            const token = localStorage.getItem('access_token');
            const response = await fetch('http://localhost:8001/api/v1/routers/1/collect/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });
            const data = await response.json();
            setResult({ status: response.status, data });
        } catch (error: any) {
            setResult({ error: error.message });
        } finally {
            setLoading(false);
        }
    };

    const checkStatus = async () => {
        setLoading(true);
        setResult(null);
        try {
            const token = localStorage.getItem('access_token');
            const response = await fetch('http://localhost:8001/api/v1/routers/1/status/', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });
            const data = await response.json();
            setResult({ status: response.status, data });
        } catch (error: any) {
            setResult({ error: error.message });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-900 p-8">
            <div className="max-w-4xl mx-auto">
                <h1 className="text-3xl font-bold text-white mb-6">Test Metrics Collection</h1>
                
                <div className="bg-gray-800 rounded-lg p-6 mb-4">
                    <div className="flex gap-4 mb-6">
                        <button
                            onClick={testCollect}
                            disabled={loading}
                            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white rounded-lg font-semibold"
                        >
                            {loading ? 'Testing...' : 'Collect Metrics (POST /routers/1/collect/)'}
                        </button>
                        <button
                            onClick={checkStatus}
                            disabled={loading}
                            className="px-6 py-3 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white rounded-lg font-semibold"
                        >
                            {loading ? 'Checking...' : 'Check Status (GET /routers/1/status/)'}
                        </button>
                    </div>

                    {result && (
                        <div className="bg-gray-900 rounded p-4">
                            <h3 className="text-white font-semibold mb-2">Result:</h3>
                            <pre className="text-green-400 text-sm overflow-auto">
                                {JSON.stringify(result, null, 2)}
                            </pre>
                        </div>
                    )}
                </div>

                <div className="bg-yellow-900/30 border border-yellow-600 rounded-lg p-4">
                    <h3 className="text-yellow-400 font-semibold mb-2">Instructions:</h3>
                    <ol className="text-yellow-200 space-y-2 text-sm list-decimal list-inside">
                        <li>Make sure you're logged in first</li>
                        <li>Click "Collect Metrics" to fetch data from MikroTik router</li>
                        <li>Click "Check Status" to see if metrics exist</li>
                        <li>Check the result below</li>
                    </ol>
                </div>
            </div>
        </div>
    );
}
