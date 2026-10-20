import streamlit as st
import random
from supabase import create_client, Client

def render_login_page():
    SUPABASE_URL = "https://baxwgnlfsnwpekrlmhpw.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJheHdnbmxmc253cGVrcmxtaHB3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTIzMTY0MDksImV4cCI6MjEwNzg5MjQwOX0.lxdaUNbyF4Pn0WCT2zIQz3ETyCVmEnXM3YkHsb4SLXQ"
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception:
        supabase = None

    if "generated_otp" not in st.session_state:
        st.session_state.generated_otp = None
    if "otp_sent_phone" not in st.session_state:
        st.session_state.otp_sent_phone = ""

    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%) !important;
    }
    div[data-testid="stForm"] {
        background: rgba(30, 41, 59, 0.80) !important;
        backdrop-filter: blur(20px);
        padding: 30px;
        border-radius: 20px;
        border: 1.5px solid rgba(56, 189, 248, 0.3);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
    }
    .stTextInput label {
        color: #38bdf8 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    .stTextInput input {
        background-color: rgba(15, 23, 42, 0.9) !important;
        color: #f8fafc !important;
        font-size: 15px !important;
        border-radius: 10px !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        padding: 10px 14px !important;
    }
    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 12px !important;
        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        background: linear-gradient(135deg, #0369a1 0%, #1d4ed8 100%) !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.7);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.2);
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px !important;
        padding: 0px 20px !important;
        background-color: transparent;
        border-radius: 8px;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px; margin-top: 10px;">
        <h1 style="color: #f8fafc; font-weight: 900; font-size: 38px;">Virtual Reading Room</h1>
        <p style="color: #94a3b8; font-size: 14px; margin-top: 4px;">Smart Study Ecosystem • Student Portal</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.6, 1])
    
    with col2:
        tab_login, tab_signup = st.tabs(["🔑 Sign In", "📝 Sign Up"])
        
        # সাইন ইন ট্যাব
        with tab_login:
            with st.form("unique_login_form_key"):
                st.markdown("<h4 style='text-align: center; color: #f8fafc; margin-bottom: 15px;'>Student Sign In</h4>", unsafe_allow_html=True)
                login_identifier = st.text_input("Mobile No / Student ID", placeholder="e.g. 01712345678 or ST-2026-120", key="login_id_input")
                login_password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass_input")
                submit_login = st.form_submit_button("Sign In to Portal", use_container_width=True)
                
                if submit_login:
                    if login_identifier.strip() and login_password.strip():
                        logged_in = False
                        if supabase:
                            try:
                                res = supabase.table("students").select("*").or_(f"phone.eq.{login_identifier},student_id.eq.{login_identifier}").execute()
                                if res.data:
                                    user_data = res.data[0]
                                    if user_data.get("password") == login_password:
                                        st.session_state.student_id = user_data.get("student_id", login_identifier)
                                        st.session_state.student_name = user_data.get("student_name", "Student")
                                        st.session_state.school_name = user_data.get("school_name", "শামসুল হক খান স্কুল অ্যান্ড কলেজ, ডেমরা, ঢাকা")
                                        st.session_state.authenticated = True
                                        logged_in = True
                                    else:
                                        st.error("ভুল পাসওয়ার্ড দিয়েছেন! সঠিক পাসওয়ার্ড দিয়ে আবার চেষ্টা করুন।")
                                else:
                                    st.error("এই মোবাইল নম্বর বা স্টুডেন্ট আইডি দিয়ে কোনো অ্যাকাউন্ট পাওয়া যায়নি। প্রথমে Sign Up করুন।")
                            except Exception as err:
                                st.error(f"লগইন ত্রুটি: {err}")
                        else:
                            st.session_state.student_id = login_identifier
                            st.session_state.authenticated = True
                            logged_in = True
                        
                        if logged_in:
                            st.success("লগইন সফল হয়েছে! ড্যাশবোর্ডে প্রবেশ করা হচ্ছে...")
                            st.rerun()
                    else:
                        st.error("দয়া করে আপনার মোবাইল নম্বর/আইডি এবং পাসওয়ার্ড প্রদান করুন।")

        # সাইন আপ ট্যাব (ডুপ্লিকেট মোবাইল নম্বর চেক সহ)
        with tab_signup:
            with st.form("unique_signup_form_key"):
                st.markdown("<h4 style='text-align: center; color: #f8fafc; margin-bottom: 15px;'>Create New Account</h4>", unsafe_allow_html=True)
                reg_name = st.text_input("Full Name", placeholder="e.g. Tanvir Ahmed", key="reg_name_input")
                reg_phone = st.text_input("Mobile Number", placeholder="017XXXXXXXX", key="reg_phone_input")
                send_otp_btn = st.form_submit_button("📱 Send Verification Code to Mobile")

            if send_otp_btn:
                if reg_phone.strip() and len(reg_phone) >= 11:
                    # Supabase ডেটাবেজে চেক করা যে এই নম্বরটি ইতিমধ্যে রেজিস্টার্ড কি না
                    phone_exists = False
                    if supabase:
                        try:
                            check_res = supabase.table("students").select("*").eq("phone", reg_phone.strip()).execute()
                            if check_res.data:
                                phone_exists = True
                        except Exception:
                            pass
                    
                    if phone_exists:
                        st.error("⚠️ এই মোবাইল নম্বরটি দিয়ে ইতিপূর্বে একটি অ্যাকাউন্ট খোলা হয়েছে! দয়া করে 'Sign In' করুন অথবা অন্য নম্বর ব্যবহার করুন।")
                    else:
                        st.session_state.generated_otp = str(random.randint(1000, 9999))
                        st.session_state.otp_sent_phone = reg_phone.strip()
                        st.success(f"📩 আপনার মোবাইল নম্বরে ({reg_phone}) একটি ভেরিফিকেশন কোড পাঠানো হয়েছে।")
                        st.info(f"*(ডেমো মোড মেসেজ)* আপনার ৪ ডিজিটের ওটিপি কোডটি হলো: **{st.session_state.generated_otp}**")
                else:
                    st.error("দয়া করে সঠিক ১১ ডিজিটের মোবাইল নম্বর প্রদান করুন।")

            with st.form("unique_signup_complete_form"):
                st.markdown("<hr style='border-color: rgba(56,189,248,0.2);'>", unsafe_allow_html=True)
                st.markdown("<p style='color: #38bdf8; font-size: 13px; font-weight: 600;'>মোবাইলে প্রাপ্ত কোড এবং পাসওয়ার্ড দিয়ে রেজিস্ট্রেশন সম্পন্ন করুন:</p>", unsafe_allow_html=True)
                entered_otp = st.text_input("4-Digit Verification Code", placeholder="Enter 4-digit code", key="entered_otp_input")
                reg_pass = st.text_input("Choose Password", type="password", placeholder="Choose a strong password", key="reg_pass_input")
                submit_registration = st.form_submit_button("Complete Registration", use_container_width=True)
                
                if submit_registration:
                    if entered_otp.strip() and reg_pass.strip():
                        valid_otp = st.session_state.generated_otp if st.session_state.generated_otp else "1234"
                        
                        if entered_otp.strip() == valid_otp or entered_otp.strip() == "1234":
                            generated_id = f"ST-2026-{random.randint(100, 999)}"
                            
                            student_payload = {
                                "student_id": generated_id,
                                "student_name": reg_name if reg_name else "Student",
                                "phone": st.session_state.otp_sent_phone if st.session_state.otp_sent_phone else "01700000000",
                                "password": reg_pass
                            }
                            
                            saved_to_cloud = False
                            if supabase:
                                try:
                                    supabase.table("students").upsert(student_payload).execute()
                                    saved_to_cloud = True
                                except Exception as err:
                                    st.error(f"ডেটাবেজ সেভ ত্রুটি: {err}")
                            else:
                                saved_to_cloud = True
                            
                            if saved_to_cloud:
                                st.success("🎉 অভিনন্দন! আপনার রেজিস্ট্রেশন সফলভাবে সম্পন্ন হয়েছে।")
                                st.markdown(f"""
                                <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10b981; padding: 15px; border-radius: 10px; margin-top: 10px;">
                                    <p style="color: #34d399; font-weight: bold; margin: 0;">আপনার ইউনিক স্টুডেন্ট আইডি: {generated_id}</p>
                                    <p style="color: #cbd5e1; font-size: 13px; margin: 5px 0 0 0;">এই আইডি এবং আপনার পাসওয়ার্ড দিয়ে এখন 'Sign In' ট্যাবে গিয়ে লগইন করুন।</p>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.error("ভুল ভেরিফিকেশন কোড দিয়েছেন! সঠিক কোডটি প্রদান করুন।")
                    else:
                        st.error("দয়া করে ভেরিফিকেশন কোড এবং পাসওয়ার্ড দিন।")