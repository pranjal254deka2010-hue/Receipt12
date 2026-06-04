import streamlit as st
from fpdf import FPDF
from datetime import datetime
import pandas as pd
import os

# --- APP SETUP ---
st.set_page_config(page_title="OSDC Receipt Portal")

# Header on the Webpage
st.markdown("<h2 style='text-align: center; color: #002e63;'>OXFORD SKILL DEVELOPMENT CENTRE</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>Dhupdhara, Goalpara, Assam</p>", unsafe_allow_html=True)

st.divider()

# --- FORM ---
with st.form("receipt_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Student Name")
    with col2:
        # Generates a sequential receipt number using the current timestamp context
        receipt_no = st.text_input("Receipt No.", value=datetime.now().strftime("OSDC-%Y%m%d%H%M%S"))

    # Updated Course List
    course = st.selectbox("Course", [
        "DMLT", 
        "ICU TECHNICIAN", 
        "FIRST AID AND PATIENT CARE"
    ])
    
    # Dynamic Academic Timeline Mapping
    # Sets the default session timeline for the first-year student lifecycle
    session_year = st.selectbox("Academic Session", ["May 2026 - May 2028", "Current Active Batch"])
    
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
    pdf.cell(0, 10, "OXFORD SKILL DEVELOPMENT CENTRE", ln=True, align='L')
    
    pdf.set_font("Arial", 'B', 10)
    pdf.set_xy(50, 22)
    pdf.cell(0, 10, "Dhupdhara, Goalpara, Assam | ESTD. 2009", ln=True, align='L')
    
    pdf.ln(25)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "OFFICIAL FEES RECEIPT", ln=True, align='C')
    
    # Receipt Content Details
    pdf.ln(15)
    pdf.set_font("Arial", '', 12)
    
    # Meta columns for Document layout alignment
    pdf.cell(100, 10, f"Receipt No: {receipt_no}", ln=False, align='L')
    pdf.cell(0, 10, f"Date: {today}", ln=True, align='R')
    pdf.set_xy(10, pdf.get_y() + 5)
    
    pdf.cell(0, 12, f"Student Name: {name.upper()}", border='B', ln=True)
    pdf.cell(0, 12, f"Course: {course}", border='B', ln=True)
    pdf.cell(0, 12, f"Academic Session: {session_year}", border='B', ln=True)
    pdf.cell(0, 12, f"Purpose: {purpose} ({months})", border='B', ln=True)
    pdf.cell(0, 12, f"Payment Mode: {mode}", border='B', ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 15, f"TOTAL PAID: Rs. {amount:,.2f}", border=1, ln=True, align='C')
    
    # Signature (Bottom Right)
    if os.path.exists("signature.png"):
        pdf.image("signature.png", 150, 180, 40)
        
    pdf.set_xy(140, 205)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(50, 10, "__________________________", ln=True, align='C')
    pdf.set_xy(140, 210)
    pdf.cell(50, 10, "Authorized Signatory", align='C')

    # Encoding processing layout configuration
    try:
        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.success(f"Receipt for {name} generated successfully!")
        st.download_button("📥 Download PDF Receipt", pdf_output, f"OSDC_Receipt_{name}.pdf")
    except Exception as e:
        st.error(f"Error compiling layout content into PDF formatting: {e}")
