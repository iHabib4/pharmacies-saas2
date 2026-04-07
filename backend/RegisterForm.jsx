// RegisterForm.jsx
import { useState } from 'react';
import axios from 'axios';

export default function RegisterForm() {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('customer'); // default

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('/api/auth/register/', { email, username, password, role })
      .then(res => alert('Registered successfully!'))
      .catch(err => alert('Error: ' + err.response.data.detail));
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} required />
      <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
      <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
      
      <select value={role} onChange={e => setRole(e.target.value)}>
        <option value="customer">Customer</option>
        <option value="pharmacy">Pharmacy</option>
        <option value="rider">Rider</option>
        <option value="supplier">Supplier</option>
      </select>

      <button type="submit">Register</button>
    </form>
  );
}
