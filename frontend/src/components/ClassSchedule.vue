<template>
  <div id="calendar-container">
    <h2>Harmonogram Zajęć</h2>
    <div id="calendar"></div>
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
import { createDragAndDropPlugin } from "@schedule-x/drag-and-drop";
import { createEventModalPlugin } from "@schedule-x/event-modal";
import { createEventRecurrencePlugin } from "@schedule-x/event-recurrence";
import "@schedule-x/theme-default/dist/index.css";

export default {
  name: "ClassSchedule",
  setup() {
    const calendar = ref(null);
    const events = ref([]);

    const fetchClasses = async () => {
  try {
    const response = await axios.get("http://localhost:8000/api/classes/");

    // Map classes to calendar events
    events.value = response.data.map((item) => {
      const baseEvent = {
        id: item.id,
        title: `${item.name} (${item.style})`,
        description: `Prowadzący: ${item.instructor}, Sala: ${item.room}`,
      };

      if (item.is_recurring) {
        return {
          ...baseEvent,
          start: item.start_time,
          end: item.end_time,
          rrule: `FREQ=WEEKLY;BYDAY=${item.days_of_week}`,
        };
      } else {
        return {
          ...baseEvent,
          start: item.start_time,
          end: item.end_time,
        };
      }
    });

    console.log("Mapped events:", events.value);
  } catch (error) {
    console.error("Błąd podczas pobierania zajęć:", error);
  }
};

    const initializeCalendar = () => {
      calendar.value = createCalendar({
        views: [viewMonthAgenda, viewWeek],
        selectedDate: new Date().toISOString().split("T")[0],
        defaultView: viewWeek.name,
        events: events.value,
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
        plugins: [
          createDragAndDropPlugin(),
          createEventModalPlugin(),
          createEventRecurrencePlugin(),
        ],
      });

      const calendarEl = document.getElementById("calendar");
      if (calendarEl) {
        calendar.value.render(calendarEl);
      }
    };

    onMounted(async () => {
      await fetchClasses();
      initializeCalendar();
    });

    return {};
  },
};
</script>

<style scoped>
#calendar-container {
  padding: 10px;
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

#calendar {
  flex: 1;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.sx__close-modal-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
</style>