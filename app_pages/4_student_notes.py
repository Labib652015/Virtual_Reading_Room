import streamlit as st
from database_connection.cloud_supabase import supabase
from datetime import datetime

def render_notes():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 25px; border-radius: 20px; color: white; margin-bottom: 20px; border: 1px solid #334155;">
        <h2 style='color: #38bdf8; font-weight: 800; margin-bottom: 5px; font-size: 26px;'>Notebook Section (Cloud Synced)</h2>
        <p style='color: #94a3b8; font-size: 14px;'>Save permanent notes directly to Supabase cloud database.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if "edit_id" not in st.session_state:
        st.session_state["edit_id"] = None
    if "current_title" not in st.session_state:
        st.session_state["current_title"] = ""
    if "current_content" not in st.session_state:
        st.session_state["current_content"] = ""
    if "current_subject" not in st.session_state:
        st.session_state["current_subject"] = "বাংলা"
        
    col_editor, col_sidebar = st.columns([2, 1], gap="large")
    
    with col_editor:
        st.markdown("<h3 style='color: #0284c7; font-size: 20px; font-weight: 700;'>Rich Text & Note Editor</h3>", unsafe_allow_html=True)
        c_top1, c_top2, c_top3 = st.columns([2, 1, 1], gap="small")
        
        with c_top1:
            note_title = st.text_input("নোটের শিরোনাম (Title):", value=st.session_state["current_title"])
        with c_top2:
            subjects_list = ["বাংলা", "ইংরেজি", "গণিত", "বিজ্ঞান", "বাংলাদেশ ও বিশ্বপরিচয়", "ধর্ম", "আইসিটি", "অন্যান্য"]
            try:
                sub_idx = subjects_list.index(st.session_state["current_subject"])
            except:
                sub_idx = 0
            note_subject = st.selectbox("বিষয় নির্বাচন করুন:", subjects_list, index=sub_idx)
        with c_top3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("+ নতুন নোট", use_container_width=True):
                st.session_state["current_title"] = ""
                st.session_state["current_content"] = ""
                st.session_state["edit_id"] = None
                st.rerun()
                
        save_choice = st.radio("নোটের ধরন:", ["Draft", "Final"], horizontal=True)
        backup_body = st.text_area("Note Content:", value=st.session_state["current_content"], height=160, placeholder="এখানে লিখুন...")
        
        btn_label = "Update Note" if st.session_state["edit_id"] is not None else "Save Note to Cloud"
        
        if st.button(btn_label, use_container_width=True, type="primary"):
            if note_title and backup_body:
                current_time_str = datetime.now().strftime("%d %B, %Y, %I:%M%p")
                note_payload = {
                    "title": note_title,
                    "content": backup_body,
                    "subject": note_subject,
                    "note_type": save_choice,
                    "created_at": current_time_str
                }
                try:
                    if st.session_state["edit_id"] is not None:
                        supabase.table("notes").update(note_payload).eq("id", st.session_state["edit_id"]).execute()
                        st.success("নোটটি ক্লাউডে আপডেট করা হয়েছে!")
                    else:
                        supabase.table("notes").insert(note_payload).execute()
                        st.success("নোটটি Supabase ডাটাবেজে সংরক্ষিত হয়েছে!")
                    
                    st.session_state["current_title"] = ""
                    st.session_state["current_content"] = ""
                    st.session_state["edit_id"] = None
                    st.rerun()
                except Exception as e:
                    st.error(f"Supabase এ সেভ করতে সমস্যা হয়েছে: {e}")
            else:
                st.error("শিরোনাম এবং কন্টেন্ট উভয়ই প্রদান করুন।")
                
        st.markdown("---")
        st.markdown("<h3 style='color: #0284c7; font-size: 18px;'>Saved Cloud Notes</h3>", unsafe_allow_html=True)
        
        try:
            res = supabase.table("notes").select("*").order("id", desc=True).execute()
            db_notes = res.data
            if db_notes:
                for row in db_notes:
                    n_id = row.get("id")
                    n_title = row.get("title")
                    n_content = row.get("content")
                    n_subject = row.get("subject")
                    n_type = row.get("note_type")
                    n_time = row.get("created_at", "")
                    
                    with st.expander(f"[{n_subject}] {n_title} ({n_type}) - {n_time}"):
                        st.markdown(n_content, unsafe_allow_html=True)
                        col_e, col_d = st.columns(2)
                        with col_e:
                            if st.button("এডিট", key=f"edit_n_{n_id}", use_container_width=True):
                                st.session_state["current_title"] = n_title
                                st.session_state["current_content"] = n_content
                                st.session_state["current_subject"] = n_subject
                                st.session_state["edit_id"] = n_id
                                st.rerun()
                        with col_d:
                            if st.button("ডিলিট", key=f"del_n_{n_id}", use_container_width=True):
                                supabase.table("notes").delete().eq("id", n_id).execute()
                                st.success("নোট মুছে ফেলা হয়েছে!")
                                st.rerun()
            else:
                st.info("Supabase এ কোনো সংরক্ষিত নোট নেই।")
        except Exception as e:
            st.error(f"ডাটা লোড করতে ব্যর্থ: {e}")
            
    with col_sidebar:
        st.info("Supabase Cloud Database status: Connected")