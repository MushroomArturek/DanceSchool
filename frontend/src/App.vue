<template>
  <div class="dashboard">
    <SideMenu />
    <MainContent />
  </div>
</template>

<script>
import SideMenu from "./components/SideMenu.vue";
import MainContent from "./components/MainContent.vue";

export default {
  name: "App",
  components: {
    SideMenu,
    MainContent,
  },
};
</script>

<style>
/* Body i dashboard global styles */
body {
  margin: 0;
  font-family: "Open Sans", sans-serif;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5;
  color: #515151;
  background-color: #e9edf4;
}

.dashboard {
  display: flex;
  min-height: 100vh; /* Pełna wysokość aplikacji */
}
</style>