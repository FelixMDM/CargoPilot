'use client';

const UploadManifest = () => {
    return (
        <div className='flex flex-col h-[80vh] text-white font-bold text-center justify-center items-center'>
            <h1 className="text-2xl mb-4">Upload Manifest</h1>
            <button 
                className="w-[300px] p-4 m-2 bg-blue-600 rounded-2xl hover:text-white"
                onClick={() => alert('Upload Manifest Clicked!')}
            >
                Upload Manifest
            </button>
        </div>
    );
};

export default UploadManifest;
