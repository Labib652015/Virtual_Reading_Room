import streamlit as st
from database_connection.cloud_supabase import supabase

def render_quiz_practice():
    st.markdown("<h2 style='color: #f8fafc;'>Practice & Preparation Section</h2>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["Practice", "Quiz Test", "Model Test", "Archives"])
    
    with tab1:
        st.info("Select Class and Subject to start practice.")
    with tab2:
        st.subheader("Quick Quiz")
    with tab3:
        st.subheader("Full Model Test")
    with tab4:
        st.subheader("Saved Test History (Supabase Archive)")
        try:
            response = supabase.table("quiz_test_history").select("*").order("id", desc=True).execute()
            history = response.data
            if history:
                for item in history:
                    st.write(f"**{item.get('quiz_title')}** | Score: {item.get('obtained_score')}/{item.get('total_marks')} | Date: {item.get('quiz_date')}")
            else:
                st.info("No quiz history found in Supabase.")
        except Exception as e:
            st.error(f"Error fetching quiz archives: {e}")