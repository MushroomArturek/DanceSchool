# DanceSchool
This project is a web application developed as part of an engineering thesis, aimed at improving the daily management of a dance school. The system streamlines administrative tasks such as scheduling classes and tracking payments, helping staff operate more efficiently and reducing the reliance on manual documentation.

The backend of the application is built with Django (Python), providing robust support for data processing and business logic. The frontend is developed using Vue.js, delivering a dynamic and responsive user interface. SQLite is used as the database engine, offering a lightweight and self-contained solution suitable for small-scale deployments.

The entire system was created using open-source technologies, making it an accessible and cost-effective option for small service-oriented businesses.

## Diagrams

### Use Case Diagrams

The following use case diagrams illustrate the main functionalities of the system and how users interact with them. They help to identify the actors involved and the operations they can perform within the application.

![Use Case Diagram 1](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/use_case_admin_ins.png?raw=true)
![Use Case Diagram 2](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/use_case_uczen_gosc.png?raw=true)

### Entity-Relationship Diagram (ERD)

The following ER diagram shows the data model used in the system. It presents the entities, their attributes, and the relationships between them.

![Entity-Relationship Diagram](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/baza_danych%20(1).png?raw=true)

## User Interface Overview

Below are selected screenshots showcasing the application's user interface for each user role. Each subsection presents views relevant to a specific type of user.

### Guest

_Screens accessible without logging in, such as landing page, class offer, or contact form._

![Guest View 1](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/Strona_glowna.png?raw=true)
![Guest View 2](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/harmonogram.png?raw=true)
![Guest View 3](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/szczegoly_tanca.png?raw=true)
![Guest View 4](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/school_info.png?raw=true)
![Guest View 5](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/Rejestracja.png?raw=true)
![Guest View 6](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/logowanie.png?raw=true)

### Student

_Screens available to registered students, such as class enrollment, schedule, or payment status._

![Student View 1](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/dostepne_zajecia.png?raw=true)
![Student View 2](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/moje_rezerwacje.png?raw=true)
![Student View 3](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/platnosci_uczen.png?raw=true)
![Student View 4](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/metoda_platnosci.png?raw=true)
![Student View 5](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/dane_do_platnosci.png?raw=true)
![Student View 6](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/oczekujaca_platnosc.png?raw=true)

### Instructor

_Views used by instructors to manage their classes, attendance lists, and check payments._

![Instructor View 1](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/lista_obecnosci.png?raw=true)
![Instructor View 2](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/dodaj_do_listy_obecnosci.png?raw=true)
![Instructor View 3](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/lista_platnosci.png?raw=true)
![Instructor View 4](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/lista_platnosci_potwierdzenie.png?raw=true)
![Instructor View 5](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/zarzadzanie_uczniami.png?raw=true)
![Instructor View 6](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/zarzadzanie_zajeciami.png?raw=true)

### Administrator

_Administrative interface for managing users, classes, schedules, and handling system settings._

![Admin View 1](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/zarzadzanie_instruktorami.png?raw=true)
![Admin View 2](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/raport_analityka.png?raw=true)
![Admin View 3](https://github.com/MushroomArturek/DanceSchool/blob/main/screenshots/raport_frekwencja.png?raw=true)
