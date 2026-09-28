import sqlite3
import pandas as pd
import os

DB_NAME = "library.db"
EXCEL_FILE = "books.xlsx"

def import_books():
    if not os.path.exists(EXCEL_FILE):
        print(f"[ERROR] '{EXCEL_FILE}' not found in directory.")
        return

    # Read Excel file
    df = pd.read_excel(EXCEL_FILE)
    df.columns = df.columns.str.strip()

    title_col = "Book Title"
    author_col = "Primary Author(s)"
    category_col = "Subject / Field"

    if not {title_col, author_col, category_col}.issubset(df.columns):
        print(f"[ERROR] Required columns missing from {EXCEL_FILE}.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Drop existing table to fix column structure mismatches
    cursor.execute("DROP TABLE IF EXISTS books;")

    # Create table with correct schema
    cursor.execute("""
        CREATE TABLE books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            is_available INTEGER DEFAULT 1
        );
    """)

    added_count = 0
    for _, row in df.iterrows():
        title = str(row[title_col]).strip()
        author = str(row[author_col]).strip()
        category = str(row[category_col]).strip()

        if title and title.lower() != "nan":
            cursor.execute(
                "INSERT INTO books (title, author, category, is_available) VALUES (?, ?, ?, 1)",
                (title, author, category)
            )
            added_count += 1

    conn.commit()
    conn.close()
    print(f"[SUCCESS] Successfully imported {added_count} books into '{DB_NAME}'!")

if __name__ == "__main__":
    import_books()