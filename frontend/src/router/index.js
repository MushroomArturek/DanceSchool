import {createRouter, createWebHistory} from "vue-router";
import HomePage from "../pages/HomePage.vue";
import ClassSchedule from "../components/ClassSchedule.vue";
import Login from "../components/Login.vue";
import Register from "../components/Register.vue";
import UserSettings from "../components/UserSettings.vue";
import PricingPage from "../pages/PricingPage.vue";
import Reservations from "../components/Reservations.vue";

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
    {
        path: "/profile",
        component: UserSettings,
    },
    {
        path: '/pricing',
        name: 'Pricing',
        component: PricingPage
    },
    {
        path: "/reservations",
        name: "Reservations",
        component: Reservations,
        meta: {requiresAuth: true}
    }

];

// Tworzenie routera
const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;