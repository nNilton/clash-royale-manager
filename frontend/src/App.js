import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

let url = `localhost`;

function App() {
  const [params, setParams] = useState({
    param1: '',
    param2: '',
    param3: '',
    param4: ''
  });
  const [results, setResults] = useState({
    winRateLoseRate: null,
    deck: null,
    loses: null,
    winRate: null,
    comboCards: null
  });
  const [activeSection, setActiveSection] = useState(null);

  const handleChange = (e) => {
    setParams({
      ...params,
      [e.target.name]: e.target.value
    });
  };

  const fetchWinRateLoseRate = async () => {
    try {
      const response = await axios.get(`http://${url}:8000/metrics/win-rate/lose-rate/${params.param1}/${params.param2}/${params.param3}`);
      setResults({ ...results, winRateLoseRate: response.data });
    } catch (error) {
      console.error(error);
    }
  };

  const fetchDeck = async () => {
    try {
      const response = await axios.get(`http://${url}:8000/metrics/deck/${params.param1}/${params.param2}/${params.param3}`);
      setResults({ ...results, deck: response.data });
    } catch (error) {
      console.error(error);
    }
  };

  const fetchLoses = async () => {
    try {
      const response = await axios.get(`http://${url}:8000/metrics/loses/${params.param1}/${params.param2}/${params.param3}`);
      setResults({ ...results, loses: response.data });
    } catch (error) {
      console.error(error);
    }
  };

  const fetchWinRate = async () => {
    try {
      const response = await axios.get(`http://${url}:8000/metrics/win-rate/${params.param1}/${params.param2}`);
      setResults({ ...results, winRate: response.data });
    } catch (error) {
      console.error(error);
    }
  };

  const fetchComboCards = async () => {
    try {
      const response = await axios.get(`http://${url}:8000/metrics/combo-cards/${params.param1}/${params.param2}/${params.param3}/${params.param4}`);
      setResults({ ...results, comboCards: response.data });
    } catch (error) {
      console.error(error);
    }
  };

  const renderInputs = (fields) => {
    return fields.map((field, index) => (
      <input
        key={index}
        type="text"
        name={field}
        placeholder={field.charAt(0).toUpperCase() + field.slice(1)}
        value={params[field]}
        onChange={handleChange}
      />
    ));
  };

  const renderResults = (data) => {
    return <pre>{JSON.stringify(data, null, 2)}</pre>;
  };

  return (
    <div className="App">
      <h1>Clash Royale Metrics</h1>
      <div className="section">
        <button onClick={() => setActiveSection('winRateLoseRate')}>Fetch Win Rate / Lose Rate</button>
        {activeSection === 'winRateLoseRate' && (
          <div className="inputs">
            {renderInputs(['param1', 'param2', 'param3'])}
            <button onClick={fetchWinRateLoseRate}>Submit</button>
            {results.winRateLoseRate && renderResults(results.winRateLoseRate)}
          </div>
        )}
      </div>
      <div className="section">
        <button onClick={() => setActiveSection('deck')}>Fetch Deck</button>
        {activeSection === 'deck' && (
          <div className="inputs">
            {renderInputs(['param1', 'param2', 'param3'])}
            <button onClick={fetchDeck}>Submit</button>
            {results.deck && renderResults(results.deck)}
          </div>
        )}
      </div>
      <div className="section">
        <button onClick={() => setActiveSection('loses')}>Fetch Loses</button>
        {activeSection === 'loses' && (
          <div className="inputs">
            {renderInputs(['param1', 'param2', 'param3'])}
            <button onClick={fetchLoses}>Submit</button>
            {results.loses && renderResults(results.loses)}
          </div>
        )}
      </div>
      <div className="section">
        <button onClick={() => setActiveSection('winRate')}>Fetch Win Rate</button>
        {activeSection === 'winRate' && (
          <div className="inputs">
            {renderInputs(['param1', 'param2'])}
            <button onClick={fetchWinRate}>Submit</button>
            {results.winRate && renderResults(results.winRate)}
          </div>
        )}
      </div>
      <div className="section">
        <button onClick={() => setActiveSection('comboCards')}>Fetch Combo Cards</button>
        {activeSection === 'comboCards' && (
          <div className="inputs">
            {renderInputs(['param1', 'param2', 'param3', 'param4'])}
            <button onClick={fetchComboCards}>Submit</button>
            {results.comboCards && renderResults(results.comboCards)}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
