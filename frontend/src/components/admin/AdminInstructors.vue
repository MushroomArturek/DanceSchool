<template>
  <div class="admin-instructors">
    <div class="header">
      <h2>Zarządzanie Instruktorami</h2>
      <button class="btn btn-primary" @click="openAddModal">
        <i class="fas fa-plus"></i> Dodaj Instruktora
      </button>
    </div>

    <!-- Lista instruktorów -->
    <div v-if="instructors.length === 0" class="no-data">
      Brak instruktorów w bazie danych
    </div>

    <table v-else class="instructors-table">
      <thead>
        <tr>
          <th>Imię i Nazwisko</th>
          <th>Email</th>
          <th>Specjalizacja</th>
          <th>Akcje</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="instructor in instructors" :key="instructor.id">
          <td>{{ instructor.first_name }} {{ instructor.last_name }}</td>
          <td>{{ instructor.email }}</td>
          <td>{{ instructor.specialization || 'Brak' }}</td>
          <td class="actions">
            <button class="btn btn-edit" @click="openEditModal(instructor)">
              <i class="fas fa-edit"></i>
            </button>
            <button class="btn btn-delete" @click="openDeleteModal(instructor)">
              <i class="fas fa-trash"></i>
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Modal formularza -->
    <div v-if="isModalOpen" class="modal" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ modalTitle }}</h3>
          <button class="btn-close" @click="closeModal">&times;</button>
        </div>
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label>Imię:</label>
            <input
              type="text"
              v-model="formData.first_name"
              required
              @input="validateForm"
            >
          </div>
          <div class="form-group">
            <label>Nazwisko:</label>
            <input
              type="text"
              v-model="formData.last_name"
              required
              @input="validateForm"
            >
          </div>
          <div class="form-group">
            <label>Email:</label>
            <input
              type="email"
              v-model="formData.email"
              required
              @input="validateForm"
            >
          </div>
          <div class="form-group">
            <label>Specjalizacja:</label>
            <input
              type="text"
              v-model="formData.specialization"
              @input="validateForm"
            >
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">
              Anuluj
            </button>
            <button
              type="submit"
              class="btn btn-primary"
              :disabled="!isFormValid || isSubmitting"
            >
              {{ isSubmitting ? 'Zapisywanie...' : 'Zapisz' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal potwierdzenia usunięcia -->
    <div v-if="isDeleteModalOpen" class="modal" @click.self="closeDeleteModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Potwierdź usunięcie</h3>
          <button class="btn-close" @click="closeDeleteModal">&times;</button>
        </div>
        <div class="modal-body">
          <p>
            Czy na pewno chcesz usunąć instruktora
            {{ selectedInstructor?.first_name }}
            {{ selectedInstructor?.last_name }}?
          </p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="closeDeleteModal">
            Anuluj
          </button>
          <button
            class="btn btn-danger"
            @click="deleteInstructor"
            :disabled="isDeleting"
          >
            {{ isDeleting ? 'Usuwanie...' : 'Usuń' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed } from 'vue';
import axios from 'axios';

export default {
  name: 'AdminInstructors',
  setup() {
    const instructors = ref([]);
    const isModalOpen = ref(false);
    const isDeleteModalOpen = ref(false);
    const selectedInstructor = ref(null);
    const isSubmitting = ref(false);
    const isDeleting = ref(false);
    const isEditing = ref(false);

    const formData = reactive({
      first_name: '',
      last_name: '',
      email: '',
      specialization: ''
    });

    const modalTitle = computed(() =>
      isEditing.value ? 'Edytuj Instruktora' : 'Dodaj Instruktora'
    );

    const isFormValid = computed(() =>
      formData.first_name &&
      formData.last_name &&
      formData.email
    );

    const fetchInstructors = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/instructors/', {
          headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
        });
        instructors.value = response.data;
      } catch (error) {
        console.error('Błąd podczas pobierania instruktorów:', error);
        alert('Nie udało się pobrać listy instruktorów');
      }
    };

    const resetForm = () => {
      Object.keys(formData).forEach(key => formData[key] = '');
      isEditing.value = false;
      selectedInstructor.value = null;
    };

    const openAddModal = () => {
      resetForm();
      isModalOpen.value = true;
    };

    const openEditModal = (instructor) => {
      isEditing.value = true;
      selectedInstructor.value = instructor;
      Object.assign(formData, instructor);
      isModalOpen.value = true;
    };

    const openDeleteModal = (instructor) => {
      selectedInstructor.value = instructor;
      isDeleteModalOpen.value = true;
    };

    const closeModal = () => {
      isModalOpen.value = false;
      resetForm();
    };

    const closeDeleteModal = () => {
      isDeleteModalOpen.value = false;
      selectedInstructor.value = null;
    };

    const submitForm = async () => {
      if (!isFormValid.value) return;

      isSubmitting.value = true;
      const url = isEditing.value
        ? `http://localhost:8000/api/instructors/${selectedInstructor.value.id}/update/`
        : 'http://localhost:8000/api/instructors/create/';

      try {
        const method = isEditing.value ? 'put' : 'post';
        await axios[method](url, formData, {
          headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
        });
        await fetchInstructors();
        closeModal();
      } catch (error) {
        console.error('Błąd podczas zapisywania:', error);
        alert('Nie udało się zapisać instruktora');
      } finally {
        isSubmitting.value = false;
      }
    };

    const deleteInstructor = async () => {
      if (!selectedInstructor.value) return;

      isDeleting.value = true;
      try {
        await axios.delete(
          `http://localhost:8000/api/instructors/${selectedInstructor.value.id}/delete/`,
          {
            headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
          }
        );
        await fetchInstructors();
        closeDeleteModal();
      } catch (error) {
        console.error('Błąd podczas usuwania:', error);
        alert('Nie udało się usunąć instruktora');
      } finally {
        isDeleting.value = false;
      }
    };

    // Inicjalne pobranie danych
    fetchInstructors();

    return {
      instructors,
      formData,
      isModalOpen,
      isDeleteModalOpen,
      selectedInstructor,
      isSubmitting,
      isDeleting,
      isFormValid,
      modalTitle,
      openAddModal,
      openEditModal,
      openDeleteModal,
      closeModal,
      closeDeleteModal,
      submitForm,
      deleteInstructor,
      validateForm: () => {} // Pusty handler dla walidacji
    };
  }
};
</script>

<style scoped>
.admin-instructors {
  padding: 20px;
  margin-left: 238px;
}

.no-data {
  text-align: center;
  padding: 20px;
  color: #777;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.instructors-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.instructors-table th,
.instructors-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.instructors-table th {
  background: #f8f9fa;
  font-weight: 600;
}

.actions {
  display: flex;
  gap: 8px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-edit {
  background: #17a2b8;
  color: white;
}

.btn-delete {
  background: #dc3545;
  color: white;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-danger {
  background: #dc3545;

  modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }

  .modal-content {
    background: white;
    border-radius: 8px;
    width: 100%;
    max-width: 500px;
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    border-bottom: 1px solid #eee;
  }

  .modal-body {
    padding: 16px;
  }

  .modal-footer {
    padding: 16px;
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    border-top: 1px solid #eee;
  }

  .form-group {
    margin-bottom: 16px;
    padding: 0 16px;
  }

  .form-group label {
    display: block;
    margin-bottom: 8px;
  }

  .form-group input {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }

  .btn-close {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
  }
}

</style>