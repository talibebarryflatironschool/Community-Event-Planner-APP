import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { useNavigate } from 'react-router-dom';
import './EventForm.css';

const EventSchema = Yup.object().shape({
  title: Yup.string().required('Title is required'),
  description: Yup.string().required('Description is required'),
  date: Yup.date().required('Date is required'),
  location: Yup.string().required('Location is required'),
  creator_id: Yup.number().required('Creator ID is required'),
});

function CreateEvent() {
  const navigate = useNavigate();
  
  return (
    <div>
      <h1>Create New Event</h1>
      <Formik
        initialValues={{
          title: '',
          description: '',
          date: '',
          location: '',
          creator_id: ''
        }}
        validationSchema={EventSchema}
        onSubmit={(values, { setSubmitting, resetForm }) => {
          fetch('/api/events', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(values)
          })
            .then(res => res.json())
            .then(() => {
              resetForm();
              navigate('/');
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
            <div>
              <label htmlFor="creator_id">Creator ID</label>
              <Field id="creator_id" name="creator_id" type="number" />
              <ErrorMessage name="creator_id" component="div" />
            </div>
            <button type="submit" disabled={isSubmitting}>
              Create Event
            </button>
          </Form>
        )}
      </Formik>
    </div>
  );
}

export default CreateEvent;

