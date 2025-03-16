import React from 'react';
import BackgroundImage from './BackgroundImage';
import SignUpForm from './SignUpForm';

const SignUpPage = () => {
  console.log("SignUpPage rendering");
  
  return (
    <div className="flex min-h-screen w-full bg-black bg-opacity-90 items-center justify-center px-4 py-8">
      <div className="flex h-[85vh] w-full max-w-5xl shadow-xl rounded-xl overflow-hidden">
        
        {/* Left side - Background Image */}
        <div className="hidden md:block w-1/2 h-full relative">
          <BackgroundImage />
        </div>
        
        {/* Right side - Now with actual SignUpForm */}
        <div className="w-full md:w-1/2 bg-black flex items-center justify-center p-6">
          <div className="w-[90%] max-w-lg">
            <SignUpForm />
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignUpPage;