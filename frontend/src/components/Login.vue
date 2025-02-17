<template>
  <div class="login">
    <h1>Zaloguj się</h1>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="email" id="email" required/>
      </div>
      <div>
        <label for="password">Hasło:</label>
        <input type="password" v-model="password" id="password" required/>
      </div>
      <p class="forgot-password">
        <a href="#">Nie pamiętam hasła</a>
      </p>
      <button type="submit" class="login-button">Zaloguj się</button>
    </form>
    <button @click="goToRegister" class="register-button">Załóż konto</button>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import {login} from "../api/auth.js"; // Import funkcji do logowania z API
import {updateAuthState} from "../state/authState"; // Import funkcji stanu globalnego

export default {
  data() {
    return {
      email: "", // dane użytkownika wprowadzone w formularzu
      password: "",
      errorMessage: "", // Błąd logowania
    };
  },
  methods: {
    async handleLogin() {
      try {
        // Get user data from login response
        const userData = await login(this.email, this.password);

        // Update auth state with user data
        updateAuthState(userData);

        // Redirect to dashboard
        this.$router.push("/");
      } catch (error) {
        this.errorMessage = "Nie udało się zalogować. Sprawdź poprawność danych i spróbuj ponownie.";
        console.error("Błąd logowania:", error.message);
      }
    },
    goToRegister() {
      // Funkcja przekierowująca do strony rejestracji
      this.$router.push("/register");
    },
  },
};
</script>

<style scoped>
/* Style pozostają bez zmian */
</style>

<style scoped>
/* Opcjonalne style dla logowania */
.login {
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
  background-color: #443ea2;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #372f8b; /* Ciemniejszy odcień dla hover */
}

.forgot-password {
  text-align: right;
  margin-bottom: 1rem;
}

.forgot-password a {
  text-decoration: none;
  color: #443ea2;
}

.forgot-password a:hover {
  text-decoration: underline;
}

.register-button {
  margin-top: 1rem;
  background-color: #17a2b8; /* Kolor dla przycisku rejestracji */
}

.register-button:hover {
  background-color: #138496; /* Hover dla rejestracji */
}

.error {
  color: red;
  margin-top: 1rem;
  text-align: center;
}
</style>