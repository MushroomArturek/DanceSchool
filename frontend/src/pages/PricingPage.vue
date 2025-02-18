<template>
  <div class="pricing-page">
    <header class="pricing-header">
      <h1>Cennik zajęć</h1>
      <p>Wybierz pakiet najlepiej dopasowany do Twoich potrzeb</p>
    </header>

    <div class="pricing-grid">
      <!-- Pakiet Basic -->
      <div class="pricing-card">
        <div class="pricing-card-header">
          <h2>Basic</h2>
          <p class="price">149 zł<span>/miesiąc</span></p>
        </div>
        <div class="pricing-card-body">
          <ul>
            <li><i class="fas fa-check"></i> 4 wejścia w miesiącu</li>
            <li><i class="fas fa-check"></i> Wszystkie style tańca</li>
            <li><i class="fas fa-check"></i> Ważność 30 dni</li>
            <li><i class="fas fa-check"></i> Możliwość odrabiania zajęć</li>
          </ul>
        </div>
        <div class="pricing-card-footer">
          <router-link to="/register" class="cta-button">Wybierz pakiet</router-link>
        </div>
      </div>

      <!-- Pakiet Standard -->
      <div class="pricing-card featured">
        <div class="pricing-card-header">
          <div class="featured-badge">Najpopularniejszy</div>
          <h2>Standard</h2>
          <p class="price">249 zł<span>/miesiąc</span></p>
        </div>
        <div class="pricing-card-body">
          <ul>
            <li><i class="fas fa-check"></i> 8 wejść w miesiącu</li>
            <li><i class="fas fa-check"></i> Wszystkie style tańca</li>
            <li><i class="fas fa-check"></i> Ważność 30 dni</li>
            <li><i class="fas fa-check"></i> Możliwość odrabiania zajęć</li>
            <li><i class="fas fa-check"></i> 1 warsztat w miesiącu gratis</li>
          </ul>
        </div>
        <div class="pricing-card-footer">
          <router-link to="/register" class="cta-button">Wybierz pakiet</router-link>
        </div>
      </div>

      <!-- Pakiet Premium -->
      <div class="pricing-card">
        <div class="pricing-card-header">
          <h2>Premium</h2>
          <p class="price">349 zł<span>/miesiąc</span></p>
        </div>
        <div class="pricing-card-body">
          <ul>
            <li><i class="fas fa-check"></i> Nielimitowane wejścia</li>
            <li><i class="fas fa-check"></i> Wszystkie style tańca</li>
            <li><i class="fas fa-check"></i> Ważność 30 dni</li>
            <li><i class="fas fa-check"></i> Pierwszeństwo zapisów</li>
            <li><i class="fas fa-check"></i> 2 warsztaty w miesiącu gratis</li>
            <li><i class="fas fa-check"></i> Lekcja indywidualna w miesiącu</li>
          </ul>
        </div>
        <div class="pricing-card-footer">
          <router-link to="/register" class="cta-button">Wybierz pakiet</router-link>
        </div>
      </div>
    </div>

    <section class="additional-info">
      <h2>Dodatkowe informacje</h2>
      <div class="info-grid">
        <div class="info-card">
          <i class="fas fa-user"></i>
          <h3>Wejście jednorazowe</h3>
          <p>45 zł</p>
        </div>
        <div class="info-card">
          <i class="fas fa-users"></i>
          <h3>Lekcja indywidualna</h3>
          <p>150 zł / 60 min</p>
        </div>
        <div class="info-card">
          <i class="fas fa-star"></i>
          <h3>Warsztaty weekend</h3>
          <p>od 199 zł</p>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.pricing-page {
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
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.pricing-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease;
  position: relative;
}

.pricing-card:hover {
  transform: translateY(-5px);
}

.pricing-card.featured {
  border: 2px solid #ff5733;
  transform: scale(1.05);
}

.featured-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: #ff5733;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
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

.price span {
  font-size: 1rem;
  color: #666;
}

.pricing-card-body {
  padding: 2rem;
}

.pricing-card-body ul {
  list-style: none;
  padding: 0;
  margin: 0;
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
}

.cta-button {
  display: inline-block;
  padding: 1rem 2rem;
  background: #443ea2;
  color: white;
  text-decoration: none;
  border-radius: 30px;
  transition: background 0.3s ease;
}

.cta-button:hover {
  background: #372f8b;
}

.additional-info {
  margin-top: 4rem;
  text-align: center;
}

.additional-info h2 {
  color: #443ea2;
  margin-bottom: 2rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.info-card {
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.info-card i {
  font-size: 2rem;
  color: #ff5733;
  margin-bottom: 1rem;
}

.info-card h3 {
  color: #443ea2;
  margin-bottom: 0.5rem;
}

.info-card p {
  color: #666;
  font-size: 1.2rem;
  font-weight: bold;
}

@media (max-width: 768px) {
  .pricing-grid {
    grid-template-columns: 1fr;
  }

  .pricing-card.featured {
    transform: none;
  }
}
</style>