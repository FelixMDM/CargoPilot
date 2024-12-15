"use client";
import { useEffect, useState } from "react";
import Image from 'next/image';
import Link from "next/link";

const Home = () => {
  // const [message, setMessage] = useState("fetching...");

  // useEffect(() => {
  //   fetch("http://localhost:8080/test")
  //     .then((response) => response.json())
  //     .then((data) => {

  //       setMessage(data.message);
  //     });
  // }, []);

  // return (
  //   <div>
  //     {message}
  //   </div>
  // );
  return (
    <div className="min-h-screen bg-blue-50 flex flex-col items-center justify-center p-4">
      {/* Increased max-w-4xl to max-w-5xl and padding from p-8 to p-12 */}
      <div className="max-w-7xl w-full bg-[#ADD8E6] rounded-lg shadow-lg p-28">
        <div className="text-center space-y-6">
          {/* Logo */}
          <div className="mx-auto w-60 h-60 relative">
            <Image
              src="/Logo.png"
              alt="CargoPilot Logo"
              fill
              style={{ objectFit: 'contain' }}
              priority
            />
          </div>

          {/* Company name */}
          <h1 className="text-5xl font-bold text-gray-800">
            CargoPilot
          </h1>

          {/* Tagline */}
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Navigating Port Efficiency Through Intelligent Container Orchestration
          </p>

          {/* Login Link - replaced button with Link */}
          <Link 
            href="/login" 
            className="inline-block mt-8 px-8 py-4 bg-white text-gray-800 rounded-lg hover:bg-gray-50 transition-colors text-lg font-bold"
          >
            Login
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Home;
