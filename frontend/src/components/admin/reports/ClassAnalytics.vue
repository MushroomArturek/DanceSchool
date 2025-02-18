<template>
  <div class="report-container">
    <div class="report-header">
      <h2>Analityka Zajęć</h2>
      <div class="filters">
        <select v-model="selectedPeriod" class="filter-select">
          <option value="">Wybierz okres czasowy</option>
          <option value="month">Ostatni miesiąc</option>
          <option value="quarter">Ostatni kwartał</option>
          <option value="year">Ostatni rok</option>
        </select>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <h3>Najpopularniejsze zajęcia</h3>
        <div class="popular-classes">
          <div v-for="cls in popularClasses" :key="cls.name" class="popular-class">
            <span class="class-name">{{ cls.name }}</span>
            <span class="class-bookings">{{ cls.booking_count }} zapisów</span>
          </div>
        </div>
      </div>

      <div class="stat-card">
        <h3>Godziny szczytu</h3>
        <canvas ref="peakHoursChart"></canvas>
      </div>

      <div class="stat-card">
        <h3>Style tańca</h3>
        <canvas ref="stylesChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import {ref, watch} from 'vue';
import axios from 'axios';
import Chart from 'chart.js/auto';

export default {
  name: 'ClassAnalytics',
  setup() {
    const selectedPeriod = ref('');
    const popularClasses = ref([]);
    const peakHoursChart = ref(null);
    const stylesChart = ref(null);
    const chartInstances = ref({});

    const fetchAnalyticsData = async () => {
      if (!selectedPeriod.value) return;
      try {
        const response = await axios.get(
            `http://localhost:8000/api/reports/analytics/${selectedPeriod.value}/`,
            {
              headers: {Authorization: `Bearer ${localStorage.getItem('access')}`}
            }
        );
        popularClasses.value = response.data.popular_classes;
        updateCharts(response.data);
      } catch (error) {
        console.error('Error fetching analytics data:', error);
      }
    };

    const updateCharts = (data) => {
      // Destroy existing charts
      Object.values(chartInstances.value).forEach(chart => {
        if (chart) chart.destroy();
      });

      // Peak Hours Chart
      if (peakHoursChart.value) {
        const ctx = peakHoursChart.value.getContext('2d');
        chartInstances.value.peakHours = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: data.peak_hours.map(item => `${item.hour}:00`),
            datasets: [{
              label: 'Liczba zajęć',
              data: data.peak_hours.map(item => item.class_count),
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
                ticks: {
                  stepSize: 1
                }
              }
            }
          }
        });
      }

      // Styles Chart
      if (stylesChart.value) {
        const ctx = stylesChart.value.getContext('2d');
        chartInstances.value.styles = new Chart(ctx, {
          type: 'doughnut',
          data: {
            labels: data.style_distribution.map(item => item.style),
            datasets: [{
              data: data.style_distribution.map(item => item.count),
              backgroundColor: [
                '#443ea2',
                '#4c45b3',
                '#5854c7',
                '#6b68d8',
                '#7e7ce8'
              ]
            }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: 'right'
              }
            }
          }
        });
      }
    };


    watch(selectedPeriod, () => {
      fetchAnalyticsData();
    });

    return {
      selectedPeriod,
      popularClasses,
      peakHoursChart,
      stylesChart
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