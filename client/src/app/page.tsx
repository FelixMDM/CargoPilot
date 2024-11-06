"use client"

import React, { useEffect, useState } from "react";

function index() {
  const [message, setMessage] = useState("Loading");

  useEffect(() => {
    fetch("http://localhost:8080/api/home")
      .then((response) => response.json())
      .then((data) => {
        // message = 'Loading'
        // once data is retrieved
        // message = data.message
        setMessage(data.message);
      });
  }, []);

  return (
    <div>
      <div>{message}</div>
    </div>
  );
}

export default index;
