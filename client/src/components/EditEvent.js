import React, { useEffect, useState } from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { useParams, useNavigate } from 'react-router-dom';

const EventSchema = Yup.object().shape({
  title: Yup.string().required('Title is required'),
  description: Yup.string().required('Description is required'),
  date: Yup.date().required('Date is required'),
  location: Yup.string().required('Location is required'),
});

function EditEvent() {
  const { id } = useParams();
  const navigate = useNavigate();
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
      <h1>Edit Event</h1>
      <Formik
        initialValues={{
          title: event.title,
          description: event.description,
          date: event.date,
          location: event.location
        }}
        validationSchema={EventSchema}
        onSubmit={(values, { setSubmitting }) => {
          fetch(`http://localhost:5000/api/events/${id}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(values)
          })
            .then(res => res.json())
            .then(() => {
              navigate(`/event/${id}`);
            })
            .catch(err => console.error(err))
            .finally(() => setSubmitting(false));
        }}
      >
        {({ isSubmitting }) => (
          <Form>
            <div>
              <label htmlFor="title">Title</label>
              <Field id="title" name="title" />
              <ErrorMessage name="title" component="div" />
            </div>
            <div>
              <label htmlFor="description">Description</label>
              <Field id="description" name="description" as="textarea" />
              <ErrorMessage name="description" component="div" />
            </div>
            <div>
              <label htmlFor="date">Date</label>
              <Field id="date" name="date" type="date" />
              <ErrorMessage name="date" component="div" />
            </div>
            <div>
              <label htmlFor="location">Location</label>
              <Field id="location" name="location" />
              <ErrorMessage name="location" component="div" />
            </div>
            <button type="submit" disabled={isSubmitting}>
              Update Event
            </button>
          </Form>
        )}
      </Formik>
    </div>
  );
}

export default EditEvent;

