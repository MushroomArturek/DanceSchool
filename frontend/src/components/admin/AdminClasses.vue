<template>
  <div class="admin-classes">
    <div class="header">
      <h2>Zarządzanie Zajęciami</h2>
      <button class="btn btn-primary" @click="openAddModal">
        <i class="fas fa-plus"></i> Dodaj Zajęcia
      </button>
    </div>

    <div v-if="classes.length === 0" class="no-data">
      Brak zajęć w bazie danych
    </div>

    <table v-else class="classes-table">
      <thead>
        <tr>
          <th>Nazwa</th>
          <th>Styl</th>
          <th>Instruktor</th>
          <th>Termin</th>
          <th>Sala</th>
          <th>Miejsca</th>
          <th>Akcje</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="classItem in classes" :key="classItem.id">
          <td>{{ classItem.name }}</td>
          <td>{{ classItem.style }}</td>
          <td>{{ classItem.instructor }}</td>
          <td>
            {{ formatDateTime(classItem.start_time) }} -
            {{ formatTime(classItem.end_time) }}
          </td>
          <td>{{ classItem.room || 'Brak' }}</td>
          <td>{{ classItem.available_slots }}/{{ classItem.max_participants }}</td>
          <td class="actions">
            <button class="btn btn-edit" @click="openEditModal(classItem)">
              <i class="fas fa-edit"></i>
            </button>
            <button class="btn btn-delete" @click="openDeleteModal(classItem)">
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
            <label>Nazwa zajęć:</label>
            <input type="text" v-model="formData.name" required>
          </div>
          <div class="form-group">
            <label>Styl tańca:</label>
            <input type="text" v-model="formData.style" required>
          </div>
          <div class="form-group">
            <label>Instruktor:</label>
            <select v-model="formData.instructor" required>
              <option v-for="instructor in instructors"
                      :key="instructor.id"
                      :value="instructor.id">
                {{ instructor.first_name }} {{ instructor.last_name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Data rozpoczęcia:</label>
            <input type="datetime-local" v-model="formData.start_time" required>
          </div>
          <div class="form-group">
            <label>Data zakończenia:</label>
            <input type="datetime-local" v-model="formData.end_time" required>
          </div>
          <div class="form-group">
            <label>Sala:</label>
            <input type="text" v-model="formData.room">
          </div>
          <div class="form-group">
            <label>Maksymalna liczba uczestników:</label>
            <input type="number" v-model="formData.max_participants" required min="1">
          </div>
          <div class="form-group">
            <label>Zajęcia cykliczne:</label>
            <input type="checkbox" v-model="formData.is_recurring">
          </div>
          <div class="form-group" v-if="formData.is_recurring">
            <label>Dni tygodnia:</label>
            <div class="checkbox-group">
              <label v-for="day in weekDays" :key="day.value">
                <input type="checkbox"
                       v-model="selectedDays"
                       :value="day.value">
                {{ day.label }}
              </label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">
              Anuluj
            </button>
            <button type="submit"
                    class="btn btn-primary"
                    :disabled="!isFormValid || isSubmitting">
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
          <p>Czy na pewno chcesz usunąć zajęcia "{{ selectedClass?.name }}"?</p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="closeDeleteModal">
            Anuluj
          </button>
          <button class="btn btn-danger"
                  @click="deleteClass"
                  :disabled="isDeleting">
            {{ isDeleting ? 'Usuwanie...' : 'Usuń' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue';
import axios from 'axios';

export default {
  name: 'AdminClasses',
  setup() {
    const classes = ref([]);
    const instructors = ref([]);
    const isModalOpen = ref(false);
    const isDeleteModalOpen = ref(false);
    const selectedClass = ref(null);
    const isSubmitting = ref(false);
    const isDeleting = ref(false);
    const isEditing = ref(false);
    const selectedDays = ref([]);

    const weekDays = [
      { value: 'MO', label: 'Poniedziałek' },
      { value: 'TU', label: 'Wtorek' },
      { value: 'WE', label: 'Środa' },
      { value: 'TH', label: 'Czwartek' },
      { value: 'FR', label: 'Piątek' },
      { value: 'SA', label: 'Sobota' },
      { value: 'SU', label: 'Niedziela' }
    ];

    const formData = reactive({
      name: '',
      style: '',
      instructor: null,
      max_participants: 1,
      start_time: '',
      end_time: '',
      room: '',
      is_recurring: false,
      days_of_week: ''
    });

    const modalTitle = computed(() =>
      isEditing.value ? 'Edytuj Zajęcia' : 'Dodaj Zajęcia'
    );

    const isFormValid = computed(() =>
      formData.name &&
      formData.style &&
      formData.instructor &&
      formData.start_time &&
      formData.end_time &&
      formData.max_participants > 0
    );

    const fetchClasses = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/classes/', {
          headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
        });
        classes.value = response.data;
      } catch (error) {
        console.error('Błąd podczas pobierania zajęć:', error);
        alert('Nie udało się pobrać listy zajęć');
      }
    };

    const fetchInstructors = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/instructors/', {
          headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
        });
        instructors.value = response.data;
      } catch (error) {
        console.error('Błąd podczas pobierania instruktorów:', error);
      }
    };

    const resetForm = () => {
      Object.keys(formData).forEach(key => formData[key] = '');
      formData.max_participants = 1;
      formData.is_recurring = false;
      selectedDays.value = [];
      isEditing.value = false;
      selectedClass.value = null;
    };

    const openAddModal = () => {
      resetForm();
      isModalOpen.value = true;
    };

    const openEditModal = (classItem) => {
      isEditing.value = true;
      selectedClass.value = classItem;
      Object.assign(formData, classItem);
      if (classItem.days_of_week) {
        selectedDays.value = classItem.days_of_week.split(',');
      }
      isModalOpen.value = true;
    };

    const openDeleteModal = (classItem) => {
      selectedClass.value = classItem;
      isDeleteModalOpen.value = true;
    };

    const closeModal = () => {
      isModalOpen.value = false;
      resetForm();
    };

    const closeDeleteModal = () => {
      isDeleteModalOpen.value = false;
      selectedClass.value = null;
    };

    const submitForm = async () => {
      if (!isFormValid.value) return;

      isSubmitting.value = true;
      const submitData = { ...formData };
      if (formData.is_recurring) {
        submitData.days_of_week = selectedDays.value.join(',');
      }

      const url = isEditing.value
        ? `http://localhost:8000/api/classes/${selectedClass.value.id}/update/`
        : 'http://localhost:8000/api/classes/create/';

      try {
        const method = isEditing.value ? 'put' : 'post';
        await axios[method](url, submitData, {
          headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
        });
        await fetchClasses();
        closeModal();
      } catch (error) {
        console.error('Błąd podczas zapisywania:', error);
        alert('Nie udało się zapisać zajęć');
      } finally {
        isSubmitting.value = false;
      }
    };

    const deleteClass = async () => {
      if (!selectedClass.value) return;

      isDeleting.value = true;
      try {
        await axios.delete(
          `http://localhost:8000/api/classes/${selectedClass.value.id}/delete/`,
          {
            headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
          }
        );
        await fetchClasses();
        closeDeleteModal();
      } catch (error) {
        console.error('Błąd podczas usuwania:', error);
        alert('Nie udało się usunąć zajęć');
      } finally {
        isDeleting.value = false;
      }
    };

    const formatDateTime = (datetime) => {
      if (!datetime) return '';
      return new Date(datetime).toLocaleString('pl-PL', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    };

    const formatTime = (datetime) => {
      if (!datetime) return '';
      return new Date(datetime).toLocaleString('pl-PL', {
        hour: '2-digit',
        minute: '2-digit'
      });
    };

    onMounted(() => {
      fetchClasses();
      fetchInstructors();
    });

    return {
      classes,
      instructors,
      formData,
      isModalOpen,
      isDeleteModalOpen,
      selectedClass,
      isSubmitting,
      isDeleting,
      isFormValid,
      modalTitle,
      weekDays,
      selectedDays,
      openAddModal,
      openEditModal,
      openDeleteModal,
      closeModal,
      closeDeleteModal,
      submitForm,
      deleteClass,
      formatDateTime,
      formatTime
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
.checkbox-group {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 8px;
  margin-top: 8px;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 4px;
}

select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
}


</style>