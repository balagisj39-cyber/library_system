Markdown# 📚 Mini Library Management System

A normalized relational database layer, CLI application, and interactive Web UI built for **Task 6 (WebX Selection Tasks 2026–27)**.

---

## 🚀 Features

- **Normalized Relational Database**: Structured database schema built with SQLite enforcing Foreign Key constraints, data integrity, and performance indexes.
- **Interactive Web UI (Streamlit)**: Modern, user-friendly browser interface for searching catalog items, issuing/returning books, managing student profiles, and viewing live analytics.
- **Interactive Terminal Menu (CLI)**: Full-featured command-line application for lightweight terminal usage.
- **Bulk Excel Import**: Automated import script (`import_books.py`) using `pandas` and `openpyxl` to populate the database with 200+ books from `books.xlsx`.
- **Smart Subject Search**: Case-insensitive search with automatic keyword and stem expansion for subjects like Mathematics, Physics, and Computer Science.
- **Core Business Rules Enforced**:
  - Prevents issuing unavailable or already borrowed books.
  - Checks and enforces active borrowing limits per student (default limit: 3 books).
  - Atomic SQL execution to prevent race conditions during concurrent borrowing attempts.
- **Automated Fine Calculation**: Tracks issue dates, due dates, and return dates, automatically computing daily overdue fines (default: Rs. 5.00/day).
- **Audit Logs & Analytics**: Displays full transaction history logs and statistics on the top 5 most borrowed books[cite: 1].

---

## 🗄️ Database Schema & Relationships (`schema.sql`)

The database consists of three core entities designed around normalized relationships[cite: 1]:

- **`students`**: Stores student profiles, emails, and borrowing limits[cite: 1].
- **`books`**: Stores book titles, authors, categories, and availability status (`is_available`)[cite: 1].
- **`issues`**: Junction table tracking loans, due dates, return dates, and calculated fines[cite: 1].

+------------------+         +------------------+         +------------------+|     students     |         |      issues      |         |      books       |+------------------+         +------------------+         +------------------+| student_id (PK)  |<-------1| issue_id (PK)    |1------->| book_id (PK)     || name             |         | student_id (FK)  |         | title            || email (UNIQUE)   |         | book_id (FK)     |         | author           || max_limit        |         | issue_date       |         | category         |+------------------+         | due_date         |         | is_available     || return_date      |         +------------------+| fine_amount      |+------------------+
### Performance Indexes
Includes indexes on search columns (`title`, `author`, `category`) and foreign keys (`student_id`, `book_id`) for optimized lookups[cite: 1].

---

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.x** installed[cite: 1].

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/library_system.git](https://github.com/your-username/library_system.git)
cd library_system
2. Install DependenciesInstall required packages listed in requirements.txt[cite: 1]:Bashpy -m pip install -r requirements.txt
📂 Step 1: Import Books DatasetImport all 200 books from books.xlsx into library.db:   Bashpy import_books.py
Expected Output: [SUCCESS] Successfully imported 200 books into 'library.db'![cite: 3]💻 How to RunOption A: Launch Web UI (Streamlit)To run the browser application:Bashpy -m streamlit run app.py
Opens automatically at http://localhost:8501.Option B: Launch Terminal CLI MenuTo run the command-line interface[cite: 1]:Bashpy library.py
🧪 Testing & Usage WalkthroughRegister Student: Create a student profile (e.g., Name: John Doe, Email: john@example.com)[cite: 1].Search Books: Search by keyword like Physics, Mathematics, or Deep Work to get corresponding Book IDs[cite: 1].Issue Book: Enter Student ID (1) and Book ID (1) to issue a book[cite: 1].Return Book: Enter Book ID (1) to complete a return and view any calculated overdue fines[cite: 1].View Audit Logs & Stats: Check transaction history and top 5 most borrowed books analytics[cite: 1].📁 Repository Structure├── app.py              # Streamlit Web UI application
├── library.py          # Database logic & CLI menu
├── import_books.py     # Bulk import script for books.xlsx
├── books.xlsx          # Dataset containing 200 books
├── schema.sql          # Table definitions & performance indexes
├── requirements.txt    # Python package dependencies
└── README.md           # Project documentation
