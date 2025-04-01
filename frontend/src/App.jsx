import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "./components/ui/themecotext";
import Dashboard from "./components/Dashboard";
import SignUpPage from "./components/SignUpPage";
import LoginPage from "./components/LoginPage";
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
          </Routes>
        </BrowserRouter>
      </ThemeProvider>
    </AuthContextProvider>
  );
}

export default App;