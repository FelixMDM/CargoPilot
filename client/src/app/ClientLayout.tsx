"use client";
import { usePathname } from 'next/navigation';
import Navbar from "@/components/Navbar";
import { UserProvider } from "@/app/UserContext";

export default function ClientLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const isHomePage = pathname === '/';

  return (
    <UserProvider>
      {!isHomePage && <Navbar />}
      {children}
    </UserProvider>
  );
}