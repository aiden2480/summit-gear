import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './Login.css';

const API_BASE_URL = 'http://localhost:8080';

const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (email.trim() && password.trim()) {
      try {
        const response = await fetch(API_BASE_URL + '/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: email, password }),
        });
        if (response.ok) {
          navigate('/login', { replace: true });
        } else {
          const err = await response.json();
          setError(err.error || 'Registration failed. Please try again.');
        }
      } catch {
        setError('Error registering. Please try again.');
      }
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Create Account</h2>
        <p>Join Summit Gear today</p>

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
