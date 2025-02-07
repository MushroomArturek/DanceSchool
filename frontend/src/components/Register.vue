<template>
  <div class="register">
    <h1>Rejestracja</h1>
    <form @submit.prevent="handleRegister">
      <div>
        <label for="first_name">Imię:</label>
        <input type="text" v-model="registerData.first_name" id="first_name" required />
      </div>
      <div>
        <label for="last_name">Nazwisko:</label>
        <input type="text" v-model="registerData.last_name" id="last_name" required />
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="registerData.email" id="email" required />
      </div>
      <div>
        <label for="password">Hasło:</label>
        <input type="password" v-model="registerData.password" id="password" required />
      </div>
      <div>
        <label for="phone_number">Numer telefonu:</label>
        <input type="tel" v-model="registerData.phone_number" id="phone_number" required />
      </div>
      <div>
        <label for="date_of_birth">Data urodzenia:</label>
        <input type="date" v-model="registerData.date_of_birth" id="date_of_birth" required />
      </div>
      <button type="submit" class="register-button">Zarejestruj się</button>
    </form>
    <p v-if="successMessage" class="success">{{ successMessage }}</p>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <router-link class="back-to-login" to="/login">Powrót do logowania</router-link>
  </div>
</template>

<script>
import { register } from "../api/auth.js"; // Import funkcji rejestracji z API

export default {
  data() {
    return {
      registerData: {
        first_name: "",
        last_name: "",
        email: "",
        password: "",
        phone_number: "",
        date_of_birth: "",
      },
      successMessage: "",
      errorMessage: "",
    };
  },
  methods: {
    async handleRegister() {
      try {
        // Wywołanie rejestracji
        await register(this.registerData);

        // Ustawienie sukcesu rejestracji
        this.successMessage = "Rejestracja zakończona sukcesem! Zaloguj się.";
        this.errorMessage = "";

        // Opcjonalnie przekierowanie do logowania po pewnym czasie
        setTimeout(() => {
          this.$router.push("/login");
        }, 2000);
      } catch (error) {
        // Obsługa błędu logowania
        console.error("Błąd rejestracji:", error);
        this.errorMessage =
          error.response?.data?.detail || "Rejestracja nie powiodła się. Spróbuj ponownie.";
        this.successMessage = "";
      }
    },
  },
};
</script>

<style scoped>
/* Style główne dla formularza rejestracji, spójne z Login.vue */
.register {
  max-width: 400px;
  margin: auto;
  padding: 1rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

form div {
  margin-bottom: 1rem;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

input {
  width: 100%;
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #ccc;
}

button {
  width: 100%;
  padding: 0.75rem;
  background-color: #17a2b8;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #138496;
}

.success {
  color: green;
  margin-top: 1rem;
  text-align: center;
}

.error {
  color: red;
  margin-top: 1rem;
  text-align: center;
}

.back-to-login {
  display: block;
  margin-top: 1rem;
  text-align: center;
  color: #443ea2;
  text-decoration: none;
}

.back-to-login:hover {
  text-decoration: underline;
}
</style>