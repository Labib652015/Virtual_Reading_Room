import streamlit.components.v1 as components
import streamlit as st

def render_login_page():
    st.markdown("""
    <style>
    .stApp {
    background-color: #062c18 !important;
}
    div[data-testid="stForm"] {
        background: rgba(30, 41, 59, 0.7) !important;
        backdrop-filter: blur(16px);
        padding: 35px;
        border-radius: 24px;
        border: 1px solid rgba(56, 189, 248, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 25px; margin-top: 30px;">
        <h1 style="color: #f8fafc; font-weight: 700; font-size: 32px;">Virtual Reading Room</h1>
        <p style="color: #94a3b8; font-size: 15px;">Smart study with AI Assistant & Supabase Cloud</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        with st.form("login_form"):
            st.markdown("<h3 style='text-align: center; color: #f8fafc;'>Student Portal Login</h3>", unsafe_allow_html=True)
            school = st.text_input("School Name & Location", value=st.session_state.get("school_name", ""))
            name = st.text_input("Student Name", value=st.session_state.get("student_name", ""))
            
            c1, c2, c3 = st.columns([2, 1.2, 1.2])
            with c1:
                selected_class = st.selectbox("Class", ["ষষ্ঠ শ্রেণি", "সপ্তম শ্রেণি", "অষ্টম শ্রেণি", "নবম শ্রেণি", "দশম শ্রেণি"], index=1)
            with c2:
                section = st.text_input("Section", value=st.session_state.get("section", ""))
            with c3:
                roll = st.text_input("Roll Number", value=st.session_state.get("roll_number", ""))
                
            submit = st.form_submit_button("Get Started", use_container_width=True)
            if submit:
                if name.strip():
                    st.session_state.school_name = school
                    st.session_state.student_name = name
                    st.session_state.class_name = selected_class
                    st.session_state.section = section
                    st.session_state.roll_number = roll
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Please enter your name to proceed.")