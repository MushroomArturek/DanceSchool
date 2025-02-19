<template>
  <div class="payment-section">
    <div class="pricing-header">
      <h1>Płatności</h1>
    </div>

    <div class="pricing-grid">
      <div v-for="plan in subscriptionPlans"
           :key="plan.type"
           :class="['pricing-card', { 'selected': selectedPlan?.type === plan.type }]"
      >
        <div class="pricing-card-header">
          <h2>{{ plan.name }}</h2>
          <div class="price">{{ plan.price }} zł</div>
        </div>
        <div class="pricing-card-body">
          <ul>
            <li v-for="feature in plan.features" :key="feature">
              <i class="fas fa-check"></i>
              {{ feature }}
            </li>
          </ul>
        </div>
        <div class="pricing-card-footer">
          <button @click="createPayment(plan)" class="cta-button">
            Wybierz plan
          </button>
        </div>
      </div>
    </div>

    <!--    <div v-if="showPaymentMethodModal" class="payment-modal">-->
    <!--    <div class="modal-content">-->
    <!--      <h3>Wybierz metodę płatności</h3>-->
    <!--      <div class="payment-methods">-->
    <!--        <button-->
    <!--          v-for="method in paymentMethods"-->
    <!--          :key="method.value"-->
    <!--          @click="selectPaymentMethod(method.value)"-->
    <!--          class="payment-method-button"-->
    <!--        >-->
    <!--          <i :class="getPaymentIcon(method.value)"></i>-->
    <!--          {{ method.label }}-->
    <!--        </button>-->
    <!--      </div>-->
    <!--      <div class="modal-footer">-->
    <!--        <button @click="showPaymentMethodModal = false" class="cancel-button">Anuluj</button>-->
    <!--      </div>-->
    <!--    </div>-->
    <!--  </div>-->
    <Transition name="fade">
      <div v-if="showPaymentMethodModal" class="payment-modal">
        <div class="modal-content">
          <h3>Wybierz metodę płatności</h3>
          <div class="payment-methods">
            <button
                v-for="method in paymentMethods"
                :key="method.value"
                @click="selectPaymentMethod(method.value)"
                :class="['payment-method-button', { 'selected': selectedMethod === method.value }]"
            >
              <i :class="getPaymentIcon(method.value)"></i>
              {{ method.label }}
            </button>
          </div>
          <div class="modal-footer">
            <button @click="closePaymentModal" class="cancel-button">Anuluj</button>
            <button
                @click="createNewPayment"
                class="purchase-button"
                :disabled="!selectedMethod"
            >
              Zakup plan
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <div class="payment-history">
      <h3>Historia płatności</h3>
      <table class="payment-table">
        <thead>
        <tr>
          <th>Data</th>
          <th>Typ</th>
          <th>Kwota</th>
          <th>Status</th>
          <th>Metoda płatności</th>
          <th>Akcje</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="payment in filteredPayments" :key="payment.id">
          <td>{{ formatDate(payment.created_at) }}</td>
          <td>{{ payment.payment_type ? translatePaymentType(payment.payment_type) : '-' }}</td>
          <td>{{ payment.amount ? `${payment.amount} zł` : '-' }}</td>
          <td>
        <span :class="['status', payment.status]">
          {{ translateStatus(payment.status) }}
        </span>
          </td>
          <td>{{ payment.payment_method ? translatePaymentMethod(payment.payment_method) : '-' }}</td>
          <td class="actions">
            <!-- ... existing action buttons ... -->
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import {ref, computed, onMounted} from 'vue';
import axios from 'axios';

const payments = ref([]);
const studentId = ref(null);
const statusFilter = ref('');
const showPaymentMethodModal = ref(false);
const selectedMethod = ref(null);
const selectedPlan = ref(null);
const API_URL = 'http://localhost:8000';
axios.defaults.baseURL = API_URL;

