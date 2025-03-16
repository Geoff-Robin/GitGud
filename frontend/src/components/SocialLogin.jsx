import React from 'react';

const SocialLogin = () => {
  return (
    <div className="mb-8">
      <button className="flex items-center justify-center w-full bg-white text-gray-700 rounded-full py-3 px-4 mb-4 transition cursor-pointer">
        <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M12 5c1.6 0 3 .5 4.1 1.4l3.2-3.2C17.1 1.4 14.7 0 12 0 7.3 0 3.3 2.6 1.3 6.3l3.7 2.8C6.1 6.3 8.8 5 12 5z" />
          <path fill="#34A853" d="M23.5 12.3c0-.8-.1-1.7-.2-2.5H12v4.8h6.5c-.3 1.6-1.1 2.9-2.4 3.8l3.6 2.8c2.1-2 3.3-4.9 3.3-8.9z" />
          <path fill="#FBBC05" d="M5 14.1c-.3-.8-.4-1.7-.4-2.6 0-.9.2-1.8.4-2.6L1.3 6.1C.5 7.9 0 9.9 0 12s.5 4.1 1.3 5.9l3.7-2.8z" />
          <path fill="#EA4335" d="M12 24c3.2 0 5.9-1.1 7.9-2.9l-3.6-2.8c-1 .7-2.3 1.1-4.3 1.1-3.2 0-5.9-1.3-7-4.1L1.3 18c2 4.2 6.2 6 10.7 6z" />
        </svg>
        Sign up with Google
      </button>
      
      <div className="flex items-center justify-between mb-4">
        <div className="w-full h-px bg-gray-300"></div>
        <div className="text-white px-4">Or</div>
        <div className="w-full h-px bg-gray-300"></div>
      </div>
      
     
    </div>
  );
};

export default SocialLogin;