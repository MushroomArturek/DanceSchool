import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../components/HomePage.vue";
import ClassSchedule from "../components/ClassSchedule.vue"; // Nowy komponent strony głównej

// Definiowanie tras
const routes = [
  {
    path: "/",
    name: "Home",
    component: HomePage, // Strona startowa
  },
    {
    path: "/schedule",
    name: "Classes Schedule",
    component: ClassSchedule, // Strona z listą zajęć
  },
];

// Tworzenie routera
const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;