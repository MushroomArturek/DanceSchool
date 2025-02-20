import axios from "axios";

const API = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 5000  // Request will fail after 5 seconds
});

// Protected endpoints that require authentication
const protectedPaths = [
  // Admin/Update operations
  '/update/',
  '/create/',
  '/delete/',

  // Profile endpoints
  '/profile/',

  // Reports endpoints
  '/reports/',

  // Protected list endpoints
  '/payments/',
  '/attendance/',
  '/instructors/',
  '/bookings/',

  // Admin endpoints
  '/admin/',

  // Student management (when accessed by admin)
  '/students/create/',
  '/students/update/',
  '/students/delete/'
];

// Add request interceptor
API.interceptors.request.use(config => {
  // Check if the request URL matches any protected path
  const isProtectedPath = protectedPaths.some(path => config.url.includes(path));

  if (isProtectedPath) {
    const token = localStorage.getItem('access');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

export default API;