<script setup>
// Można dodać dowolne funkcjonalności w przyszłości, np. dynamiczne ładowanie wydarzeń
</script>

<template>
  <div class="homepage">
    <!-- Nagłówek strony z dużym catchphrase -->
    <header class="hero-section">
      <div class="hero-overlay">
        <h1>Zapraszamy do szkoły tańca <span>De la Salsa</span></h1>
        <p>
          Najlepsze miejsce, gdzie rytm łączy ludzi. Naucz się salsy, bachaty, czy tańca towarzyskiego!
        </p>
        <router-link to="/schedule" class="cta-button">Sprawdź grafik zajęć</router-link>
      </div>
    </header>

    <!-- Sekcja z dodatkowymi informacjami -->
    <section class="about-us">
      <h2>Dlaczego warto wybrać naszą szkołę?</h2>
      <div class="features">
        <div class="feature">
          <i class="fa-solid fa-music"></i>
          <h3>Niezapomniana atmosfera</h3>
          <p>
            Oferujemy zajęcia w rodzinnej i przyjaznej atmosferze, która sprawi, że pokochasz taniec.
          </p>
        </div>
        <div class="feature">
          <i class="fa-solid fa-user-group"></i>
          <h3>Profesjonalni instruktorzy</h3>
          <p>
            Nasza kadra to doświadczeni tancerze, którzy uczynią każdy krok przyjemnością.
          </p>
        </div>
        <div class="feature">
          <i class="fa-solid fa-calendar-day"></i>
          <h3>Elastyczny harmonogram</h3>
          <p>
            Dopasuj zajęcia do swojego planu dnia. Prowadzimy lekcje poranne, wieczorne i weekendowe.
          </p>
        </div>
      </div>
    </section>

    <!-- Sekcja wydarzeń lub CTA -->
    <section class="events">
      <h2>Aktualności i wydarzenia</h2>
      <div class="event-list">
        <div class="event">
          <h3>Warsztaty Bachaty</h3>
          <p>Już 15 listopada startują warsztaty bachaty z naszym specjalnym gościem.</p>
          <router-link to="/events" class="link-button">Dowiedz się więcej</router-link>
        </div>
        <div class="event">
          <h3>Wieczory taneczne</h3>
          <p>Każdy piątek zapraszamy na wieczory taneczne. To świetna okazja na naukę i zabawę!</p>
          <router-link to="/events" class="link-button">Sprawdź szczegóły</router-link>
        </div>
        <div class="event">
          <h3>Nowy kurs tańca</h3>
          <p>Od 1 grudnia ruszają nowe kursy tańca dla wszystkich poziomów zaawansowania.</p>
          <router-link to="/courses" class="link-button">Zapisz się już dziś</router-link>
        </div>
      </div>
    </section>

    <!-- Stopka z informacjami kontaktowymi -->
    <footer class="footer">
      <div class="footer-content">
        <p>&copy; 2023 Szkoła tańca De la Salsa. Wszystkie prawa zastrzeżone.</p>
        <p>Kontakt: kontakt@delaasalsa.pl | Telefon: +48 123 456 789</p>
      </div>
    </footer>
  </div>
</template>

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
  font-size: 0.9rem;
}
</style>