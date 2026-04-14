import streamlit as st
from fpdf import FPDF
from datetime import datetime
import pandas as pd
import os

# --- APP SETUP ---
st.set_page_config(page_title="OPI Receipt Portal")

# Header on the Webpage
st.markdown("<h2 style='text-align: center; color: #002e63;'>OXFORD PARAMEDICAL INSTITUTE</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>Dhupdhara, Goalpara, Assam</p>", unsafe_allow_html=True)

st.divider()

# --- FORM ---
with st.form("receipt_form"):
    name = st.text_input("Student Name")
    
    # Updated Course List
    course = st.selectbox("Course", [
        "DMLT", 
        "ICU TECHNICIAN", 
        "FIRST AID AND PATIENT CARE"
    ])
    
    # Updated Fee Purpose
    purpose = st.selectbox("Purpose of Payment", [
        "Monthly Fee", 
        "Admission Fee", 
        "Examination Fee", 
        "Registration Fee", 
        "Other"
    ])
    
    months = st.text_input("For Months (e.g. Jan-Feb)", "N/A")
    amount = st.number_input("Total Amount Paid (₹)", min_value=0.0)
    mode = st.selectbox("Payment Mode", ["Cash", "Online", "UPI", "Cheque"])
    
    submit = st.form_submit_button("Generate Official PDF")

if submit and name:
    today = datetime.now().strftime("%d-%m-%Y")
    
    # --- PDF GENERATION ---
    pdf = FPDF()
    pdf.add_page()
    
    # Simple Border
    pdf.rect(5, 5, 200, 287)
    
    # Logo (Top Left) - Matches the file name you uploaded
    if os.path.exists("logo.png"):
        pdf.image("logo.png", 12, 12, 35)
    
    # Header Text
    pdf.set_font("Arial", 'B', 16)
    pdf.set_xy(50, 15)
    pdf.cell(0, 10, "OXFORD PARAMEDICAL INSTITUTE", ln=True, align='L')
    
    pdf.set_font("Arial", 'B', 10)
    pdf.set_xy(50, 22)
    pdf.cell(0, 10, "Dhupdhara, Goalpara, Assam | ESTD. 2009", ln=True, align='L')
    
    pdf.ln(25)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "OFFICIAL FEES RECEIPT", ln=True, align='C')
    
    # Receipt Content
    pdf.ln(15)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Date: {today}", ln=True, align='R')
    pdf.cell(0, 12, f"Student Name: {name.upper()}", border='B', ln=True)
    pdf.cell(0, 12, f"Course: {course}", border='B', ln=True)
    pdf.cell(0, 12, f"Purpose: {purpose} ({months})", border='B', ln=True)
    pdf.cell(0, 12, f"Payment Mode: {mode}", border='B', ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 15, f"TOTAL PAID: Rs. {amount:,.2f}", border=1, ln=True, align='C')
    
    # Signature (Bottom Right)
    if os.path.exists("signature.png"):
        pdf.image("signature.png", 150, 160, 40)
        
    pdf.set_xy(140, 185)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(50, 10, "__________________________", ln=True, align='C')
    pdf.set_xy(140, 190)
    pdf.cell(50, 10, "Authorized Signatory", align='C')

    # Create Download
    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.success(f"Receipt for {name} generated successfully!")
    st.download_button("📥 Download PDF Receipt", pdf_output, f"OPI_Receipt_{name}.pdf")
