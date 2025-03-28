import React from 'react';
import { Link } from 'react-router-dom';
import './NavBar.css';

function NavBar() {
  return (
    <nav>
      <Link to="/">Home</Link> |{" "}
      <Link to="/create">Create Event</Link> |{" "}
      <Link to="/login">Login</Link> |{" "}
      <Link to="/register">Register</Link>
    </nav>
  );
}

export default NavBar;

