"use client"

import { useState } from "react";

const Login = () => {
    const [username, setUsername] = useState('');

    const handleLogin = () => {
        if (username === '') {
            alert(`Please provide credentials`);
        } else {
            alert(`Logged in as: ${username}`);
            alert(`Please select 'Options' to proceed or login again below`); 
        }
    };

    return (
        <div className="flex flex-col h-[80vh] bg-[#f7f7f7] space-y-2 justify-center items-center">
            <p className="font-bold">Login Below</p>
            <input
                type="text"
                placeholder="Name"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-[300px] p-[10px] border-[1px] border-[#ccc] rounded-md"
            />
            <button
                onClick={handleLogin}
                className="px-5 py-2 bg-blue-600 text-white border-none rounded cursor-pointer"
            >
                Login
            </button>
        </div>
    );
}

export default Login;
