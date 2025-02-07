<template>
  <div class="dashboard-app">
    <div class="dashboard-toolbar">
      Pasek nawigacyjny / nagłówek (jeśli jest potrzebny)
    </div>
    <div class="dashboard-content">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: "MainContent",
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

.dashboard-content {
  margin-top: 84px; /* Dolna krawędź toolbar */
  padding: 25px;
  flex-grow: 2;
}
</style>