import Link from "next/link";
import Options from "@/components/options/Options";

const Navbar = () => {
    return (
        <>
            <div className="top-0 w-full bg-slate-200 font-archivo-narrow text-2xl font-bold z-40">
                <div className="flex justify-between items-center p-4">
                    {/* Navbar Link */}
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
