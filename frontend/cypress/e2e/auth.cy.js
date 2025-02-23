// frontend/cypress/e2e/auth.cy.js
describe('Authentication Flow', () => {
    it('should register a new user', () => {
        cy.visit('/register')
        cy.get('input#first_name').type('Test')
        cy.get('input#last_name').type('User')
        cy.get('input#email').type('test@example.com')
        cy.get('input#password').type('testpass123')
        cy.get('input#phone_number').type('123456789')
        cy.get('input#date_of_birth').type('2003-01-01')
        cy.get('button[type="submit"]').click()

        // Check for success message
        cy.get('.success-message').should('be.visible')

        // Increase timeout for URL assertion
        cy.url({timeout: 10000}).should('include', '/login')
    })

    it('should login and access protected route', () => {
        cy.visit('/login')
        cy.get('input#email').type('test@example.com')
        cy.get('input#password').type('testpass123')
        cy.get('button[type="submit"]').click()
        cy.url().should('include', '/schedule')

        // Verify token storage
        cy.window().its('localStorage.access').should('exist')
        cy.window().its('localStorage.role').should('exist')
    })
})