const subscriptionPlans = [
  {
    type: 'single',
    name: 'Wejście jednorazowe',
    price: 45,
    features: [
      'Jednorazowy wstęp',
      'Wszystkie style tańca',
      'Ważność 1 dzień',
      'Możliwość odrabiania'
    ]
  },
  {
    type: 'monthly',
    name: 'Karnet miesięczny',
    price: 249,
    featured: true,
    features: [
      '8 wejść w miesiącu',
      'Wszystkie style tańca',
      'Ważność 30 dni',
      'Możliwość odrabiania zajęć',
      '1 warsztat w miesiącu gratis'
    ]
  },
  {
    type: 'quarterly',
    name: 'Karnet kwartalny',
    price: 649,
    features: [
      'Nielimitowane wejścia',
      'Wszystkie style tańca',
      'Ważność 90 dni',
      'Pierwszeństwo zapisów',
      '2 warsztaty gratis'
    ]
  },
  {
    type: 'yearly',
    name: 'Karnet roczny',
    price: 2499,
    features: [
      'Nielimitowane wejścia',
      'Wszystkie style tańca',
      'Ważność 365 dni',
      'Pierwszeństwo zapisów',
      '4 warsztaty gratis',
      '2 lekcje indywidualne'
    ]
  }
];

const paymentMethods = [
  {value: 'cash', label: 'Gotówka'},
  {value: 'transfer', label: 'Przelew bankowy'},
  {value: 'blik', label: 'BLIK'},
  {value: 'card', label: 'Karta płatnicza w studio'}
];

const filteredPayments = computed(() => {
  if (!statusFilter.value) return payments.value;
  return payments.value.filter(payment => payment.status === statusFilter.value);
});

const fetchStudentProfile = async () => {
  try {
    const response = await axios.get('/api/student/profile/', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access')}`
      }
    });
    studentId.value = response.data.id;
  } catch (error) {
    console.error('Error fetching student profile:', error);
  }
};

const fetchPayments = async () => {
  try {
    const response = await axios.get('/api/payments/', {
      headers: {Authorization: `Bearer ${localStorage.getItem('access')}`}
    });
    // Ensure payments.value is always an array
    payments.value = Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error('Error fetching payments:', error);
    payments.value = []; // Set empty array on error
  }
};


const createPayment = (plan) => {
  selectedPlan.value = plan;
  showPaymentMethodModal.value = true;
};

const updatePayment = async (id, status) => {
  try {
    await axios.patch(`/api/payments/${id}/update/`, {
      status: status
    }, {
      headers: {Authorization: `Bearer ${localStorage.getItem('access')}`}
    });
    await fetchPayments();
  } catch (error) {
    console.error('Error updating payment:', error);
  }
};

const selectPaymentMethod = (method) => {
  selectedMethod.value = method;
};

const createNewPayment = async () => {
  if (!studentId.value || !selectedPlan.value || !selectedMethod.value) return;

  try {
    await axios.post('/api/payments/create/', {
      payment_type: selectedPlan.value.type,
      amount: selectedPlan.value.price,
      student: studentId.value,
      payment_method: selectedMethod.value
    }, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access')}`,
        'Content-Type': 'application/json'
      }
    });
    await fetchPayments();
    showPaymentMethodModal.value = false;
    selectedMethod.value = null;
  } catch (error) {
    console.error('Error creating payment:', error);
  }
};

const closePaymentModal = () => {
  showPaymentMethodModal.value = false;
  selectedMethod.value = null;
  setTimeout(() => {
    selectedPlan.value = null;
  }, 300);
};

const translatePaymentMethod = (method) => {
  const methods = {
    'cash': 'Gotówka',
    'transfer': 'Przelew bankowy',
    'blik': 'BLIK',
    'card': 'Karta płatnicza w studio'
  };
  return methods[method] || method;
};

const getPaymentIcon = (method) => {
  const icons = {
    'cash': 'fas fa-money-bill-wave',
    'transfer': 'fas fa-university',
    'blik': 'fas fa-mobile-alt',
    'card': 'fas fa-credit-card'
  };
  return icons[method] || 'fas fa-money-bill';
};

const deletePayment = async (id) => {
  if (!confirm('Czy na pewno chcesz usunąć tę płatność?')) return;

  try {
    await axios.delete(`/api/payments/${id}/delete/`, {
      headers: {Authorization: `Bearer ${localStorage.getItem('access')}`}
    });
    await fetchPayments();
  } catch (error) {
    console.error('Error deleting payment:', error);
  }
};

