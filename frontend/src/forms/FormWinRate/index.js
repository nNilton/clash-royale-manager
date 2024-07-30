import React, {useState} from 'react';
import {TextField, Button, Card, CardContent, Typography, CircularProgress, Container} from '@mui/material';
import '../../App.css';
import {SearchCard} from '../../components/SearchCard';
import api from '../../config/api';

export function FormWinRate({activeSection, setActiveSection}) {
    const [cardValue, setCardValue] = useState(null)
    const [trophiesValue, setTrophiesValue] = useState("")

    const [isLoading, setIsLoading] = useState(false)
    const [results, setResults] = useState(null)
    const renderResults = (data) => {
        return <pre>{JSON.stringify(data, null, 2)}</pre>;
    };

    async function fetchWinRate(cardId, trophiesDiff) {
        try {
            const response = await api.get(`metrics/win-rate/${cardId}/${trophiesDiff}`);
            return response.data;
        } catch (error) {

        }

    };


    async function handleSubmit() {
        if (cardValue && cardValue?._id && trophiesValue?.length > 0) {
            const cardId = cardValue._id;
            const trophiesDiff = trophiesValue;

            setIsLoading(true)
            const data = await fetchWinRate(cardId, trophiesDiff)
            setResults(data)
            setIsLoading(false)
        } else {
            alert("Preencha todos os dados")
        }
    }

    return (<div className="section">
        <Button variant="contained" color="primary" onClick={() => setActiveSection('winRate')}>
            Fetch Win Rate
        </Button>
        {activeSection === 'winRate' && (
            <Card className="card">
                <CardContent>
                    <SearchCard value={cardValue} setValue={setCardValue}/>

                    <TextField
                        label={"Porcentagem de diferença de trófeus"}
                        name={"trophiesDiff"}
                        value={trophiesValue}
                        onChange={(event) => {
                            setTrophiesValue(event.target.value);
                        }}
                        variant="outlined"
                        margin="normal"
                        fullWidth
                    />
                    <Button
                        variant="contained"
                        color="secondary"
                        onClick={handleSubmit}
                        disabled={isLoading}
                    >
                        Submit
                    </Button>
                    {
                        isLoading && <CircularProgress/>
                    }
                    {
                        results && results.length > 0 ? <div>
                            {results.map(item => (
                                <div key={item._id} style={{marginBottom: '10px'}}>
                                    <div><strong>ID:</strong> {item._id}</div>
                                    <div><strong>Win Rate:</strong> {item.winRate}</div>
                                </div>
                            ))}
                        </div> : null
                    }
                </CardContent>
            </Card>
        )}
    </div>)
}