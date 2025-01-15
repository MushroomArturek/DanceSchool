<template>
     <div>
       <h2>Lista studentów</h2>
       <ul v-if="students.length">
         <li v-for="student in students" :key="student.id">
           {{ student.first_name }}
         </li>
       </ul>
       <p v-else>Brak studentów do wyświetlenia.</p>
     </div>
   </template>




   <script>
   import axios from 'axios';

   export default {
     data() {
       return {
         students: [] // Miejsce, gdzie dane studentów będą przechowywane
       };
     },
     mounted() {
       // Pobierz listę studentów z backendu, gdy komponent jest zamontowany
       axios.get('http://127.0.0.1:8000/api/students/')
         .then(response => {
           this.students = response.data; // Przypisz dane do zmiennej students
         })
         .catch(error => {
           console.error('Błąd podczas ładowania danych: ', error);
         });
     }
   };
   </script>

   <style scoped>
   h2 {
     color: #007bff;
   }
   ul {
     list-style-type: none;
     padding: 0;
   }
   li {
     margin: 5px 0;
     padding: 8px;
     background: #f8f9fa;
     border-radius: 4px;
   }
   </style>