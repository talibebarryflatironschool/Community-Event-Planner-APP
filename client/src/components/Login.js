import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import { useNavigate } from 'react-router-dom';
import * as Yup from 'yup';
import './Auth.css';

const LoginSchema = Yup.object().shape({
  username: Yup.string().required('Username is required'),
  password: Yup.string().required('Password is required'),
});

function Login() {
  const navigate = useNavigate();

  return (
    <div>
      <h1>Login</h1>
      <Formik
        initialValues={{ username: '', password: '' }}
        validationSchema={LoginSchema}
        onSubmit={(values, { setSubmitting }) => {
          fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(values)
          })
            .then(res => {
              if (!res.ok) {
                throw new Error('Login failed');
              }
              return res.json();
            })
            .then(() => {
              // Handle login success (e.g., store user info or token)
              navigate('/');
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
              <label htmlFor="password">Password</label>
              <Field id="password" name="password" type="password" />
              <ErrorMessage name="password" component="div" />
            </div>
            <button type="submit" disabled={isSubmitting}>
              Login
            </button>
          </Form>
        )}
      </Formik>
    </div>
  );
}

export default Login;