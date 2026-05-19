import { Routes, Route, BrowserRouter, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import './App.css'
import Login from "./pages/Login";

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
} 

export default App
