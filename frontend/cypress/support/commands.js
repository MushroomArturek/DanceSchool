// frontend/cypress/support/commands.js
Cypress.Commands.add('login', (email, password) => {
  cy.request({
    method: 'POST',
    url: 'http://localhost:8000/api/auth/login/',
    body: {
      email: email,
      password: password
    }
  }).then((response) => {
    window.localStorage.setItem('token', response.body.access)
  })
})

Cypress.Commands.add('createClass', (classData) => {
  cy.request({
    method: 'POST',
    url: 'http://localhost:8000/api/classes/create/',
    headers: {
      Authorization: `Bearer ${window.localStorage.getItem('token')}`
    },
    body: classData
  })
})