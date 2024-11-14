
import Link from "next/link";

const Navbar = () => {
    return (
        <>
        <div className="top-0 h-[10vh] font-archivo-narrow text-2xl font-bold">
            <div className="flex flex-row space-x-2 w-full">
                <Link href="/login" className="text-black bg-slate-400 rounded-2xl p-4 m-2 hover:text-white">
                    Login
                </Link>
                <Link href="/options" className="text-black bg-slate-400 rounded-2xl p-4 m-2 hover:text-white">
                    Options
                </Link>
            </div>
        </div>
        </>
    );
};

export default Navbar;