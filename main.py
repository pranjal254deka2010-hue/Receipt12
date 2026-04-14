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
    if not os.path.exists(f): pd.DataFrame().to_csv(f, index=False)

# --- ADDRESS & HEADER ---
CAMPUS_ADDRESS = "Dhupdhara, Goalpara, Assam - 783123"

col1, col2 = st.columns([1, 3])
with col1:
    if os.path.exists("logo.png"): st.image("logo.png", width=120)
with col2:
    st.markdown("<h1 style='color: #002e63; margin-bottom: 0;'>OXFORD PARAMEDICAL INSTITUTE</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #CC0000; font-weight: bold; margin:0;'>{CAMPUS_ADDRESS}</p>", unsafe_allow_html=True)

st.divider()

menu = st.sidebar.selectbox("MENU", ["Generate Receipt", "Payment History", "Mark Attendance", "Student Records"])

# --- 1. GENERATE RECEIPT ---
if menu == "Generate Receipt":
    st.markdown("### 📝 Fees Receipt")
    with st.form("receipt_form"):
        student_name = st.text_input("STUDENT NAME")
        course = st.selectbox("COURSE", ["DMLT", "ICU Technology", "ECG Technician", "First Aid"])
        
        fee_purpose = st.selectbox("PURPOSE", ["Monthly Fee", "Admission Fee", "Examination Fee", "Registration Fee", "Other"])
        
        # New Logic for Multiple Months
        num_months = 1
        month_range = "N/A"
        if fee_purpose == "Monthly Fee":
            c1, c2, c3 = st.columns(3)
            with c1: num_months = st.number_input("No. of Months", min_value=1, max_value=12, value=1)
            with c2: start_month = st.selectbox("From", ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
            with c3: end_month = st.selectbox("To", ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
            month_range = f"{start_month} to {end_month}" if num_months > 1 else start_month

        pay_mode = st.selectbox("PAYMENT MODE", ["Cash", "Online", "UPI", "Cheque"])
        amount_per_month = st.number_input("Amount per Month (₹)", min_value=0.0, step=100.0)
        total_amount = amount_per_month * num_months
        
        st.info(f"Total Amount to be Paid: ₹{total_amount:,.2f}")
        generate = st.form_submit_button("GENERATE BOLD RECEIPT")

    if generate and student_name:
        receipt_no = f"OPI-{datetime.now().strftime('%y%m%d%H%M')}"
        date_str = datetime.now().strftime("%d-%m-%Y")
        
        # Save to Database
        p_row = pd.DataFrame([[date_str, receipt_no, student_name, fee_purpose, month_range, total_amount, pay_mode]], 
                            columns=["Date", "Receipt_No", "Name", "Purpose", "Month", "Amount", "Mode"])
        p_row.to_csv(PAYMENT_FILE, mode='a', header=not os.path.exists(PAYMENT_FILE), index=False)

        # PDF GENERATION
        pdf = FPDF()
        pdf.add_page()
        pdf.set_line_width(1.0); pdf.rect(5, 5, 200, 287) # Double Border
        pdf.set_line_width(0.2); pdf.rect(6, 6, 198, 285)
        
        if os.path.exists("logo.png"): pdf.image("logo.png", 15, 12, 30)
        
        pdf.set_font("Arial", 'B', 18); pdf.set_text_color(0, 46, 99)
        pdf.set_xy(50, 15); pdf.cell(0, 10, "OXFORD PARAMEDICAL INSTITUTE", ln=True, align='C')
        pdf.set_font("Arial", 'B', 9); pdf.set_text_color(204, 0, 0)
        pdf.set_xy(50, 23); pdf.cell(0, 10, CAMPUS_ADDRESS, ln=True, align='C')
        
        pdf.ln(25); pdf.set_font("Arial", 'B', 14); pdf.set_text_color(0,0,0)
        pdf.cell(0, 10, "OFFICIAL FEES RECEIPT", ln=True, align='C')
        pdf.line(80, 62, 130, 62)
        
        pdf.ln(10); pdf.set_font("Arial", 'B', 11)
        pdf.cell(100, 10, f"Receipt No: {receipt_no}")
        pdf.cell(0, 10, f"Date: {date_str}", ln=True, align='R')
        
        pdf.ln(5); pdf.set_font("Arial", '', 12)
        pdf.cell(0, 12, f"Student Name:   {student_name.upper()}", border='B', ln=True)
        pdf.cell(0, 12, f"Course:               {course}", border='B', ln=True)
        
        # Purpose text with month range
        purpose_display = f"Purpose:             {fee_purpose}"
        if fee_purpose == "Monthly Fee":
            purpose_display += f" for {num_months} Month(s) ({month_range})"
        pdf.cell(0, 12, purpose_display, border='B', ln=True)
        
        pdf.cell(0, 12, f"Payment Mode:   {pay_mode}", border='B', ln=True)
        
        pdf.ln(10); pdf.set_font("Arial", 'B', 13); pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 15, f"TOTAL AMOUNT PAID: Rs. {total_amount:,.2f}", border=1, ln=True, align='C', fill=True)
        
        if os.path.exists("signature.png"): pdf.image("signature.png", 150, 170, 35)
        pdf.set_xy(140, 190); pdf.set_font("Arial", 'B', 10)
        pdf.cell(50, 10, "__________________________", ln=True, align='C')
        pdf.set_xy(140, 195); pdf.cell(50, 10, "Authorized Signatory", align='C')

        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.success(f"✅ Receipt for {num_months} month(s) generated!")
        st.download_button(label="📥 Download PDF", data=pdf_output, file_name=f"OPI_{student_name}.pdf")

# (Other menu sections...)
