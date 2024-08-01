import React, { useState } from 'react';
import { TextField, Button, Card, CardContent, Typography, CircularProgress, Container } from '@mui/material';
import '../../App.css';
import api from '../../config/api';
import { useCards } from "../../context/CardsContext"

export function FormMostPopularDeck({ activeSection, setActiveSection }) {
    const { findById } = useCards()
    const [criteriaValue, setCriteriaValue] = useState("")


    const [isLoading, setIsLoading] = useState(false)
    const [resultsTransformed, setResultsTransformed] = useState(null)


    async function fetchMostPicked(criteria) {
        try {
            const response = await api.get(`metrics/ten-most-popular-decks/{criteria]?criteria=${criteria}`);
            return response.data;
        } catch (error) {

        }

    };

    async function handleSubmit() {
        if (criteriaValue?.length > 0) {
            setIsLoading(true)
            const data = await fetchMostPicked(criteriaValue)
            const resultsTransform = data.map(item => ({ cards: item["_id"].split("-").map(cardId => findById(cardId)), tagCount: item["tagCount"], uniqueTags: item["uniqueTags"] }))
            //setResults(data)
            setResultsTransformed(resultsTransform)
            setIsLoading(false)
        } else {
            alert("Preencha todos os dados")
        }
    }


    return (<div className="section">
        <Button variant="contained" color="primary" onClick={() => setActiveSection('mostPopularCards')}>
        Fetch Most Popular Cards
        </Button>
        {activeSection === 'mostPopularCards' && (
            <Card className="card">
                <CardContent>
                    <TextField
                        label={"Critério"}
                        name={"criteria"}
                        value={criteriaValue}
                        onChange={(event) => {
                            setCriteriaValue(event.target.value);
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
                        {resultsTransformed.map(({ cards, uniqueTags, tagCount }) => {
                            return (<div>
                                <div style={{ display: "flex", width: 120 }}>
                                    <strong>Jogadores:</strong> {JSON.stringify(uniqueTags)}
                                </div>
                                <div style={{ display: "flex", width: 120 }}>
                                    <strong>Quantidade:</strong> {tagCount}
                                </div>
                                <div style={{ display: "flex", flexDirection: "row", gap: 4, border: "2px solid #eaeaea", marginBottom: 6, marginTop: 6, borderRadius: 6 }}>
                                    {cards.map(value => (<div style={{ display: "flex", width: 120, flexDirection: "column", alignItems: "center", justifyItems: "center", marginBottom: 16 }} >
                                        <img src={value["iconUrls"]["medium"]} width={100} height={120} alt="card"></img>
                                        <span style={{ textAlign: "center" }}>{value["name"]}</span>
                                    </div>))}
                                </div>
                            </div>)
                        })}
                    </div>) : null}
                </CardContent>
            </Card>
        )}
    </div>)
}   