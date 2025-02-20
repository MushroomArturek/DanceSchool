<template>
 <div class="attendance-panel">
    <h2>Lista obecności</h2>

    <!-- Class selector -->
    <div class="class-selector">
      <select v-model="selectedClass">
        <option value="">Wybierz zajęcia</option>
        <option
          v-for="classItem in instructorClasses"
          :key="classItem.id"
          :value="classItem.id"
        >
          {{ classItem.name }} - {{ formatDateTime(classItem.start_time) }}
        </option>
      </select>
    </div>

    <!-- Attendance list -->
    <div v-if="selectedClass" class="attendance-list">
      <div class="attendance-header">
        <h3>Lista obecności</h3>
        <button @click="showAddStudentModal" class="add-student-btn">
          Dodaj studenta
        </button>
      </div>

      <table class="attendance-table">
        <thead>
          <tr>
            <th>Student</th>
            <th>Status rezerwacji</th>
            <th>Obecność</th>
            <th>Notatki</th>
            <th>Akcje</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in attendanceRecords" :key="record.id">
            <td>{{ record.student_name }}</td>
            <td>
              <span :class="['booking-status', record.booking_status]">
                {{ translateBookingStatus(record.booking_status) }}
              </span>
            </td>
            <td>
              <select v-model="record.status">
                <option value="present">Obecny</option>
                <option value="absent">Nieobecny</option>
                <option value="late">Spóźniony</option>
              </select>
            </td>
            <td>
              <input type="text" v-model="record.notes" placeholder="Notatki">
            </td>
            <td>
              <button @click="updateAttendance(record)" class="save-btn">
                Zapisz
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add student modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h3>Dodaj studenta do listy</h3>
        <select v-model="newStudentId">
          <option value="">Wybierz studenta</option>
          <option v-for="student in availableStudents"
                  :key="student.id"
                  :value="student.id">
            {{ student.first_name }} {{ student.last_name }}
          </option>
        </select>
        <div class="modal-actions">
          <button @click="addStudent" class="add-btn">Dodaj</button>
          <button @click="showModal = false" class="cancel-btn">Anuluj</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted} from 'vue'
import API from '../../axios.js'

const selectedClass = ref(null)
const instructorClasses = ref([])
const attendanceRecords = ref([])
const showModal = ref(false)
const availableStudents = ref([])
const newStudentId = ref('')

const fetchInstructorClasses = async () => {
  const response = await API.get('/classes/', {
    headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
  })
  instructorClasses.value = response.data
}

const fetchAttendance = async () => {
  if (!selectedClass.value) return
  const response = await API.get(`/classes/${selectedClass.value}/attendance/`, {
    headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
  })
  attendanceRecords.value = response.data
}

const updateAttendanceStatus = async (studentId, status) => {
  await API.put(`/classes/${selectedClass.value}/attendance/${studentId}/`,
    { status },
    { headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }}
  )
}

const addStudentToClass = async () => {
  await API.post(`/classes/${selectedClass.value}/attendance/`,
    { student: newStudentId.value },
    { headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }}
  )
  await fetchAttendance()
  showModal.value = false
}

const showAddStudentModal = async () => {
  const response = await API.get('/students/', {
    headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
  })
  availableStudents.value = response.data
  showModal.value = true
}

onMounted(() => {
  fetchInstructorClasses()
})
</script>

<style scoped>
.attendance-panel {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

h2 {
  color: #443ea2;
  margin-bottom: 2rem;
}

.class-selector {
  margin-bottom: 2rem;
}

.class-selector select {
  width: 100%;
  padding: 0.8rem;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: white;
}

.attendance-list {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.attendance-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.add-student-btn {
  padding: 0.8rem 1.5rem;
  background: #443ea2;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.add-student-btn:hover {
  background: #372f8b;
}

.attendance-table {
  width: 100%;
  border-collapse: collapse;
}

.attendance-table th,
.attendance-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.attendance-table th {
  font-weight: 600;
  color: #443ea2;
  background: #f8f9fa;
}

.attendance-table select,
.attendance-table input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.save-btn {
  padding: 0.5rem 1rem;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.save-btn:hover {
  background: #218838;
}

.booking-status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.9rem;
}

.booking-status.confirmed {
  background: #d4edda;
  color: #155724;
}

.booking-status.cancelled {
  background: #f8d7da;
  color: #721c24;
}

.booking-status.waiting {
  background: #fff3cd;
  color: #856404;
}

.attendance-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
}

.modal-content select {
  width: 100%;
  padding: 0.8rem;
  margin: 1rem 0;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.add-btn {
  padding: 0.8rem 1.5rem;
  background: #443ea2;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.add-btn:hover {
  background: #372f8b;
}

.cancel-btn {
  padding: 0.8rem 1.5rem;
  background: #6c757d;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.cancel-btn:hover {
  background: #5a6268;
}

/* Responsive styles */
@media (max-width: 768px) {
  .attendance-panel {
    padding: 1rem;
  }

  .attendance-table {
    display: block;
    overflow-x: auto;
  }

  .modal-content {
    width: 95%;
    margin: 0 1rem;
  }
}
</style>