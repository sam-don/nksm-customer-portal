import React, { useState } from 'react';
import './Reset.css';
import './App.css';

function App() {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [company, setCompany] = useState('');
  const [email, setEmail] = useState('');
  const [mobile, setMobile] = useState('');
  const [address, setAddress] = useState('');

  // useEffect(() => {
  //   fetch('/api/customers', {
  //     method: 'GET',
  //     headers: {
  //       'Access-Control-Allow-Origin': '*'
  //     }
  //   })
  //     .then(response => response.json())
  //     .then(data => { setCustomers(data) });
  // }, []);

  const handleSubmit = (event) => {
    event.preventDefault();
    // const dobdate = dobGuess.split()
    // const month = dobdate[1]
    // const day = dobdate[2]
    const newCustomer = {
      name: name,
      company: company,
      email: email,
      mobile: mobile,
      address: address
    };
    fetch('/api/customers', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify(newCustomer)
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        setCustomers([...customers, data]);
        setName('');
        setCompany('');
        setEmail('');
        setMobile('');
        setAddress('');
      })
      .catch(error => console.error(error));
    // showCustomers();
  };

  // const handleShowGuesses = (event) => {
  //   event.preventDefault();
  //   var container = document.getElementById("container");
  //   container.classList.toggle("hidden");
  // }

  // const showCustomers = () => {
  //   var container = document.getElementById("container");
  //   container.classList.remove("hidden");
  // }

  return (
    <div className="App">
      <div id='header'>
        <img id='titleimg' src='./nksm-logo-horizontal.png' alt='9 triangles stacked together to make one big triangle, with each one coloured various shades of blue.'></img>
        <div id='title'>
          <h2>New Customer Form</h2>
        </div>
      </div>

      <form id="customer-form" onSubmit={handleSubmit}>
          <input type="text" placeholder="Name (required)" value={name} onChange={(event) => setName(event.target.value)} required />
          <input type="text" placeholder="Mobile (required)" value={mobile} onChange={(event) => setMobile(event.target.value)} required />
          <input type="text" placeholder="Company" value={company} onChange={(event) => setCompany(event.target.value)} />
          <input type="text" placeholder="Email" value={email} onChange={(event) => setEmail(event.target.value)} />
          <input type="text" placeholder="Address" value={address} onChange={(event) => setAddress(event.target.value)} />
        <div className="buttons">
          {/* <button className="button-67" onClick={handleShowGuesses}>Show Guesses</button> */}
          <button className="submit-button" type="submit">Submit</button>
        </div>
      </form>
    </div>
  );
}

export default App;
