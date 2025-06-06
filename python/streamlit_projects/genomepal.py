import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from datetime import datetime
import json
import os
import re

# ---------------------- CONFIG ----------------------
st.set_page_config(page_title="GenomePal", page_icon="🧬", layout="centered")

# ---------------------- LOGO & THEME ----------------------
st.markdown("""
    <style>
        .css-1d391kg { background-color: #f8f3ff; }
        .css-1v0mbdj { color: #1c0034; }
        .st-emotion-cache-1v0mbdj { color: #1c0034; }
    </style>
""", unsafe_allow_html=True)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/DNA_icon.svg/2048px-DNA_icon.svg.png", use_column_width=True)

# ---------------------- USER LOGIN ----------------------
username = st.sidebar.text_input("👤 Enter your name:", value="Guest")

# ---------------------- MULTI PAGE NAV ----------------------
page = st.sidebar.radio("Go to", ["Home", "Dashboard", "About"])

# ---------------------- SNP TRAIT MAP ----------------------
snp_map = {
    "rs4994": {"trait": "Fast Metabolism", "mutation": "TT"},
    "rs4988235": {"trait": "Lactose Intolerant", "mutation": "AA"},
    "rs762551": {"trait": "Caffeine Sensitive", "mutation": "AA"},
    "rs1815739": {"trait": "Sprinter Gene", "mutation": "CC"},
    "rs1256049": {"trait": "Vitamin D Deficiency Prone", "mutation": "GG"},
}

# ---------------------- FUNCTIONS ----------------------
def remove_emoji(text):
    return re.sub(r'[^
