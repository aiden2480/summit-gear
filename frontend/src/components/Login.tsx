import { useState, useEffect, useRef } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { authApi } from '../services/api';
import Toast from './Toast';
import useToast from '../hooks/useToast';
import './Login.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const location = useLocation();
  const navigate = useNavigate();
  const { login } = useAuth();
  const { toasts, addToast } = useToast();

  const registered = (location.state as { registered?: boolean })?.registered;
  const toastedRef = useRef(false);

  useEffect(() => {
    if (registered && !toastedRef.current) {
      toastedRef.current = true;
      addToast("Account created! Sign in to get started.", "success");
    }
  });

  const handleLogin = async (e: React.SubmitEvent) => {
    e.preventDefault();

    if (email.trim() && password.trim()) {
      try {
        const data = await authApi.login(email, password);
        login(data.user, data.token, data.role, data.id, data.avatar);
        navigate('/', { replace: true });
      } catch (err: unknown) {
        addToast(err instanceof Error ? err.message : 'Login failed. Please try again.', "error");
      }
    }
  };

  return (
    <div className="login-container">
      <Toast toasts={toasts} />
      <div className="login-card">
        <div className="login-header">
          <img src="/sunrise.svg" alt="Summit Gear" className="login-logo-img" />
          <div className="login-header-text">
            <h2>Welcome Back</h2>
            <p className="login-subtext">Your adventure starts here</p>
          </div>
        </div>
        <form onSubmit={handleLogin}>
          <div className="input-group">
            <label>Email Address</label>
            <input
              type="email"
              placeholder="name@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <label>Password</label>
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit" className="login-button">Sign In</button>
        </form>

        <div className="login-footer">
          <span>Don't have an account? <Link to="/register">Sign Up</Link></span>
        </div>
      </div>
    </div>
  );
};

export default Login;
