<template>
  <div class="dashboard-app">
    <div class="dashboard-toolbar">
      <div v-if="authState.isLoggedIn" class="user-info">
        Zalogowano jako: {{ authState.email }}
      </div>
      <div v-else class="user-info">
        Niezalogowany
      </div>
    </div>
    <div class="dashboard-content">
      <router-view />
    </div>
  </div>
</template>

<script>
import { authState } from '../state/authState'; // Importujemy stan autoryzacji

export default {
  name: "MainContent",
  setup() {
    console.log(authState); // Sprawdzamy zawartość authState w konsoli

    return {
      authState, // Udostępniamy stan autoryzacji w szablonie
    };
  },
};
</script>

<style scoped>
/* Styles for the main content (dashboard-app) */
.dashboard-app {
  margin-left: 238px; /* Przesunięcie na prawo o szerokość sidebar */
  display: flex;
  flex-direction: column;
  flex-grow: 2;
  position: relative; /* Układ względem sidebar */
}

.dashboard-toolbar {
  height: 84px;
  background-color: #dfdfdf;
  display: flex;
  align-items: center;
  padding: 8px 27px;
  position: fixed;
  top: 0;
  right: 0;
  left: 238px; /* Uwzględnienie sidebar w górnym pasku */
  z-index: 1000;
}

.user-info {
  margin-left: auto; /* Przesuwa informację o użytkowniku na prawo */
  font-size: 16px;
  color: #333;
}

.dashboard-content {
  margin-top: 84px; /* Dolna krawędź toolbar */
  padding: 25px;
  flex-grow: 2;
}
</style>