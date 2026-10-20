import streamlit as st
from supabase import create_client, Client

SUPABASE_URL = "https://baxwgnlfsnwpekrlmhpw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJheHdnbmxmc253cGVrcmxtaHB3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTIzMTY0MDksImV4cCI6MjEwNzg5MjQwOX0.lxdaUNbyF4Pn0WCT2zIQz3ETyCVmEnXM3YkHsb4SLXQ"

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()
