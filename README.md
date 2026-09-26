# Mini Library Management System

A normalized relational database layer and CLI application built for Task 6 (WebX Selection Tasks).

## Features
- Student registration and book management.
- Case-insensitive book search by title, author, or category.
- Business rule enforcement (borrowing limits, availability checks).
- Dynamic overdue fine calculation upon return.

## Schema Overview (`schema.sql`)
- `students`: Stores student profiles and borrowing limits.
- `books`: Tracks book details and availability.
- `issues`: Tracks loans, due dates, return dates, and calculated fines.

## Requirements
- Python 3.x (Uses standard library packages: `sqlite3`, `os`, `datetime`)

## How to Run
```bash
python library.py
