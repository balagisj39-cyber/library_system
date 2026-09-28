import streamlit as st
import sqlite3
import pandas as pd
from datetime import date, timedelta

DB_NAME = "library.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# Page Configuration
st.set_page_config(
    page_title="Mini Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Theme Selector in Sidebar ---
st.sidebar.markdown("### 🎨 Theme Settings")
theme = st.sidebar.radio("Select Style Variant:", ["Neon Dark (Blue & Black)", "Classic Light"], index=0)

# --- Dynamic CSS Injection ---
if theme == "Neon Dark (Blue & Black)":
    st.markdown("""
        <style>
        /* Force App Background in Dark Variant */
        .stApp {
            background: linear-gradient(135deg, #0a0e17 0%, #030508 100%) !important;
        }

        /* High Contrast White Headers & Text for Dark Mode */
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, 
        .stApp p, .stApp label, .stApp .stMarkdown, .stApp span:not([data-baseweb="tag"]) {
            color: #ffffff !important;
        }

        /* Metric Cards */
        div[data-testid="stMetric"] {
            background: #111827 !important;
            padding: 16px !important;
            border-radius: 12px !important;
            border: 1px solid #00d2ff !important;
            box-shadow: 0px 0px 15px rgba(0, 210, 255, 0.25) !important;
        }

        div[data-testid="stMetricValue"] {
            font-size: 2.2rem !important;
            font-weight: 800 !important;
            color: #00d2ff !important;
        }

        div[data-testid="stMetricLabel"] {
            color: #ffffff !important;
            font-weight: 600 !important;
        }

        /* Input Fields */
        input, textarea, select, div[role="combobox"] {
            background-color: #1a2234 !important;
            color: #ffffff !important;
            border: 1px solid #00d2ff !important;
            border-radius: 8px !important;
        }

        /* Header Banner */
        .header-banner {
            background: linear-gradient(90deg, #00112c 0%, #0052d4 50%, #4364f7 100%);
            padding: 24px;
            border-radius: 16px;
            margin-bottom: 24px;
            border: 1px solid #00d2ff;
            box-shadow: 0px 0px 20px rgba(0, 210, 255, 0.4);
        }

        .header-banner h1, .header-banner p {
            color: #ffffff !important;
            margin: 0;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #080d1a 0%, #02040a 100%) !important;
            border-right: 1px solid #00d2ff !important;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label {
            background-color: #0d1527 !important;
            border-radius: 10px !important;
            margin-bottom: 8px !important;
            border: 1px solid #1e293b !important;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label span {
            color: #ffffff !important;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
            background: linear-gradient(90deg, #0052d4 0%, #00d2ff 100%) !important;
            box-shadow: 0px 0px 12px rgba(0, 210, 255, 0.6) !important;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid #00d2ff !important;
            border-radius: 10px !important;
        }
        </style>
    """, unsafe_allow_html=True)

else:
    # Classic Light Mode Custom CSS
    st.markdown("""
        <style>
        /* Force App Background in Light Variant */
        .stApp {
            background-color: #f8f9fa !important;
        }

        /* Dark High-Contrast Text for Light Mode */
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, 
        .stApp p, .stApp label, .stApp .stMarkdown, .stApp span {
            color: #0f172a !important;
        }

        /* Metric Cards */
        div[data-testid="stMetric"] {
            background: #ffffff !important;
            padding: 16px !important;
            border-radius: 12px !important;
            border-left: 5px solid #2563eb !important;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05) !important;
            border-top: 1px solid #e2e8f0 !important;
            border-right: 1px solid #e2e8f0 !important;
            border-bottom: 1px solid #e2e8f0 !important;
        }

        div[data-testid="stMetricValue"] {
            font-size: 2.2rem !important;
            font-weight: 800 !important;
            color: #2563eb !important;
        }

        div[data-testid="stMetricLabel"] {
            color: #475569 !important;
            font-weight: 600 !important;
        }

        /* Input Fields */
        input, textarea, select, div[role="combobox"] {
            background-color: #ffffff !important;
            color: #0f172a !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 8px !important;
        }

        /* Header Banner */
        .header-banner {
            background: linear-gradient(90deg, #1e3a8a 0%, #2563eb 100%);
            padding: 24px;
            border-radius: 16px;
            margin-bottom: 24px;
            box-shadow: 0px 4px 12px rgba(37, 99, 235, 0.2);
        }

        .header-banner h1, .header-banner p {
            color: #ffffff !important;
            margin: 0;
        }

        /* Sidebar Light Theme */
        section[data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 2px solid #e2e8f0 !important;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label {
            background-color: #f1f5f9 !important;
            border-radius: 10px !important;
            margin-bottom: 8px !important;
            border: 1px solid #cbd5e1 !important;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label span {
            color: #0f172a !important;
            font-weight: 600 !important;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
            background: #2563eb !important;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] span {
            color: #ffffff !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Visual Header Banner
st.markdown("""
    <div class="header-banner">
        <h1>📚 Mini Library Management System</h1>
        <p>Fast, Normalized SQLite Relational Database & Management Console</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📖 Console Navigation")

menu = [
    "📊 Dashboard & Search",
    "📖 Issue Book",
    "🔄 Return Book",
    "👤 Student Directory",
    "➕ Add New Book",
    "📋 Transaction Audit Log"
]
choice = st.sidebar.radio("Navigation Menu", menu, label_visibility="collapsed")

st.sidebar.markdown("---")

# --- 1. Dashboard & Search ---
if choice == "📊 Dashboard & Search":
    with get_connection() as conn:
        total_books = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
        issued_books = conn.execute("SELECT COUNT(*) FROM books WHERE is_available = 0").fetchone()[0]
        available_books = total_books - issued_books
        students_count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Catalog Books", total_books)
    kpi2.metric("Available On Shelf", available_books)
    kpi3.metric("Currently Issued", issued_books)
    kpi4.metric("Registered Students", students_count)

    st.markdown("---")
    st.subheader("🔍 Search Catalog")
    
    query = st.text_input("Enter Title, Author, or Category/Subject (e.g., 'Physics', 'Dune', 'Cal Newport'):")

    with get_connection() as conn:
        clean_query = query.strip().lower()
        search_terms = {clean_query} if clean_query else {""}

        if "physics" in clean_query or "physic" in clean_query:
            search_terms.update(["physic", "physics", "quantum", "thermodynamic", "mechanic", "astrophysic", "optics"])
        elif "math" in clean_query or "mathematics" in clean_query:
            search_terms.update(["math", "mathematic", "algebra", "geometry", "calculus", "topology"])
        elif "cs" in clean_query or "computer" in clean_query:
            search_terms.update(["computer", "programming", "software", "data", "algorithm", "code"])

        where_clauses = []
        params = []
        for term in search_terms:
            pattern = f"%{term}%"
            where_clauses.append("(LOWER(title) LIKE ? OR LOWER(author) LIKE ? OR LOWER(category) LIKE ?)")
            params.extend([pattern, pattern, pattern])

        sql = f"""
            SELECT book_id AS 'Book ID', title AS 'Title', author AS 'Author', category AS 'Category', 
                   CASE WHEN is_available = 1 THEN 'Available' ELSE 'Issued (Unavailable)' END AS 'Status' 
            FROM books 
            WHERE {' OR '.join(where_clauses)}
        """
        
        df = pd.read_sql_query(sql, conn, params=params)

    st.success(f"Found **{len(df)}** matching results:")
    st.dataframe(df, use_container_width=True)

# --- 2. Issue Book ---
elif choice == "📖 Issue Book":
    st.subheader("📖 Issue Book Transaction")
    
    col1, col2 = st.columns(2)
    with col1:
        student_id = st.number_input("Enter Student ID", min_value=1, step=1)
    with col2:
        book_id = st.number_input("Enter Book ID", min_value=1, step=1)

    days_allowed = st.slider("Borrowing Period (Days)", min_value=1, max_value=30, value=14)

    if st.button("🚀 Issue Book", type="primary"):
        with get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT name, max_limit FROM students WHERE student_id = ?", (student_id,))
            student = cursor.fetchone()
            
            if not student:
                st.error("❌ Student ID not found in database.")
            else:
                cursor.execute("SELECT COUNT(*) FROM issues WHERE student_id = ? AND return_date IS NULL", (student_id,))
                active_count = cursor.fetchone()[0]
                
                if active_count >= student["max_limit"]:
                    st.error(f"❌ Student '{student['name']}' has reached their limit of {student['max_limit']} books.")
                else:
                    cursor.execute("UPDATE books SET is_available = 0 WHERE book_id = ? AND is_available = 1", (book_id,))
                    if cursor.rowcount == 0:
                        st.error("❌ Book ID is either invalid or currently unavailable.")
                    else:
                        issue_date = date.today().isoformat()
                        due_date = (date.today() + timedelta(days=days_allowed)).isoformat()
                        
                        cursor.execute("""
                            INSERT INTO issues (student_id, book_id, issue_date, due_date)
                            VALUES (?, ?, ?, ?)
                        """, (student_id, book_id, issue_date, due_date))
                        conn.commit()
                        st.balloons()
                        st.success(f"🎉 Issued successfully to {student['name']}! Due Date: **{due_date}**")

# --- 3. Return Book ---
elif choice == "🔄 Return Book":
    st.subheader("🔄 Return Borrowed Book")
    
    col1, col2 = st.columns(2)
    with col1:
        book_id = st.number_input("Enter Book ID to Return", min_value=1, step=1)
    with col2:
        fine_rate = st.number_input("Fine Rate per Day (Rs.)", value=5.0, step=1.0)

    if st.button("📥 Return Book", type="primary"):
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
                st.error("❌ No active borrowing record found for this Book ID.")
            else:
                return_date = date.today()
                due_date = date.fromisoformat(issue["due_date"])
                overdue_days = (return_date - due_date).days
                fine = max(0.0, overdue_days * fine_rate) if overdue_days > 0 else 0.0

                cursor.execute("""
                    UPDATE issues SET return_date = ?, fine_amount = ? WHERE issue_id = ?
                """, (return_date.isoformat(), fine, issue["issue_id"]))
                
                cursor.execute("UPDATE books SET is_available = 1 WHERE book_id = ?", (book_id,))
                conn.commit()

                st.success(f"✅ '{issue['book_title']}' returned by {issue['student_name']}.")
                if fine > 0:
                    st.warning(f"⚠️ Overdue by **{overdue_days} days**. Fine Amount Due: **Rs.{fine:.2f}**")

# --- 4. Student Directory ---
elif choice == "👤 Student Directory":
    st.subheader("👤 Student Registration & Directory")
    
    tab1, tab2 = st.tabs(["Register New Student", "Student Directory"])
    
    with tab1:
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        limit = st.number_input("Max Borrowing Limit", min_value=1, max_value=10, value=3)

        if st.button("Register Student", type="primary"):
            if name and email:
                try:
                    with get_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO students (name, email, max_limit) VALUES (?, ?, ?)", (name, email, limit))
                        conn.commit()
                        st.success(f"✅ Registered '{name}' successfully with Student ID: **{cursor.lastrowid}**")
                except sqlite3.IntegrityError:
                    st.error("❌ A student with this email address is already registered.")
            else:
                st.warning("Please fill in all fields.")

    with tab2:
        with get_connection() as conn:
            df_students = pd.read_sql_query("SELECT student_id AS 'Student ID', name AS 'Name', email AS 'Email', max_limit AS 'Borrow Limit' FROM students", conn)
            st.dataframe(df_students, use_container_width=True)

# --- 5. Add New Book ---
elif choice == "➕ Add New Book":
    st.subheader("➕ Add New Book Entry")
    
    title = st.text_input("Book Title")
    author = st.text_input("Author(s)")
    category = st.text_input("Category / Subject Field")

    if st.button("Add Book to Database", type="primary"):
        if title and author and category:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO books (title, author, category, is_available) VALUES (?, ?, ?, 1)", (title, author, category))
                conn.commit()
                st.success(f"✅ Successfully added '{title}' with Book ID: **{cursor.lastrowid}**")
        else:
            st.warning("Please fill in all fields.")

# --- 6. Transaction Audit Log ---
elif choice == "📋 Transaction Audit Log":
    st.subheader("📋 Complete Audit History")
    
    tab1, tab2 = st.tabs(["Active Loans", "Complete Historical Log"])
    
    with tab1:
        with get_connection() as conn:
            df_borrowed = pd.read_sql_query("""
                SELECT i.issue_id AS 'Issue ID', b.title AS 'Book Title', s.name AS 'Student Name', 
                       i.issue_date AS 'Issued Date', i.due_date AS 'Due Date'
                FROM issues i
                JOIN books b ON i.book_id = b.book_id
                JOIN students s ON i.student_id = s.student_id
                WHERE i.return_date IS NULL
            """, conn)
            st.dataframe(df_borrowed, use_container_width=True)

    with tab2:
        with get_connection() as conn:
            df_audit = pd.read_sql_query("""
                SELECT i.issue_id AS 'Tx #', b.title AS 'Book Title', s.name AS 'Student Name', 
                       i.issue_date AS 'Issued', i.due_date AS 'Due', 
                       COALESCE(i.return_date, 'Active / Not Returned') AS 'Returned Date', 
                       i.fine_amount AS 'Fine Amount (Rs.)'
                FROM issues i
                JOIN books b ON i.book_id = b.book_id
                JOIN students s ON i.student_id = s.student_id
                ORDER BY i.issue_id DESC
            """, conn)
            st.dataframe(df_audit, use_container_width=True)