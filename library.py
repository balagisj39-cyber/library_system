import sqlite3
import os
from datetime import date

DB_NAME = "library.db"
SCHEMA_FILE = "schema.sql"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database using schema.sql ignoring decoding errors."""
    if not os.path.exists(SCHEMA_FILE):
        print(f"[ERROR] {SCHEMA_FILE} not found in directory.")
        return

    # errors="ignore" ensures non-ASCII bytes don't crash Windows
    with open(SCHEMA_FILE, "r", encoding="utf-8", errors="ignore") as f:
        schema_script = f.read()

    with get_connection() as conn:
        conn.executescript(schema_script)
        conn.commit()

# --- Core Database Operations ---

def register_student(name: str, email: str, max_limit: int = 3):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO students (name, email, max_limit) VALUES (?, ?, ?)",
                (name, email, max_limit)
            )
            conn.commit()
            print(f"[OK] Student '{name}' registered successfully with ID: {cursor.lastrowid}")
    except sqlite3.IntegrityError:
        print("[ERROR] A student with this email already exists.")

def add_book(title: str, author: str, category: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO books (title, author, category) VALUES (?, ?, ?)",
            (title, author, category)
        )
        conn.commit()
        print(f"[OK] Book '{title}' added successfully with ID: {cursor.lastrowid}")

def search_books(query: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        q = f"%{query}%"
        cursor.execute("""
            SELECT * FROM books 
            WHERE title LIKE ? OR author LIKE ? OR category LIKE ?
        """, (q, q, q))
        books = cursor.fetchall()

        if not books:
            print("No matching books found.")
            return

        print("\n--- Search Results ---")
        for b in books:
            status = "Available" if b["is_available"] == 1 else "Issued"
            print(f"ID: {b['book_id']} | Title: {b['title']} | Author: {b['author']} | Category: {b['category']} | Status: {status}")

def issue_book(student_id: int, book_id: int, days_allowed: int = 14):
    with get_connection() as conn:
        cursor = conn.cursor()

        # Check student existence & active borrowing limit
        cursor.execute("SELECT name, max_limit FROM students WHERE student_id = ?", (student_id,))
        student = cursor.fetchone()
        if not student:
            print("[ERROR] Student ID not found.")
            return

        cursor.execute("""
            SELECT COUNT(*) as active_count FROM issues 
            WHERE student_id = ? AND return_date IS NULL
        """, (student_id,))
        active_borrows = cursor.fetchone()["active_count"]

        if active_borrows >= student["max_limit"]:
            print(f"[ERROR] Student '{student['name']}' has reached their borrowing limit of {student['max_limit']} books.")
            return

        # Check book availability
        cursor.execute("SELECT title, is_available FROM books WHERE book_id = ?", (book_id,))
        book = cursor.fetchone()
        if not book:
            print("[ERROR] Book ID not found.")
            return
        if book["is_available"] == 0:
            print(f"[ERROR] Book '{book['title']}' is currently issued to another student.")
            return

        # Issue book
        issue_date = date.today().isoformat()
        due_date = date.fromordinal(date.today().toordinal() + days_allowed).isoformat()

        cursor.execute("""
            INSERT INTO issues (student_id, book_id, issue_date, due_date)
            VALUES (?, ?, ?, ?)
        """, (student_id, book_id, issue_date, due_date))

        cursor.execute("UPDATE books SET is_available = 0 WHERE book_id = ?", (book_id,))
        conn.commit()
        print(f"[OK] Book '{book['title']}' successfully issued to {student['name']}. Due Date: {due_date}")

def return_book(book_id: int, fine_rate_per_day: float = 5.0):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT i.issue_id, i.due_date, s.name as student_name, b.title as book_title
            FROM issues i
            JOIN students s ON i.student_id = s.student_id
            JOIN books b ON i.book_id = b.book_id
            WHERE i.book_id = ? AND i.return_date IS NULL
        """, (book_id,))
        issue = cursor.fetchone()

        if not issue:
            print("[ERROR] Active issue record not found for this Book ID.")
            return

        return_date = date.today()
        due_date = date.fromisoformat(issue["due_date"])
        overdue_days = (return_date - due_date).days
        fine = max(0.0, overdue_days * fine_rate_per_day) if overdue_days > 0 else 0.0

        cursor.execute("""
            UPDATE issues 
            SET return_date = ?, fine_amount = ? 
            WHERE issue_id = ?
        """, (return_date.isoformat(), fine, issue["issue_id"]))

        cursor.execute("UPDATE books SET is_available = 1 WHERE book_id = ?", (book_id,))
        conn.commit()

        print(f"[OK] Book '{issue['book_title']}' returned by {issue['student_name']}.")
        if fine > 0:
            print(f"[WARNING] Overdue by {overdue_days} days. Fine Amount: Rs.{fine:.2f}")

def list_borrowed_books():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.issue_id, b.title, s.name AS student_name, i.issue_date, i.due_date
            FROM issues i
            JOIN books b ON i.book_id = b.book_id
            JOIN students s ON i.student_id = s.student_id
            WHERE i.return_date IS NULL
        """)
        records = cursor.fetchall()

        if not records:
            print("\nNo books are currently borrowed.")
            return

        print("\n--- Currently Borrowed Books ---")
        for r in records:
            print(f"Issue ID: {r['issue_id']} | Book: {r['title']} | Borrowed By: {r['student_name']} | Due: {r['due_date']}")

# --- Interactive Terminal Menu ---

def main():
    init_db()
    while True:
        print("\n=== MINI LIBRARY MANAGEMENT SYSTEM ===")
        print("1. Register Student")
        print("2. Add Book")
        print("3. Search Books")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. Show Currently Borrowed Books")
        print("7. Exit")

        choice = input("Select an option (1-7): ").strip()

        if choice == "1":
            name = input("Enter Student Name: ").strip()
            email = input("Enter Student Email: ").strip()
            register_student(name, email)
        elif choice == "2":
            title = input("Enter Book Title: ").strip()
            author = input("Enter Author: ").strip()
            category = input("Enter Category: ").strip()
            add_book(title, author, category)
        elif choice == "3":
            query = input("Enter Title/Author/Category to search: ").strip()
            search_books(query)
        elif choice == "4":
            try:
                s_id = int(input("Enter Student ID: ").strip())
                b_id = int(input("Enter Book ID: ").strip())
                issue_book(s_id, b_id)
            except ValueError:
                print("[ERROR] Invalid input. ID must be an integer.")
        elif choice == "5":
            try:
                b_id = int(input("Enter Book ID to Return: ").strip())
                return_book(b_id)
            except ValueError:
                print("[ERROR] Invalid input. ID must be an integer.")
        elif choice == "6":
            list_borrowed_books()
        elif choice == "7":
            print("Exiting System. Goodbye!")
            break
        else:
            print("Invalid selection. Try again.")

if __name__ == "__main__":
    main()