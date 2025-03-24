import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

export default function EventList() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    fetch('/api/events')
      .then(res => res.json())
      .then(data => setEvents(data));
  }, []);

  return (
    <div>
      {events.map(event => (
        <div key={event.id}>
          <h2>
            <Link to={`/events/${event.id}`}>{event.title}</Link>
          </h2>
          <p>{event.location}</p>
        </div>
      ))}
    </div>
  );
}