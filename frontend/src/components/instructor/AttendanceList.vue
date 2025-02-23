<template>
  <div class="attendance-container">
    <h2>Lista obecności</h2>
    <div class="class-selector" v-if="!classId">
      <select v-model="selectedClass" @change="loadAttendance">
        <option value="">Wybierz zajęcia</option>
        <option v-for="class_ in classes" :key="class_.id" :value="class_.id">
          {{ class_.name }} - {{ formatDateTime(class_.start_time) }}
        </option>
      </select>
    </div>

    <div v-if="selectedClass || classId" class="attendance-list">
      <div class="attendance-header">
        <h3>{{ currentClass?.name }}</h3>
        <p>{{ formatDateTime(currentClass?.start_time) }}</p>
      </div>

      <table class="attendance-table">
        <thead>
          <tr>
            <th>Student</th>
            <th>Status</th>
            <th>Rezerwacja</th>
            <th>Akcje</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in attendanceRecords" :key="record.id">
            <td>{{ record.student_name }}</td>
            <td>
              <span :class="['status-badge', record.status]">
                {{ translateStatus(record.status) }}
              </span>
            </td>
            <td>
              <span :class="['booking-badge', record.booking_status]">
                {{ translateBookingStatus(record.booking_status) }}
              </span>
            </td>
            <td>
              <div class="action-buttons">
                <button
                  @click="updateStatus(record.student, 'present')"
                  :class="['btn', record.status === 'present' ? 'active' : '']"
                >
                  <i class="fas fa-check"></i>
                </button>
                <button
                  @click="updateStatus(record.student, 'absent')"
                  :class="['btn', record.status === 'absent' ? 'active' : '']"
                >
                  <i class="fas fa-times"></i>
                </button>
                <button
                  @click="updateStatus(record.student, 'late')"
                  :class="['btn', record.status === 'late' ? 'active' : '']"
                >
                  <i class="fas fa-clock"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const classId = ref(route.params.classId);
const selectedClass = ref(classId.value || '');
const classes = ref([]);
const currentClass = ref(null);
const attendanceRecords = ref([]);
const API_URL = 'http://localhost:8000';
axios.defaults.baseURL = API_URL;

const loadClasses = async () => {
  try {
    const response = await axios.get('/api/classes/', {
      headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
    });
    classes.value = response.data;
    if (classId.value) {
      currentClass.value = response.data.find(c => c.id === parseInt(classId.value));
    }
  } catch (error) {
    console.error('Error loading classes:', error);
  }
};

const loadAttendance = async () => {
  const id = classId.value || selectedClass.value;
  if (!id) return;

  try {
    const response = await axios.get(`/api/classes/${id}/attendance/`, {
      headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
    });
    attendanceRecords.value = response.data;

    if (!classId.value) {
      currentClass.value = classes.value.find(c => c.id === parseInt(selectedClass.value));
    }
  } catch (error) {
    console.error('Error loading attendance:', error);
  }
};

const updateStatus = async (studentId, status) => {
  const id = classId.value || selectedClass.value;
  try {
    const response = await axios.patch(
      `/api/classes/${id}/attendance/${studentId}/`,
      { status },
      { headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }}
    );

    // Update local state
    const index = attendanceRecords.value.findIndex(record => record.student === studentId);
    if (index !== -1) {
      attendanceRecords.value[index] = response.data;
    }
  } catch (error) {
    console.error('Error updating attendance:', error);
  }
};

const formatDateTime = (datetime) => {
  if (!datetime) return '';
  return new Date(datetime).toLocaleString('pl-PL', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const translateStatus = (status) => {
  const statuses = {
    'present': 'Obecny',
    'absent': 'Nieobecny',
    'late': 'Spóźniony'
  };
  return statuses[status] || status;
};

const translateBookingStatus = (status) => {
  const statuses = {
    'confirmed': 'Potwierdzona',
    'cancelled': 'Anulowana',
    'waiting': 'Oczekująca',
    null: 'Brak'
  };
  return statuses[status] || status;
};

watch(selectedClass, () => {
  if (selectedClass.value) {
    loadAttendance();
  }
});

onMounted(() => {
  loadClasses();
  if (classId.value || selectedClass.value) {
    loadAttendance();
  }
});
</script>

<style scoped>
.attendance-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.class-selector {
  margin-bottom: 2rem;
}

.class-selector select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}

.attendance-header {
  margin-bottom: 2rem;
}

.attendance-header h3 {
  margin: 0;
  color: #443ea2;
}

.attendance-header p {
  margin: 0.5rem 0 0;
  color: #666;
}

.attendance-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

.attendance-table th,
.attendance-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.attendance-table th {
  background: #f8f9fa;
  font-weight: 600;
  color: #443ea2;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.status-badge.present {
  background: #d4edda;
  color: #155724;
}

.status-badge.absent {
  background: #f8d7da;
  color: #721c24;
}

.status-badge.late {
  background: #fff3cd;
  color: #856404;
}

.booking-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.booking-badge.confirmed {
  background: #d4edda;
  color: #155724;
}

.booking-badge.cancelled {
  background: #f8d7da;
  color: #721c24;
}

.booking-badge.waiting {
  background: #fff3cd;
  color: #856404;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.btn {
  padding: 0.5rem;
  border: none;
  border-radius: 4px;
  background: #eee;
  cursor: pointer;
  transition: all 0.2s;
}

.btn:hover {
  background: #ddd;
}

.btn.active {
  background: #443ea2;
  color: white;
}

.btn i {
  font-size: 1rem;
}
</style>