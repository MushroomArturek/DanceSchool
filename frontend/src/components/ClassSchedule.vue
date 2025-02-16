<template>
  <div id="calendar-container">
    <h2>Harmonogram Zajęć</h2>
    <div id="calendar"></div> <!-- Kontener na kalendarz -->
  </div>
</template>

<script>
import { onMounted, ref } from "vue";
import axios from "axios";
import {
  createCalendar,
  viewMonthAgenda,
  viewWeek,
} from "@schedule-x/calendar";
import {createDragAndDropPlugin} from "@schedule-x/drag-and-drop";
import {createEventModalPlugin} from "@schedule-x/event-modal";
import "@schedule-x/theme-default/dist/index.css";

export default {
  name: "ClassSchedule",
  setup() {
    const calendar = ref(null); // Referencja do kalendarza
    const events = ref([]); // Lista wydarzeń

    // Funkcja do pobierania zajęć
    const fetchClasses = async () => {
      try {
        const token = localStorage.getItem("access"); // Pobierz token z localStorage
        if (!token) {
          throw new Error("No access token found");
        }

        const response = await axios.get("http://localhost:8000/api/classes/", {
          headers: {
            Authorization: `Bearer ${token}`, // Dodaj token do nagłówków
          },
        });

        // Mapowanie zajęć do struktury wydarzeń dla kalendarza
        events.value = response.data.map((item) => ({
          id: item.id,
          title: `${item.name} (${item.style})`,
          start: item.start_time,
          end: item.end_time,
          description: `Prowadzący: ${item.instructor}, Sala: ${item.room}`,
        }));
      } catch (error) {
        console.error("Błąd podczas pobierania zajęć:", error);
      }
    };

    // Funkcja inicjalizująca kalendarz
    const initializeCalendar = () => {
      calendar.value = createCalendar({
        views: [viewMonthAgenda, viewWeek],
        selectedDate: new Date().toISOString().split("T")[0], // Obecna data
        defaultView: viewWeek.name,
        events: events.value, // Dynamiczne wydarzenia
        calendars: {
          default: {
            colorName: "primary",
            lightColors: {
              main: "#1c7df9",
              container: "#d2e7ff",
              onContainer: "#002859",
            },
            darkColors: {
              main: "#c0dfff",
              onContainer: "#dee6ff",
              container: "#426aa2",
            },
          },
        },
        plugins: [createDragAndDropPlugin(), createEventModalPlugin()],
      });

      const calendarEl = document.getElementById("calendar");
      calendar.value.render(calendarEl); // Renderowanie kalendarza
    };

    // Pobierz dane o zajęciach i zainicjalizuj kalendarz
    onMounted(async () => {
      await fetchClasses(); // Pobranie danych z backendu
      initializeCalendar(); // Inicjalizacja kalendarza
    });

    return {};
  },
};
</script>

<style scoped>
/* Kontener całego komponentu */
#calendar-container {
  padding: 10px;
  width: 100%; /* Rozciągnij na całą szerokość */
  height: 100vh; /* Wysokość całego widoku przeglądarki */
  display: flex;
  flex-direction: column; /* Ułóż w kolumnie (nagłówek + kalendarz) */
  box-sizing: border-box;
}

/* Nagłówek */
h2 {
  text-align: center;
  margin-bottom: 20px;
}

/* Kalendarz */
#calendar {
  flex: 1; /* Zajmij całą dostępną przestrzeń */
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden; /* Obcinaj nadmiar treści */
}

.sx__close-modal-btn {
  background-color: #007bff; /* Kolor tła przycisku */
  color: white; /* Kolor tekstu */
  border: none; /* Brak ramki */
  padding: 10px 20px; /* Padding wokół tekstu */
  border-radius: 5px; /* Zaokrąglone rogi */
  font-size: 16px; /* Rozmiar czcionki */
  cursor: pointer; /* Kursor w postaci ręki przy najechaniu */
  transition: background-color 0.3s ease; /* Płynna zmiana koloru tła */
}
</style>