// src/contexts/DataContext.js
import React, { createContext, useContext, useEffect, useState } from 'react';
import axios from 'axios';
import { url } from '../App';

const DataContext = createContext();

const CARDS_KEY = "CLASHROYALE_CARDS"
export const CardsProvider = ({ children }) => {
  const [isLoading, setIsLoading] = useState(true);
  const [data, setData] = useState(null);
  const [dataFiltered, setDataFiltered] = useState([])

  function searchByName(searchString) {
    const filtered = data.filter(item => item.name.toLowerCase().includes(searchString.toLowerCase()));
    const slicedData = filtered.slice(0, 3);
    setDataFiltered(slicedData);
    return slicedData;
  }

  useEffect(() => {
    fetchData();

    return () => { }
  }, [])




  async function fetchData() {
    try {
      setIsLoading(true);
      const storedData = localStorage.getItem(CARDS_KEY);
      if (storedData) {
        setData(JSON.parse(storedData));
        setIsLoading(false);
      } else {
        const response = await axios.get(`http://${url}:8000/card/`);
        localStorage.setItem(CARDS_KEY, JSON.stringify(response.data));
        setData(response.data);
        setIsLoading(false);
      }
    } catch (error) {
      console.error('Failed to fetch data:', error);
    }
  };

  return (
    <DataContext.Provider value={{ data, isLoading, dataFiltered, searchByName }}>
      {children}
    </DataContext.Provider>
  );

};

export const useCards = () => useContext(DataContext);
