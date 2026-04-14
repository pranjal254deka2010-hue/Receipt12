import streamlit as st
from fpdf import FPDF
from datetime import datetime
import pandas as pd
import os

# --- APP SETUP ---
st.set_page_config(page_title="OPI Portal", layout="centered")

# File to save payment history
PAY_LOG = "payments.csv"
if not os.path.exists(PAY_LOG):
    pd.DataFrame(columns=["Date", "Name", "Purpose", "Amount", "Mode"]).to_csv(PAY_LOG, index=False)

# --- WEB INTERFACE ---
st.markdown("<h1 style='text-align: center; color: #002e63;'>OXFORD PARAMEDICAL INSTITUTE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>Dhupdhara, Goalpara, Assam</p>", unsafe_allow_html=True)

st.divider()

# Sidebar Menu
menu = st.sidebar.selectbox("Select Action", ["New Receipt", "View History"])

if menu == "New Receipt":
    st.subheader("📝 Generate New Receipt")
    
    with st.form("receipt_form"):
        name = st.text_input("Student Name")
        course = st.selectbox("Course", ["DMLT", "ICU Technology", "ECG Tech", "First Aid"])
        purpose = st.selectbox("Purpose", ["Monthly Fee", "Admission Fee", "Registration Fee", "Other"])
        
        # Simple Month Logic
        months = st.text_input("For Months (e.g., April to June)", value="N/A")
        
        amount = st.number_input("Total Amount Paid (₹)", min_value=0.0)
        mode = st.selectbox("Payment Mode", ["Cash", "Online", "UPI", "Cheque"])
        
        submit = st.form_submit_button("Create PDF Receipt")

    if submit and name:
        today = datetime.now().strftime("%d-%m-%Y")
        
        # 1. Save to History
        new_entry = pd.DataFrame([[today, name, purpose, amount, mode]], columns=["Date", "Name", "Purpose", "Amount", "Mode"])
        new_entry.to_csv(PAY_LOG, mode='a', header=False, index=False)

        # 2. Build PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Add a simple border
        pdf.rect(5, 5, 200, 287)
        
        # Header - Check for Logo
        if os.path.exists("logo.png"):
            pdf.image("logo.png", 10, 10, 30)
        
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "OXFORD PARAMEDICAL INSTITUTE", ln=True, align='C')
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 5, "Dhupdhara, Goalpara, Assam | ESTD. 2009", ln=True, align='C')
        pdf.ln(20)
        
        # Receipt Body
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "OFFICIAL FEES RECEIPT", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"Date: {today}", ln=True, align='R')
        pdf.cell(0, 12, f"Student: {name.upper()}", border='B', ln=True)
        pdf.cell(0, 12, f"Course: {course}", border='B', ln=True)
        pdf.cell(0, 12, f"Purpose: {purpose} ({months})", border='B', ln=True)
        pdf.cell(0, 12, f"Payment Mode: {mode}", border='B', ln=True)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 15, f"TOTAL PAID: Rs. {amount:,.2f}", border=1, ln=True, align='C')
        
        # Check for Signature
        if os.path.exists("signature.png"):
            pdf.image("signature.png", 150, 160, 40)
            
        pdf.ln(40)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 10, "__________________________", ln=True, align='R')
        pdf.cell(0, 5, "Authorized Signatory      ", ln=True, align='R')

        # Output the PDF
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.success("✅ Success! Receipt is ready.")
        st.download_button("Download PDF", pdf_bytes, f"Receipt_{name}.pdf")

elif menu == "View History":
    st.subheader("💰 Payment Records")
    if os.path.exists(PAY_LOG):
        df = pd.read_csv(PAY_LOG)
        st.dataframe(df, use_container_width=True)
        st.download_button("Export to Excel (CSV)", df.to_csv(index=False), "OPI_Payments.csv")
