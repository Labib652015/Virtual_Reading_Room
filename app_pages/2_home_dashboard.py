import streamlit as st
from datetime import datetime

def render_dashboard():
    head_col1, head_col2, head_col3 = st.columns([1.8, 2.0, 3.2])
    with head_col1:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 14px; padding-top: 5px;">
            <div>
                <h2 style="margin: 0; font-size: 20px; color: #f8fafc; font-weight: 800;">Virtual Reading Room</h2>
                <p style="margin: 0; font-size: 11px; color: #94a3b8;">Cloud Sync with Supabase</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with head_col2:
        search_query = st.text_input("Search", placeholder="Search books, notes, exams...", label_visibility="collapsed")
        if search_query:
            st.info(f"Searching for: {search_query}")
    with head_col3:
        profile_html = f"""
        <div style="display: flex; align-items: center; justify-content: flex-end; gap: 12px; background: #1e293b; padding: 8px 16px; border-radius: 20px; border: 1px solid #334155;">
            <div style="text-align: right;">
                <div style="font-size: 15px; font-weight: 800; color: #f8fafc;">{st.session_state.student_name}</div>
                <div style="font-size: 11px; color: #38bdf8;">{st.session_state.class_name}</div>
            </div>
        </div>
        """
        st.markdown(profile_html, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    col_main, col_ai = st.columns([2.3, 1.2], gap="large")
    
    with col_main:
        current_hour = datetime.now().hour
        greeting = "Good Morning" if 5 <= current_hour < 12 else ("Good Afternoon" if 12 <= current_hour < 17 else ("Good Evening" if 17 <= current_hour < 21 else "Good Night"))
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 26px; border-radius: 24px; border: 1px solid #334155; margin-bottom: 24px;">
            <h2 style="color: #f8fafc; font-weight: 800; margin-bottom: 6px;">{greeting}, {st.session_state.student_name}!</h2>
            <p style="color: #94a3b8; font-size: 13px;">Welcome back to your Supabase-powered reading room!</p>
        </div>
        """, unsafe_allow_html=True)
        
        qc1, qc2, qc3, qc4, qc5 = st.columns(5)
        with qc1:
            if st.button("My Books", use_container_width=True):
                st.session_state.current_page = "My Books"; st.rerun()
        with qc2:
            if st.button("Notebook", use_container_width=True):
                st.session_state.current_page = "Notes"; st.rerun()
        with qc3:
            if st.button("Take Quiz", use_container_width=True):
                st.session_state.current_page = "Quiz & Practice"; st.rerun()
        with qc4:
            if st.button("Study Plan", use_container_width=True):
                st.session_state.current_page = "Study Planner"; st.rerun()
        with qc5:
            if st.button("Exams", use_container_width=True):
                st.session_state.current_page = "Exam & Assignment"; st.rerun()
                
    with col_ai:
        st.markdown("""
        <div class="dashboard-card" style="border: 2px solid #3b82f6;">
            <h4 style="color: #f8fafc; font-weight: 700;">AI Study Assistant</h4>
            <p style="font-size: 12px; color: #cbd5e1;">Ask me anything about your studies!</p>
        </div>
        """, unsafe_allow_html=True)