import streamlit as st
import datetime
import json
from supabase import create_client, Client

def render_student_profile():
    # =========================================================================
    # ১. কাস্টম সিএসএস (CSS) স্টাইলিং ব্লক
    # এখান থেকে আপনি ফন্ট সাইজ, রঙ, ব্যাকগ্রাউন্ড, প্যাডিং ইত্যাদি যেকোনো সময় কাস্টমাইজ করতে পারবেন।
    # =========================================================================
    st.markdown("""
        <style>
            /* মূল পেজের ব্যাকগ্রাউন্ড ও প্যাডিং */
            .main {
                background-color: #F8FAFC;
            }
            
            /* মূল টাইটেল (শিক্ষার্থীর পরিচিতি ও বায়োগ্রাফি) */
            .page-title {
                text-align: center;
                color: #1E3A8A; /* গাঢ় নীল রঙ (Navy Blue) - এখান থেকে টাইটেলের রঙ বদলাতে পারেন */
                font-size: 32px; /* ফন্ট সাইজ */
                font-weight: 800;
                margin-top: 10px;
                margin-bottom: 20px;
                letter-spacing: 0.5px;
            }

            /* সেকশন হেডার বা সাব-টাইটেল (যেমন: ১. প্রতিষ্ঠানের তথ্য) */
            .section-header {
                font-size: 22px; /* ফন্ট সাইজ */
                font-weight: bold;
                color: #047857; /* ডিপ ফরেস্ট গ্রিন রঙ - সেকশন হেডার কালার বদলাতে পারেন */
                border-bottom: 3px solid #047857;
                padding-bottom: 8px;
                margin-top: 30px;
                margin-bottom: 18px;
            }

            /* ইনপুট ফিল্ডের লেবেল (যেমন: "শিক্ষার্থীর পূর্ণ নাম") */
            label {
                font-size: 15px !important;
                font-weight: 600 !important;
                color: #1E293B !important; /* লেবেলের লেখার রঙ */
            }

            /* ইনপুট বক্সের বর্ডার ও ব্যাকগ্রাউন্ড স্টাইল */
            .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
                border-radius: 6px !important;
                border: 1px solid #CBD5E1 !important;
            }

            /* সংরক্ষণ (Save) বাটনের কাস্টম ডিজাইন */
            .stButton>button {
                background-color: #047857 !important; /* প্রাইমারি গ্রিন কালার (বাটনের ব্যাকগ্রাউন্ড) */
                color: #FFFFFF !important;             /* সাদা টেক্সট */
                font-size: 19px !important;            /* বাটন লেখার সাইজ */
                font-weight: bold !important;
                border-radius: 8px !important;
                padding: 12px 24px !important;
                border: none !important;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1) !important;
                transition: all 0.3s ease !important;
            }
            
            /* বাটনে মাউস পয়েন্টার নিলে যে পরিবর্তন হবে (Hover Effect) */
            .stButton>button:hover {
                background-color: #065F46 !important; /* আরও ডার্ক গ্রিন */
                transform: translateY(-2px);
                box-shadow: 0px 6px 14px rgba(0, 0, 0, 0.15) !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # পেজের মূল শিরোনাম প্রদর্শন
    st.markdown("<div class='page-title'>🎓 শিক্ষার্থীর পরিচিতি ও বায়োগ্রাফি</div>", unsafe_allow_html=True)
    st.markdown("---")

    # =========================================================================
    # ২. প্রতিষ্ঠানের তথ্য সেকশন
    # =========================================================================
    st.markdown("<div class='section-header'>১. প্রতিষ্ঠানের তথ্য</div>", unsafe_allow_html=True)
    
    school_name = st.text_input("প্রতিষ্ঠানের নাম", "সামসুল হক খান স্কুল অ্যান্ড কলেজ")
    school_address = st.text_input("প্রতিষ্ঠানের ঠিকানা", "ডেমরা, ঢাকা, বাংলাদেশ")
    
    col1, col2 = st.columns(2)
    with col1:
        default_sid = st.session_state.get("student_id", "STU-2026-001")
        student_id = st.text_input("স্টুডেন্ট আইডি", default_sid)
        class_name = st.text_input("শ্রেণি", "সপ্তম")
        section = st.text_input("সেকশন", "বি")
    with col2:
        group = st.text_input("বিভাগ (যেমন: বিজ্ঞান/মানবিক)", "বিজ্ঞান")
        roll_number = st.text_input("রোল নম্বর", "১২০")
        academic_session = st.text_input("সেশন", "২০২৬")

    # =========================================================================
    # ৩. শিক্ষার্থীর ব্যক্তিগত তথ্য সেকশন
    # =========================================================================
    st.markdown("<div class='section-header'>২. শিক্ষার্থীর ব্যক্তিগত তথ্য</div>", unsafe_allow_html=True)
    
    student_name = st.text_input("শিক্ষার্থীর পূর্ণ নাম", "লাবিব বিন লালন")
    
    col3, col4 = st.columns(2)
    with col3:
        # জন্ম তারিখ ক্যালেন্ডার (১৯৫০ থেকে আজকের দিন পর্যন্ত)
        dob = st.date_input(
            "জন্ম তারিখ",
            min_value=datetime.date(1950, 1, 1),
            max_value=datetime.date.today(),
            value=datetime.date(2012, 5, 15)
        )
        gender = st.selectbox("লিঙ্গ", ["পুরুষ", "নারী", "অন্যান্য"])
        religion = st.selectbox("ধর্ম", ["ইসলাম", "হিন্দু", "খ্রিস্টান", "বৌদ্ধ", "অন্যান্য"])
                    
    with col4:
        blood_group = st.selectbox("ব্লাড গ্রুপ", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        student_phone = st.text_input("শিক্ষার্থীর নিজের ফোন (যদি থাকে)", "০১৭৪২০৬৩৯০২")

    # =========================================================================
    # ৪. পিতামাতা ও অভিভাবকের তথ্য সেকশন
    # =========================================================================
    st.markdown("<div class='section-header'>৩. পিতামাতা ও অভিভাবকের তথ্য</div>", unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    with col5:
        father_name = st.text_input("পিতার নাম", "বিএম লালন স্যার")
        father_phone = st.text_input("পিতা/অভিভাবকের মোবাইল নম্বর", "০১৭XXXXXXXX")
        father_occupation = st.text_input("পিতার পেশা", "উপপরিচালক / শিক্ষক")
    
    with col6:
        mother_name = st.text_input("মাতার নাম", "মোসাম্মাৎ সহিদা খাতুন")
        mother_phone = st.text_input("মাতার মোবাইল নম্বর", "০১৮XXXXXXXX")
        mother_occupation = st.text_input("মাতার পেশা", "গৃহিণী")
        
    guardian_email = st.text_input("অভিভাবক/শিক্ষার্থীর ইমেইল ঠিকানা", "lalon.acc@gmail.com")

    # =========================================================================
    # ৫. ঠিকানা সংক্রান্ত তথ্য সেকশন
    # =========================================================================
    st.markdown("<div class='section-header'>৪. যোগাযোগের ঠিকানা</div>", unsafe_allow_html=True)
    
    present_address = st.text_area("বর্তমান ঠিকানা", "মধুবাগ মসজিদ গলি, নতুন ইংলিশ ভার্সন ভবনের পেছনে, ডেমরা, ঢাকা")
    permanent_address = st.text_area("স্থায়ী ঠিকানা", "গ্রাম: শাহপুর, ডাকঘর: মীর শাহপুর, উপজেলা: কসবা, জেলা: ব্রাহ্মণবাড়িয়া")

    # =========================================================================
    # ৬. অতিরিক্ত দক্ষতা, শখ ও ক্লাবের তথ্য সেকশন
    # =========================================================================
    st.markdown("<div class='section-header'>৫. মেধা, দক্ষতা ও সহ-পাঠ্যক্রমিক কার্যাবলী</div>", unsafe_allow_html=True)
    
    col7, col8 = st.columns(2)
    with col7:
        special_skills = st.text_input("বিশেষ দক্ষতা", "পাইথন প্রোগ্রামিং, ইংরেজি ব্যাকরণ, আবৃত্তি")
        hobbies = st.text_input("শখ", "বই পড়া, সাঁতার কাটা, নতুন প্রযুক্তি শিক্ষা")
    
    with col8:
        club_options = [
            "আইটি ক্লাব (IT Club)",
            "বিজ্ঞান ক্লাব (Science Club)",
            "ডিবেটিং ক্লাব (Debating Club)",
            "গণিত ক্লাব (Math Club)",
            "স্পোর্টস ক্লাব (Sports Club)",
            "সাংস্কৃতিক ক্লাব (Cultural Club)",
            "স্কাউটস / গার্ল গাইডস (Scouts)"
        ]
        clubs = st.multiselect("যুক্ত থাকা ক্লাবসমূহ", club_options, default=["আইটি ক্লাব (IT Club)", "বিজ্ঞান ক্লাব (Science Club)"])
    
    achievements = st.text_area("জাতীয়/অভ্যন্তরীণ প্রোগ্রামে অংশগ্রহণ ও অর্জন", "জাতীয় বিজ্ঞান মেলা ২০২৫ (অংশগ্রহণকারী), বাংলাদেশ গণিত অলিম্পিয়াড ২০২৬")

    # =========================================================================
    # ৭. ভাইবোনের বিবরণ সেকশন (ডায়নামিক ইনপুট)
    # =========================================================================
    st.markdown("<div class='section-header'>৬. ভাইবোনের বিবরণ</div>", unsafe_allow_html=True)
    
    num_siblings = st.number_input("ভাইবোনের সংখ্যা", min_value=0, max_value=10, value=1, step=1)
    
    siblings_info = []
    if num_siblings > 0:
        st.write("---")
        st.write("**ভাইবোনদের নাম ও বর্তমান পেশা/শ্রেণি লিখুন:**")
        for i in range(int(num_siblings)):
            col_sib1, col_sib2 = st.columns(2)
            with col_sib1:
                sib_name = st.text_input(f"ভাই/বোন {i+1}-এর নাম", "লাবিবা বিনতে লালন", key=f"sib_name_{i}")
            with col_sib2:
                sib_occ = st.text_input(f"ভাই/বোন {i+1}-এর শ্রেণি/পেশা", "১ম শ্রেণি, সামসুল হক খান স্কুল অ্যান্ড কলেজ", key=f"sib_occ_{i}")
            
            siblings_info.append({"name": sib_name, "occ": sib_occ})

    # =========================================================================
    # ৮. স্থায়ী ডেটাবেজ সংরক্ষণ (Supabase Direct Integration)
    # =========================================================================
    st.markdown("---")
    
    if st.button("প্রোফাইল তথ্য সংরক্ষণ করুন", use_container_width=True):
        
        # আপনার প্রদানকৃত সঠিক Supabase URL এবং সঠিক API Key এখানে সরাসরি সেটআপ করা হলো
        SUPABASE_URL = "https://baxwgnlfsnwpekrlmhpw.supabase.co"
        SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJheHdnbmxmc253cGVrcmxtaHB3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTIzMTY0MDksImV4cCI6MjEwNzg5MjQwOX0.lxdaUNbyF4Pn0WCT2zIQz3ETyCVmEnXM3YkHsb4SLXQ"
        
        try:
            # সুপাবেজ ক্লায়েন্ট ইনিশিয়ালাইজ করা
            local_supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
            
            # ডেটা ডিকশনারি তৈরি (সকল ফিল্ডের ডেটা একসাথে গোছানো)
            profile_data = {
                "student_id": student_id,
                "student_name": student_name,
                "school_name": school_name,
                "school_address": school_address,
                "class_name": class_name,
                "section": section,
                "group": group,
                "roll_number": roll_number,
                "academic_session": academic_session,
                "dob": str(dob),
                "gender": gender,
                "religion": religion,
                "blood_group": blood_group,
                "student_phone": student_phone,
                "father_name": father_name,
                "father_phone": father_phone,
                "father_occupation": father_occupation,
                "mother_name": mother_name,
                "mother_phone": mother_phone,
                "mother_occupation": mother_occupation,
                "guardian_email": guardian_email,
                "present_address": present_address,
                "permanent_address": permanent_address,
                "special_skills": special_skills,
                "hobbies": hobbies,
                "clubs": clubs,
                "achievements": achievements,
                "num_siblings": int(num_siblings),
                "siblings_info": siblings_info
            }
            
            # ডেটাবেজে আপসার্ট (Upsert) করার মাধ্যমে ডেটা স্থায়ীভাবে সংরক্ষণ করা
            response = local_supabase.table("student_profile").upsert(profile_data, on_conflict="student_id").execute()
            
            st.success("🎉 অভিনন্দন! আপনার সমস্ত তথ্য সফলভাবে এবং স্থায়ীভাবে Supabase ক্লাউড ডেটাবেজে সংরক্ষিত হয়েছে।")
            
        except Exception as e:
            st.error(f"❌ ডেটা সংরক্ষণে ত্রুটি ঘটেছে: {e}")

if __name__ == "__main__":
    render_student_profile()