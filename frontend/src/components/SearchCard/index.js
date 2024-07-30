import React, { useEffect, useState } from "react"
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import { useCards } from "../../context/CardsContext";
import { Box, IconButton } from "@mui/material";
import CloseIcon from '@mui/icons-material/Close';

export function SearchCard({ value, setValue, onClose = null }) {
    const { data, dataFiltered, searchByName } = useCards()

    const [textFieldValue, setTextFieldValue] = useState('');

    useEffect(() => {
        if (textFieldValue.length > 1)
            searchByName(textFieldValue)

    }, [textFieldValue]);

    return (<div style={{ height: 300, width: 300, position: "relative", display: "flex", flexDirection: "column", justifyItems: "center" }}>

        {onClose !== null ? <IconButton aria-label="" onClick={onClose} size="large" color="error" style={{ position: "absolute", top: 0, right: 0 }}>
            <CloseIcon />
        </IconButton> : null}

        {value && value?.iconUrls ? (
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyItems: "center", marginBottom: 16 }} >
                <img src={value["iconUrls"]["medium"]} width={150} height={180} alt="card"></img>
                <span>{value["name"]}</span>
            </div>
        ) : <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyItems: "center", marginBottom: 16 }} >
            <img src={"/clash/MysteryCard.webp"} width={150} height={180} alt="card"></img>
            <span>Nenhuma carta selecionada</span>
        </div>}

        <Autocomplete
            value={value}
            onChange={(event, newValue) => {
                setValue(newValue);
            }}
            renderOption={(props, option) => {
                const { key, ...optionProps } = props;
                return (
                    <Box
                        key={key}
                        component="li"
                        sx={{ '& > img': { mr: 2, flexShrink: 0 } }}
                        {...optionProps}
                    >
                        <img
                            loading="lazy"
                            width="20"
                            src={option["iconUrls"]["medium"]}
                            alt=""
                        />
                        {option.name}
                    </Box>
                );
            }}

            getOptionLabel={(option) => option.name}
            id="controllable-states-demo"
            options={textFieldValue.length > 0 ? dataFiltered : data}
            sx={{ width: 300 }}
            renderInput={(params) => <TextField value={textFieldValue} onChange={(event) => {
                setTextFieldValue(event.target.value);
            }}
                {...params} label="Selecione uma carta" />}
        />
    </div>)
}