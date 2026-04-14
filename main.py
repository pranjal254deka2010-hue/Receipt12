import streamlit as st
from fpdf import FPDF
from datetime import datetime
import pandas as pd
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="OPI Management Portal", layout="centered")

# --- DATABASE SETUP ---
STUDENT_FILE = "students.csv"
PAYMENT_FILE = "payments.csv"

for f in [STUDENT_FILE, PAYMENT_FILE]:
    if not os.path.exists(f):
        pd.DataFrame().to_csv(f, index=False)

# --- ADDRESS & HEADER ---
CAMPUS_ADDRESS = "Dhupdhara, Goalpara, Assam - 783123"

col1, col2 = st.columns([1, 3])
with col1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=140)
with col2:
    st.title("OXFORD PARAMEDICAL INSTITUTE")
    st.write(f"**{CAMPUS_ADDRESS}**")
    st.write("*ESTD. 2009 | Excellence in Healthcare Education*")

st.divider()

menu = st.sidebar.selectbox("MENU", ["Generate Receipt", "Payment History", "Student Records"])

# --- 1. GENERATE RECEIPT ---
if menu == "Generate Receipt":
    st.subheader("📝 Create Fees Receipt")
    with st.form("receipt_form"):
        name = st.text_input("Student Name")
        course = st.selectbox("Course", ["DMLT", "ICU Technology", "ECG Technician", "First Aid"])
        purpose = st.selectbox("Purpose", ["Monthly Fee", "Admission Fee", "Examination Fee", "Registration Fee", "Other"])
        
        # Multiple months logic
        num_m = 1
        m_range = "N/A"
        if purpose == "Monthly Fee":
            num_m = st.number_input("Number of Months", min_value=1, value=1)
            m_range = st.text_input("For Months (e.g. Jan to March)")

        mode = st.selectbox("Payment Mode", ["Cash", "Online", "UPI", "Cheque"])
        amt = st.number_input("Amount per Month (₹)", min_value=0.0)
        total = amt * num_m
        
        st.write(f"**Total to Pay: ₹{total}**")
        submit = st.form_submit_button("Generate PDF")

    if submit and name:
        date_str = datetime.now().strftime("%d-%m-%Y")
        receipt_id = f"OPI-{datetime.now().strftime('%H%M%S')}"
        
        # Save record
        new_data = pd.DataFrame([[date_str, receipt_id, name, purpose, m_range, total, mode]], 
                               columns=["Date", "ID", "Name", "Purpose", "Months", "Amount", "Mode"])
        new_data.to_csv(PAYMENT_FILE, mode='a', header=not os.path.exists(PAYMENT_FILE), index=False)

        # PDF GENERATION (Simple & Stable)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        
        # Header
        if os.path.exists("logo.png"):
            pdf.image("logo.png", 10, 10, 30)
        
        pdf.cell(0, 10, "OXFORD PARAMEDICAL INSTITUTE", ln=True, align='C')
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 5, CAMPUS_ADDRESS, ln=True, align='C')
        pdf.ln(20)
        
        # Receipt Content
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "OFFICIAL FEES RECEIPT", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font("Arial", '', 12)
        pdf.cell(100, 10, f"Receipt: {receipt_id}")
        pdf.cell(0, 10, f"Date: {date_str}", ln=True, align='R')
        pdf.ln(5)
        
        pdf.cell(0, 10, f"Student: {name.upper()}", border='B', ln=True)
        pdf.cell(0, 10, f"Course: {course}", border='B', ln=True)
        pdf.cell(0, 10, f"Purpose: {purpose} ({m_range})", border='B', ln=True)
        pdf.cell(0, 10, f"Mode: {mode}", border='B', ln=True)
        pdf.ln(10)
        
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 15, f"TOTAL PAID: Rs. {total}", border=1, ln=True, align='C')
        
        # Signature
        if os.path.exists("signature.png"):
            pdf.image("signature.png", 150, 150, 40)
        
        pdf.ln(30)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 10, "__________________________", ln=True, align='R')
        pdf.cell(0, 5, "Authorized Signatory      ", ln=True, align='R')

        pdf_bytes = pdf.output()
        st.success("Receipt Created!")
        st.download_button("Download PDF", pdf_bytes, f"{name}_receipt.pdf")

# --- OTHER SECTIONS ---
elif menu == "Payment History":
    st.subheader("Collection Records")
    if os.path.exists(PAYMENT_FILE):
        st.dataframe(pd.read_csv(PAYMENT_FILE))

elif menu == "Student Records":
    st.subheader("Student List")
    with st.expander("Add Student"):
        n = st.text_input("Full Name")
        if st.button("Save"):
            pd.DataFrame([[n]], columns=["Name"]).to_csv(STUDENT_FILE, mode='a', header=False, index=False)
            st.rerun()
    if os.path.exists(STUDENT_FILE):
        st.dataframe(pd.read_csv(STUDENT_FILE))
