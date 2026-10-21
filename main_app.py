import streamlit as st
import importlib
from supabase import create_client, Client

# =========================================================================
# Supabase ক্লাউড ডেটাবেজ গ্লোবাল কানেকশন
# =========================================================================
SUPABASE_URL = "https://baxwgnlfsnwpekrlmhpw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJheHdnbmxmc253cGVrcmxtaHB3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTIzMTY0MDksImV4cCI6MjEwNzg5MjQwOX0.lxdaUNbyF4Pn0WCT2zIQz3ETyCVmEnXM3YkHsb4SLXQ"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    supabase = None

# পেজ মডিউল ইমপোর্ট
login_page = importlib.import_module("app_pages.1_login_page")
home_dashboard = importlib.import_module("app_pages.2_home_dashboard")
books_library = importlib.import_module("app_pages.3_books_library")
student_notes = importlib.import_module("app_pages.4_student_notes")
exam_routine = importlib.import_module("app_pages.5_exam_routine")
quiz_practice = importlib.import_module("app_pages.6_quiz_practice")
student_profile = importlib.import_module("app_pages.7_student_profile")

render_login_page = login_page.render_login_page
render_dashboard = home_dashboard.render_dashboard
render_my_books = books_library.render_my_books
render_notes = student_notes.render_notes
render_exams = exam_routine.render_exams
render_quiz_practice = quiz_practice.render_quiz_practice
render_student_profile = student_profile.render_student_profile

# স্ট্রীমলিট পেজ কনফিগারেশন
st.set_page_config(
    layout="wide",
    page_icon="📚",
    page_title="Virtual Reading Room",
    initial_sidebar_state="expanded"
)

# =========================================================================
# সেশন স্টেট (Session State) ইনিশিয়ালাইজেশন (ড্যাশবোর্ডের এরর দূর করার জন্য অপরিহার্য)
# =========================================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "student_id" not in st.session_state:
    st.session_state.student_id = ""
if "student_name" not in st.session_state:
    st.session_state.student_name = ""
if "school_name" not in st.session_state:
    st.session_state.school_name = ""
if "class_name" not in st.session_state:
    st.session_state.class_name = ""
if "section" not in st.session_state:
    st.session_state.section = ""
if "roll_number" not in st.session_state:
    st.session_state.roll_number = ""
if "group" not in st.session_state:
    st.session_state.group = ""
if "academic_session" not in st.session_state:
    st.session_state.academic_session = ""
if "phone" not in st.session_state:
    st.session_state.phone = ""
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

# গেটকিপার লজিক
if not st.session_state.authenticated:
    render_login_page()
else:
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <h3 style="color: white; margin: 0; font-size: 18px;">Virtual Reading Room</h3>
            <p style="color: #94A3B8; font-size: 11px;">{st.session_state.school_name}</p>
        </div>
        """, unsafe_allow_html=True)
        
        nav_options = [
            ("🏠 Dashboard", "Dashboard"),
            ("📖 Books & Reading", "My Books"),
            ("✍️ Practice & Preparation", "Quiz & Practice"),
            ("📝 NoteBook", "Notes"),
            ("📅 Exams & Assignment", "Exam & Assignment"),
            ("👨‍🎓 Student Profile", "Student Profile")
        ]
        
        for label, page_key in nav_options:
            if st.button(label, use_container_width=True, key=f"nav_{page_key}"):
                st.session_state.current_page = page_key
                st.rerun()
                
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            st.session_state.authenticated = False
            st.session_state.student_id = ""
            st.rerun()

    # পেজ রাউটিং হ্যান্ডলার
    page = st.session_state.current_page
    if page == "Dashboard":
        render_dashboard()
    elif page == "My Books":
        render_my_books()
    elif page == "Quiz & Practice":
        render_quiz_practice()
    elif page == "Notes":
        render_notes()
    elif page == "Exam & Assignment":
        render_exams()
    elif page == "Student Profile":
        render_student_profile()