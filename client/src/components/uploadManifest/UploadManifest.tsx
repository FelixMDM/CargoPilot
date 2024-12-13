'use client';

import React from "react";
import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';

const UploadManifest = () => {
    const [isUploaded, setIsUploaded] = useState(false);
    const [dynamicLink, setDynamicLink] = useState('');
    const [file, setFile] = React.useState<File>();
    const [fileName, setFileName] = useState<string>(''); // State for file name
    const searchParams = useSearchParams();

    // URL redirect logic
    useEffect(() => {
        const redirectTo = searchParams.get('redirectTo');
        if (redirectTo === '/loadUnload' || redirectTo === '/balance') {
            setDynamicLink(redirectTo);
        } else {
            setDynamicLink('/loadUnload');
        }
    }, [searchParams]);

    // Handle file selection
    const handleFileChange = function (e: React.ChangeEvent<HTMLInputElement>) {
        const filelist = e.target.files;
        if (!filelist) return;
        const selectedFile = filelist[0];
        console.log("Selected File:", selectedFile);
        setFile(selectedFile);
        setFileName(selectedFile.name); // Save the file name
    };

    // Handle the form submission (sending the file to the server)
    const handleSubmit = async () => {
        if (!file) {
            alert("Please select a file!");
            return;
        }
        const formData = new FormData();
        formData.append("manifest", file);

        try {
            const response = await fetch("http://localhost:8080/uploadManifest", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(errorText || 'Upload failed');
            }

            const result = await response.json();
            alert(result.message);
        } catch (error) {
            console.error("Full error details:", error);
            alert("There was an error uploading the file.");
        }
        setIsUploaded(true);
    };

    return (
        <div className="flex flex-col h-[80vh] text-white font-bold text-center justify-center items-center">
            <h1 className="text-2xl mb-4">Upload Manifest</h1>
            {!isUploaded ? (
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <label
                        style={{
                            display: 'flex',
                            alignItems: 'center',
                            padding: '8px',
                            border: '1px solid gray',
                            borderRadius: '8px',
                            width: '300px',
                            cursor: 'pointer',
                            backgroundColor: '#f0f0f0',
                        }}
                    >
                        <input
                            type="file"
                            onChange={handleFileChange}
                            style={{ display: 'none' }} // Hide the file input
                        />
                        <span style={{ flex: 1, color: fileName ? 'black' : '#999' }}>
                            {fileName || 'Choose File'}
                        </span>
                    </label>
                    <button
                        style={{
                            width: '300px',
                            padding: '16px',
                            marginTop: '8px',
                            backgroundColor: '#1D4ED8',
                            borderRadius: '16px',
                            color: 'white',
                            cursor: 'pointer',
                        }}
                        onClick={handleSubmit}
                    >
                        Upload Manifest
                    </button>
                </div>
            ) : (
                <div>
                    <p 
                    className="text-green-500"
                    style={{
                        marginBottom: '16px', // Adds space below the text
                        fontSize: '1.25rem'
                    }}
                    >Manifest Uploaded Successfully!</p>
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
