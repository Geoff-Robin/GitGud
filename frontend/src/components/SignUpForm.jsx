import React from 'react';
// Import but don't use immediately


const SignUpForm = () => {
  return (
    <div className="w-full max-w-md">
      <div className="text-center mb-10">
        <h1 className="text-3xl font-normal text-white mb-2">Hello!</h1>
        <p className="text-xl text-white">We are glad to see you :)</p>
      </div>
      
       
      
      
      
      
      {/* Form fields */}
      <form>
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-white text-sm mb-1">Name</label>
            <input type="text" className="w-full bg-transparent border border-white rounded-full px-4 py-2 text-white" />
          </div>
          <div>
            <label className="block text-white text-sm mb-1">Email Adress</label>
            <input type="email" className="w-full bg-transparent border border-white rounded-full px-4 py-2 text-white" />
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block text-white text-sm mb-1">Password</label>
            <input type="password" className="w-full bg-transparent border border-white rounded-full px-4 py-2 text-white" placeholder="xxxxxxxx" />
          </div>
          <div>
            <label className="block text-white text-sm mb-1">Repead Password</label>
            <input type="password" className="w-full bg-transparent border border-white rounded-full px-4 py-2 text-white" placeholder="xxxxxxxx" />
          </div>
        </div>
        
        <div className="mb-6">
          <label className="flex items-center">
            <input type="checkbox" className="form-checkbox rounded text-teal-500 border-white border transition cursor-pointer" />
            <span className="ml-2 text-white text-sm transition cursor-pointer">
              I agree <a href="#" className="underline">Terms of Service</a> and <a href="#" className="underline">Privacy Policy</a>
            </span>
          </label>
        </div>
        
        <button
          type="submit"
          className="w-full bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-3 px-4 rounded-full transition cursor-pointer"
        >
          Sign Up
        </button>
      </form>
    </div>
  );
};

export default SignUpForm;