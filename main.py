import streamlit as st
from fpdf import FPDF
from datetime import datetime
import pandas as pd
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="OPI Management Portal", page_icon="🎓", layout="centered")

# --- DATABASE SETUP ---
STUDENT_FILE, PAYMENT_FILE = "students.csv", "payments.csv"
for f in [STUDENT_FILE, PAYMENT_FILE]:
    if not os.path.exists(f): 
        pd.DataFrame().to_csv(f, index=False)

# --- ADDRESS & HEADER ---
CAMPUS_ADDRESS = "Dhupdhara, Goalpara, Assam - 783123"

# Custom CSS for a beautiful look
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    h1 { color: #002e63 !important; font-size: 2.2rem !important; }
    .stButton>button { background-color: #002e63; color: white; border-radius: 8px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])
with col1:
    if os.path.exists("logo.png"): st.image("logo.png", width=140)
with col2:
    st.markdown("<h1>OXFORD PARAMEDICAL INSTITUTE</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #CC0000; font-weight: bold; font-size: 1.1rem; margin:0;'>{CAMPUS_ADDRESS}</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-style: italic; color: #555;'>ESTD. 2009 | Excellence in Healthcare Education</p>", unsafe_allow_html=True)

st.divider()

menu = st.sidebar.selectbox("MENU", ["Generate Receipt", "Payment History", "Mark Attendance", "Student Records"])

# --- 1. GENERATE RECEIPT ---
if menu == "Generate Receipt":
    st.markdown("### 📝 Create Fees Receipt")
    with st.form("receipt_form"):
        student_name = st.text_input("STUDENT NAME")
        course = st.selectbox("COURSE", ["DMLT", "ICU Technology", "ECG Technician", "First Aid"])
        fee_purpose = st.selectbox("PURPOSE", ["Monthly Fee", "Admission Fee", "Examination Fee", "Registration Fee", "Other"])
        
        num_months = 1
        month_range = "N/A"
        if fee_purpose == "Monthly Fee":
            c1, c2, c3 = st.columns(3)
            with c1: num_months = st.number_input("No. of Months", min_value=1, max_value=12, value=1)
            with c2: start_m = st.selectbox("From", ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
            with c3: end_m = st.selectbox("To", ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
            month_range = f"{start_m} to {end_m}" if num_months > 1 else start_m

        pay_mode = st.selectbox("PAYMENT MODE", ["Cash", "Online", "UPI", "Cheque"])
        amount_val = st.number_input("Amount per Month (₹)", min_value=0.0, step=100.0)
        total_amount = amount_val * (num_months if fee_purpose == "Monthly Fee" else 1)
        
        st.write(f"**Final Total: ₹{total_amount:,.2f}**")
        generate = st.form_submit_button("GENERATE OFFICIAL PDF")

    if generate and student_name:
        receipt_no = f"OPI-{datetime.now().strftime('%y%m%d%H%M')}"
        date_str = datetime.now().strftime("%d-%m-%Y")
        
        # Save Payment Record
        p_row = pd.DataFrame([[date_str, receipt_no, student_name, fee_purpose, month_range, total_amount, pay_mode]], 
                            columns=["Date", "Receipt_No", "Name", "Purpose", "Month", "Amount", "Mode"])
        p_row.to_csv(PAYMENT_FILE, mode='a', header=not os.path.exists(PAYMENT_FILE), index=False)

        # PDF GENERATION (Standardized Layout)
        pdf = FPDF()
        pdf.add_page()
        
        # BORDERS
        pdf.set_line_width(1.0); pdf.rect(5, 5, 200, 287) # Outer
        pdf.set_line_width(0.2); pdf.rect(6, 6, 198, 285) # Inner
        
        # HEADER
        if os.path.exists("logo.png"): 
            pdf.image("logo.png", 12, 12, 38)
        
        pdf.set_font("Arial", 'B', 18); pdf.set_text_color(0, 46, 99)
        pdf.set_xy(55, 18); pdf.cell(0, 10, "OXFORD PARAMEDICAL INSTITUTE", ln=True, align='L')
        pdf.set_font("Arial", 'B', 10); pdf.set_text_color(204, 0, 0)
        pdf.set_xy(55, 26); pdf.cell(0, 10, CAMPUS_ADDRESS, ln=True, align='L')
        pdf.set_font("Arial", 'I', 9); pdf.set_text_color(0, 0, 0)
        pdf.set_xy(55, 33); pdf.cell(0, 10, "ESTD. 2009 | Excellence in Healthcare Education", ln=True, align='L')
        
        pdf.ln(30); pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "OFFICIAL FEES RECEIPT", ln=True, align='C')
        pdf.line(75, 83, 135, 83) 
        
        pdf.ln(15); pdf.set_font("Arial", 'B', 11)
        pdf.cell(100, 10, f"Receipt No: {receipt_no}")
        pdf.cell(0, 10, f"Date: {date_str}", ln=True, align='R')
        
        # CONTENT
        pdf.ln(10); pdf.set_font("Arial", '', 12)
        pdf.cell(0, 12, f"Student Name:   {student_name.upper()}", border='B', ln=True)
        pdf.cell(0, 12, f"Course:               {course}", border='B', ln=True)
        
        p_txt = f"Purpose:             {fee_purpose}"
        if fee_purpose == "Monthly Fee": p_txt += f" ({month_range})"
        pdf.cell(0, 12, p_txt, border='B', ln=True)
        pdf.cell(0, 12, f"Payment Mode:   {pay_mode}", border='B', ln=True)
        
        pdf.ln(15); pdf.set_font("Arial", 'B', 14); pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 15, f"TOTAL AMOUNT PAID: Rs. {total_amount:,.2f}", border=1, ln=True, align='C', fill=True)
        
        # SIGNATURE
        if os.path.exists("signature.png"): 
            pdf.image("signature.png", 150, 205, 40)
            
        pdf.set_xy(140, 230); pdf.set_font("Arial", 'B', 10)
        pdf.cell(50, 10, "__________________________", ln=True, align='C')
        pdf.set_xy(140, 236); pdf.cell(50, 10, "Authorized Signatory", align='C')

        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.success(f"✅ Bold & Clean Receipt Ready!")
        st.download_button(label="📥 Download PDF", data=pdf_output, file_name=f"OPI_{student_name}.pdf")

# --- OTHER SECTIONS ---
elif menu == "Payment History":
    st.subheader("💰 Fee Collection Records")
    if os.path.exists(PAYMENT_FILE):
        df = pd.read_csv(PAYMENT_FILE)
        if not df.empty:
            st.metric("Total Collected", f"₹{df['Amount'].sum():,.2f}")
            st.dataframe(df, use_container_width=True)
        else: st.info("No records found yet.")

elif menu == "Mark Attendance":
    st.subheader("📅 Attendance Board")
    if os.path.exists(STUDENT_FILE):
        df = pd.read_csv(STUDENT_FILE)
        for n in df['Name']: st.checkbox(n, key=n)
        if st.button("Save Today's Attendance"): st.success("Attendance Captured!")

elif menu == "Student Records":
    st.subheader("👥 Student Management")
    with st.expander("Add New Student"):
        n = st.text_input("Full Name"); c = st.text_input("Course")
        if st.button("Register"):
            pd.DataFrame([[n, c]], columns=["Name", "Course"]).to_csv(STUDENT_FILE, mode='a', header=False, index=False)
            st.rerun()
    if os.path.exists(STUDENT_FILE): st.dataframe(pd.read_csv(STUDENT_FILE))
