import streamlit as st
from database_connection.cloud_supabase import supabase
from design_styles.custom_css import apply_custom_design


def render_my_books():
    apply_custom_design()
    st.markdown('<h1 class="main-title">পাঠ্যবই ও গাইড লাইব্রেরি</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">NCTB পাঠ্যবই ও রেফারেন্স বইসমূহের ডিজিটাল সংগ্রহশালা</p>', unsafe_allow_html=True)
    class_options = {
        "ষষ্ঠ শ্রেণি": "class6",
        "সপ্তম শ্রেণি": "class7",
        "অষ্টম শ্রেণি": "class8",
        "নবম শ্রেণি": "class9",
        "দশম শ্রেণি": "class10",
        "একাদশ-দ্বাদশ শ্রেণি": "inter"
    }
    
    selected_label = st.selectbox("আপনার শ্রেণি নির্বাচন করুন:", list(class_options.keys()), key="class_selection_dropdown")
    selected_class_code = class_options[selected_label]
    st.markdown("<br>", unsafe_allow_html=True)
    
    try:
        response = supabase.table("class_books").select("*").execute()
        all_data = response.data if response and hasattr(response, 'data') else []
        books_data = [book for book in all_data if (book.get("class_name", "")).strip() == selected_class_code]
        
        if books_data:
            st.success(f"**{selected_label}**-এর মোট **{len(books_data)}টি** পাঠ্যবই পাওয়া গেছে।")
            st.markdown("<br>", unsafe_allow_html=True)
            
            cols = st.columns(2)
            for idx, book in enumerate(books_data):
                col = cols[idx % 2]
                with col:
                    sub_title = book.get('subject_title', 'পাঠ্যবই')
                    pdf_url = book.get('pdf_url', '')
                    
                    st.markdown(f"""
                    <div class="book-card">
                        <div class="book-title">{sub_title}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if pdf_url:
                        st.markdown(f'<a href="{pdf_url}" target="_blank" class="btn-link">নতুন ট্যাবে সরাসরি খুলুন</a>', unsafe_allow_html=True)
                        with st.expander("অ্যাপের ভেতরে সরাসরি পড়ুন"):
                            st.info("টিপস: লেখা সিলেক্ট করতে সমস্যা হলে ওপরের বাটনে ক্লিক করে ব্রাউজারে খুলুন।")
                            st.markdown(f'<iframe src="{pdf_url}#toolbar=1" width="100%" height="550px"></iframe>', unsafe_allow_html=True)
                    else:
                        st.warning("পিডিএফ লিংক পাওয়া যায়নি।")
        else:
            st.info(f"এখনো **{selected_label}**-এর কোনো বই ডাটাবেজে এন্ট্রি করা হয়নি।")
    except Exception as e:
        st.error(f"ডাটাবেজ কানেকশনে সমস্যা হয়েছে: {e}")