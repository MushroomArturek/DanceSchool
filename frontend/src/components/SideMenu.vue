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
      <router-link
          v-if="authState.isLoggedIn && authState.role === 'student'"
          to="/reservations"
          class="dashboard-nav-item">
        <i class="fas fa-bookmark"></i> Rezerwacje
      </router-link>
      <router-link
          v-if="authState.isLoggedIn && authState.role === 'student'"
          to="/payments"
          class="dashboard-nav-item">
        <i class="fas fa-credit-card"></i> Płatności
      </router-link>
      <router-link
          v-if="authState.isLoggedIn && authState.role === 'instructor'"
          to="/attendance"
          class="dashboard-nav-item">
        <i class="fas fa-clipboard-list"></i> Lista obecności
      </router-link>
      <router-link
          v-if="!authState.isLoggedIn"
          to="/pricing"
          class="dashboard-nav-item">
        <i class="fas fa-tags"></i> Cennik
      </router-link>
      <!--      <div class="dashboard-nav-dropdown">-->
      <!--        <a href="#!" class="dashboard-nav-item dashboard-nav-dropdown-toggle">-->
      <!--          <i class="fas fa-users"></i> Users-->
      <!--        </a>-->
      <!--        <div class="dashboard-nav-dropdown-menu">-->
      <!--          <a href="#" class="dashboard-nav-dropdown-item">All Users</a>-->
      <!--          <a href="#" class="dashboard-nav-dropdown-item">Subscribed</a>-->
      <!--          <a href="#" class="dashboard-nav-dropdown-item">Banned</a>-->
      <!--        </div>-->
      <!--      </div>-->
      <router-link v-if="authState.isLoggedIn" to="/profile" class="dashboard-nav-item">
        <i class="fas fa-cogs"></i> Ustawienia konta
      </router-link>
      <!-- Admin Panel Section -->
      <template v-if="authState.isLoggedIn && authState.role === 'admin'">
        <div class="nav-item-divider"></div>
        <div class="dashboard-nav-dropdown" :class="{ 'show': isAdminMenuOpen }">
          <a href="#" class="dashboard-nav-item dashboard-nav-dropdown-toggle" @click.prevent="toggleAdminMenu">
            <i class="fas fa-users-cog"></i> Panel Administracyjny
            <i class="fas fa-chevron-down dropdown-arrow"></i>
          </a>
          <div class="dashboard-nav-dropdown-menu">
            <router-link to="/admin/instructors" class="dashboard-nav-dropdown-item">
              <i class="fas fa-chalkboard-teacher"></i> Instruktorzy
            </router-link>
            <router-link to="/admin/students" class="dashboard-nav-dropdown-item">
              <i class="fas fa-user-graduate"></i> Uczniowie
            </router-link>
            <router-link to="/admin/classes" class="dashboard-nav-dropdown-item">
              <i class="fas fa-calendar-alt"></i> Zajęcia
            </router-link>
          </div>
        </div>

        <div class="dashboard-nav-dropdown" :class="{ 'show': isReportsMenuOpen }">
          <a href="#" class="dashboard-nav-item dashboard-nav-dropdown-toggle" @click.prevent="toggleReportsMenu">
            <i class="fas fa-chart-line"></i> Raporty
            <i class="fas fa-chevron-down dropdown-arrow"></i>
          </a>
          <div class="dashboard-nav-dropdown-menu">
            <router-link to="/admin/reports/attendance" class="dashboard-nav-dropdown-item">
              <i class="fas fa-chart-bar"></i> Frekwencja
            </router-link>
            <router-link to="/admin/reports/financial" class="dashboard-nav-dropdown-item">
              <i class="fas fa-dollar-sign"></i> Finanse
            </router-link>
            <router-link to="/admin/reports/analytics" class="dashboard-nav-dropdown-item">
              <i class="fas fa-chart-pie"></i> Analityka
            </router-link>
          </div>
        </div>

      </template>
      <router-link to="/school-info" class="dashboard-nav-item">
        <i class="fas fa-info-circle"></i> Dane szkoły
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
import {ref} from 'vue';
import {authState, updateAuthState} from "../state/authState";
import {logout} from "../api/auth.js";

export default {
  name: 'SideMenu',
  setup() {
    const isAdminMenuOpen = ref(false);
    const isReportsMenuOpen = ref(false);

    const toggleAdminMenu = () => {
      isAdminMenuOpen.value = !isAdminMenuOpen.value;
      if (isAdminMenuOpen.value) isReportsMenuOpen.value = false;
    };

    const toggleReportsMenu = () => {
      isReportsMenuOpen.value = !isReportsMenuOpen.value;
      if (isReportsMenuOpen.value) isAdminMenuOpen.value = false;
    };

    const handleLogout = async () => {
      try {
        await logout();
        updateAuthState(false, null);
      } catch (error) {
        console.error('Logout error:', error);
      }
    };

    return {
      authState,
      isAdminMenuOpen,
      isReportsMenuOpen,
      toggleAdminMenu,
      toggleReportsMenu,
      handleLogout
    };
  }
};
</script>

<style scoped>
/* Styles for the sidebar (dashboard-nav) */
.dashboard-nav {
  min-width: 280px; /* Zwiększamy minimalną szerokość */
  width: 280px; /* Stała szerokość */
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  overflow-y: auto;
  overflow-x: hidden; /* Zapobiegamy poziomemu scrollowaniu */
  background-color: #443ea2;
  z-index: 1100; /* Wyższy z-index niż reszta elementów */
}

.dashboard-nav header {
  min-height: 84px;
  width: 100%; /* Pełna szerokość */
  padding: 8px 27px;
  display: flex;
  align-items: center;
  justify-content: flex-start; /* Wyrównanie do lewej */
}

.dashboard-nav a {
  color: #fff;
  text-decoration: none;
}


.brand-logo {
  width: 100%;
  font-family: "Nunito", sans-serif;
  font-weight: bold;
  font-size: 20px;
  display: flex;
  align-items: center;
  gap: 15px; /* Dodajemy stały odstęp między ikoną a tekstem */
  color: #fff;
  padding: 0 27px; /* Zamieniamy padding-right na padding po obu stronach */
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
  padding: 15px 27px; /* Ujednolicamy padding */
  display: flex;
  align-items: center;
  gap: 15px; /* Stały odstęp między ikoną a tekstem */
  font-size: 20px;
  color: #fff;
  text-decoration: none;
  transition: background 0.3s, color 0.3s;
}

.dashboard-nav-item i {
  width: 24px; /* Stała szerokość dla ikon */
  font-size: 24px;
  text-align: center; /* Centrujemy ikony w ich kontenerze */
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
  padding: 10px 27px 10px 66px; /* 66px = 27px (podstawowy padding) + 24px (szerokość ikony) + 15px (gap) */
  display: flex;
  align-items: center;
  gap: 15px;
  font-size: 18px;
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

.dashboard-nav-dropdown {
  position: relative;
}

.dashboard-nav-dropdown-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.dropdown-arrow {
  margin-left: auto; /* Przesuwa strzałkę na prawo */
  font-size: 0.8em;
}

.dashboard-nav-dropdown.show .dropdown-arrow {
  transform: rotate(180deg);
}

.dashboard-nav-dropdown-menu {
  display: none;
  background: rgba(0, 0, 0, 0.15);
}

.dashboard-nav-dropdown.show .dashboard-nav-dropdown-menu {
  display: block;
}

.dashboard-nav-dropdown-item {
  display: block;
  padding: 8px 20px 8px 40px;
  font-size: 0.85em;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.3s;
}

.dashboard-nav-dropdown-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}
</style>