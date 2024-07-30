import React, { useState } from 'react';
import { TextField, Button, Card, CardContent, Typography, CircularProgress, Container } from '@mui/material';
import '../../App.css';
import { SearchCard } from '../../components/SearchCard';
import api from '../../config/api';


export function FormWinRateLoseRate({ activeSection, setActiveSection }) {
    const [cardValue, setCardValue] = useState(null)
    const [minTimeStampValue, setMinTimeStampValue] = useState(0)
    const [maxTimeStampValue, setMaxTimeStampValue] = useState(0)

    const [isLoading, setIsLoading] = useState(false)
    const [results, setResults] = useState(null)
    const renderResults = (data) => {
        return <pre>{JSON.stringify(data, null, 2)}</pre>;
    };

    async function fetchWinRateLoseRate(cardId, minTimeStamp, maxTimeStamp) {
        try {
            const response = await api.get(`metrics/win-rate/lose-rate/${cardId}/${minTimeStamp}/${maxTimeStamp}`);
            return response.data;
        } catch (error) {

        }

    };


    async function handleSubmit() {
        if (cardValue && cardValue?._id && minTimeStampValue?.length > 0 && maxTimeStampValue?.length > 0) {
            const cardId = cardValue._id;

            setIsLoading(true)
            const data = await fetchWinRateLoseRate(cardId, minTimeStampValue, maxTimeStampValue)
            setResults(data)
            setIsLoading(false)
        }
        else {
            alert("Preencha todos os dados")
        }
    }

    return (<div className="section">
        <Button variant="contained" color="primary" onClick={() => setActiveSection('winRateLoseRate')}>
            Fetch Win Rate / Lose Rate
        </Button>
        {activeSection === 'winRateLoseRate' && (
            <Card className="card">
                <CardContent>
                    <SearchCard value={cardValue} setValue={setCardValue} />
                    <TextField
                        label={"Menor Data"}
                        name={"minTimeStampValue"}
                        value={minTimeStampValue}
                        onChange={(event) => {
                            setMinTimeStampValue(event.target.value);
                        }}
                        variant="outlined"
                        margin="normal"
                        fullWidth
                    />
                    <TextField
                        label={"Maior Data"}
                        name={"maxTimeStampValue"}
                        value={maxTimeStampValue}
                        onChange={(event) => {
                            setMaxTimeStampValue(event.target.value);
                        }}
                        variant="outlined"
                        margin="normal"
                        fullWidth
                    />
                    <Button variant="contained" color="secondary"
                        onClick={handleSubmit}
                        disabled={isLoading}
                    >
                        Submit
                    </Button>
                    {
                        isLoading && <CircularProgress />
                    }

                    {
                        results && results.length > 0 ? <div>
                            {results.map(item => (
                                <div key={item._id} style={{ marginBottom: '10px' }}>
                                    <div><strong>ID:</strong> {item._id}</div>
                                    <div><strong>Win Rate:</strong> {item.winRate}</div>
                                    <div><strong>Lose Rate:</strong> {item.loseRate}</div>
                                </div>
                            ))}
                        </div> : null
                    }
                </CardContent>
            </Card>
        )}
    </div>)
}