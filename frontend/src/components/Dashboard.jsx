import React from "react";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const navigate = useNavigate();
  
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-black p-4">
      <h1 className="text-white 3xl font-bold mb-8">Welcome to the Dashboard</h1>
      
      <div className="flex gap-4">
        <button 
          className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition cursor-pointer"
          onClick={() => navigate("/signup")}
        >
          Sign Up
        </button>
        
        <button 
          className="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition cursor-pointer"
          onClick={() => navigate("/login")}
        >
          Log In
        </button>
      </div>
    </div>
  );
};

export default Dashboard;