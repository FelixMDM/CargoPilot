"use client";
import { useEffect, useState } from "react";

const Home = () => {
  const [message, setMessage] = useState("fetching...");

  useEffect(() => {
    fetch("http://localhost:8080/test")
      .then((response) => response.json())
      .then((data) => {

        setMessage(data.message);
      });
  }, []);

  return (
    <div>
      {message}
    </div>
  );
}

export default Home;
