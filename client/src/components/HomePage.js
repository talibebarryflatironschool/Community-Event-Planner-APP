import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    fetch('/api/events')
      .then(res => res.json())
      .then(data => setEvents(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h1>Upcoming Events</h1>
      {events.map(event => (
        <div key={event.id}>
          <h2>
            <Link to={`/event/${event.id}`}>{event.title}</Link>
          </h2>
          <p>{event.date}</p>
          <p>{event.location}</p>
        </div>
      ))}
    </div>
  );
}

export default HomePage;