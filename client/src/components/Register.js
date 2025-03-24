import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import { useNavigate } from 'react-router-dom';
import * as Yup from 'yup';
import './Auth.css';

const RegisterSchema = Yup.object().shape({
  username: Yup.string().required('Username is required'),
  email: Yup.string().email('Invalid email').required('Email is required'),
  password: Yup.string().min(6, 'Password too short').required('Password is required'),
});

function Register() {
  const navigate = useNavigate();

  return (
    <div>
      <h1>Register</h1>
      <Formik
        initialValues={{ username: '', email: '', password: '' }}
        validationSchema={RegisterSchema}
        onSubmit={(values, { setSubmitting }) => {
          fetch('/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(values)
          })
            .then(res => {
              if (!res.ok) {
                throw new Error('Registration failed');
              }
              return res.json();
            })
            .then(() => {
              navigate('/login');
            })
            .catch(err => console.error(err))
            .finally(() => setSubmitting(false));
        }}
      >
        {({ isSubmitting }) => (
          <Form>
            <div>
              <label htmlFor="username">Username</label>
              <Field id="username" name="username" />
              <ErrorMessage name="username" component="div" />
            </div>
            <div>
              <label htmlFor="email">Email</label>
              <Field id="email" name="email" type="email" />
              <ErrorMessage name="email" component="div" />
            </div>
            <div>
              <label htmlFor="password">Password</label>
              <Field id="password" name="password" type="password" />
              <ErrorMessage name="password" component="div" />
            </div>
            <button type="submit" disabled={isSubmitting}>
              Register
            </button>
          </Form>
        )}
      </Formik>
    </div>
  );
}

export default Register;