import sqlite3

def create_table():
    conn = sqlite3.connect("college.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS student (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        course TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_student():
    name = input("Enter student name: ")
    course = input("Enter course: ")
    conn = sqlite3.connect("college.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO student (name, course) VALUES (?, ?)", (name, course))
    conn.commit()
    conn.close()
    print("Student added successfully!")

def view_students():
    conn = sqlite3.connect("college.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()
    if rows:
        print("ID | Name | Course")
        for row in rows:
            print(row[0], "|", row[1], "|", row[2])
    else:
        print("No students found!")
    conn.close()

def update_student():
    student_id = input("Enter student ID to update: ")
    name = input("Enter new name: ")
    course = input("Enter new course: ")
    conn = sqlite3.connect("college.db")
    cur = conn.cursor()
    cur.execute("UPDATE student SET name=?, course=? WHERE id=?", (name, course, student_id))
    conn.commit()
    conn.close()
    print("Student updated successfully!")

def delete_student():
    student_id = input("Enter student ID to delete: ")
    conn = sqlite3.connect("college.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM student WHERE id=?", (student_id,))
    conn.commit()
    conn.close()
    print("Student deleted successfully!")

def menu():
    create_table()
    while True:
        print("\n===== Student Management =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            update_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    menu()
