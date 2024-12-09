'use client';

import { useState } from 'react';

const UploadManifest = () => {
    const [file, setFile] = useState(null);

    // Handle file selection
    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
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
        <div className='flex flex-col h-[80vh] text-white font-bold text-center justify-center items-center'>
            <h1 className="text-2xl mb-4">Upload Manifest</h1>
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
    );
};

export default UploadManifest;
