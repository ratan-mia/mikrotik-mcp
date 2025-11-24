'use client';

import DashboardLayout from '@/components/DashboardLayout';
import LoginPage from '@/components/LoginPage';
import Overview from '@/components/Overview';
import { useAuthStore } from '@/lib/store';
import { useEffect, useState } from 'react';

export default function Home() {
    const { isAuthenticated, checkAuth } = useAuthStore();
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        checkAuth().finally(() => setIsLoading(false));
    }, [checkAuth]);

    if (isLoading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
                <div className="text-white text-xl">Loading...</div>
            </div>
        );
    }

    if (!isAuthenticated) {
        return <LoginPage />;
    }

    return (
        <DashboardLayout>
            <Overview />
        </DashboardLayout>
    );
}
