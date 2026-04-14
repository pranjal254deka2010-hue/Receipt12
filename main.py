import streamlit as st
from fpdf import FPDF
from datetime import datetime
import pandas as pd
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="OPI Management Portal", page_icon="🎓", layout="centered")

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #002e63;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
col1, col2 = st.columns([1, 4])
with col1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=100)
with col2:
    st.markdown("<h2 style='color: #002e63; margin-bottom: 0;'>OXFORD PARAMEDICAL INSTITUTE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='margin-top: 0;'>ESTD. 2009 | Excellence in Healthcare Education</p>", unsafe_allow_html=True)

st.divider()

# --- APP NAVIGATION ---
menu = st.sidebar.selectbox("MENU", ["Generate Receipt", "Mark Attendance", "Student Records"])

# --- DATABASE SETUP (CSV) ---
if not os.path.exists("students.csv"):
    pd.DataFrame(columns=["Name", "Course", "Phone"]).to_csv("students.csv", index=False)

# --- 1. GENERATE RECEIPT ---
if menu == "Generate Receipt":
    st.subheader("📝 Fee Receipt Generator")
    
    with st.form("receipt_form"):
        receipt_no = f"OPI-{datetime.now().strftime('%y%m%s')[:6]}"
        date_str = datetime.now().strftime("%d %b, %Y")
        
        student_name = st.text_input("STUDENT NAME")
        course = st.selectbox("COURSE ENROLLED", ["DMLT", "ICU Technology", "ECG Technician", "First Aid"])
        pay_mode = st.radio("PAYMENT MODE", ["Online", "Cash", "Cheque"], horizontal=True)
        amount = st.number_input("AMOUNT RECEIVED (₹)", min_value=0.0, step=500.0)
        
        generate = st.form_submit_button("Generate Professional PDF")

    if generate and student_name:
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Add Border
        pdf.rect(5, 5, 200, 287)
        
        # Header in PDF
        if os.path.exists("logo.png"):
            pdf.image("logo.png", 10, 10, 25)
        
        pdf.set_font("Arial", 'B', 16)
        pdf.set_text_color(0, 46, 99)
        pdf.cell(0, 10, "OXFORD PARAMEDICAL INSTITUTE", ln=True, align='C')
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 5, "ESTD. 2009", ln=True, align='C')
        pdf.cell(0, 5, "Excellence in Healthcare Education", ln=True, align='C')
        pdf.ln(15)
        
        # Receipt Details
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "FEES RECEIPT", ln=True, align='C')
        pdf.ln(5)
        
        pdf.set_font("Arial", '', 11)
        pdf.cell(100, 10, f"Receipt No: {receipt_no}")
        pdf.cell(0, 10, f"Date: {date_str}", ln=True, align='R')
        pdf.line(10, 65, 200, 65)
        pdf.ln(10)
        
        pdf.cell(0, 10, f"STUDENT NAME: {student_name.upper()}", ln=True)
        pdf.cell(0, 10, f"COURSE ENROLLED: {course}", ln=True)
        pdf.cell(0, 10, f"PAYMENT MODE: {pay_mode}", ln=True)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 15, f"AMOUNT RECEIVED: Rs. {amount:,.2f}", ln=True)
        
        pdf.ln(20)
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(0, 10, "This is a computer generated receipt.", align='C')

        # Download Button
        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.success(f"Receipt for {student_name} generated!")
        st.download_button(label="⬇️ Download PDF Receipt", data=pdf_output, file_name=f"OPI_Receipt_{student_name}.pdf", mime="application/pdf")

# --- 2. ATTENDANCE ---
elif menu == "Mark Attendance":
    st.subheader(f"📅 Attendance: {datetime.now().strftime('%d-%m-%Y')}")
    df = pd.read_csv("students.csv")
    
    if df.empty:
        st.info("Please add students in 'Student Records' first.")
    else:
        attendance_data = []
        for index, row in df.iterrows():
            status = st.checkbox(f"{row['Name']} ({row['Course']})", key=row['Name'])
            attendance_data.append({"Name": row['Name'], "Status": "Present" if status else "Absent"})
        
        if st.button("Save Today's Attendance"):
            att_df = pd.DataFrame(attendance_data)
            att_df['Date'] = datetime.now().strftime('%Y-%m-%d')
            att_df.to_csv("attendance.csv", mode='a', index=False, header=not os.path.exists("attendance.csv"))
            st.success("Attendance Recorded!")

# --- 3. STUDENT RECORDS ---
elif menu == "Student Records":
    st.subheader("👥 Student Management")
    
    # Add Student
    with st.expander("Add New Student"):
        new_name = st.text_input("Name")
        new_course = st.selectbox("Course", ["DMLT", "ICU Tech", "First Aid"], key="new_course")
        new_phone = st.text_input("Phone Number")
        if st.button("Save Student"):
            new_row = pd.DataFrame([[new_name, new_course, new_phone]], columns=["Name", "Course", "Phone"])
            new_row.to_csv("students.csv", mode='a', header=False, index=False)
            st.success("Student Added!")
            st.rerun()

    # View Data
    df = pd.read_csv("students.csv")
    st.dataframe(df, use_container_width=True)
