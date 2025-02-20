<template>
  <div class="homepage">
    <header class="hero-section">
      <div class="hero-overlay">
        <h1>Szkoła Tańca <span>De la Salsa</span></h1>
        <p>Odkryj pasję do tańca i dołącz do naszej społeczności!</p>
        <router-link to="/schedule" class="cta-button">Zobacz grafik zajęć</router-link>
      </div>
    </header>

    <section class="about-us">
      <h2>Dlaczego warto wybrać naszą szkołę?</h2>
      <div class="features">
        <div class="feature">
          <i class="fas fa-star"></i>
          <h3>Doświadczeni instruktorzy</h3>
          <p>Nasi instruktorzy to profesjonaliści z wieloletnim doświadczeniem.</p>
        </div>
        <div class="feature">
          <i class="fas fa-users"></i>
          <h3>Przyjazna atmosfera</h3>
          <p>Tworzymy społeczność pasjonatów tańca.</p>
        </div>
        <div class="feature">
          <i class="fas fa-music"></i>
          <h3>Różnorodne style</h3>
          <p>Od salsy po bachate - każdy znajdzie coś dla siebie.</p>
        </div>
      </div>
    </section>

    <section class="events">
      <h2>Dołącz do nas już dziś!</h2>
      <div class="event-list">
        <div class="event">
          <h3>Zapisz się na zajęcia</h3>
          <p>Sprawdź nasz grafik i wybierz odpowiednie zajęcia dla siebie.</p>
          <router-link to="/schedule" class="link-button">Zobacz grafik</router-link>
        </div>
        <div class="event">
          <h3>Skontaktuj się z nami</h3>
          <p>Masz pytania? Chętnie na nie odpowiemy!</p>
          <a :href="`tel:${schoolInfo?.phone}`" class="link-button">Zadzwoń</a>
        </div>
      </div>
    </section>

    <footer v-if="schoolInfo" class="footer">
      <div class="footer-content">
        <div class="contact-info">
          <h3>{{ schoolInfo.name }}</h3>
          <p><i class="fas fa-map-marker-alt"></i> {{ schoolInfo.address }}</p>
          <p><i class="fas fa-phone"></i> {{ schoolInfo.phone }}</p>
          <p><i class="fas fa-envelope"></i> {{ schoolInfo.email }}</p>
        </div>
        <div class="payment-info">
          <h3>Dane do przelewu</h3>
          <p><strong>{{ schoolInfo.bank_name }}</strong></p>
          <p>{{ schoolInfo.bank_recipient }}</p>
          <p>{{ schoolInfo.bank_account }}</p>
          <p v-if="schoolInfo.blik_number"><strong>BLIK:</strong> {{ schoolInfo.blik_number }}</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import API from '../axios';

const schoolInfo = ref(null);

const fetchSchoolInfo = async () => {
  try {
    const response = await API.get('/school-info/');
    schoolInfo.value = response.data;
  } catch (error) {
    console.error('Error fetching school info:', error);
  }
};

onMounted(() => {
  fetchSchoolInfo();
});
</script>

<style scoped>
/* Stylizacja całego kontenera strony */
.homepage {
  font-family: 'Arial', sans-serif;
  color: #333;
  text-align: center;
  line-height: 1.6;
}

/* HERO SECTION */
.hero-section {
  position: relative;
  background: url('https://images.unsplash.com/photo-1521334887297-893c062f2db2?fit=crop&w=1650&q=80') no-repeat center center / cover;
  height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.hero-overlay {
  background: rgba(0, 0, 0, 0.6);
  padding: 2rem;
  border-radius: 12px;
}

.hero-section h1 {
  font-size: 2.5rem;
  margin: 0 0 1rem;
}

.hero-section h1 span {
  color: #ff5733;
}

.hero-section p {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
}

.cta-button {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background-color: #ff5733;
  color: #fff;
  text-decoration: none;
  border-radius: 8px;
  font-weight: bold;
}

.cta-button:hover {
  background-color: #e14e2c;
}

/* ABOUT US SECTION */
.about-us {
  padding: 4rem 2rem;
  background: #f9f9f9;
}

.about-us h2 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #443ea2;
}

.features {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 2rem;
}

.feature {
  max-width: 300px;
  text-align: center;
}

.feature i {
  font-size: 2.5rem;
  color: #ff5733;
  margin-bottom: 1rem;
}

.feature h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

/* EVENTS SECTION */
.events {
  padding: 4rem 2rem;
}

.events h2 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #443ea2;
}

.event-list {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 2rem;
}

.event {
  max-width: 300px;
  background: #fff;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: left;
}

.event h3 {
  color: #ff5733;
  margin-bottom: 0.75rem;
}

.link-button {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: #443ea2;
  color: #fff;
  text-decoration: none;
  border-radius: 4px;
}

.link-button:hover {
  background: #372f8b;
}

/* FOOTER */
.footer {
  background: #333;
  color: #fff;
  padding: 1rem 0;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: 2rem;
}

.contact-info, .payment-info {
  text-align: left;
}

.contact-info h3, .payment-info h3 {
  color: #ff5733;
  margin-bottom: 1rem;
}

.contact-info p, .payment-info p {
  margin: 0.5rem 0;
}

.contact-info i {
  width: 20px;
  margin-right: 10px;
  color: #ff5733;
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
    text-align: center;
  }

  .contact-info, .payment-info {
    text-align: center;
  }
}
</style>