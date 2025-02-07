// authState.js
import { reactive } from "vue";

// Tworzymy obiekt reaktywny, który śledzi stan logowania
export const authState = reactive({
  isLoggedIn: !!localStorage.getItem("access"), // Sprawdzamy czy token istnieje w localStorage
  role: localStorage.getItem("role") || null, // Przechowuje rolę użytkownika (np. student, instruktor)
  firstName: localStorage.getItem("firstName") || null, // Przechowuje imię użytkownika
  lastName: localStorage.getItem("lastName") || null, // Przechowuje nazwisko użytkownika
});

// Funkcja, która aktualizuje stan logowania
export function updateAuthState(userData = null) {
  authState.isLoggedIn = !!localStorage.getItem("access");
  if (userData) {
    authState.role = userData.role || null;
    authState.firstName = userData.firstName || null;
    authState.lastName = userData.lastName || null;

    // Zapisujemy szczegóły użytkownika w localStorage (opcjonalne, w razie odświeżenia strony)
    localStorage.setItem("role", userData.role);
    localStorage.setItem("firstName", userData.firstName);
    localStorage.setItem("lastName", userData.lastName);
  }
}