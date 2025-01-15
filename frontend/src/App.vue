   <template>
     <div id="app">
       <h1>Witamy w DanceSchool</h1>
       <StudentsList />
     </div>
   </template>

   <script>
   import StudentsList from './components/StudentsList.vue';

   export default {
     components: {
       StudentsList
     }
   };
   </script>

   <style>
   #app {
     text-align: center;
     margin-top: 20px;
   }
   </style>