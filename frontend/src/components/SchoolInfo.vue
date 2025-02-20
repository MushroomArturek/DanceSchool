<template>
  <div class="school-info-container">
    <h2>Informacje o szkole</h2>

    <div class="info-card" v-if="schoolInfo">
      <!-- Basic Info Section -->
      <div class="info-section">
        <h3>Dane podstawowe</h3>
        <div class="info-grid">
          <div class="info-item">
            <i class="fas fa-school"></i>
            <div>
              <strong>Nazwa:</strong>
              <p>{{ schoolInfo.name }}</p>
            </div>
          </div>
          <div class="info-item">
            <i class="fas fa-map-marker-alt"></i>
            <div>
              <strong>Adres:</strong>
              <p>{{ schoolInfo.address }}</p>
            </div>
          </div>
          <div class="info-item">
            <i class="fas fa-phone"></i>
            <div>
              <strong>Telefon:</strong>
              <p>{{ schoolInfo.phone }}</p>
            </div>
          </div>
          <div class="info-item">
            <i class="fas fa-envelope"></i>
            <div>
              <strong>Email:</strong>
              <p>{{ schoolInfo.email }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Payment Info Section -->
      <div class="info-section">
        <h3>Dane do płatności</h3>
        <div class="info-grid">
          <div class="info-item">
            <i class="fas fa-university"></i>
            <div>
              <strong>Bank:</strong>
              <p>{{ schoolInfo.bank_name }}</p>
            </div>
          </div>
          <div class="info-item">
            <i class="fas fa-money-check"></i>
            <div>
              <strong>Numer konta:</strong>
              <p>{{ schoolInfo.bank_account }}</p>
            </div>
          </div>
          <div class="info-item">
            <i class="fas fa-user"></i>
            <div>
              <strong>Odbiorca:</strong>
              <p>{{ schoolInfo.bank_recipient }}</p>
            </div>
          </div>
          <div class="info-item">
            <i class="fas fa-file-invoice"></i>
            <div>
              <strong>Tytuł przelewu:</strong>
              <p>{{ schoolInfo.transfer_title_prefix }}</p>
            </div>
          </div>
          <div class="info-item">
            <i class="fas fa-mobile-alt"></i>
            <div>
              <strong>Numer BLIK:</strong>
              <p>{{ schoolInfo.blik_number || 'Brak' }}</p>
            </div>
          </div>
          <div class="info-item">
            <i class="fas fa-id-card"></i>
            <div>
              <strong>NIP:</strong>
              <p>{{ schoolInfo.tax_id || 'Brak' }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Admin Edit Section -->
      <div v-if="isAdmin" class="admin-section">
        <button @click="openEditModal" class="edit-button">
          <i class="fas fa-edit"></i> Edytuj dane
        </button>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal && isAdmin" class="modal">
      <div class="modal-content">
        <h3>Edycja danych szkoły</h3>
        <form @submit.prevent="updateSchoolInfo">
          <div class="form-group">
            <label>Nazwa szkoły:</label>
            <input v-model="editForm.name" type="text" required>
          </div>
          <div class="form-group">
            <label>Adres:</label>
            <textarea v-model="editForm.address" required></textarea>
          </div>
          <div class="form-group">
            <label>Telefon:</label>
            <input v-model="editForm.phone" type="text" required>
          </div>
          <div class="form-group">
            <label>Email:</label>
            <input v-model="editForm.email" type="email" required>
          </div>
          <div class="form-group">
            <label>Nazwa banku:</label>
            <input v-model="editForm.bank_name" type="text" required>
          </div>
          <div class="form-group">
            <label>Numer konta:</label>
            <input v-model="editForm.bank_account" type="text" required>
          </div>
          <div class="form-group">
            <label>Odbiorca:</label>
            <input v-model="editForm.bank_recipient" type="text" required>
          </div>
          <div class="form-group">
            <label>Prefix tytułu przelewu:</label>
            <input v-model="editForm.transfer_title_prefix" type="text" required>
          </div>
          <div class="form-group">
            <label>Numer BLIK:</label>
            <input v-model="editForm.blik_number" type="text">
          </div>
          <div class="form-group">
            <label>NIP:</label>
            <input v-model="editForm.tax_id" type="text">
          </div>
          <div class="modal-buttons">
            <button type="submit" class="save-button">Zapisz zmiany</button>
            <button type="button" @click="showEditModal = false" class="cancel-button">Anuluj</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted} from 'vue';
import {authState} from '../state/authState';
import API from '../axios';

const schoolInfo = ref(null);
const showEditModal = ref(false);
const isAdmin = authState.role === 'admin';
const editForm = ref({});

const fetchSchoolInfo = async () => {
  try {
    const response = await API.get('/school-info/');
    schoolInfo.value = response.data;
  } catch (error) {
    console.error('Error fetching school info:', error);
  }
};

const openEditModal = () => {
  editForm.value = {...schoolInfo.value};  // Kopiujemy aktualne dane do formularza
  showEditModal.value = true;
};

const updateSchoolInfo = async () => {
  try {
    const token = localStorage.getItem('access');
    await API.patch('/school-info/update/', editForm.value, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    await fetchSchoolInfo();
    showEditModal.value = false;
  } catch (error) {
    console.error('Error updating school info:', error);
  }
};

onMounted(() => {
  fetchSchoolInfo();
});
</script>

<style scoped>
.school-info-container {
  padding: 1.5rem;
  max-width: 1000px;
  margin: 0 auto;
}

h2 {
  color: #443ea2;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
}

.info-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.info-section {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.info-section h3 {
  color: #443ea2;
  margin-bottom: 1.2rem;
  font-size: 1.3rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e9ecef;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.2rem;
}

.info-item {
  display: flex;
  gap: 0.8rem;
  padding: 0.8rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s;
}

.info-item:hover {
  transform: translateY(-2px);
}

.info-item i {
  color: #443ea2;
  font-size: 1.1rem;
  min-width: 24px;
  margin-top: 3px;
}

.info-item strong {
  display: block;
  margin-bottom: 0.3rem;
  color: #495057;
  font-size: 0.9rem;
}

.info-item p {
  margin: 0;
  color: #212529;
  font-size: 1rem;
}

.modal {
  position: fixed;
  top: 84px; /* Start from toolbar height */
  left: 280px; /* Start from sidebar width */
  width: calc(100% - 280px); /* Full width minus sidebar */
  height: calc(100vh - 84px); /* Full height minus toolbar */
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1200;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
  top: -42px; /* Move up to center in available space */
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #495057;
  font-weight: 500;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group textarea {
  min-height: 100px;
}

.modal-buttons {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

.save-button,
.cancel-button {
  padding: 0.7rem 1.2rem;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background 0.2s;
}

.save-button {
  background: #443ea2;
  color: white;
}

.save-button:hover {
  background: #372f8b;
}

.cancel-button {
  background: #e9ecef;
  color: #495057;
}

.cancel-button:hover {
  background: #dee2e6;
}

.admin-section {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  text-align: right;
}

.edit-button {
  background: #443ea2;
  color: white;
  border: none;
  padding: 0.7rem 1.2rem;
  border-radius: 6px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  transition: background 0.2s;
}

.edit-button:hover {
  background: #372f8b;
}

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }

  .info-section {
    padding: 0.8rem;
  }

  .info-item {
    padding: 0.6rem;
  }
}
</style>