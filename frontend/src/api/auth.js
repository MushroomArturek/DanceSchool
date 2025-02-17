import axios from 'axios';

const API_URL = 'http://localhost:8000/api/auth/'; // Adres API backendu

// Funkcja do logowania użytkownika
// auth.js
async function login(email, password) {
  try {
    const response = await axios.post(`${API_URL}login/`, { email, password });
    console.log('Login response:', response.data); // For debugging

    const { access, refresh, role, firstName, lastName, email: userEmail } = response.data;

    // Store in localStorage
    localStorage.setItem('access', access);
    localStorage.setItem('refresh', refresh);
    localStorage.setItem('role', role);
    localStorage.setItem('email', userEmail); // Store email
    localStorage.setItem('firstName', firstName);
    localStorage.setItem('lastName', lastName);

    // Return all user data
    return {
      access,
      refresh,
      role,
      email: userEmail,
      firstName,
      lastName
    };
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
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