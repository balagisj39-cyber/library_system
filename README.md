# 📚 Mini Library Management System

Welcome to the **Mini Library Management System**! 

This application allows you to search a database of 200+ books, register students, issue books, process returns with automatic fine calculation, and track borrowing logs using a web interface or terminal.

---

## 📌 Prerequisites (Before You Start)

Before running this project, ensure you have **Python** installed on your computer.

1. Download and install Python from [python.org](https://www.python.org/downloads/).
2. During installation, make sure to check the box that says **"Add Python to PATH"**.

---

## 🚀 How to Run the Project (Step-by-Step)

### Step 1: Open Your Terminal or Command Prompt
- **Windows**: Press the `Windows Key`, type `cmd`, and press `Enter`.
- **Mac**: Press `Cmd + Space`, type `Terminal`, and press `Enter`.

---

### Step 2: Navigate to the Project Folder
Type `cd` followed by the path to your project folder, then press `Enter`.

*Example for Windows:*
```cmd
cd C:\Users\YourName\Downloads\library_system-main
```
### Step 3: Install Required Dependencies
Copy and paste this command into your terminal, then press Enter:
     BASH
        py -m pip install -r requirements.txt
    (On Mac/Linux, use python3 instead of py)

    This installs the necessary background software (pandas, openpyxl, and streamlit).

### Step 4: Load the 200 Books into the Database
Run this command once to read books.xlsx and load all 200 books into your database:
         ```py import_books.py```
    
You should see a message saying:
     
     [SUCCESS] Successfully imported 200 books into 'library.db'!

### Step 5: Launch the Application
You can use the application in two ways:

## 🌐 Option A: Interactive Web UI (Recommended)
To open the graphical web dashboard in your browser, run:
         ``` py -m streamlit run app.py```

1.If Streamlit asks for an email on its first run, simply press Enter to skip it.                                                     
2.A new tab will automatically open in your web browser at http://localhost:8501.                                      
3.Use the left sidebar to switch between Neon Dark and Classic Light themes or navigate between modules!                                

## 💻 Option B: Command Line Interface (CLI)
If you prefer running the program inside your terminal, run:
          ``` py library.py```


```##📖 How to Use the Web Application:```

```#📊 Dashboard & Search:```
      Search for books by title, author, or subject (e.g., type Physics,   Dune, or Cal Newport).                                          
```#👤 Student Directory:```                                 
       Register a new student with their name and email.                                        
```#📖 Issue Book:```                                                                     
       Enter a Student ID and a Book ID to issue a book. The system automatically enforces borrowing limits.                                   
```#🔄 Return Book:```                                                                                     
       Enter a Book ID to process a return. Overdue fines are calculated automatically if the book is returned past its due date.                ```#📋 Transaction Audit Log:```                                                         
       View active loans and complete borrowing history.                                                          

```##📁 Repository Structure:```

├── app.py              # Interactive Web Interface (Streamlit)                                                 
├── library.py          # Core database logic & Command Line menu                                                    
├── import_books.py     # Excel dataset importer script                                                           
├── books.xlsx          # Dataset containing 200 catalog books                                                   
├── schema.sql          # Database table structure and performance indexes                                              
├── requirements.txt    # List of required external packages                                                            
└── README.md           # Beginner-friendly instructions                                                                        
