import React, {useState} from 'react';
import {TextField, Button, Card, CardContent, Typography, CircularProgress, Container} from '@mui/material';
import '../../App.css';
import {SearchCard} from '../../components/SearchCard';
import api from '../../config/api';
import {useSearchMultipleCards} from '../../components/SearchMultipleCards/hooks';
import {SearchMultipleCards} from '../../components/SearchMultipleCards';

export function FormLoses({activeSection, setActiveSection}) {
    const {countFields, handleAddCard, handleSetValue, handleCloseCard} = useSearchMultipleCards()
    const [minTimeStampValue, setMinTimeStampValue] = useState(0)
    const [maxTimeStampValue, setMaxTimeStampValue] = useState(0)

    const [isLoading, setIsLoading] = useState(false)
    const [results, setResults] = useState(null)
    const renderResults = (data) => {
        return <pre>{JSON.stringify(data, null, 2)}</pre>;
    };

    async function fetchLoses(cardsIds, minTimeStamp, maxTimeStamp) {
        try {
            const response = await api.get(`metrics/loses/${cardsIds}/${minTimeStamp}/${maxTimeStamp}`);
            return response.data;
        } catch (error) {

        }
    }


    async function handleSubmit() {
        const countInvalidsCards = countFields.filter(item => !item.value || !item?.value?._id)
        if (countInvalidsCards.length === 0 && minTimeStampValue?.length > 0 && maxTimeStampValue?.length > 0) {
            const cardsIds = countFields.map(item => item.value._id)
            const cardsIdsSorted = cardsIds.sort((a, b) => a - b)
            const concatenatedString = cardsIdsSorted.join('-')

            setIsLoading(true)
            const data = await fetchLoses(concatenatedString, minTimeStampValue, maxTimeStampValue)
            setResults(data)
            setIsLoading(false)
        } else {
            alert("Preencha todos os dados")
        }
    }


    return (<div className="section">
        <Button variant="contained" color="primary" onClick={() => setActiveSection('loses')}>
            Fetch Loses
        </Button>
        {activeSection === 'loses' && (
            <Card className="card">
                <CardContent>
                    <SearchMultipleCards countFields={countFields} handleAddCard={handleAddCard}
                                         handleCloseCard={handleCloseCard} handleSetValue={handleSetValue}/>
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

                    <Button variant="contained" color="secondary" onClick={handleSubmit}
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
                                    <div><strong>totalMatches:</strong> {item.totalMatches}</div>
                                    <div><strong>loses:</strong> {item.loses}</div>
                                </div>
                            ))}
                        </div> : null
                    }
                </CardContent>
            </Card>
        )}
    </div>)
}