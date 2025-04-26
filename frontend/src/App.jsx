import { BrowserRouter, Routes, Route } from "react-router-dom";
<<<<<<< HEAD
import { ThemeProvider } from "./components/ui/themecotext";

import Dashboard from "./pages/Dashboard";
import SignUpPage from "./components/SignUpPage";
import LoginPage from "./components/LoginPage";
import ProblemEntryPage from "./pages/ProblemEntryPage";
import ChatPage from "./pages/ChatPage";
import ProblemEntryPage from "./pages/ProblemEntryPage";
import ChatPage from "./pages/ChatPage";

function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/signup" element={<SignUpPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/problems" element={<ProblemEntryPage />} />
          <Route path="/chat" element={<ChatPage />} /> 
          <Route path="/chat" element={<ChatPage />} /> 
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
=======
import { ThemeProvider } from "@/context/theme-context";
import Dashboard from "@/pages/Dashboard";
import SignUpPage from "@/pages/SignUpPage";
import LoginPage from "@/pages/LoginPage";
import ProblemEntryPage from "@/pages/ProblemEntryPage";
import ChatPage from "@/pages/ChatPage";
import { AuthContextProvider } from "./context/auth-context";
function App() {
  return (
    <AuthContextProvider>
      <ThemeProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/signup" element={<SignUpPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/home" element={<ProblemEntryPage />} />
            <Route path="/chat/:id" element={<ChatPage />} /> 
          </Routes>
        </BrowserRouter>
      </ThemeProvider>
    </AuthContextProvider>
>>>>>>> c7b3440e5ad509bce6a7cb1fd10528d1514d5cc3
  );
}

export default App;