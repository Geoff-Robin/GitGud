
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "./components/ui/themecotext";

import Dashboard from "./pages/Dashboard";
import SignUpPage from "./components/SignUpPage";
import LoginPage from "./components/LoginPage";
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
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;