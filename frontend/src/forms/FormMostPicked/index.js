import React, { useState } from 'react';
import { TextField, Button, Card, CardContent, Typography, CircularProgress, Container } from '@mui/material';
import '../../App.css';
import api from '../../config/api';
import { useCards } from "../../context/CardsContext"

export function FormMostPicked({ activeSection, setActiveSection }) {
    const { findById } = useCards()
    const [sizeValue, setSizeValue] = useState("")


    const [isLoading, setIsLoading] = useState(false)
    const [results, setResults] = useState(null)
    const [resultsTransformed, setResultsTransformed] = useState(null)



    async function fetchMostPickedCards(size) {
        try {
            const response = await api.get(`metrics/ten-most-picked-cards/${size}`);
            return response.data;
        } catch (error) {

        }

    };

    async function handleSubmit() {
        if (sizeValue?.length > 0) {
            setIsLoading(true)
            const data = await fetchMostPickedCards(sizeValue)
            const resultsTransform = data.map(item => ({ cards: item["_id"].split("-").map(cardId => findById(cardId)), totalMatches: item["totalMatches"] }))
            //setResults(data)
            setResultsTransformed(resultsTransform)
            setIsLoading(false)
        } else {
            alert("Preencha todos os dados")
        }
    }



    return (<div className="section">
        <Button variant="contained" color="primary" onClick={() => setActiveSection('mostPickedCards')}>
            Fetch Most Picked Cards
        </Button>
        {activeSection === 'mostPickedCards' && (
            <Card className="card">
                <CardContent>
                    <TextField
                        label={"Tamanho"}
                        name={"size"}
                        value={sizeValue}
                        onChange={(event) => {
                            setSizeValue(event.target.value);
                        }}
                        variant="outlined"
                        margin="normal"
                        fullWidth
                    />
                    <Button variant="contained" color="secondary" onClick={handleSubmit}
                        disabled={isLoading}>
                        Submit
                    </Button>
                    {isLoading && <CircularProgress />}
                    {resultsTransformed ? (<div>
                        {resultsTransformed.map(({ cards, totalMatches }) => {
                            return (<div>
                                <div style={{ display: "flex", flexDirection: "row", gap: 4, border: "2px solid #eaeaea", marginBottom: 6, marginTop: 6, borderRadius: 6 }}>
                                    {cards.map(value => (<div style={{ display: "flex", width:120, flexDirection: "column", alignItems: "center", justifyItems: "center", marginBottom: 16 }} >
                                        <img src={value["iconUrls"]["medium"]} width={100} height={120} alt="card"></img>
                                        <span style={{textAlign: "center"}}>{value["name"]}</span>
                                    </div>))}
                                    <div style={{display: "flex", width: 120, alignItems: "center", textAlign: "center"}}>
                                       <strong> Total de partidas:</strong> {totalMatches}
                                    </div>
                                </div>
                                

                            </div>)
                        })}
                    </div>) : null}
                </CardContent>
            </Card>
        )}
    </div>)
}   