<template>
  <div class="report-container">
    <div class="report-header">
      <h2>Raport Frekwencji</h2>
      <div class="filters">
        <select v-model="selectedPeriod" class="filter-select">
          <option value="">Wybierz okres czasowy</option>
          <option value="week">Ostatni tydzień</option>
          <option value="month">Ostatni miesiąc</option>
          <option value="quarter">Ostatni kwartał</option>
        </select>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <h3>Średnia Frekwencja</h3>
        <div class="stat-value">{{ averageAttendance }}%</div>
        <div class="stat-label">wszystkich zajęć</div>
      </div>

      <div class="stat-card">
        <h3>Liczba Zajęć</h3>
        <div class="stat-value">{{ totalClasses }}</div>
        <div class="stat-label">w wybranym okresie</div>
      </div>

      <div class="stat-card">
        <h3>Aktywni Uczniowie</h3>
        <div class="stat-value">{{ activeStudents }}</div>
        <div class="stat-label">uczęszczających na zajęcia</div>
      </div>
    </div>

    <div class="chart-container">
      <h3>Frekwencja według zajęć</h3>
      <canvas ref="chart"></canvas>
    </div>

    <div class="attendance-table">
      <h3>Szczegółowe dane</h3>
      <table>
        <thead>
        <tr>
          <th>Nazwa zajęć</th>
          <th>Instruktor</th>
          <th>Data</th>
          <th>Frekwencja</th>
          <th>Zapisanych</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="item in attendanceData" :key="item.date">
          <td>{{ item.class_name }}</td>
          <td>{{ item.instructor_name }}</td>
          <td>{{ formatDate(item.date) }}</td>
          <td>{{ Math.round(item.attendance_rate) }}%</td>
          <td>{{ item.booked_slots }}/{{ item.max_slots }}</td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import {ref, computed, watch} from 'vue';
import axios from 'axios';
import Chart from 'chart.js/auto';

export default {
  name: 'AttendanceReport',
  setup() {
    const selectedPeriod = ref('');
    const attendanceData = ref([]);
    const chart = ref(null);
    const chartInstance = ref(null);

    const averageAttendance = computed(() => {
      if (!attendanceData.value.length) return 0;
      const sum = attendanceData.value.reduce((acc, curr) => acc + curr.attendance_rate, 0);
      return Math.round(sum / attendanceData.value.length);
    });

    const totalClasses = computed(() => attendanceData.value.length);

    const activeStudents = computed(() => {
      if (!attendanceData.value.length) return 0;
      const totalBookings = attendanceData.value.reduce((acc, curr) => acc + curr.booked_slots, 0);
      return Math.round(totalBookings / attendanceData.value.length);
    });

    const fetchAttendanceData = async () => {
      if (!selectedPeriod.value) return;
      try {
        const response = await axios.get(
            `http://localhost:8000/api/reports/attendance/${selectedPeriod.value}`,
            {
              headers: {Authorization: `Bearer ${localStorage.getItem('access')}`}
            }
        );
        attendanceData.value = response.data;
        updateChart();
      } catch (error) {
        console.error('Error fetching attendance data:', error);
      }
    };

    const updateChart = () => {
      if (chartInstance.value) {
        chartInstance.value.destroy();
      }

      const canvas = chart.value;
      if (!canvas) return;

      const ctx = canvas.getContext('2d');
      chartInstance.value = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: attendanceData.value.map(item => item.class_name),
          datasets: [{
            label: 'Frekwencja (%)',
            data: attendanceData.value.map(item => Math.round(item.attendance_rate)),
            backgroundColor: '#443ea2',
            borderColor: '#443ea2',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              max: 100
            }
          }
        }
      });
    };

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('pl-PL', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    };

    watch(selectedPeriod, () => {
      fetchAttendanceData();
    });

    return {
      selectedPeriod,
      attendanceData,
      averageAttendance,
      totalClasses,
      activeStudents,
      chart,
      formatDate
    };
  }
};
</script>

<style scoped>
.report-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.filters {
  display: flex;
  align-items: center;
}

.filter-select {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  text-align: center;
}

.stat-card h3 {
  margin-bottom: 1rem;
  font-size: 1.2rem;
  color: #443ea2;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #443ea2;
}

.stat-label {
  font-size: 1rem;
  color: #666;
}

.chart-container {
  margin-bottom: 2rem;
}

.attendance-table {
  margin-top: 2rem;
}

.attendance-table table {
  width: 100%;
  border-collapse: collapse;
}

.attendance-table th, .attendance-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #ccc;
}

.attendance-table th {
  background: #f5f5f5;
  font-weight: bold;
}

.attendance-table tr:nth-child(even) {
  background: #f9f9f9;
}

.popular-classes {
  display: flex;
  flex-direction: column;
}

.popular-class {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
}

.class-name {
  font-weight: bold;
}

.class-bookings {
  color: #666;
}

.trends-container {
  margin-top: 2rem;
}
</style>