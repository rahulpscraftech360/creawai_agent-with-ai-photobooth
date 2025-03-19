import React, { useState } from 'react';

const UserForm = () => {
  const [userName, setUserName] = useState('');
  const [email, setEmail] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [error, setError] = useState(null); // added error state to handle validation errors

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!userName || !email || !phoneNumber) {
      setError('Please fill in all fields.');
    } else if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email)) {
      setError('Invalid email address.');
    } else if (!/^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/.test(phoneNumber)) {
      setError('Invalid phone number.');
    } else {
      setIsSubmitted(true);
    }
  };

  return (
    <div>
      {isSubmitted ? (
        <h2>Thank you for submitting the form!</h2>
      ) : (
        <form onSubmit={handleSubmit}>
          {error && (
            <div style={{ color: 'red' }} role="alert">
              {error}
            </div>
          )}
          <label>
            Name:
            <input
              type="text"
              value={userName}
              onChange={(event) => setUserName(event.target.value)}
              required
              aria-required="true"
            />
          </label>
          <br />
          <label>
            Email:
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
              aria-required="true"
            />
          </label>
          <br />
          <label>
            Phone Number:
            <input
              type="tel"
              value={phoneNumber}
              onChange={(event) => setPhoneNumber(event.target.value)}
              required
              aria-required="true"
            />
          </label>
          <br />
          <button type="submit">Submit</button>
        </form>
      )}
    </div>
  );
};

export default UserForm;