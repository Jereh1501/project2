import sqlite3

DATABASE = "course_registration.db"


def connect():
    connection = sqlite3.connect(DATABASE)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_tables():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_code TEXT NOT NULL,
                course_title TEXT NOT NULL,
                credit_units INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
                    ON DELETE CASCADE
            )
        """)


def register_student():
    try:
        student_id = int(input("Student ID: "))
        name = input("Student full name: ").strip()
        email = input("Email: ").strip()
        with connect() as conn:
            conn.execute(
                "INSERT INTO students (student_id, full_name, email) VALUES (?, ?, ?)",
                (student_id, name, email or None)
            )
        print("Student registered.")
    except ValueError:
        print("Student ID must be a number.")
    except sqlite3.IntegrityError as error:
        print("Could not register student:", error)


def register_course():
    try:
        student_id = int(input("Student ID to register for this course: "))
        code = input("Course code: ").strip().upper()
        title = input("Course title: ").strip()
        units = int(input("Credit units: "))
        if units <= 0:
            print("Credit units must be greater than zero.")
            return
        with connect() as conn:
            conn.execute("""
                INSERT INTO courses (course_code, course_title, credit_units, student_id)
                VALUES (?, ?, ?, ?)
            """, (code, title, units, student_id))
        print("Course registered for student.")
    except ValueError:
        print("Student ID and credit units must be numbers.")
    except sqlite3.IntegrityError as error:
        print("Could not register course. Check the student ID and details:", error)


def view_students():
    with connect() as conn:
        rows = conn.execute(
            "SELECT student_id, full_name, email FROM students ORDER BY student_id"
        ).fetchall()
    print("\nREGISTERED STUDENTS")
    if not rows:
        print("No students registered.")
    for row in rows:
        print(row)


def view_courses():
    with connect() as conn:
        rows = conn.execute("""
            SELECT course_id, course_code, course_title, credit_units, student_id
            FROM courses ORDER BY course_id
        """).fetchall()
    print("\nREGISTERED COURSES")
    if not rows:
        print("No courses registered.")
    for row in rows:
        print(row)


def view_student_courses():
    with connect() as conn:
        rows = conn.execute("""
            SELECT students.student_id, students.full_name,
                   courses.course_code, courses.course_title, courses.credit_units
            FROM students
            INNER JOIN courses ON students.student_id = courses.student_id
            ORDER BY students.full_name, courses.course_code
        """).fetchall()
    print("\nSTUDENT COURSE REGISTRATION")
    if not rows:
        print("No student-course registrations found.")
    for row in rows:
        print(f"ID: {row[0]} | Student: {row[1]} | Course: {row[2]} - "
              f"{row[3]} | Units: {row[4]}")


def main():
    create_tables()
    actions = {
        "1": register_student,
        "2": register_course,
        "3": view_students,
        "4": view_courses,
        "5": view_student_courses,
    }
    while True:
        print("""
COURSE REGISTRATION SYSTEM
1. Register student
2. Register course for a student
3. View students
4. View courses
5. View students with their courses (JOIN)
0. Exit
""")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye.")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
