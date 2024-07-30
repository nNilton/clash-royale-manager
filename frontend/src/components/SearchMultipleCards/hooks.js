import { useState } from "react";

export function useSearchMultipleCards() {
    const [countFields, setCountFields] = useState([getRandomSearchObject()])

    const handleAddCard = () => {
        setCountFields(oldValue => oldValue.length < 8 ? [...oldValue, getRandomSearchObject()] : oldValue)
    }

    function handleSetValue(id, valueA) {
        setCountFields(oldValue => {
            const oldItem = oldValue.find(item => item.id === id)
            const newItem = { ...oldItem, value: valueA }
            return oldValue.map(item => item.id === id ? newItem : item)
        });
    }

    function handleCloseCard(id) {
        setCountFields(oldValue => {
            return oldValue.filter(item => item.id != id);
        });
    }

    function getRandomSearchObject() {
        return {
            id: getRandomInt(),
            value: null
        }
    }

    function getRandomInt() {
        return Math.floor(Math.random() * (10000 + 1));
    }

    return { countFields, handleAddCard, handleSetValue, handleCloseCard }
}