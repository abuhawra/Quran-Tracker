import streamlit as st
import json
import uuid
import urllib.parse 

# إعدادات الصفحة (تم التعديل لتكون الواجهة عريضة لتناسب البطاقات الأربع)
st.set_page_config(page_title="متابعة ختمة القرآن", page_icon="📖", layout="wide")

# ==========================================
# كود التصميم (CSS) للغة العربية والبطاقات المستوحاة من الصورة
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
    
    /* تنسيق بطاقات الإحصائيات العلوية */
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
    
    /* ألوان البطاقات مطابقة للصورة */
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

# الإعدادات العامة
MASTER_PASSWORD = "admin" 
BASE_URL = "https://your-app-name.streamlit.app" # ⚠️ ضع رابط موقعك الحقيقي هنا

# دالة لقراءة البيانات
def load_data():
    with open('data.json', 'r', encoding='utf-8') as file:
        return json.load(file)

# دالة لحفظ البيانات
def save_data(data):
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

db = load_data()
query_params = st.query_params

if "group" in query_params and query_params["group"] in db["groups"]:
    # ==========================================
    # واجهة المشاركين (داخل المجموعة)
    # ==========================================
    group_id = query_params["group"]
    group_data = db["groups"][group_id]
    
    # حساب الأجزاء المكتملة لربطها بشريط التقدم
    completed_parts = 0
    for status in group_data['parts']:
        if status == True or status == "تمت القراءة":
            completed_parts += 1
            
    progress_percentage = completed_parts / 30.0
    
    st.title(f"📖 {group_data['name']}")
    
    # الشعار النصي العلوي المترجم
    st.markdown("<div class='main-subtitle'>خطّط لرحلتك · تتبّع تقدمك · أتمم حفظ القرآن</div>", unsafe_allow_html=True)

    # البطاقات الأربع المترجمة
    c1, c2, c3, c4 = st.columns(4)
    with c1: 
        st.markdown("<div class='dashboard-card card-green'><div class='icon'>📅</div><h2>528</h2><p>الأيام المتبقية</p></div>", unsafe_allow_html=True)
    with c2: 
        st.markdown("<div class='dashboard-card card-yellow'><div class='icon'>🌙</div><h2>17.6</h2><p>الأشهر</p></div>", unsafe_allow_html=True)
    with c3: 
        st.markdown("<div class='dashboard-card card-dark'><div class='icon'>📖</div><h2>3/114</h2><p>السور المحفوظة</p></div>", unsafe_allow_html=True)
    with c4: 
        st.markdown("<div class='dashboard-card card-brown'><div class='icon'>🏁</div><h2>ديسمبر 2027</h2><p>موعد الإتمام المتوقع</p></div>", unsafe_allow_html=True)

    # شريط التقدم التفاعلي (مربوط بنسبة إنجاز الختمة الفعلية)
    st.markdown(f"""
    <div class='stats-row'>
        <span class='stats-text'>مكتمل بنسبة {int(progress_percentage * 100)}%</span>
        <span class='stats-text'>الأجزاء المنجزة: {completed_parts}/30 جزء</span>
    </div>
    """, unsafe_allow_html=True)
    st.progress(progress_percentage)
    st.write("---")

    # التبويبات المترجمة من الصورة
    tab_mark, tab_details, tab_schedule, tab_overview = st.tabs([
        "✅ تأكيد الحفظ", 
        "📖 تفاصيل السورة", 
        "📅 الجدول الزمني", 
        "📊 ملخص الأجزاء"
    ])

    with tab_mark:
        st.info("هذا القسم مخصص لتأكيد الحفظ اليومي للمشاركين.")
    
    with tab_details:
        st.info("هذا القسم مخصص لعرض تفاصيل السور ومتابعتها.")
        
    with tab_schedule:
        st.info("هذا القسم مخصص للجدول الزمني لخطة القراءة أو الحفظ.")

    # وضعنا جدول الـ 30 جزء داخل تبويب (ملخص الأجزاء) ليكون في مكانه الصحيح
    with tab_overview:
        st.subheader("جدول القراءة الحالي")
        status_options = ["لم تبدأ", "جاري القراءة", "تمت القراءة"]

        for i in range(30):
            col1, col2, col3, col4 = st.columns([1, 1.5, 1.5, 1])
            
            with col1:
                st.write(f"**الجزء {i+1}**")
            with col2:
                st.write(f"القارئ: {group_data['readers'][i]}")
                
            current_status = group_data['parts'][i]
            if current_status == False: current_status = "لم تبدأ"
            elif current_status == True: current_status = "تمت القراءة"
                
            with col3:
                selected_status = st.selectbox(
                    "الحالة", 
                    status_options, 
                    index=status_options.index(current_status), 
                    key=f"status_{i}", 
                    label_visibility="collapsed"
                )
                
                if selected_status != current_status:
                    group_data['parts'][i] = selected_status
                    save_data(db)
                    st.rerun()

            with col4:
                if current_status != "تمت القراءة":
                    msg = f"السلام عليكم\nتذكير بقراءة *الجزء {i+1}*\nالقارئ: *{group_data['readers'][i]}*\n\nالرابط لتسجيل الإتمام:\n{BASE_URL}/?group={group_id}"
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

else:
    # ==========================================
    # واجهة لوحة التحكم المركزية (الآدمن الرئيسي)
    # ==========================================
    st.title("⚙️ لوحة التحكم المركزية")
    st.warning("هذه الصفحة مخصصة لمدير النظام. الرجاء إدخال كلمة المرور للوصول للإعدادات.")
    
    admin_login = st.text_input("كلمة المرور المركزية:", type="password")
    
    if admin_login == MASTER_PASSWORD:
        st.success("تم تسجيل الدخول بنجاح.")
        
        tab1, tab2, tab3, tab4 = st.tabs(["🔗 الروابط", "➕ إضافة مجموعة", "📝 تعديل الأسماء", "📱 رسالة الواتساب"])
        
        with tab1:
            st.subheader("روابط المجموعات الحالية")
            for g_id, g_info in db["groups"].items():
                st.write(f"**{g_info['name']}**")
                st.code(f"{BASE_URL}/?group={g_id}", language="text")
                
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
                    st.success("تم إنشاء المجموعة بنجاح!")
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
                group_link = f"{BASE_URL}/?group={wa_group_id}"
                
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
