import streamlit as st
import importlib

# সংখ্যা দিয়ে শুরু হওয়া ফাইলগুলো নিরাপদে ইমপোর্ট করার জন্য importlib ব্যবহার করা হলো
login_page = importlib.import_module("app_pages.1_login_page")
home_dashboard = importlib.import_module("app_pages.2_home_dashboard")
books_library = importlib.import_module("app_pages.3_books_library")
student_notes = importlib.import_module("app_pages.4_student_notes")
exam_routine = importlib.import_module("app_pages.5_exam_routine")
quiz_practice = importlib.import_module("app_pages.6_quiz_practice")

render_login_page = login_page.render_login_page
render_dashboard = home_dashboard.render_dashboard
render_my_books = books_library.render_my_books
render_notes = student_notes.render_notes
render_exams = exam_routine.render_exams
render_quiz_practice = quiz_practice.render_quiz_practice


st.set_page_config(
    layout="wide",
    page_icon="📚",
    page_title="Virtual Reading Room",
    initial_sidebar_state="expanded"
)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "student_name" not in st.session_state:
    st.session_state.student_name = "লাবিব বিন লালন"
if "school_name" not in st.session_state:
    st.session_state.school_name = "শামসুল হক খান স্কুল অ্যান্ড কলেজ, ডেমরা, ঢাকা"
if "class_name" not in st.session_state:
    st.session_state.class_name = "সপ্তম শ্রেণি"
if "roll_number" not in st.session_state:
    st.session_state.roll_number = "১২০"
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

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
            ("📅 Exams & Assignment", "Exam & Assignment")
           
        ]
        
        for label, page_key in nav_options:
            if st.button(label, use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()
                
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

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
    