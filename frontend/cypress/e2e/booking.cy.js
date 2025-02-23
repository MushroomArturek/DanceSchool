// frontend/cypress/e2e/booking.cy.js
describe('Class Booking Flow', () => {
  beforeEach(() => {
    cy.login('test@example.com', 'testpass123')
  })

  it('should book a class from available classes', () => {
    cy.visit('/reservations')
    cy.get('button.tab-btn').contains('Dostępne zajęcia').click()
    cy.get('.class-card').first().find('button.book-btn').click()
    cy.get('.notification.success').should('contain', 'Pomyślnie zapisano na zajęcia!')
  })

  it('should cancel a booking', () => {
    cy.visit('/reservations')
    cy.get('button.tab-btn').contains('Moje rezerwacje').click()
    cy.get('.booking-card').first().find('button.cancel-btn').click()
    cy.get('.notification.success').should('contain', 'Anulowano rezerwację')
  })
})