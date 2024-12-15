'use client';

import Link from 'next/link';
import { useUser } from '@/app/UserContext';

const Options = () => {
    const { currentUser } = useUser();

    const downloadLogs = () => {
        window.location.href = 'http://localhost:8080/download-logs';
    };

    // Check if the current user is Mr. Keogh (case variations handled)
    const isAdmin = currentUser.toLowerCase() === 'mr. keogh' || 
                   currentUser.toLowerCase() === 'mr.keogh' ||
                   currentUser.toLowerCase() === 'mr keogh';

    return (
        <div className='flex flex-col h-[80vh] text-white font-bold text-center justify-center items-center space-y-2'>
            <Link 
                href="/uploadManifest?redirectTo=/loadUnload"
                className="w-[300px] p-4 m-2 bg-blue-600 rounded-2xl hover:text-white"
            >
                Load/Unload
            </Link>
            <Link 
                href="/uploadManifest?redirectTo=/balance"
                className="w-[300px] p-4 m-2 bg-blue-600 rounded-2xl hover:text-white">
                    Balance
            </Link>
            {isAdmin && (
                <button
                    onClick={downloadLogs}
                    className="w-[300px] p-4 m-2 bg-green-600 rounded-2xl hover:text-white cursor-pointer"
                >
                    Download Logs
                </button>
            )}
        </div>
    );
};

export default Options;