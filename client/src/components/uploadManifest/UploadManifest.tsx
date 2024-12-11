'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';

const UploadManifest = () => {
    const [isUploaded, setIsUploaded] = useState(false);
    const [dynamicLink, setDynamicLink] = useState('');
    const [file, setFile] = useState(null);
    const searchParams = useSearchParams();

    //url redirect so can decide if it proceeds to load unload or balance
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

    //file logic, click to upload file button
    
    const handleUpload = () => {
        // Simulate the upload process (you can replace this with your actual upload logic)
        setIsUploaded(true);
    };

    // Handle file selection
    const handleFileChange = () => {
        // setFile(event.target.files[0]);
    };

    // Handle the form submission (sending the file to the server)
    const handleSubmit = async () => {
        if (!file) {
            alert("Please select a file!");
            return;
        }
        const formData = new FormData();
        formData.append("file", file);
        try {
            const response = await fetch("/upload", {
                method: "POST",
                body: formData,
            });
            const result = await response.json();
            alert(result.message); // Show the server response message
        } catch (error) {
            console.error("Error uploading the file:", error);
            alert("There was an error uploading the file.");
        }
    };

    return (
        <div className="flex flex-col h-[80vh] text-white font-bold text-center justify-center items-center">
            <h1 className="text-2xl mb-4">Upload Manifest</h1>
            {!isUploaded ? (
                <div>
                    <input
                        type="file"
                        onChange={handleFileChange}
                        className="mb-4 p-2 border border-gray-400 rounded-md"
                    />
                    <button
                        className="w-[300px] p-4 m-2 bg-blue-600 rounded-2xl hover:text-white"
                        onClick={handleSubmit}
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
