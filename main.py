import streamlit as st
from fpdf import FPDF
from datetime import datetime
import pandas as pd
import os

# --- BASIC CONFIG ---
st.set_page_config(page_title="OPI Portal")

# --- DATA STORAGE ---
PAYMENT_FILE = "payments.csv"
if not os.path.exists(PAYMENT_FILE):
    pd.DataFrame(columns=["Date", "Name", "Purpose", "Amount"]).to_csv(PAYMENT_FILE, index=False)

# --- HEADER ---
st.title("OXFORD PARAMEDICAL INSTITUTE")
st.write("**Dhupdhara, Goalpara, Assam**")
st.write("ESTD. 2009")

st.divider()

# --- MENU ---
menu = st.sidebar.selectbox("Menu", ["Create Receipt", "View History"])

if menu == "Create Receipt":
    st.subheader("📝 New Receipt")
    with st.form("f1"):
        name = st.text_input("Student Name")
        course = st.selectbox("Course", ["DMLT", "ICU Tech", "ECG Tech", "First Aid"])
        purpose = st.selectbox("Purpose", ["Monthly Fee", "Admission Fee", "Registration Fee", "Other"])
        
        # Monthly Logic
        months = st.text_input("For Months (e.g., April-May)", value="N/A")
        amt = st.number_input("Total Amount (₹)", min_value=0.0)
        mode = st.selectbox("Mode", ["Cash", "Online", "UPI"])
        
        submit = st.form_submit_button("Generate PDF")

    if submit and name:
        # Save record
        date_now = datetime.now().strftime("%d-%m-%Y")
        new_rec = pd.DataFrame([[date_now, name, purpose, amt]], columns=["Date", "Name", "Purpose", "Amount"])
        new_rec.to_csv(PAYMENT_FILE, mode='a', header=False, index=False)

        # PDF - SIMPLE & STABLE
        pdf = FPDF()
        pdf.add_page()
        
        # Add Logo if it exists
        if os.path.exists("logo.png"):
            pdf.image("logo.png", 10, 8, 33)
            
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "OXFORD PARAMEDICAL INSTITUTE", ln=True, align='C')
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 5, "Dhupdhara, Goalpara, Assam", ln=True, align='C')
        pdf.ln(20)
        
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "FEES RECEIPT", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"Date: {date_now}", ln=True, align='R')
        pdf.cell(0, 10, f"Student: {name.upper()}", border='B', ln=True)
        pdf.cell(0, 10, f"Course: {course}", border='B', ln=True)
        pdf.cell(0, 10, f"Purpose: {purpose} ({months})", border='B', ln=True)
        pdf.cell(0, 10, f"Payment Mode: {mode}", border='B', ln=True)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 15, f"TOTAL PAID: Rs. {amt}", border=1, ln=True, align='C')
        
        # Add Signature if it exists
        if os.path.exists("signature.png"):
            pdf.image("signature.png", 150, 140, 40)
        
        pdf.ln(30)
        pdf.cell(0, 10, "__________________________", ln=True, align='R')
        pdf.cell(0, 5, "Authorized Signatory      ", ln=True, align='R')

        # Output
        pdf_out = pdf.output(dest='S').encode('latin-1')
        st.success("Receipt Created!")
        st.download_button("Download PDF", pdf_out, f"{name}_receipt.pdf")

elif menu == "View History":
    st.subheader("💰 Collection Records")
    if os.path.exists(PAYMENT_FILE):
        df = pd.read_csv(PAYMENT_FILE)
        st.dataframe(df)

