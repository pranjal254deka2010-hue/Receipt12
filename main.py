import streamlit as st
from fpdf import FPDF
from datetime import datetime
import pandas as pd
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="OPI Management Portal", page_icon="🎓", layout="centered")

# --- HEADER SECTION ---
# Updated to match your specific filename: logo.png.JPG
col1, col2 = st.columns([1, 4])
with col1:
    if os.path.exists("logo.png.JPG"):
        st.image("logo.png.JPG", width=100)
    else:
        st.warning("Logo file 'logo.png.JPG' not found on GitHub.")
with col2:
    st.markdown("<h2 style='color: #002e63; margin-bottom: 0;'>OXFORD PARAMEDICAL INSTITUTE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='margin-top: 0;'>ESTD. 2009 | Excellence in Healthcare Education</p>", unsafe_allow_html=True)

st.divider()

# --- APP NAVIGATION ---
menu = st.sidebar.selectbox("MENU", ["Generate Receipt", "Mark Attendance", "Student Records"])

# --- DATABASE SETUP ---
if not os.path.exists("students.csv"):
    pd.DataFrame(columns=["Name", "Course", "Phone"]).to_csv("students.csv", index=False)

# --- 1. GENERATE RECEIPT ---
if menu == "Generate Receipt":
    st.subheader("📝 Fee Receipt Generator")
    
    with st.form("receipt_form"):
        receipt_no = f"OPI-{datetime.now().strftime('%y%m%d%H%M')}"
        date_str = datetime.now().strftime("%d %b, %Y")
        
        student_name = st.text_input("STUDENT NAME")
        course = st.selectbox("COURSE ENROLLED", ["DMLT", "ICU Technology", "ECG Technician", "First Aid"])
        fee_purpose = st.selectbox("PURPOSE OF FEES", ["Monthly Fee", "Admission Fee", "Examination Fee", "Registration Fee", "Uniform/Books", "Other"])
        
        target_month = ""
        if fee_purpose == "Monthly Fee":
            target_month = st.selectbox("FOR WHICH MONTH", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
        
        pay_mode = st.radio("PAYMENT MODE", ["Online", "Cash", "Cheque"], horizontal=True)
        amount = st.number_input("AMOUNT RECEIVED (₹)", min_value=0.0, step=100.0)
        
        generate = st.form_submit_button("Generate Professional PDF")

    if generate and student_name:
        pdf = FPDF()
        pdf.add_page()
        pdf.rect(5, 5, 200, 287) 
        
        # Logo using the corrected filename
        if os.path.exists("logo.png.JPG"):
            pdf.image("logo.png.JPG", 10, 10, 25)
        
        pdf.set_font("Arial", 'B', 16)
        pdf.set_text_color(0, 46, 99)
        pdf.cell(0, 10, "OXFORD PARAMEDICAL INSTITUTE", ln=True, align='C')
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 5, "ESTD. 2009 | Excellence in Healthcare Education", ln=True, align='C')
        pdf.ln(15)
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "OFFICIAL FEES RECEIPT", ln=True, align='C')
        pdf.ln(5)
        
        pdf.set_font("Arial", '', 11)
        pdf.cell(100, 10, f"Receipt No: {receipt_no}")
        pdf.cell(0, 10, f"Date: {date_str}", ln=True, align='R')
        pdf.line(10, 65, 200, 65)
        pdf.ln(10)
        
        pdf.cell(0, 10, f"STUDENT NAME: {student_name.upper()}", ln=True)
        pdf.cell(0, 10, f"COURSE: {course}", ln=True)
        purpose_text = f"PURPOSE: {fee_purpose}"
        if target_month: purpose_text += f" ({target_month})"
        pdf.cell(0, 10, purpose_text, ln=True)
        pdf.cell(0, 10, f"PAYMENT MODE: {pay_mode}", ln=True)
        
        pdf.set_font("Arial", 'B', 13)
        pdf.cell(0, 15, f"TOTAL AMOUNT PAID: Rs. {amount:,.2f}", ln=True)
        
        # Signature & Footer
        pdf.ln(40)
        pdf.set_font("Arial", 'I', 9)
        pdf.set_xy(15, 150)
        pdf.cell(0, 10, "* This is an electronically generated receipt.")
        pdf.set_xy(15, 155)
        pdf.cell(0, 10, "* Fees once paid are non-refundable.")

        pdf.set_font("Arial", 'B', 10)
        pdf.set_xy(140, 150)
        pdf.cell(50, 10, "__________________________", align='C', ln=True)
        pdf.set_xy(140, 155)
        pdf.cell(50, 10, "Authorized Signatory", align='C')

        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.success("Receipt successfully created!")
        st.download_button(label="⬇️ Download PDF Receipt", data=pdf_output, file_name=f"OPI_Receipt_{student_name}.pdf", mime="application/pdf")

# --- OTHER SECTIONS ---
elif menu == "Mark Attendance":
    st.subheader(f"📅 Daily Attendance")
    if os.path.exists("students.csv"):
        df = pd.read_csv("students.csv")
        if not df.empty:
            attendance_data = []
            for index, row in df.iterrows():
                status = st.checkbox(f"{row['Name']} ({row['Course']})", key=row['Name'])
                attendance_data.append({"Name": row['Name'], "Status": "Present" if status else "Absent"})
            if st.button("Save Attendance"):
                att_df = pd.DataFrame(attendance_data)
                att_df['Date'] = datetime.now().strftime('%Y-%m-%d')
                att_df.to_csv("attendance.csv", mode='a', index=False, header=not os.path.exists("attendance.csv"))
                st.success("Recorded!")
        else: st.info("Add students first in 'Student Records'.")

elif menu == "Student Records":
    st.subheader("👥 Student Management")
    with st.expander("Add New Student"):
        n = st.text_input("Name")
        c = st.selectbox("Course", ["DMLT", "ICU Tech", "ECG Tech", "First Aid"])
        p = st.text_input("Phone")
        if st.button("Save"):
            pd.DataFrame([[n, c, p]], columns=["Name", "Course", "Phone"]).to_csv("students.csv", mode='a', header=False, index=False)
            st.rerun()
    if os.path.exists("students.csv"):
        st.dataframe(pd.read_csv("students.csv"), use_container_width=True)
