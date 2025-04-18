import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "@/context/theme-context";
import Dashboard from "@/pages/Dashboard";
import SignUpPage from "@/pages/SignUpPage";
import LoginPage from "@/pages/LoginPage";
import ProblemEntryPage from "@/pages/ProblemEntryPage";
import ChatPage from "@/pages/ChatPage";

function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/signup" element={<SignUpPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/home" element={<ProblemEntryPage />} />
          <Route path="/chat" element={<ChatPage />} /> 
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;