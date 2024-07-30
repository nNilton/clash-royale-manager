import React, { useState } from "react"
import { Button } from "@mui/material"
import { SearchCard } from "../SearchCard"
import AddIcon from '@mui/icons-material/Add';


export function SearchMultipleCards({countFields, handleAddCard, handleSetValue, handleCloseCard}) {
    return (<div style={{ display: "grid", gridTemplateColumns: "repeat(3, 300px)" }}>
        {countFields.map((item) => {
            return <SearchCard value={item.value} setValue={(value) => handleSetValue(item.id, value)} onClose={countFields.length > 1 ? () => handleCloseCard(item.id) : null} />
        })}
        {countFields.length < 8 ? (<div style={{ width: 300, height: 300, display: "flex" }}>
            <Button style={{flex: 1, alignItems: "center", justifyItems: "center"}} onClick={() => handleAddCard()}><AddIcon color="error" sx={{ fontSize: 40 }}  /></Button>
        </div>) : null}
    </div>)
}