<template>
  <div class="profile-settings">
    <h1>Zmiana danych</h1>
    <form @submit.prevent="handleUpdate">
      <div>
        <label for="first_name">Imię:</label>
        <input type="text" v-model="userData.first_name" id="first_name" required />
      </div>
      <div>
        <label for="last_name">Nazwisko:</label>
        <input type="text" v-model="userData.last_name" id="last_name" required />
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="userData.email" id="email" disabled />
      </div>
      <div>
        <label for="phone_number">Numer telefonu:</label>
        <input type="tel" v-model="userData.phone_number" id="phone_number" required />
      </div>
      <div>
        <label for="date_of_birth">Data urodzenia:</label>
        <input type="date" v-model="userData.date_of_birth" id="date_of_birth" required />
      </div>
      <button type="submit" class="update-button">Zaktualizuj</button>
    </form>
    <p v-if="successMessage" class="success">{{ successMessage }}</p>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      userData: {
        first_name: "",
        last_name: "",
        email: "",
        phone_number: "",
        date_of_birth: "",
      },
      successMessage: "",
      errorMessage: "",
    };
  },
  created() {
    this.loadUserData();
  },
  methods: {
    async loadUserData() {
      try {
        const response = await axios.get("http://localhost:8000/api/student/profile/", {
          headers: {Authorization: `Bearer ${localStorage.getItem("token")}`},
        });
        this.userData = response.data;
      } catch (error) {
        console.error("Błąd ładowania danych użytkownika:", error);
        this.errorMessage = "Nie udało się pobrać danych.";
      }
    },
    async handleUpdate() {
      try {
        await axios.patch("http://localhost:8000/api/student/profile/update/", this.userData, {
          headers: {Authorization: `Bearer ${localStorage.getItem("token")}`},
        });
        this.successMessage = "Dane zostały zaktualizowane!";
        this.errorMessage = "";
      } catch (error) {
        console.error("Błąd aktualizacji danych:", error);
        this.errorMessage = error.response?.data?.detail || "Aktualizacja nie powiodła się.";
        this.successMessage = "";
      }
    },
  },
};
</script>

<style scoped>
.profile-settings {
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
</style>
