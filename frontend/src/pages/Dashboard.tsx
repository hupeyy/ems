import { useCurrentUser } from "../hooks/useCurrentUser";
import { useNavigate } from "react-router-dom";

function Dashboard() {
    const { user, loading, error } = useCurrentUser();
    const navigate = useNavigate();

    return (
        <div className="page-content dashboard-page">
            <div className="dashboard-header">
                <h2 className="section-title">Dashboard</h2>
                <p className="dashboard-subtitle">Account overview and quick navigation.</p>
            </div>
            {loading && <p className="status-text">Loading...</p>}
            {error && <p className="error-message">{error}</p>}
            {!loading && !error && user && (
                <div className="dashboard-info dashboard-info-card">
                    <p className="dashboard-row"><strong className="dashboard-label">Email:</strong> <span className="dashboard-value">{user.email}</span></p>
                    <p className="dashboard-row"><strong className="dashboard-label">Role:</strong> <span className="dashboard-value role-chip">{user.role}</span></p>

                </div>
            )}
            <div className="dashboard-actions">
                <button
                    className="btn-primary"
                    onClick={() => navigate('/employees')}
                >
                    View All Employees
                </button>
            </div>
        </div>
    )
}

export default Dashboard;