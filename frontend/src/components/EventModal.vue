<template>
  <div v-if="show" class="modal-overlay">
    <div class="modal">
      <h3>{{ eventData.title }}</h3>
      <p>{{ eventData.description }}</p>
      <p>Start: {{ eventData.start }}</p>
      <p>Koniec: {{ eventData.end }}</p>

      <button v-if="authState.isLoggedIn && authState.role === 'student'"
              @click="reserveClass(eventData.id)">
        Zarezerwuj
      </button>

      <button @click="closeModal">Zamknij</button>
    </div>
  </div>
</template>

<script>
import { authState } from "../state/authState.js";
import axios from "axios";

export default {
  props: ["show", "eventData"],
  emits: ["close"],

  setup(props, { emit }) {
    const reserveClass = async (classId) => {
      try {
        await axios.post(
          "http://localhost:8000/api/bookings/create/",
          { class_model: classId },
          {
            headers: { Authorization: `Bearer ${localStorage.getItem("access")}` },
          }
        );
        alert("Rezerwacja zakończona sukcesem!");
        emit("close");
      } catch (error) {
        alert(error.response?.data?.detail || "Wystąpił błąd podczas rezerwacji.");
      }
    };

    const closeModal = () => emit("close");

    return { reserveClass, closeModal, authState };
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}

button {
  margin-top: 10px;
  padding: 8px 12px;
  border: none;
  cursor: pointer;
}

button:first-of-type {
  background: #1c7df9;
  color: white;
}

button:last-of-type {
  background: #d9534f;
  color: white;
}
</style>
