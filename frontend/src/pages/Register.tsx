import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { authService } from "../services/AuthService";
import { useAuth } from "../context/AuthContext";

function Register() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [role, setRole] = useState("");
    const [error, setError] = useState("");
    const { register } = useAuth();
    const navigate = useNavigate();


    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (password.length < 6) {
            setError("Password must be at least 6 characters");
            return;
        }
        if (password !== confirmPassword) {
            setError("Passwords do not match");
            return;
        }
        try {
            const response = await authService.register(email, password);
            register(response.data.access_token);
            navigate('/login');
        } catch (err: any) {
            const detail = err?.response?.data?.detail;
            if (Array.isArray(detail)) {
                setError(detail.map((d: any) => d.msg).join(", "));
            } else {
                setError(detail ?? "Registration failed");
            }
        }
    }

    return (
        <div className="auth-wrapper">
            <div className="auth-card register-card">
                <form className="auth-form" onSubmit={handleSubmit}>
                    <h2 className="auth-title">Register</h2>
                    <p className="auth-subtitle">Create your account to access the EMS dashboard.</p>
                    <input
                        className="form-input"
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    <input
                        className="form-input"
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        minLength={6}
                        required
                    />
                    <input
                        className="form-input"
                        type="password"
                        placeholder="Confirm Password"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        required
                    />
                    <div className="role-field">
                        <label className="field-label" htmlFor="role-select">Role</label>
                        <select
                            id="role-select"
                            className="form-input"
                            value={role}
                            onChange={(e) => setRole(e.target.value)}
                            required
                        >
                            <option value="">Select Role</option>
                            <option value="user">User</option>
                            <option value="admin">Admin</option>
                        </select>
                    </div>
                    {error && <p className="error-message">{error}</p>}
                    <button className="form-button" type="submit">Register</button>
                </form>
            </div>
        </div>
    )
}

export default Register;