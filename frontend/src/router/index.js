import {createRouter, createWebHistory} from "vue-router";
import HomePage from "../pages/HomePage.vue";
import ClassSchedule from "../components/ClassSchedule.vue";
import Login from "../components/auth/Login.vue";
import Register from "../components/auth/Register.vue";
import UserSettings from "../components/UserSettings.vue";
import PricingPage from "../pages/PricingPage.vue";
import Reservations from "../components/Reservations.vue";
import PaymentList from "../components/PaymentList.vue";

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
    },
    {
        path: '/admin/instructors',
        name: 'AdminInstructors',
        component: () => import('../components/admin/AdminInstructors.vue'),
        meta: {requiresAuth: true, requiresAdmin: true}
    },
    {
        path: '/admin/classes',
        name: 'AdminClasses',
        component: () => import('../components/admin/AdminClasses.vue'),
        meta: {requiresAuth: true, requiresAdmin: true}
    },
    {
        path: '/admin/students',
        name: 'AdminStudents',
        component: () => import('../components/admin/AdminStudents.vue'),
        meta: {requiresAuth: true, requiresAdmin: true}
    },
    {
        path: '/admin/reports/attendance',
        name: 'AttendanceReport',
        component: () => import('../components/admin/reports/AttendanceReport.vue'),
        meta: {requiresAuth: true, requiresAdmin: true}
    },
    {
        path: '/admin/reports/analytics',
        name: 'ClassAnalytics',
        component: () => import('../components/admin/reports/ClassAnalytics.vue'),
        meta: {requiresAuth: true, requiresAdmin: true}
    },
    {
        path: "/payments",
        name: "Payments",
        component: PaymentList,
        meta: {requiresAuth: true}
    },
    {
        path: '/attendance/:classId?',
        name: 'Attendance',
        component: () => import('../components/instructor/AttendanceList.vue'),
        meta: {requiresAuth: true, roles: ['instructor']}
    },
    {
        path: '/school-info',
        name: 'SchoolInfo',
        component: () => import('../components/SchoolInfo.vue')
    },


];

// Tworzenie routera
const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;