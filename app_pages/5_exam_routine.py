import streamlit as st
from database_connection.cloud_supabase import supabase
from datetime import datetime

def render_exams():
    st.markdown("<h2 style='color: #f8fafc;'>Exams & Assignment Schedule (Supabase)</h2>", unsafe_allow_html=True)
    with st.form("add_exam_form"):
        e_name = st.text_input("পরীক্ষার নাম:")
        e_type = st.selectbox("ধরন:", ["বার্ষিক পরীক্ষা", "অর্ধ-বার্ষিক পরীক্ষা", "সাপ্তাহিক কুইজ", "অ্যাসাইনমেন্ট"])
        e_date = st.date_input("তারিখ:")
        e_desc = st.text_input("নোট/সিলেবাস:")
        
        if st.form_submit_button("Save Exam"):
            if e_name:
                try:
                    supabase.table("exams").insert({
                        "exam_name": e_name,
                        "exam_type": e_type,
                        "exam_date": str(e_date),
                        "description": e_desc
                    }).execute()
                    st.success("পরীক্ষা তালিকা ক্লাউডে যুক্ত হয়েছে!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving exam: {e}")
                    
    st.markdown("---")
    try:
        res = supabase.table("exams").select("*").order("exam_date", desc=False).execute()
        exams = res.data
        if exams:
            for ex in exams:
                st.write(f"**{ex.get('exam_name')}** ({ex.get('exam_type')}) - Date: {ex.get('exam_date')}")
        else:
            st.info("কোনো পরীক্ষার তারিখ পাওয়া যায়নি।")
    except Exception as e:
        st.error(f"Error loading exams: {e}")