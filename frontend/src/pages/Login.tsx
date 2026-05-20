import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { authService } from "../services/authService";
import { useAuth } from "../context/AuthContext";

function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const { data } = await authService.login(email, password);
            login(data.access_token);
            navigate('/dashboard');
        } catch (err) {
            setError("Invalid email or password");
        }
    }

    return (
        <div className="auth-wrapper">
            <div className="auth-card">
                <form className="auth-form" onSubmit={handleSubmit}>
                    <h2 className="auth-title">Login</h2>
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
                        required
                    />
                    <button className="btn-primary" type="submit">Login</button>
                    {error && <p className="error-text">{error}</p>}
                    <p className="auth-footer">No account? <Link className="auth-link" to="/register">Register</Link></p>
                </form>
            </div>
        </div>
    )
}

export default Login