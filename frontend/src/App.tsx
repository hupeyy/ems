import { Routes, Route, BrowserRouter, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import './App.css'
import Login from "./pages/Login";
import EmployeesList from "./pages/EmployeesList";

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<Login />} />
          <Route path="/employees" element={<EmployeesList />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
} 

export default App
