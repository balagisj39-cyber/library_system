# Mini Library Management System

A normalized relational database layer and CLI application built for Task 6 (WebX Selection Tasks)[cite: 1].

## Features
- Student registration and book management[cite: 1].
- Case-insensitive book search by title, author, or category[cite: 1].
- Business rule enforcement (borrowing limits, availability checks)[cite: 1].
- Dynamic overdue fine calculation upon return[cite: 1].

## Schema Overview (`schema.sql`)
- `students`: Stores student profiles and borrowing limits[cite: 1].
- `books`: Tracks book details and availability[cite: 1].
- `issues`: Tracks loans, due dates, return dates, and calculated fines[cite: 1].

## Requirements
- Python 3.x (Uses standard library packages: `sqlite3`, `os`, `datetime`)[cite: 1]

## How to Run
```bash
python library.py
