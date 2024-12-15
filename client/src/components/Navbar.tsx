"use client";
import Link from "next/link";
import { useUser } from "@/app/UserContext";

const Navbar = () => {
    const { currentUser } = useUser();

    return (
        <>
            <div className="top-0 w-full bg-slate-200 font-archivo-narrow text-2xl font-bold z-40">
                <div className="flex justify-between items-center p-4">
                    {/* Navbar Links */}
                    <div className="flex items-center gap-4">
                        <Link href="/login" className="text-black bg-slate-400 rounded-2xl p-4 m-2 hover:text-white">
                            Login
                        </Link>
                        <Link href="/options" className="text-black bg-slate-400 rounded-2xl p-4 m-2 hover:text-white">
                            Options
                        </Link>
                    </div>
                    {/* Display username if logged in */}
                    {currentUser && (
                        <span className="text-black px-4">
                            Welcome, {currentUser}
                        </span>
                    )}
                </div>
            </div>
        </>
    );
};

export default Navbar;