
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Header() {
    const { logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <header className="app-header">
            <span className="app-title">EMS</span>
            <nav className="app-nav">
                <Link className="nav-link" to="/dashboard">Dashboard</Link>
                <Link className="nav-link" to="/employees">Employees List</Link>
            </nav>
            <button className="btn-logout" onClick={handleLogout}>Logout</button>
        </header>
    );
}