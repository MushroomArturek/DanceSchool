<template>
  <div class="dashboard-nav">
    <header>
      <a href="#" class="brand-logo">
        <i class="fa-solid fa-music"></i>
        <span>De la Salsa</span>
      </a>
    </header>
    <nav class="dashboard-nav-list">
      <router-link to="/" class="dashboard-nav-item">
        <i class="fas fa-home"></i> Strona Główna
      </router-link>
      <router-link to="/schedule" class="dashboard-nav-item">
        <i class="fa-solid fa-calendar-days"></i> Harmonogram zajęć
      </router-link>
      <div class="dashboard-nav-dropdown">
        <a href="#!" class="dashboard-nav-item dashboard-nav-dropdown-toggle">
          <i class="fas fa-users"></i> Users
        </a>
        <div class="dashboard-nav-dropdown-menu">
          <a href="#" class="dashboard-nav-dropdown-item">All Users</a>
          <a href="#" class="dashboard-nav-dropdown-item">Subscribed</a>
          <a href="#" class="dashboard-nav-dropdown-item">Banned</a>
        </div>
      </div>
      <router-link v-if="authState.isLoggedIn" to="/profile" class="dashboard-nav-item">
        <i class="fas fa-cogs"></i> Ustawienia konta
      </router-link>
      <div class="nav-item-divider"></div>
      <!-- Przycisk Logowanie widoczny tylko dla niezalogowanych -->
      <router-link v-if="!authState.isLoggedIn" to="/login" class="dashboard-nav-item">
        <i class="fas fa-sign-in-alt"></i> Logowanie
      </router-link>
      <!-- Przycisk Logout widoczny tylko dla zalogowanych -->
      <a v-if="authState.isLoggedIn" href="#" class="dashboard-nav-item" @click="handleLogout">
        <i class="fas fa-sign-out-alt"></i> Wyloguj się
      </a>
    </nav>
  </div>
</template>

<script>
import { authState, updateAuthState } from "../state/authState";
import { logout } from "../api/auth.js";

export default {
  setup() {
    return {
      authState,
    };
  },
  methods: {
    handleLogout() {
      logout(); // Wywołanie funkcji logout (czyszczenie tokenów)
      updateAuthState(); // Aktualizacja stanu globalnego
      this.$router.push("/login"); // Przekierowanie na stronę logowania
    },
  },
};
</script>

<style scoped>
/* Styles for the sidebar (dashboard-nav) */
.dashboard-nav {
  min-width: 238px;
  height: 100vh; /* Rozciągnięcie na całą wysokość okna przeglądarki */
  position: fixed;
  left: 0;
  top: 0; /* Zaczyna się od samej góry */
  bottom: 0;
  overflow: auto;
  background-color: #443ea2;
}

.dashboard-nav header {
  min-height: 84px;
  padding: 8px 27px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.dashboard-nav a {
  color: #fff;
  text-decoration: none;
}



.brand-logo {
  font-family: "Nunito", sans-serif;
  font-weight: bold;
  font-size: 20px;
  display: flex;
  align-items: center;
  color: #fff;
}

.brand-logo i {
  color: #d2d1d1;
  font-size: 27px;
  margin-right: 10px;
}

.dashboard-nav-list {
  display: flex;
  flex-direction: column;
  list-style: none; /* Brak znaczników listy */
  padding: 0;
  margin: 0;
}

.dashboard-nav-item {
  min-height: 56px;
  padding: 15px 20px; /* Większe paddingi dla większych kafelków */
  display: flex;
  align-items: center;
  transition: ease-out 0.5s;
  font-size: 20px; /* Zwiększenie rozmiaru czcionki */
  color: #fff;
  text-decoration: none;
  transition: background 0.3s, color 0.3s; /* Łagodny efekt hover */
}

.dashboard-nav-item i {
  width: 36px;
  font-size: 28px; /* Większa ikona */
  margin-right: 30px; /* Większy odstęp między ikoną a tekstem */
}

.dashboard-nav-item:hover {
  background: rgba(255, 255, 255, 0.1); /* Delikatne tło po hover */
}

.dashboard-nav-item:active {
  background: rgba(255, 255, 255, 0.2); /* Aktywne kliknięcie */
}

.dashboard-nav-dropdown {
  display: flex;
  flex-direction: column;
  margin-top: 10px;
}

.dashboard-nav-dropdown-menu {
  display: none;
  flex-direction: column;
}

.dashboard-nav-dropdown.show > .dashboard-nav-dropdown-menu {
  display: flex;
}

.dashboard-nav-dropdown-item {
  min-height: 40px;
  padding: 10px 20px;
  display: flex;
  margin-right: 30px; /* Add consistent spacing for dropdown items */
  transition: ease-out 0.5s;
  font-size: 18px; /* Podmenu może być trochę mniejsze */
  color: #fff;
  text-decoration: none;
  transition: background 0.3s, color 0.3s;
}

.dashboard-nav-dropdown-item:hover {
  background: rgba(255, 255, 255, 0.1); /* Hover dla podmenu */
}

.nav-item-divider {
  height: 2px;
  background: rgba(255, 255, 255, 0.2);
  margin: 10px 0;
}
</style>