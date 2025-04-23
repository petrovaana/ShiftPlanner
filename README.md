# ShiftPlanner
This application is made specifically for restaurants and other companies possibly hosting private events. It helps employees to track important information about the events and other information about a shift.
  - Users can log in and register in the application.
  - Private events can be recorded in the application, along with important details related to them, such as dates, guests and booked space.
  - The application's home page shows 7 upcoming private events, as well as 10 missing items.
  - It also allows users to search for private events based on keywords from their title, desciption or booked space.
  - Users can register missing items so that everybody knows if the restaurant is out of something.
  - In addition, user can delete items and private events.
  - Users are able to comment on private events if something notable happened/changed during the event, and as well delete the event if needed.
  - Both search pages show the whole lists of all added private events or missing items.
  - In addition, the app allows the user to log in any wastage and classify it based on reasons of the wastage, and view all of the wasted items. 

Startup instructions:

Install flask libraby:
pip install flask

Create the database table and insert initial data:
sqlite3 database.db < schema.sql
sqlite3 database.db < init.sql

Start the application like this:
venv\Scripts\activate
python3 -m flask run

