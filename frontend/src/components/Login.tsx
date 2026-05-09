import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './Login.css';

const API_BASE_URL = 'http://localhost:8080';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e: React.SubmitEvent) => {
    e.preventDefault();
    if (email.trim() && password.trim()) {
      try {
        const response = await fetch(API_BASE_URL + '/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: email, password }),
        });
        if (response.ok) {
          const data = await response.json();
          localStorage.setItem('user', data.user);
          localStorage.setItem('token', data.token);
          localStorage.setItem('role', data.role);
          navigate('/', { replace: true });
        } else {
          alert('Login failed. Please check your credentials.');
        }
      } catch {
        alert('Error logging in. Please try again.');
      }
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Welcome Back</h2>
        <p>Your adventure starts here</p>

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