const formatDate = (date) => {
  if (!date) return '-';
  try {
    return new Date(date).toLocaleDateString('pl-PL');
  } catch (error) {
    return '-';
  }
};

const translatePaymentType = (type) => {
  const types = {
    'single': 'Pojedyncze zajęcia',
    'monthly': 'Karnet miesięczny',
    'quarterly': 'Karnet kwartalny',
    'yearly': 'Karnet roczny'
  };
  return types[type] || type;
};

const translateStatus = (status) => {
  const statuses = {
    'pending': 'Oczekująca',
    'completed': 'Zrealizowana',
    'failed': 'Nieudana',
    'refunded': 'Zwrócona'
  };
  return statuses[status] || status;
};

onMounted(async () => {
  await fetchStudentProfile();
  await fetchPayments();
});
</script>

<style scoped>
.payment-section {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.pricing-header {
  text-align: center;
  margin-bottom: 3rem;
}

.pricing-header h1 {
  color: #443ea2;
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.pricing-header p {
  color: #666;
  font-size: 1.2rem;
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* Changes from auto-fit to fixed 4 columns */
  gap: 2rem;
  margin-bottom: 3rem;
}

.pricing-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  border: 2px solid transparent;
  transition: transform 0.3s ease, border-color 0.3s ease;
  position: relative;
  display: flex; /* Add flex display */
  flex-direction: column; /* Stack children vertically */
  height: 100%; /* Full height */
}

.pricing-card:hover {
  transform: translateY(-5px);
}

.pricing-card.selected {
  border-color: #443ea2;
  box-shadow: 0 0 15px rgba(68, 62, 162, 0.3);
}

.pricing-card-header {
  background: #f8f9fa;
  padding: 2rem;
  text-align: center;
}

.pricing-card-header h2 {
  color: #443ea2;
  margin-bottom: 1rem;
}

.price {
  font-size: 2.5rem;
  color: #333;
  font-weight: bold;
}

.pricing-card-body {
  padding: 2rem;
  flex-grow: 1; /* Allow body to grow and push footer down */
  display: flex; /* Make body a flex container */
  flex-direction: column; /* Stack content vertically */
}

.pricing-card-body ul {
  list-style: none;
  padding: 0;
  margin: 0;
  flex-grow: 1; /* Allow list to grow and push footer down */
}

.pricing-card-body li {
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
}

.pricing-card-body li i {
  color: #28a745;
  margin-right: 0.5rem;
}

.pricing-card-footer {
  padding: 2rem;
  text-align: center;
  margin-top: auto; /* Push footer to bottom */
}

.cta-button {
  display: inline-block;
  padding: 1rem 2rem;
  background: #443ea2;
  color: white;
  text-decoration: none;
  border: none;
  border-radius: 30px;
  transition: background 0.3s ease;
  cursor: pointer;
}

.cta-button:hover {
  background: #372f8b;
}

.payment-history {
  margin-top: 4rem;
}

.payment-table {
  width: 100%;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

@media (max-width: 1200px) {
  .pricing-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .pricing-grid {
    grid-template-columns: 1fr;
  }
}

.payment-modal {
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  width: 90%;
  max-width: 800px;
  margin: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

/* Fade animation */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Payment methods grid */
.payment-methods {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin: 2rem 0;
}

.payment-method-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1.1rem;
}

.payment-method-button:hover {
  background: #e9ecef;
  transform: translateY(-2px);
}

.payment-method-button i {
  font-size: 1.5rem;
  color: #443ea2;
}

.payment-method-button.selected {
  border: 2px solid #443ea2;
  box-shadow: 0 0 10px rgba(68, 62, 162, 0.2);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.purchase-button {
  padding: 0.8rem 2rem;
  background: #443ea2;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.purchase-button:hover:not(:disabled) {
  background: #372f8b;
}

.purchase-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.cancel-button {
  padding: 0.8rem 2rem;
  background: #6c757d;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease;
  font-size: 1rem;
}

.cancel-button:hover {
  background: #5a6268;
}
</style>