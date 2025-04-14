import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "./context/theme-context";
import Dashboard from "./pages/Dashboard";
import SignUpPage from "./pages/SignUpPage";
import LoginPage from "./pages/LoginPage";
import ProblemEntryPage from "./pages/ProblemEntryPage";

function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/signup" element={<SignUpPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/problems" element={<ProblemEntryPage />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;