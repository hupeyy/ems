import { Routes, Route, BrowserRouter, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import './App.css'
import { ProtectedRoute } from "./components/ProtectedRoute";
import Header from "./components/Header";
import Login from "./pages/Login";
import EmployeesList from "./pages/EmployeesList";
import EmployeesForm from "./pages/EmployeesForm";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/employees" element={<ProtectedRoute><><Header /><EmployeesList /></></ProtectedRoute>} />
          <Route path="/employees/form" element={<ProtectedRoute><><Header /><EmployeesForm /></></ProtectedRoute>} />
          <Route path="/dashboard" element={<ProtectedRoute><><Header /><Dashboard /></></ProtectedRoute>} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
} 

export default App
