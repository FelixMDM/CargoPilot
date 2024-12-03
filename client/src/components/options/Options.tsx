'use client';

import Link from 'next/link';

const Options = () => {
    return (
        <div className='flex flex-col h-[80vh] text-white font-bold text-center justify-center items-center space-y-2'>
            <Link 
                href="/loadUnload"
                className="w-[300px] p-4 m-2 bg-blue-600 rounded-2xl hover:text-white"
            >
                Load/Unload
            </Link>
            <Link 
                href="/balance"
                className="w-[300px] p-4 m-2 bg-blue-600 rounded-2xl hover:text-white">
                    Balance
            </Link>
        </div>
    );
};

export default Options;
