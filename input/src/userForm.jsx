import React, { useState } from 'react';

const UserForm = () => {
  const [userName, setUserName] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [email, setEmail] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!userName || !phoneNumber || !email) {
      setError('Please fill in all fields.');
    } else if (!/^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/.test(phoneNumber)) {
      setError('Invalid phone number.');
    } else {
      setIsSubmitted(true);
    }
  };

  return (
    <div
      style={{
        maxWidth: '400px',
        margin: '40vh auto', /* Center the form vertically */
        padding: '20px',
        backgroundColor: '#f7f7f7', /* Change background color to light grey */
        fontSize: '16px' /* Change font size to 16px */
      }}
      role="form"
      aria-live="polite"
    >
      {isSubmitted ? (
        <h2 style={{ color: 'green', animation: 'fadeIn 2s' }}>
          Thank you for submitting the form!
        </h2>
      ) : (
        <form onSubmit={handleSubmit} autoComplete="off">
          {error && (
            <div
              style={{
                color: 'red',
                fontSize: '16px',
                fontWeight: 'bold',
                animation: 'shake 0.5s'
              }}
              role="alert"
            >
              {error}
            </div>
          )}
          <label
            style={{ display: 'block', marginBottom: '10px' }}
            htmlFor="name"
          >
            Name:
            <input
              type="text"
              id="name"
              value={userName}
              onChange={(event) => setUserName(event.target.value)}
              required
              aria-required="true"
              aria-label="Name"
              style={{
                padding: '10px',
                fontSize: '16px',
                borderRadius: '5px',
                border: '1px solid #ccc',
                transition: 'border 0.3s',
                width: '100%',
                boxSizing: 'border-box' // added to fix overflowing
              }}
              onFocus={(event) => event.target.style.border = '1px solid #4CAF50'}
              onBlur={(event) => event.target.style.border = '1px solid #ccc'}
              className="input-field"
            />
          </label>
          <br />
          <label
            style={{ display: 'block', marginBottom: '10px' }}
            htmlFor="phone-number"
          >
            Phone Number:
            <input
              type="tel"
              id="phone-number"
              value={phoneNumber}
              onChange={(event) => setPhoneNumber(event.target.value)}
              required
              aria-required="true"
              aria-label="Phone Number"
              pattern="\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})"
              style={{
                padding: '10px',
                fontSize: '16px',
                borderRadius: '5px',
                border: '1px solid #ccc',
                transition: 'border 0.3s',
                width: '100%',
                boxSizing: 'border-box' // added to fix overflowing
              }}
              onFocus={(event) => event.target.style.border = '1px solid #4CAF50'}
              onBlur={(event) => event.target.style.border = '1px solid #ccc'}
              className="input-field"
            />
          </label>
          <br />
          <label
            style={{ display: 'block', marginBottom: '10px' }}
            htmlFor="email"
          >
            Email:
            <input
              type="email"
              id="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
              aria-required="true"
              aria-label="Email"
              style={{
                padding: '10px',
                fontSize: '16px',
                borderRadius: '5px',
                border: '1px solid #ccc',
                transition: 'border 0.3s',
                width: '100%',
                boxSizing: 'border-box' // added to fix overflowing
              }}
              onFocus={(event) => event.target.style.border = '1px solid #4CAF50'}
              onBlur={(event) => event.target.style.border = '1px solid #ccc'}
              className="input-field"
            />
          </label>
          <br />
          <button
            type="submit"
            style={{
              padding: '10px 20px',
              fontSize: '16px',
              backgroundColor: 'green', /* Change button color to green */
              color: '#ffffff',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer',
              transition: 'background-color 0.3s',
              ':hover': {
                backgroundColor: '#3e8e41'
              }
            }}
            className="submit-button"
          >
            Submit 
          </button>
        </form>
      )}
    </div>
  );
};

export default UserForm;