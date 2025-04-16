import React from "react";
import { useNavigate } from "react-router-dom";
import { useTheme } from "@/context/theme-context";

const Navbar = () => {
  const navigate = useNavigate();

  return (
    <div className="md:sticky md:top-0 md:z-50 bg-background bg-opacity-30 backdrop-filter backdrop-blur-lg border-b-0 border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo/Brand */}
          <div className="flex-shrink-0">
            <h1
              className="text-foreground text-xl cursor-pointer title" 
              onClick={() => navigate("/")}
            >
              GitGud
            </h1>
          </div>

          {/* Right side buttons */}
          <div className="flex items-center space-x-4">
            {/* Login Button */}
            <button
              onClick={() => navigate("/login")}
              className="text-foreground hover:text-gray-300 px-3 py-2 rounded-md text-sm font-medium cursor-pointer"
            >
              Login
            </button>

            {/* Sign Up Button */}
            <button
              onClick={() => navigate("/signup")}
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-full text-sm font-medium transition-colors duration-200 cursor-pointer"
            >
              Sign Up
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Navbar;
