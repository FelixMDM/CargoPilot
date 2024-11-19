'use client';

import Link from 'next/link';
import { useState } from 'react';

const Options = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const handleToggleModal = () => {
        setIsModalOpen((prev) => !prev);
    };

    const handleLinkClick = () => {
        setIsModalOpen(false); // automatically close list
    };

    const handleCloseModal = () => {
        setIsModalOpen(false); //close button
    };

    return (
        <>
            {/* actual button */}
            <button
                onClick={handleToggleModal}
                className="text-black bg-slate-400 rounded-2xl p-4 m-2 hover:text-white z-50"
            >
                Options
            </button>

            {/* list */}
            {isModalOpen && (
                <div
                    style={{
                        position: 'fixed',
                        top: 0,
                        left: 0,
                        width: '100vw',
                        height: '100vh',
                        backgroundColor: 'rgba(0, 0, 0, 0.5)',
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        zIndex: 999,
                    }}
                >
                    <div
                        style={{
                            backgroundColor: '#fff',
                            padding: '20px',
                            borderRadius: '10px',
                            boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
                            textAlign: 'center',
                            width: '300px',
                        }}
                    >
                        <h2>Options</h2>
                        <div style={{ margin: '20px 0' }}>
                            <Link href="/load-unload">
                                <button
                                    onClick={handleLinkClick}
                                    className="w-full p-4 m-2 text-black bg-slate-400 rounded-2xl hover:text-white"
                                >
                                    Load/Unload
                                </button>
                            </Link>
                            <Link href="/balance">
                                <button
                                    onClick={handleLinkClick}
                                    className="w-full p-4 m-2 text-black bg-slate-400 rounded-2xl hover:text-white"
                                >
                                    Balance
                                </button>
                            </Link>
                            <Link href="/login">
                                <button
                                    onClick={handleLinkClick}
                                    className="w-full p-4 m-2 text-black bg-slate-400 rounded-2xl hover:text-white"
                                >
                                    Login
                                </button>
                            </Link>
                        </div>
                        <button
                            onClick={handleCloseModal} // Close the modal manually
                            style={{
                                padding: '10px 20px',
                                backgroundColor: 'red',
                                color: '#fff',
                                border: 'none',
                                borderRadius: '5px',
                                cursor: 'pointer',
                                width: '100%',
                            }}
                        >
                            Close
                        </button>
                    </div>
                </div>
            )}
        </>
    );
};

export default Options;
