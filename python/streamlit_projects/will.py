import streamlit as st
import pandas as pd
import hashlib
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="Digital Will Generator", layout="centered")

st.title("🧾 Digital Will Generator (Modern Secure Edition)")
st.markdown("Generate a legally inspired digital will with a blockchain-style verification hash.")

# ----------- INPUT SECTION -----------
with st.form("will_form"):
    st.subheader("👤 Your Personal Information")
    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=18, max_value=120)
    address = st.text_area("Residential Address")

    st.subheader("💰 Assets")
    assets = st.text_area("List all major assets with description and value")

    st.subheader("👥 Beneficiaries")
    beneficiaries = st.text_area("Mention names and relation of beneficiaries")

    st.subheader("📜 Final Wishes")
    wishes = st.text_area("Enter any specific instructions or wishes")

    submitted = st.form_submit_button("Generate Will")

# ----------- PDF GENERATION + HASHING -----------
if submitted:
    st.success("✅ Will Generated!")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    will_text = f"""
    DIGITAL WILL DOCUMENT

    Name: {name}
    Age: {age}
    Address: {address}

    --- ASSETS ---
    {assets}

    --- BENEFICIARIES ---
    {beneficiaries}

    --- FINAL WISHES ---
    {wishes}

    Timestamp: {timestamp}
    """

    # Generate Hash
    will_hash = hashlib.sha256(will_text.encode()).hexdigest()

    # PDF Generation
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in will_text.split("\n"):
        pdf.multi_cell(0, 10, txt=line)
    pdf.ln()
    pdf.multi_cell(0, 10, txt=f"🔐 Blockchain-style Hash: {will_hash}")

    # Save
    pdf_output = f"/tmp/{name.replace(' ', '_')}_digital_will.pdf"
    pdf.output(pdf_output)

    st.code(will_hash, language='plaintext')
    st.download_button("📄 Download Your Will (PDF)", open(pdf_output, "rb").read(), file_name="digital_will.pdf")

    st.caption("This hash simulates blockchain immutability. Save it to verify integrity later.")
