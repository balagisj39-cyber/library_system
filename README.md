# 📚 Mini Library Management System

A normalized relational database layer, interactive Web UI, and CLI application built for **Task 6 (WebX Selection Tasks 2026–27)**.

---

## 🌟 Overview

The **Mini Library Management System** provides an end-to-end solution for managing college library operations. It features a normalized SQLite database engine, business rule validation, automatic fine calculations, a bulk Excel import pipeline, and a modern, dual-themed **Streamlit** web application.

---

## ✨ Features

- **Normalized Schema**: Relational database design (`students`, `books`, `issues`) enforcing foreign key constraints and atomic SQL operations.
- **Dual-Themed Streamlit Web UI**: Interactive dashboard featuring KPI metrics, dynamic search, tabbed forms, and a **Theme Switcher** (Neon Dark & Classic Light mode).
- **Terminal CLI Interface**: Full-featured command-line application for terminal-only environments.
- **Bulk Excel Import**: Built-in import script (`import_books.py`) using `pandas` and `openpyxl` to populate 200+ pre-formatted books from `books.xlsx` into `library.db`.
- **Smart Subject Search**: Case-insensitive partial matching and automatic keyword/stem expansion (e.g., Physics, Mathematics, CS).
- **Business Rule Enforcement**:
  - Blocks issuing unavailable or already borrowed books.
  - Checks active borrowing limits per student (default limit: 3 books).
  - Prevents race conditions using atomic SQL queries.
- **Dynamic Fine Calculation**: Calculates overdue days upon return and applies fine rates (default: Rs. 5.00/day).
- **Audit Logging & Analytics**: Live transaction logs and top borrowed book insights.

---

## 🗄️ Database Schema & Architecture (`schema.sql`)

The database consists of three core tables:

- **`students`**: Stores student profiles, contact details, and borrowing limits.
- **`books`**: Tracks catalog inventory and availability status (`is_available`).
- **`issues`**: Junction table tracking active loans, issue/due dates, return dates, and fine amounts.
+------------------+         +------------------+         +------------------+
|     students     |         |      issues      |         |      books       |
+------------------+         +------------------+         +------------------+
| student_id (PK)  |<-------1| issue_id (PK)    |1------->| book_id (PK)     |
| name             |         | student_id (FK)  |         | title            |
| email (UNIQUE)   |         | book_id (FK)     |         | author           |
| max_limit        |         | issue_date       |         | category         |
+------------------+         | due_date         |         | is_available     |
                             | return_date      |         +------------------+
                             | fine_amount      |
                             +------------------+

### Performance Index        
Includes database indexes on frequent search fields (`title`, `author`, `category`) and foreign key columns (`student_id`, `book_id`) for fast lookups.

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/library_system.git]
           (https://github.com/your-username/library_system.git)
cd library_system
2. Install Dependencies
Install all required external packages listed in requirements.txt
    Bash
    py -m pip install -r requirements.txt

📂 Step 1: Import Dataset into Database
Populate library.db with the 200 catalog books from books.xlsx:
   Bash
   py import_books.py
Expected Output: [SUCCESS] Successfully imported 200 books into 'library.db'!
💻 How to RunOption A: 
 Launch Web UI (Streamlit — Recommended)
 Run the browser-based dashboard:
 Bash
 py -m streamlit run app.py
Opens automatically at http://localhost:8501. Use the sidebar to switch between Neon Dark and Classic Light mode!
Option B: Launch Terminal CLIRun the command-line interface:
Bash
py library.py
🧪 Quick Walkthrough
1.Register Student: Go to Student Directory and add a student (e.g., Name: John Doe, Email: john@example.com).
2.Search Catalog: Search for topics like Physics, Mathematics, or Deep Work to get corresponding Book IDs.
3.Issue Book: Go to Issue Book, enter Student ID (1) and Book ID (1).
4.Return Book: Enter Book ID (1) in Return Book to complete the loan and calculate any overdue fines.
5.Audit Logs: View live active loans and full transaction history under Transaction Audit Log.

📁 Repository Structure
├── app.py              # Streamlit Web UI application
├── library.py          # SQLite database logic & Terminal CLI menu
├── import_books.py     # Bulk import script for books.xlsx
├── books.xlsx          # Dataset containing 200 books
├── schema.sql          # Table definitions & performance indexes
├── requirements.txt    # Python package dependencies
└── README.md           # Project documentation
