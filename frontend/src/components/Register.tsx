import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authApi } from '../services/api';
import './Login.css';

const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e: React.SubmitEvent) => {
    e.preventDefault();
    setError('');
    if (email.trim() && password.trim()) {
      try {
        await authApi.register(email, password);
        navigate('/login', { replace: true });
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'Registration failed. Please try again.');
      }
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <img src="/sunrise.svg" alt="Summit Gear" className="login-logo-img" />
          <div className="login-header-text">
            <h2>Create Account</h2>
            <p className="login-subtext">Join Summit Gear today</p>
          </div>
        </div>
        <form onSubmit={handleRegister}>
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
              minLength={8}
              required
            />
          </div>

          <button type="submit" className="login-button">Sign Up</button>
          {error && <p className="login-error">{error}</p>}
        </form>

        <div className="login-footer">
          <span>Already have an account? <Link to="/login">Sign In</Link></span>
        </div>
      </div>
    </div>
  );
};

export default Register;
