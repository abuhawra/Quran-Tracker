import streamlit as st
import json
import uuid
import urllib.parse 

# إعدادات الصفحة
st.set_page_config(page_title="متابعة ختمة القرآن", page_icon="📖", layout="centered")

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
    
    st.title(f"📖 {group_data['name']}")
    st.info(f"**عدد الختمات المكتملة لهذه المجموعة: {group_data['khatma_count']} ختمة**")
    st.write("---")

    st.subheader("جدول القراءة الحالي")
    completed_parts = 0
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
            # زر الواتساب الفردي يظهر فقط لمن لم يتم القراءة
            if current_status != "تمت القراءة":
                msg = f"السلام عليكم\nتذكير بقراءة *الجزء {i+1}*\nالقارئ: *{group_data['readers'][i]}*\n\nالرابط لتسجيل الإتمام:\n{BASE_URL}/?group={group_id}"
                encoded_msg = urllib.parse.quote(msg)
                wa_link = f"https://wa.me/?text={encoded_msg}"
                st.link_button("📱 تذكير", wa_link)
            else:
                st.write("✅ مكتمل")

        if group_data['parts'][i] == "تمت القراءة":
            completed_parts += 1

    st.write("---")
    st.subheader("⚙️ إدارة الختمة (لآدمن المجموعة)")
    st.progress(completed_parts / 30)
    st.write(f"الأجزاء المكتملة: {completed_parts} من 30")

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
                    
                    # إدراج الجزء واسم القارئ فقط إذا لم تتم القراءة
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
