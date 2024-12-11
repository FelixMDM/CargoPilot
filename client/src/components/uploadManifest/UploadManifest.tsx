'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';

const UploadManifest = () => {
    const [isUploaded, setIsUploaded] = useState(false);
    const [dynamicLink, setDynamicLink] = useState('');
    const searchParams = useSearchParams();

    useEffect(() => {
        // Extract the redirectTo query parameter from the URL using useSearchParams
        const redirectTo = searchParams.get('redirectTo');
        
        // Set dynamicLink based on the value of redirectTo
        if (redirectTo === '/loadUnload' || redirectTo === '/balance') {
            setDynamicLink(redirectTo);
        } else {
            // Default case, in case no valid redirectTo is found
            setDynamicLink('/loadUnload');
        }
    }, [searchParams]); // Dependency array ensures this runs when searchParams changes

    const handleUpload = () => {
        // Simulate the upload process (you can replace this with your actual upload logic)
        setIsUploaded(true);
    };

    return (
        <div className="flex flex-col h-[80vh] text-white font-bold text-center justify-center items-center">
            <h1 className="text-2xl mb-4">Upload Manifest</h1>
            
            {!isUploaded ? (
                <div>
                    <button
                        onClick={handleUpload}
                        className="w-[300px] p-4 m-2 bg-blue-600 rounded-2xl hover:text-white"
                    >
                        Upload Manifest
                    </button>
                </div>
            ) : (
                <div>
                    <p className="text-green-500">Manifest Uploaded Successfully!</p>
                    <Link 
                        href={dynamicLink}
                        className="w-[300px] p-4 m-2 bg-blue-600 rounded-2xl hover:text-white"
                    >
                        Proceed
                    </Link>
                </div>
            )}
        </div>
    );
};

export default UploadManifest;
