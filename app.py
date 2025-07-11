import streamlit as st
from datetime import datetime
import pyt

fuso = pytz.timezone("Europe/Madrid")
hoje = datetime.now(fuso).date()

st.set_page_config("Consultoria Cris Lash", layout="wide")
