import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [params, setParams] = useState({
    param1: '',
    param2: '',
    param3: '',
    param4: ''
  });
  const [winRateLoseRate, setWinRateLoseRate] = useState(null);
  const [deck, setDeck] = useState(null);
  const [loses, setLoses] = useState(null);
  const [winRate, setWinRate] = useState(null);
  const [comboCards, setComboCards] = useState(null);

  const handleChange = (e) => {
    setParams({
      ...params,
      [e.target.name]: e.target.value
    });
  };

  const fetchWinRateLoseRate = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/metrics/win-rate/lose-rate/${params.param1}/${params.param2}/${params.param3}`);
      setWinRateLoseRate(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchDeck = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/metrics/deck/${params.param1}/${params.param2}/${params.param3}`);
      setDeck(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchLoses = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/metrics/loses/${params.param1}/${params.param2}/${params.param3}`);
      setLoses(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchWinRate = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/metrics/win-rate/${params.param1}/${params.param2}`);
      setWinRate(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchComboCards = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/metrics/combo-cards/${params.param1}/${params.param2}/${params.param3}/${params.param4}`);
      setComboCards(response.data);
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="App">
      <h1>Clash Royale Metrics</h1>
      <div>
        <input
          type="text"
          name="param1"
          placeholder="Param 1"
          value={params.param1}
          onChange={handleChange}
        />
        <input
          type="text"
          name="param2"
          placeholder="Param 2"
          value={params.param2}
          onChange={handleChange}
        />
        <input
          type="text"
          name="param3"
          placeholder="Param 3"
          value={params.param3}
          onChange={handleChange}
        />
        <input
          type="text"
          name="param4"
          placeholder="Param 4"
          value={params.param4}
          onChange={handleChange}
        />
      </div>
      <div>
        <button onClick={fetchWinRateLoseRate}>Fetch Win Rate / Lose Rate</button>
        {winRateLoseRate && <pre>{JSON.stringify(winRateLoseRate, null, 2)}</pre>}
      </div>
      <div>
        <button onClick={fetchDeck}>Fetch Deck</button>
        {deck && <pre>{JSON.stringify(deck, null, 2)}</pre>}
      </div>
      <div>
        <button onClick={fetchLoses}>Fetch Loses</button>
        {loses && <pre>{JSON.stringify(loses, null, 2)}</pre>}
      </div>
      <div>
        <button onClick={fetchWinRate}>Fetch Win Rate</button>
        {winRate && <pre>{JSON.stringify(winRate, null, 2)}</pre>}
      </div>
      <div>
        <button onClick={fetchComboCards}>Fetch Combo Cards</button>
        {comboCards && <pre>{JSON.stringify(comboCards, null, 2)}</pre>}
      </div>
    </div>
  );
}

export default App;
