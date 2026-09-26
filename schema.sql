PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    max_limit INTEGER DEFAULT 3
);

CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT NOT NULL,
    is_available INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS issues (
    issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    issue_date TEXT NOT NULL,
    due_date TEXT NOT NULL,
    return_date TEXT,
    fine_amount REAL DEFAULT 0.0,
    FOREIGN KEY (student_id) REFERENCES students (student_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books (book_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_books_search ON books (title, author, category);
CREATE INDEX IF NOT EXISTS idx_issues_active ON issues (book_id, student_id) WHERE return_date IS NULL;