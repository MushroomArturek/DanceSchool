// authState.js
import { reactive } from "vue";

export const authState = reactive({
  isLoggedIn: !!localStorage.getItem("access"),
  role: localStorage.getItem("role") || null,
  email: localStorage.getItem("email") || null,
  firstName: localStorage.getItem("firstName") || null, // Imię użytkownika
  lastName: localStorage.getItem("lastName") || null, // Nazwisko użytkownika
});

export function updateAuthState(userData = null) {
  authState.isLoggedIn = !!localStorage.getItem("access");
  if (userData) {
    authState.role = userData.role || null;
    authState.email = userData.email || null;
    authState.firstName = userData.firstName || null; // Aktualizacja imienia
    authState.lastName = userData.lastName || null; // Aktualizacja nazwiska

    // Zapisujemy dane w localStorage
    localStorage.setItem("role", userData.role);
    localStorage.setItem("email", userData.email);
    localStorage.setItem("firstName", userData.firstName); // Zapisujemy imię
    localStorage.setItem("lastName", userData.lastName); // Zapisujemy nazwisko
  }
}