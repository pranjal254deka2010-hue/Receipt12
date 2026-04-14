import streamlit as st
from fpdf import FPDF
from datetime import datetime
import pandas as pd
import os

# --- APP SETUP ---
st.set_page_config(page_title="OPI Receipt Portal")

# Header on the Webpage
st.header("OXFORD PARAMEDICAL INSTITUTE")
st.write("Dhupdhara, Goalpara, Assam")

st.divider()

# --- FORM ---
with st.form("receipt_form"):
    name = st.text_input("Student Name")
    course = st.selectbox("Course", ["DMLT", "ICU Technology", "ECG Tech", "First Aid"])
    purpose = st.selectbox("Purpose", ["Monthly Fee", "Admission Fee", "Registration Fee", "Other"])
    months = st.text_input("Months (e.g. Jan-Feb)", "N/A")
    amount = st.number_input("Total Amount (₹)", min_value=0.0)
    mode = st.selectbox("Mode", ["Cash", "Online", "UPI"])
    
    submit = st.form_submit_button("Generate PDF")

if submit and name:
    # 1. Prepare Data
    today = datetime.now().strftime("%d-%m-%Y")
    
    # 2. Build PDF
    pdf = FPDF()
    pdf.add_page()
    
    # SIMPLE BORDER
    pdf.rect(5, 5, 200, 287)
    
    # LOGO (Top Left)
    if os.path.exists("logo.png"):
        pdf.image("logo.png", 12, 12, 35)
    
    # HEADER TEXT
    pdf.set_font("Arial", 'B', 16)
    pdf.set_xy(50, 15)
    pdf.cell(0, 10, "OXFORD PARAMEDICAL INSTITUTE", ln=True, align='L')
    
    pdf.set_font("Arial", 'B', 10)
    pdf.set_xy(50, 22)
    pdf.cell(0, 10, "Dhupdhara, Goalpara, Assam | ESTD. 2009", ln=True, align='L')
    
    pdf.ln(25)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "OFFICIAL FEES RECEIPT", ln=True, align='C')
    
    # RECEIPT CONTENT
    pdf.ln(15)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Date: {today}", ln=True, align='R')
    pdf.cell(0, 12, f"Student Name: {name.upper()}", border='B', ln=True)
    pdf.cell(0, 12, f"Course: {course}", border='B', ln=True)
    pdf.cell(0, 12, f"Purpose: {purpose} ({months})", border='B', ln=True)
    pdf.cell(0, 12, f"Payment Mode: {mode}", border='B', ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 15, f"TOTAL PAID: Rs. {amount}", border=1, ln=True, align='C')
    
    # SIGNATURE (Bottom Right)
    if os.path.exists("signature.png"):
        pdf.image("signature.png", 150, 160, 40)
        
    pdf.set_xy(140, 185)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(50, 10, "__________________________", ln=True, align='C')
    pdf.set_xy(140, 190)
    pdf.cell(50, 10, "Authorized Signatory", align='C')

    # DOWNLOAD
    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.success("Receipt Generated!")
    st.download_button("Download PDF", pdf_output, f"Receipt_{name}.pdf")
