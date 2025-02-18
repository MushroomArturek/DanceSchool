<template>
  <div class="reservations-container">
    <h2>Rezerwacje zajęć</h2>

    <!-- Tabs -->
    <div class="tabs">
      <button
          :class="['tab-btn', { active: activeTab === 'available' }]"
          @click="activeTab = 'available'"
      >
        Dostępne zajęcia
      </button>
      <button
          :class="['tab-btn', { active: activeTab === 'my' }]"
          @click="activeTab = 'my'"
      >
        Moje rezerwacje
      </button>
    </div>

    <!-- Available Classes -->
    <div v-if="activeTab === 'available'" class="classes-grid">
      <div v-for="classItem in availableClasses" :key="classItem.id" class="class-card">
        <div class="class-header">
          <h3>{{ classItem.name }}</h3>
          <span class="style-badge">{{ classItem.style }}</span>
        </div>
        <div class="class-details">
          <p><i class="fas fa-user"></i> Instruktor: {{ classItem.instructor }}</p>
          <p><i class="fas fa-clock"></i> {{ formatDateTime(classItem.start_time) }}</p>
          <p><i class="fas fa-map-marker-alt"></i> Sala: {{ classItem.room }}</p>
          <p><i class="fas fa-users"></i> Wolne miejsca: {{ classItem.available_slots || 0 }}</p>
        </div>
        <button
            @click="bookClass(classItem.id)"
            :disabled="!classItem.available_slots"
            class="book-btn"
        >
          {{ classItem.available_slots ? 'Zapisz się' : 'Brak miejsc' }}
        </button>
      </div>
    </div>

    <!-- My Reservations -->
    <div v-else class="reservations-grid">
      <div v-for="booking in myBookings" :key="booking.id" class="booking-card">
        <div class="booking-header">
          <h3>{{ booking.class_details.name }}</h3>
          <span :class="['status-badge', booking.status]">{{ translateStatus(booking.status) }}</span>
        </div>
        <div class="booking-details">
          <p><i class="fas fa-clock"></i> {{ formatDateTime(booking.class_details.start_time) }}</p>
          <p><i class="fas fa-user"></i> Instruktor: {{ booking.class_details.instructor }}</p>
          <p><i class="fas fa-map-marker-alt"></i> Sala: {{ booking.class_details.room }}</p>
          <p><i class="fas fa-bookmark"></i> Data rezerwacji: {{ formatDate(booking.booking_date) }}</p>
        </div>
        <button
            v-if="booking.status === 'confirmed'"
            @click="cancelBooking(booking.id)"
            class="cancel-btn"
        >
          Anuluj rezerwację
        </button>
      </div>
    </div>
  </div>
  <div v-if="notification.show" :class="['notification', notification.type]">
    {{ notification.message }}
  </div>
</template>

<script>
import {ref, onMounted} from 'vue';
import axios from 'axios';
import {authState} from '../state/authState';

export default {
  name: 'Reservations',
  setup() {
    const activeTab = ref('available');
    const availableClasses = ref([]);
    const myBookings = ref([]);
    const notification = ref({show: false, message: '', type: 'success'});

    // Add the missing translateStatus function
    const translateStatus = (status) => {
      const translations = {
        'confirmed': 'Potwierdzona',
        'cancelled': 'Anulowana',
        'waiting': 'Oczekująca'
      };
      return translations[status] || status;
    };

    const fetchAvailableClasses = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/classes/');
        availableClasses.value = response.data;
      } catch (error) {
        console.error('Error fetching classes:', error);
      }
    };

    const fetchMyBookings = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/bookings/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access')}`
          }
        });
        myBookings.value = response.data;
      } catch (error) {
        console.error('Error fetching bookings:', error);
      }
    };

    const showNotification = (message, type = 'success') => {
      notification.value = {show: true, message, type};
      setTimeout(() => {
        notification.value.show = false;
      }, 3000);
    };

    const bookClass = async (classId) => {
      try {
        await axios.post(
            'http://localhost:8000/api/bookings/create/',
            {class_model: classId},
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('access')}`
              }
            }
        );
        await fetchAvailableClasses();
        await fetchMyBookings();
        showNotification('Pomyślnie zapisano na zajęcia!');
      } catch (error) {
        console.error('Error booking class:', error);
        showNotification('Nie udało się zapisać na zajęcia.', 'error');
      }
    };

    // const bookClass = async (classId) => {
    //   try {
    //     await axios.post(
    //       'http://localhost:8000/api/bookings/create/',
    //       { class_model: classId },
    //       {
    //         headers: {
    //           Authorization: `Bearer ${localStorage.getItem('access')}`
    //         }
    //       }
    //     );
    //     await fetchAvailableClasses();
    //     await fetchMyBookings();
    //   } catch (error) {
    //     console.error('Error booking class:', error);
    //   }
    // };

    const cancelBooking = async (bookingId) => {
      try {
        await axios.delete(`http://localhost:8000/api/bookings/${bookingId}/delete/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access')}`
          }
        });
        await fetchMyBookings();
        await fetchAvailableClasses();
      } catch (error) {
        console.error('Error canceling booking:', error);
      }
    };

    const formatDateTime = (datetime) => {
      if (!datetime) return '';
      return new Date(datetime).toLocaleString('pl-PL', {
        weekday: 'long',
        hour: '2-digit',
        minute: '2-digit'
      });
    };

    const formatDate = (datetime) => {
      if (!datetime) return '';
      return new Date(datetime).toLocaleString('pl-PL', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    };

    onMounted(() => {
      fetchAvailableClasses();
      fetchMyBookings();
    });

    return {
      activeTab,
      availableClasses,
      myBookings,
      authState,
      bookClass,
      cancelBooking,
      formatDateTime,
      formatDate,
      translateStatus, // Add this to returned object
      notification
    };
  }
};
</script>

<style scoped>
.reservations-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.tabs {
  margin-bottom: 2rem;
  border-bottom: 2px solid #eee;
}

.tab-btn {
  padding: 1rem 2rem;
  font-size: 1rem;
  background: none;
  border: none;
  cursor: pointer;
  margin-right: 1rem;
  color: #666;
}

.tab-btn.active {
  color: #443ea2;
  border-bottom: 2px solid #443ea2;
  margin-bottom: -2px;
}

.classes-grid, .reservations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.class-card, .booking-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.class-header, .booking-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.style-badge, .status-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
}

.style-badge {
  background: #443ea2;
  color: white;
}

.status-badge {
  &.confirmed {
    background: #28a745;
    color: white;
  }

  &.cancelled {
    background: #dc3545;
    color: white;
  }

  &.waiting {
    background: #ffc107;
    color: black;
  }
}

.class-details, .booking-details {
  margin-bottom: 1rem;
}

.class-details p, .booking-details p {
  margin: 0.5rem 0;
  color: #666;
}

.book-btn, .cancel-btn {
  width: 100%;
  padding: 0.8rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s;
}

.book-btn {
  background: #443ea2;
  color: white;

  &:disabled {
    background: #ccc;
    cursor: not-allowed;
  }
}

.cancel-btn {
  background: #dc3545;
  color: white;
}

i {
  width: 20px;
  margin-right: 0.5rem;
}
</style>