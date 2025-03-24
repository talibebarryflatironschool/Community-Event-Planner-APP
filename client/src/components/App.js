// // import React, { useEffect, useState } from "react";
// // import { Switch, Route } from "react-router-dom";

// // function App() {
// //   return <h1>Project Client</h1>;
// // }

// // export default App;






// // client/src/components/App.js

// import React from "react";
// import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
// import EventDetail from "./EventDetail";
// import CreateEvent from "./CreateEvent";
// import EditEvent from "./EditEvent";

// function App() {
//   return (
//     <Router>
//       <nav>
//         <ul>
//           <li><Link to="/">Home</Link></li>
//           <li><Link to="/create">Create Event</Link></li>
//         </ul>
//       </nav>
//       <Switch>
//         <Route exact path="/" component={Home} />
//         <Route exact path="/event/:id" component={EventDetail} />
//         <Route exact path="/create" component={CreateEvent} />
//         <Route exact path="/edit/:id" component={EditEvent} />
//       </Switch>
//     </Router>
//   );
// }

// export default App;







import React from 'react';
import { Routes, Route } from 'react-router-dom';
import NavBar from './NavBar';
import HomePage from './HomePage';
import EventDetail from './EventDetail';
import CreateEvent from './CreateEvent';
import EditEvent from './EditEvent';
import Login from './Login';
import Register from './Register';

function App() {
  return (
    <div>
      <NavBar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/event/:id" element={<EventDetail />} />
        <Route path="/create" element={<CreateEvent />} />
        <Route path="/edit/:id" element={<EditEvent />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </div>
  );
}

export default App;