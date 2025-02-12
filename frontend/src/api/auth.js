import axios from 'axios';

const API_URL = 'http://localhost:8000/api/auth/'; // Adres API backendu

// Funkcja do logowania użytkownika
// auth.js
async function login(email, password) {
  const response = await axios.post(`${API_URL}login/`, { email, password });
  console.log(response.data); // Zobacz, czy dane są poprawnie w odpowiedzi
  const { access, refresh, role, firstName, lastName } = response.data;

  // Przechowujemy tokeny i dane użytkownika w localStorage
  localStorage.setItem('access', access);
  localStorage.setItem('refresh', refresh);
  localStorage.setItem('role', role);
  localStorage.setItem('firstName', firstName); // Zapisujemy imię
  localStorage.setItem('lastName', lastName); // Zapisujemy nazwisko

  return response.data;
}

async function register(userData) {
  /*
    Uwaga: userData to obiekt zawierający dane takie jak:
    {
      email, password, first_name, last_name, phone_number, date_of_birth
    }
  */
  return await axios.post(`${API_URL}register/`, userData);
}

function logout() {
  // Usuwamy tokeny z localStorage
  localStorage.removeItem('access');
  localStorage.removeItem('refresh');
  localStorage.removeItem('role');
}

export { login, register, logout };