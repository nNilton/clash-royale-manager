import React, {useState} from 'react';
import axios from 'axios';
import {TextField, Button, Card, CardContent, Typography, CircularProgress, Container} from '@mui/material';
import './App.css';
import {useCards} from './context/CardsContext';
import {FormWinRate} from './forms/FormWinRate';
import {FormWinRateLoseRate} from './forms/FormWinRateLoseRate';
import {FormLoses} from './forms/FormLoses';

export let url = `127.0.0.1`;

function App() {
    const {isLoading} = useCards()


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
        comboCards: null,
        mostPickedCards: null,
        mostPopularCards: null,
        crownDiff: null
    });
    const [activeSection, setActiveSection] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        setParams({
            ...params,
            [e.target.name]: e.target.value
        });
    };


    const fetchDeck = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`http://${url}:8000/metrics/deck/${params.param1}/${params.param2}/${params.param3}`);
            setResults({...results, deck: response.data});
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
            setResults({...results, comboCards: response.data});
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const fetchTenMostPickedCards = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`http://${url}:8000/metrics/ten-most-picked-cards/${params.param1}`);
            setResults({...results, mostPickedCards: response.data});
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const fetchMostPopularCards = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`http://${url}:8000/metrics/ten-most-popular-decks/{criteria]?criteria=${params.param1}`);
            setResults({...results, mostPopularCards: response.data});
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const fetchCrownDiff = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`http://${url}:8000/metrics/card/highest-crownDiff`);
            setResults({...results, crownDiff: response.data});
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

    if (isLoading) {
        return <div>Carregando...</div>
    }

    return (
        <Container maxWidth="lg">
            <Typography variant="h2" align="center" gutterBottom>
                Clash Royale Metrics
            </Typography>
            <FormWinRateLoseRate activeSection={activeSection} setActiveSection={setActiveSection}/>
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
                            {loading && <CircularProgress/>}
                            {results.deck && renderResults(results.deck)}
                        </CardContent>
                    </Card>
                )}
            </div>
            <FormLoses activeSection={activeSection} setActiveSection={setActiveSection}/>
            <FormWinRate activeSection={activeSection} setActiveSection={setActiveSection}/>
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
                            {loading && <CircularProgress/>}
                            {results.comboCards && renderResults(results.comboCards)}
                        </CardContent>
                    </Card>
                )}
            </div>
            <div className="section">
                <Button variant="contained" color="primary" onClick={() => setActiveSection('mostPickedCards')}>
                    Fetch Most Picked Cards
                </Button>
                {activeSection === 'mostPickedCards' && (
                    <Card className="card">
                        <CardContent>
                            {renderInputs(['param1'])}
                            <Button variant="contained" color="secondary" onClick={fetchTenMostPickedCards}
                                    disabled={loading}>
                                Submit
                            </Button>
                            {loading && <CircularProgress/>}
                            {results.mostPickedCards && renderResults(results.mostPickedCards)}
                        </CardContent>
                    </Card>
                )}
            </div>
            <div className="section">
                <Button variant="contained" color="primary" onClick={() => setActiveSection('mostPopularCards')}>
                    Fetch Most Popular Cards
                </Button>
                {activeSection === 'mostPopularCards' && (
                    <Card className="card">
                        <CardContent>
                            {renderInputs(['param1'])}
                            <Button variant="contained" color="secondary" onClick={fetchMostPopularCards}
                                    disabled={loading}>
                                Submit
                            </Button>
                            {loading && <CircularProgress/>}
                            {results.mostPopularCards && renderResults(results.mostPopularCards)}
                        </CardContent>
                    </Card>
                )}
            </div>
            <div className="section">
                <Button variant="contained" color="primary" onClick={() => setActiveSection('crownDiff')}>
                    Fetch Highest Crown Diff
                </Button>
                {activeSection === 'crownDiff' && (
                    <Card className="card">
                        <CardContent>
                            <Button variant="contained" color="secondary" onClick={fetchCrownDiff} disabled={loading}>
                                Submit
                            </Button>
                            {loading && <CircularProgress/>}
                            {results.crownDiff && renderResults(results.crownDiff)}
                        </CardContent>
                    </Card>
                )}
            </div>
        </Container>
    );
}

export default App;
