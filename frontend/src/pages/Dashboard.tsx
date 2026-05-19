import { useCurrentUser } from "../hooks/UseCurrentUser";
import { useNavigate } from "react-router-dom";

function Dashboard() {
    const { user, loading, error } = useCurrentUser();
    const navigate = useNavigate();

    return (
        <div className="page-content">
            <h2 className="section-title">Dashboard</h2>
            {loading && <p>Loading...</p>}
            {error && <p className="error-message">{error}</p>}
            {!loading && !error && user && (
                <div className="dashboard-info">
                    <p><strong>Email:</strong> {user.email}</p>
                    <p><strong>Role:</strong> {user.role}</p>
                </div>
            )}
            <button
                className="btn-primary"
                onClick={() => navigate('/employees')}
            >
                View All Employees
            </button>
        </div>
    )
}

export default Dashboard;