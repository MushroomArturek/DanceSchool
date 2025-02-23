// frontend/cypress/e2e/admin.cy.js
describe('Admin Panel Flow', () => {
  beforeEach(() => {
    cy.login('admin@admin.pl', 'arturg15')
    cy.window().its('localStorage.role').should('eq', 'admin')
  })

  it('should create a new class', () => {
    cy.visit('/admin/classes')
    cy.get('button[data-test="add-class"]').click()
    cy.get('input[name="name"]').type('New Dance Class')
    cy.get('select[name="style"]').select('Salsa')
    cy.get('input[name="max_participants"]').type('15')
    cy.get('input[name="start_time"]').type('2024-03-01T18:00')
    cy.get('input[name="end_time"]').type('2024-03-01T19:00')
    cy.get('button[type="submit"]').click()
    cy.get('.success-message').should('be.visible')
  })

  it('should manage instructors', () => {
    cy.visit('/admin/instructors')
    cy.get('button[data-test="add-instructor"]').click()
    cy.get('input[name="first_name"]').type('John')
    cy.get('input[name="last_name"]').type('Doe')
    cy.get('input[name="email"]').type('john@example.com')
    cy.get('input[name="specialization"]').type('Salsa, Bachata')
    cy.get('button[type="submit"]').click()
    cy.get('.instructor-list').should('contain', 'John Doe')
  })
})