# Course Registration Database

A Python and SQLite command-line application for registering students and assigning courses to them.

## Database design
- `students`: one row per student; `student_id` is the primary key.
- `courses`: course registrations; `course_id` is the primary key and `student_id` is a foreign key referencing `students.student_id`.
- This design demonstrates a one-to-many relationship: one student can have multiple course registrations.

## Features
- Register students.
- Register courses for existing students.
- View students and courses.
- Use an SQL `INNER JOIN` to display each student with their registered courses.

## Requirements
Python 3. SQLite is available through Python's built-in `sqlite3` module.

## Run
```bash
python main.py
```
The `course_registration.db` database and its tables are created automatically.
