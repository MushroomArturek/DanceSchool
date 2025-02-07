import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../pages/HomePage.vue";
import ClassSchedule from "../components/ClassSchedule.vue";
import Login from "../components/Login.vue";
import Register from "../components/Register.vue"; // Nowy komponent strony głównej

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
  {
    path: '/login',
    component: Login,
  },
  {
    path: "/register",
    component: Register,
  },
];

// Tworzenie routera
const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;