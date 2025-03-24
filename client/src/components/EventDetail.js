import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import './EventDetail.css';

function EventDetail() {
  const { id } = useParams();
  const [event, setEvent] = useState(null);

  useEffect(() => {
    fetch(`/api/events/${id}`)
      .then(res => res.json())
      .then(data => setEvent(data))
      .catch(err => console.error(err));
  }, [id]);

  if (!event) return <p>Loading...</p>;

  return (
    <div>
      <h1>{event.title}</h1>
      <p>Date: {event.date}</p>
      <p>Location: {event.location}</p>
      <p>Description: {event.description}</p>
      <Link to={`/edit/${event.id}`}>Edit Event</Link>
    </div>
  );
}

export default EventDetail;

