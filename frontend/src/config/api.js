import axios from 'axios';

const url = `http://127.0.0.1:8000`;

export default axios.create({
  baseURL: url,
  timeout: 30 * 1000,
});
