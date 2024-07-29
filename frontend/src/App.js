import React, { useState } from 'react';
import axios from 'axios';
import { TextField, Button, Card, CardContent, Typography, CircularProgress, Container } from '@mui/material';
import './App.css';

let url = `127.0.0.1`;

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
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setParams({
      ...params,
      [e.target.name]: e.target.value
    });
  };

  const fetchWinRateLoseRate = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://${url}:8000/metrics/win-rate/lose-rate/${params.param1}/${params.param2}/${params.param3}`);
      setResults({ ...results, winRateLoseRate: response.data });
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const fetchDeck = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://${url}:8000/metrics/deck/${params.param1}/${params.param2}/${params.param3}`);
      setResults({ ...results, deck: response.data });
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const fetchLoses = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://${url}:8000/metrics/loses/${params.param1}/${params.param2}/${params.param3}`);
      setResults({ ...results, loses: response.data });
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const fetchWinRate = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://${url}:8000/metrics/win-rate/${params.param1}/${params.param2}`);
      setResults({ ...results, winRate: response.data });
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const fetchComboCards = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://${url}:8000/metrics/combo-cards/${params.param1}/${params.param2}/${params.param3}/${params.param4}`);
      setResults({ ...results, comboCards: response.data });
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const renderInputs = (fields) => {
    return fields.map((field, index) => (
      <TextField
        key={index}
        label={field.charAt(0).toUpperCase() + field.slice(1)}
        name={field}
        value={params[field]}
        onChange={handleChange}
        variant="outlined"
        margin="normal"
        fullWidth
      />
    ));
  };

  const renderResults = (data) => {
    return <pre>{JSON.stringify(data, null, 2)}</pre>;
  };

  return (
    <Container maxWidth="md">
      <Typography variant="h2" align="center" gutterBottom>
        Clash Royale Metrics
      </Typography>
      <div className="section">
        <Button variant="contained" color="primary" onClick={() => setActiveSection('winRateLoseRate')}>
          Fetch Win Rate / Lose Rate
        </Button>
        {activeSection === 'winRateLoseRate' && (
          <Card className="card">
            <CardContent>
              {renderInputs(['param1', 'param2', 'param3'])}
              <Button variant="contained" color="secondary" onClick={fetchWinRateLoseRate} disabled={loading}>
                Submit
              </Button>
              {loading && <CircularProgress />}
              {results.winRateLoseRate && renderResults(results.winRateLoseRate)}
            </CardContent>
          </Card>
        )}
      </div>
      <div className="section">
        <Button variant="contained" color="primary" onClick={() => setActiveSection('deck')}>
          Fetch Deck
        </Button>
        {activeSection === 'deck' && (
          <Card className="card">
            <CardContent>
              {renderInputs(['param1', 'param2', 'param3'])}
              <Button variant="contained" color="secondary" onClick={fetchDeck} disabled={loading}>
                Submit
              </Button>
              {loading && <CircularProgress />}
              {results.deck && renderResults(results.deck)}
            </CardContent>
          </Card>
        )}
      </div>
      <div className="section">
        <Button variant="contained" color="primary" onClick={() => setActiveSection('loses')}>
          Fetch Loses
        </Button>
        {activeSection === 'loses' && (
          <Card className="card">
            <CardContent>
              {renderInputs(['param1', 'param2', 'param3'])}
              <Button variant="contained" color="secondary" onClick={fetchLoses} disabled={loading}>
                Submit
              </Button>
              {loading && <CircularProgress />}
              {results.loses && renderResults(results.loses)}
            </CardContent>
          </Card>
        )}
      </div>
      <div className="section">
        <Button variant="contained" color="primary" onClick={() => setActiveSection('winRate')}>
          Fetch Win Rate
        </Button>
        {activeSection === 'winRate' && (
          <Card className="card">
            <CardContent>
              {renderInputs(['param1', 'param2'])}
              <Button variant="contained" color="secondary" onClick={fetchWinRate} disabled={loading}>
                Submit
              </Button>
              {loading && <CircularProgress />}
              {results.winRate && renderResults(results.winRate)}
            </CardContent>
          </Card>
        )}
      </div>
      <div className="section">
        <Button variant="contained" color="primary" onClick={() => setActiveSection('comboCards')}>
          Fetch Combo Cards
        </Button>
        {activeSection === 'comboCards' && (
          <Card className="card">
            <CardContent>
              {renderInputs(['param1', 'param2', 'param3', 'param4'])}
              <Button variant="contained" color="secondary" onClick={fetchComboCards} disabled={loading}>
                Submit
              </Button>
              {loading && <CircularProgress />}
              {results.comboCards && renderResults(results.comboCards)}
            </CardContent>
          </Card>
        )}
      </div>
    </Container>
  );
}

export default App;
