import streamlit as st
import json
import uuid
import urllib.parse 

# إعدادات الصفحة
st.set_page_config(page_title="متابعة ختمة القرآن", page_icon="📖", layout="wide")

# ==========================================
# كود التصميم (CSS) للغة العربية 
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Tajawal', sans-serif !important;
    }
    
    .stApp { direction: rtl; }
    
    p, div, h1, h2, h3, h4, h5, h6, span, label, input, textarea {
        text-align: right !important;
    }
    
    [data-testid="column"] { direction: rtl; }
    
    .dashboard-card {
        border-radius: 12px;
        padding: 20px 10px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .dashboard-card h2 { margin: 10px 0 5px 0 !important; font-size: 2.2rem !important; font-weight: 700 !important; color: white !important; text-align: center !important;}
    .dashboard-card p { margin: 0 !important; font-size: 1rem !important; opacity: 0.9 !important; text-align: center !important;}
    .dashboard-card .icon { font-size: 1.5rem !important; margin-bottom: 5px !important; text-align: center !important;}
    
    .card-green { background-color: #277953; }
    .card-yellow { background-color: #d4a32a; }
    .card-dark { background-color: #1a4d33; }
    .card-brown { background-color: #a47e1b; }
    
    .main-subtitle { text-align: center !important; color: #888; font-size: 1.1rem; margin-bottom: 25px; font-weight: 500;}
    .stats-text { color: #555; font-size: 0.95rem; font-weight: bold; }
    .stats-row { display: flex; justify-content: space-between; margin-top: 15px; margin-bottom: 5px; direction: rtl; }
    
    .dashboard-card * { text-align: center !important; }
</style>
""", unsafe_allow_html=True)

# كلمة المرور المركزية
MASTER_PASSWORD = "admin" 

# دوال التعامل مع البيانات
def load_data():
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            # التأكد من وجود مفتاح للرابط الأساسي
            if "base_url" not in data:
                data["base_url"] = ""
            return data
    except:
        return {"groups": {}, "base_url": ""}

def save_data(data):
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

db = load_data()
BASE_URL = db.get("base_url", "")
query_params = st.query_params

# ==========================================
# 1. واجهة المشاركين (تفتح مباشرة بدون تسجيل)
# ==========================================
if "group" in query_params and query_params["group"] in db["groups"]:
    group_id = query_params["group"]
    group_data = db["groups"][group_id]
    
    completed_parts = 0
    for status in group_data['parts']:
        if status == True or status == "تمت القراءة":
            completed_parts += 1
            
    progress_percentage = completed_parts / 30.0
    
    st.title(f"📖 {group_data['name']}")
    st.markdown("<div class='main-subtitle'>خطّط لرحلتك · تتبّع تقدمك · أتمم حفظ القرآن</div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: 
        st.markdown("<div class='dashboard-card card-green'><div class='icon'>📅</div><h2>528</h2><p>الأيام المتبقية</p></div>", unsafe_allow_html=True)
    with c2: 
        st.markdown("<div class='dashboard-card card-yellow'><div class='icon'>🌙</div><h2>17.6</h2><p>الأشهر</p></div>", unsafe_allow_html=True)
    with c3: 
        st.markdown("<div class='dashboard-card card-dark'><div class='icon'>📖</div><h2>3/114</h2><p>السور المحفوظة</p></div>", unsafe_allow_html=True)
    with c4: 
        st.markdown("<div class='dashboard-card card-brown'><div class='icon'>🏁</div><h2>ديسمبر 2027</h2><p>موعد الإتمام المتوقع</p></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='stats-row'>
        <span class='stats-text'>مكتمل بنسبة {int(progress_percentage * 100)}%</span>
        <span class='stats-text'>الأجزاء المنجزة: {completed_parts}/30 جزء</span>
    </div>
    """, unsafe_allow_html=True)
    st.progress(progress_percentage)
    st.write("---")

    tab_mark, tab_details, tab_schedule, tab_overview = st.tabs([
        "✅ تأكيد الحفظ", "📖 تفاصيل السورة", "📅 الجدول الزمني", "📊 ملخص الأجزاء"
    ])

    with tab_mark:
        st.subheader("حدد السور المحفوظة")
        btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
        with btn_col1: st.button("تحديد الكل", use_container_width=True)
        with btn_col2: st.button("إلغاء التحديد", use_container_width=True)
        with btn_col3: st.button("تحديد الجزء 30", use_container_width=True)
        with btn_col4: st.button("تحديد الجزأين 29 و 30", use_container_width=True)
        st.write("---")
        st.info("هذا القسم مخصص لتأكيد الحفظ اليومي للمشاركين، سيتم تفعيل خصائصه لاحقاً.")
    
    with tab_details: st.info("هذا القسم مخصص لعرض تفاصيل السور ومتابعتها.")
    with tab_schedule: st.info("هذا القسم مخصص للجدول الزمني لخطة القراءة أو الحفظ.")

    with tab_overview:
        st.subheader("جدول القراءة الحالي")
        status_options = ["لم تبدأ", "جاري القراءة", "تمت القراءة"]

        for i in range(30):
            col1, col2, col3, col4 = st.columns([1, 1.5, 1.5, 1])
            with col1: st.write(f"**الجزء {i+1}**")
            with col2: st.write(f"القارئ: {group_data['readers'][i]}")
                
            current_status = group_data['parts'][i]
            if current_status == False: current_status = "لم تبدأ"
            elif current_status == True: current_status = "تمت القراءة"
                
            with col3:
                selected_status = st.selectbox(
                    "الحالة", status_options, index=status_options.index(current_status), 
                    key=f"status_{i}", label_visibility="collapsed"
                )
                if selected_status != current_status:
                    group_data['parts'][i] = selected_status
                    save_data(db)
                    st.rerun()

            with col4:
                if current_status != "تمت القراءة":
                    app_link_to_use = BASE_URL if BASE_URL else "الرابط_غير_متوفر"
                    msg = f"السلام عليكم\nتذكير بقراءة *الجزء {i+1}*\nالقارئ: *{group_data['readers'][i]}*\n\nالرابط لتسجيل الإتمام:\n{app_link_to_use}/?group={group_id}"
                    encoded_msg = urllib.parse.quote(msg)
                    wa_link = f"https://wa.me/?text={encoded_msg}"
                    st.link_button("📱 تذكير", wa_link)
                else:
                    st.write("✅ مكتمل")

        st.write("---")
        st.subheader("⚙️ إدارة الختمة (لآدمن المجموعة)")
        if completed_parts == 30:
            st.success("🎉 ما شاء الله! اكتملت قراءة جميع الأجزاء.")
            admin_password = st.text_input("أدخل كلمة المرور لإغلاق الختمة وترحيل الأسماء:", type="password")
            if st.button("حفظ وإغلاق الختمة"):
                if admin_password == group_data["password"]:
                    group_data["khatma_count"] += 1
                    readers = group_data["readers"]
                    group_data["readers"] = [readers[-1]] + readers[:-1] 
                    group_data["parts"] = ["لم تبدأ"] * 30 
                    save_data(db)
                    st.success("تم إغلاق الختمة بنجاح، وترحيل الأسماء للختمة الجديدة!")
                    st.rerun()
                else:
                    st.error("كلمة المرور غير صحيحة!")
        else:
            st.warning("يجب إتمام قراءة جميع الأجزاء الـ 30 لتفعيل زر إغلاق الختمة.")

# ==========================================
# 2. لوحة التحكم المركزية (للآدمن فقط)
# ==========================================
else:
    st.title("⚙️ لوحة التحكم المركزية")
    st.warning("هذه الصفحة مخصصة لمدير النظام. الرجاء إدخال كلمة المرور للوصول للإعدادات.")
    
    admin_login = st.text_input("كلمة المرور المركزية:", type="password")
    
    if admin_login == MASTER_PASSWORD:
        st.success("تم تسجيل الدخول بنجاح.")
        
        tab1, tab2, tab3, tab4 = st.tabs(["🔗 إعداد الروابط", "➕ إضافة مجموعة", "📝 تعديل الأسماء", "📱 رسالة الواتساب"])
        
        # --- التبويب الجديد للتعرف التلقائي على الرابط ---
        with tab1:
            st.subheader("إعداد الرابط الأساسي للتطبيق")
            st.info("انسخ رابط موقعك من أعلى المتصفح (مثال: https://quran-tracker.streamlit.app) والصقه هنا مرة واحدة لكي تعمل جميع روابط المجموعات والواتساب بشكل صحيح.")
            
            new_base_url = st.text_input("الرابط الأساسي:", value=BASE_URL)
            if st.button("حفظ الرابط الأساسي"):
                db["base_url"] = new_base_url.strip("/")
                save_data(db)
                st.success("تم حفظ الرابط بنجاح! جميع الروابط الآن ستعمل دون مشاكل.")
                st.rerun()
                
            st.write("---")
            st.subheader("روابط المجموعات الحالية (جاهزة للنسخ والنشر)")
            if not BASE_URL:
                st.error("يرجى إدخال الرابط الأساسي في الأعلى أولاً لتوليد روابط المجموعات.")
            else:
                for g_id, g_info in db["groups"].items():
                    st.write(f"**{g_info['name']}**")
                    group_direct_link = f"{BASE_URL}/?group={g_id}"
                    st.code(group_direct_link, language="text")
                    st.markdown(f"[اضغط هنا للدخول المباشر للمجموعة]({group_direct_link})")
                
        with tab2:
            st.subheader("إنشاء مجموعة جديدة")
            new_group_name = st.text_input("اسم المجموعة (مثال: عائلة أحمد):")
            new_group_pass = st.text_input("كلمة المرور الخاصة بإغلاق ختمة هذه المجموعة:")
            
            default_names = "\n".join([f"قارئ {i+1}" for i in range(30)])
            new_readers_text = st.text_area("أدخل أسماء القراء الـ 30 (كل اسم في سطر جديد):", value=default_names, height=350)
            
            if st.button("إنشاء المجموعة ورفع البيانات"):
                readers_list = [name.strip() for name in new_readers_text.split('\n') if name.strip()]
                
                if not new_group_name or not new_group_pass:
                    st.error("الرجاء كتابة اسم المجموعة وكلمة المرور.")
                elif len(readers_list) != 30:
                    st.error(f"يجب إدخال 30 اسماً بالضبط! (أنت أدخلت {len(readers_list)} اسم).")
                else:
                    new_id = "group_" + str(uuid.uuid4())[:8] 
                    db["groups"][new_id] = {
                        "name": new_group_name,
                        "password": new_group_pass,
                        "khatma_count": 0,
                        "parts": ["لم تبدأ"] * 30,
                        "readers": readers_list
                    }
                    save_data(db)
                    st.success("تم إنشاء المجموعة بنجاح! اذهب لتبويب 'الروابط' لنسخ رابطها.")
                    st.rerun()

        with tab3:
            st.subheader("تعديل قراء مجموعة حالية")
            if db["groups"]:
                edit_group_id = st.selectbox("اختر المجموعة المراد تعديلها:", list(db["groups"].keys()), format_func=lambda x: db["groups"][x]["name"], key="edit_select")
                current_readers_text = "\n".join(db["groups"][edit_group_id]["readers"])
                
                edited_readers_text = st.text_area("قم بتعديل الأسماء هنا (تأكد أن العدد 30):", value=current_readers_text, height=350, key="edit_area")
                
                if st.button("حفظ التعديلات"):
                    edited_list = [name.strip() for name in edited_readers_text.split('\n') if name.strip()]
                    if len(edited_list) != 30:
                        st.error(f"يجب أن يظل العدد 30 اسماً! (العدد الحالي: {len(edited_list)}).")
                    else:
                        db["groups"][edit_group_id]["readers"] = edited_list
                        save_data(db)
                        st.success("تم تحديث أسماء القراء بنجاح!")
                        st.rerun()
            else:
                st.info("لا توجد مجموعات حالياً.")
                
        with tab4:
            st.subheader("تجهيز رسالة الواتساب (لغير المكتملين فقط)")
            if db["groups"]:
                wa_group_id = st.selectbox("اختر المجموعة لتوليد الرسالة:", list(db["groups"].keys()), format_func=lambda x: db["groups"][x]["name"], key="wa_select")
                wa_group_info = db["groups"][wa_group_id]
                
                app_link_to_use = BASE_URL if BASE_URL else "الرابط_غير_متوفر"
                group_link = f"{app_link_to_use}/?group={wa_group_id}"
                
                msg_lines = []
                msg_lines.append(f"📖 *تذكير بالأجزاء المتبقية - {wa_group_info['name']}* 📖")
                msg_lines.append("ــــــــــــــــــــــــــــــــــــــــــ")
                
                has_remaining = False
                for i in range(30):
                    part_status = wa_group_info['parts'][i]
                    if part_status == False: part_status = "لم تبدأ"
                    elif part_status == True: part_status = "تمت القراءة"
                    
                    if part_status != "تمت القراءة":
                        msg_lines.append(f"الجزء {i+1} : {wa_group_info['readers'][i]}")
                        has_remaining = True
                        
                if not has_remaining:
                    msg_lines.append("🎉 اكتملت قراءة جميع الأجزاء بفضل الله!")
                    
                msg_lines.append("ــــــــــــــــــــــــــــــــــــــــــ")
                msg_lines.append(f"🔗 *رابط المجموعة لتسجيل القراءة:*")
                msg_lines.append(group_link)
                
                whatsapp_text = "\n".join(msg_lines)
                st.write("انسخ النص التالي وقم بلصقه في الواتساب:")
                st.code(whatsapp_text, language="text")
            else:
                st.info("لا توجد مجموعات حالياً.")
                
    elif admin_login != "":
        st.error("كلمة المرور خاطئة!")
