import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. إعدادات الصفحة الكلية بأسلوب احترافي
st.set_page_config(
    page_title="نظام الإنذار المبكر الذكي - EWS",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. حقن الـ CSS المتقدم لضبط واجهة المستخدم (RTL، الخطوط، والبطاقات المخصصة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    /* ضبط الاتجاه والخطوط لكافة عناصر التطبيق */
    html, body, [data-testid="stSidebar"], .stApp, p, div, h1, h2, h3, h4, h5, h6 {
        font-family: 'Cairo', sans-serif !important;
        direction: RTL !important;
        text-align: right !important;
    }
    
    /* تنسيق البطاقات المالية الرقمية */
    .metric-card {
        background-color: #1e293b;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    .metric-title {
        color: #94a3b8;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .metric-value {
        color: #f8fafc;
        font-size: 24px;
        font-weight: 700;
    }
    
    /* ضبط القائمة الجانبية */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-left: 1px solid #1e293b;
    }
    
    /* إلغاء أيقونات الاستجابة التلقائية المقلوبة */
    [data-testid="stMetricDelta"] {
        direction: LTR !important;
        text-align: left !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. القائمة الجانبية المتقدمة للتنقل ( Multi-page Navigation )
st.sidebar.markdown("<h2 style='color:#38bdf8; text-align:center;'>🛡️ نظام EWS الذكي</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align:center; color:#94a3b8; font-size:12px;'>حوكمة الإدارة المالية بالهيئات الرياضية</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

st.sidebar.subheader("📌 قائمة التنقل الرئيسية")
page = st.sidebar.radio(
    "اختر الشاشة الرقابية :",
    ["🎛️ لوحة المؤشرات العامة", "🚨 محرك الإنذار المبكر", "📊 تحليلات بنود الموازنة", "🛡️ سجل التتبع والحوكمة ( Audit )"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ محددات النظام الحالي")
selected_club = st.sidebar.selectbox("الهيئة الرياضية :", ["مجمع أبو الهول للألعاب الرياضية", "نادي الإسكندرية الرياضي", "نادي سبورتنج الرياضي"])
financial_period = st.sidebar.selectbox("الفترة المالية :", ["الربع السنوي الحالي (2026)", "الحساب الختامي المتوقع"])

# بيانات ممررة عامة للمحاكاة التفصيلية
budget_data = {
    "عقود اللاعبين": {"مخطط": 6000000, "فعلي": 6500000, "متبقي": -500000, "نسبة": 108.3},
    "صيانة المنشآت": {"مخطط": 3000000, "فعلي": 1200000, "متبقي": 1800000, "نسبة": 40.0},
    "رواتب الموظفين": {"مخطط": 4000000, "فعلي": 3800000, "متبقي": 200000, "نسبة": 95.0},
    "المصروفات الإدارية": {"مخطط": 2000000, "فعلي": 1500000, "متبقي": 500000, "نسبة": 75.0}
}

# ==========================================
# الشاشة الأولى: لوحة المؤشرات العامة
# ==========================================
if page == "🎛️ لوحة المؤشرات العامة":
    st.markdown("<h1 style='color:#f8fafc;'>🎛️ لوحة المؤشرات المالية العامة</h1>", unsafe_allow_html=True)
    st.markdown(f"الوضع المالي الموحد الحالي لـ **{selected_club}** بناءً على المدخلات الرقمية واللوائح المستندية .")
    st.markdown("---")
    
    # عرض البطاقات بأسلوب الكروت الاحترافي الداكن
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-title">إجمالي الاعتمادات المعتمدة</div>
            <div class="metric-value">15,000,000 ج.م</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-title">إجمالي الصرف الفعلي</div>
            <div class="metric-value" style="color:#ef4444;">13,000,000 ج.م</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-title">السيولة النقدية المتاحة</div>
            <div class="metric-value" style="color:#10b981;">2,000,000 ج.م</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-title">معدل الامتثال والحوكمة</div>
            <div class="metric-value" style="color:#38bdf8;">94 %</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("### 📊 نظرة عامة على كفاءة بنود الصرف")
    
    # تحويل البيانات إلى DataFrame للرسم البياني المتطور عبر Plotly
    df_chart = pd.DataFrame.from_dict(budget_data, orient='index').reset_index()
    df_chart.columns = ['البند المالي', 'المخطط', 'الفعلي', 'المتبقي', 'النسبة']
    
    fig = px.bar(
        df_chart, 
        x='البند المالي', 
        y=['المخطط', 'الفعلي'], 
        barmode='group',
        template='plotly_dark',
        color_discrete_sequence=['#38bdf8', '#ef4444'],
        labels={'value': 'المبلغ بالجنيه المصري', 'variable': 'نوع البيان'}
    )
    fig.update_layout(font_family="Cairo", title_text="مقارنة الصرف الفعلي بالاعتمادات المخططة لكل بند")
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# الشاشة الثانية: محرك الإنذار المبكر
# ==========================================
elif page == "🚨 محرك الإنذار المبكر":
    st.markdown("<h1 style='color:#ef4444;'>🚨 محرك التنبؤ ورصد الانحرافات اللحظي</h1>", unsafe_allow_html=True)
    st.markdown("شاشة فحص التنبيهات الصادرة عن خوارزميات اكتشاف الشذوذ ( Anomaly Detection ) والمادة 97 بقانون العقوبات .")
    st.markdown("---")
    
    st.subheader("⚠️ الإنذارات النشطة حالياً")
    
    # إنذار أحمر
    st.error("""
        **🔴 إنذار حرج - تجاوز الصرف الفعلي للاعتماد ( بند عقود اللاعبين والأجهزة الفنية ) :** * **طبيعة المخالفة :** تم رصد قيد ارتباط مالي بقيمة 500,000 ج.م يمثل تجاوزاً صريحاً للربط المالي السنوي المعتمد .  
        * **المستند المصدر :** استمارة 50 ع.ح رقم ( 98213 ) .  
        * **التأثير القانوني :** عائق إجرائي يخالف اللائحة المالية الموحدة للأندية .  
        * **التوصية الآلية للنظام :** تجميد أمر الصرف فوراً ، وإحالة المعاملة لمدير الشئون المالية لإعادة تدقيق المستندات الورقية عبر الـ OCR .
    """)
    
    # إنذار برتقالي
    st.warning("""
        **🟡 إنذار استباقي - مخاطر نقص سيولة حاد ( بند التزامات الضرائب والتأمينات ) :** * **طبيعة المخالفة :** التحليل التنبئي يشير إلى عجز متوقع في تغذية الحسابات الجارية خلال 45 يوماً نتيجة تباطؤ تحصيل نسب عقود الرعاية .  
        * **التوصية الآلية للنظام :** تفعيل تقنيات تنقيب العمليات ( Process Mining ) لتسريع الدورة الإجرائية لتحصيل عوائد البث المتأخرة .
    """)

# ==========================================
# الشاشة الثالثة: تحليلات بنود الموازنة
# ==========================================
elif page == "📊 تحليلات بنود الموازنة":
    st.markdown("<h1 style='color:#38bdf8;'>📊 التفاصيل التحليلية المتقدمة لبنود الموازنة</h1>", unsafe_allow_html=True)
    st.markdown("جداول تفصيلية ومؤشرات مرئية لكافة مراكز التكلفة داخل الهيئة الرياضية .")
    st.markdown("---")
    
    df_table = pd.DataFrame.from_dict(budget_data, orient='index').reset_index()
    df_table.columns = ['البند المالي المستهدف', 'الربط المالي المعتمد (ج.م)', 'الصرف الفعلي اللحظي (ج.م)', 'الوفر / العجز الحالي (ج.م)', 'نسبة الاستهلاك %']
    
    st.subheader("📋 جدول المطابقة المالية التفصيلي")
    st.dataframe(df_table.style.format({
        'الربط المالي المعتمد (ج.م)': '{:,.0f}',
        'الصرف الفعلي اللحظي (ج.م)': '{:,.0f}',
        'الوفر / العجز الحالي (ج.م)': '{:,.0f}',
        'نسبة الاستهلاك %': '{:.1f}%'
    }), use_container_width=True)
    
    st.markdown("---")
    st.subheader("🔮 النمذجة التنبؤية لحركة السيولة المستقبلية")
    
    # رسم بياني خطي متطور للتنبؤ بالشهور القادمة عبر Plotly
    months = ['يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
    predicted_flow = [5800000, 5400000, 4900000, 4200000, 3900000, 5500000]
    
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=months, y=predicted_flow, mode='lines+markers', name='السيولة المتوقعة', line=dict(color='#10b981', width=3)))
    fig_line.update_layout(template='plotly_dark', font_family="Cairo", title_text="تحليل محاكاة التدفقات النقدية الخارجة المتوقعة")
    st.plotly_chart(fig_line, use_container_width=True)

# ==========================================
# الشاشة الرابعة: سجل التتبع والحوكمة
# ==========================================
elif page == "🛡️ سجل التتبع والحوكمة ( Audit )":
    st.markdown("<h1 style='color:#10b981;'>🛡️ سجل تتبع نزاهة البيانات والامتثال الرقمي</h1>", unsafe_allow_html=True)
    st.markdown("توثيق برمجية غير قابلة للتعديل ( Audit Trail ) لكافة الحركات والوصول المعلوماتي لحماية المراقب المالي .")
    st.markdown("---")
    
    audit_log = pd.DataFrame({
        'التوقيت والزمن اللحظي': ['2026-06-10 14:22:15', '2026-06-10 11:05:02', '2026-06-09 09:15:40', '2026-06-08 13:01:12'],
        'المستخدم / الكادر البشري': ['المراقب المالي المعتمد', 'نظام EWS ( خوارزمية تلقائية )', 'مدير إدارة الشئون المالية', 'مفتش وزارة الشباب والرياضة'],
        'الإجراء المتخذ تفصيلاً': ['اعتماد طلب صرف مستحقات شركة المقاولات صيانة منشآت', 'رفض معاملة تعديل بند حوافز صفقات اللاعبين لعدم قانونيته', 'تحديث وتغذية قاعدة بيانات الموردين والمقاولين المتعثرين', 'ولوج للرقابة عن بعد ومراجعة تقارير المطابقة للمخازن'],
        'حالة الامتثال للائحة الموحدة': ['✅ متوافق وممتثل تشريعياً', '❌ تم الحجب - محاولة تجاوز بند مالي', '⚠️ مراجعة بشرية معلقة', '✅ فحص نظامي سليم']
    })
    
    st.table(audit_log)