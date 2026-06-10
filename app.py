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
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght=400;600;700&display=swap');
    
    html, body, [data-testid="stSidebar"], .stApp, p, div, h1, h2, h3, h4, h5, h6 {
        font-family: 'Cairo', sans-serif !important;
        direction: RTL !important;
        text-align: right !important;
    }
    
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
    
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-left: 1px solid #1e293b;
    }
    
    [data-testid="stMetricDelta"] {
        direction: LTR !important;
        text-align: left !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. قاعدة البيانات الشاملة المحدثة بناءً على تقرير المديونيات والانحرافات الفعلي
clubs_database = {
    "نادي سموحة الرياضي": {
        "metrics": {"budget": "120,000,000 ج.م", "spent": "142,500,000 ج.م", "liquidity": "-22,500,000 ج.م", "compliance": "78 %"},
        "budget_data": {
            "عقود وعمولات اللاعبين": {"مخطط": 50000000, "فعلي": 68000000, "متبقي": -18000000, "نسبة": 136.0},
            "إنشاءات ومقاولات مدرجات": {"مخطط": 40000000, "فعلي": 43500000, "متبقي": -3500000, "نسبة": 108.7},
            "الأجور ومرتبات العاملين": {"مخطط": 20000000, "فعلي": 19800000, "متبقي": 200000, "نسبة": 99.0},
            "المصروفات النثرية والإدارية": {"مخطط": 10000000, "فعلي": 11200000, "متبقي": -1200000, "نسبة": 112.0}
        },
        "alerts": {
            "critical": "🔴 إنذار حرج - رصد مديونيات متراكمة وعقود غير مغطاة بنادي سموحة :\nخوارزميات الشذوذ المالي كشفت عن إبرام ملحقات عقود إضافية لقطاع كرة القدم دون وجود غطاء مالي معتمد بالموازنة ، مما تسبب في عجز نقدي حاد وتجاوز لنسب الصرف المقررة قانوناً .",
            "warning": "🟡 إنذار استباقي - مخالفة إدارية في مسارات الصرف بند المقاولات :\nتم رصد قيد ارتباط مالي مستندي يتضمن صرف مستحقات لمقاول بناء قبل إتمام مرحلة الفحص الفني والاعتماد من الإدارة الهندسية بالمخالفة للدورة المستندية للحوكمة ."
        },
        "forecast": [-5000000, -12000000, -18000000, -22500000, -15000000, 2000000],
        "audit_user": "مراقب الحسابات المعين من الجهة الإدارية"
    },
    "النادي الأوليمبي المصري": {
        "metrics": {"budget": "35,000,000 ج.م", "spent": "41,200,000 ج.م", "liquidity": "-6,200,000 ج.م", "compliance": "81 %"},
        "budget_data": {
            "عقود وعمولات اللاعبين": {"مخطط": 15000000, "فعلي": 19500000, "متبقي": -4500000, "نسبة": 130.0},
            "صيانة وإيجار الملاعب": {"مخطط": 10000000, "فعلي": 11200000, "متبقي": -1200000, "نسبة": 112.0},
            "الأجور ومرتبات العاملين": {"مخطط": 7000000, "فعلي": 7100000, "متبقي": -100000, "نسبة": 101.4},
            "المصروفات النثرية والإدارية": {"مخطط": 3000000, "فعلي": 3400000, "متبقي": -400000, "نسبة": 113.3}
        },
        "alerts": {
            "critical": "🔴 إنذار حرج - شبهة تكرار مستندي وانحراف إداري بالنادي الأوليمبي :\nتقنيات الـ OCR كشفت عن مطابقة كاملة في البيانات المستندية لفاتورتين منفصلتين لتوريد ملابس رياضية بفروق زمنية قصيرة ، مما يشير لشبهة تكرار صرف واختلال في الرقابة الداخلية .",
            "warning": "🟡 إنذار استباقي - تراكم مديونيات هيئة الأوقاف والضرائب :\nالنظام يتوقع صدور حكم قضائي بالحجز على الحسابات الجارية للنادي نتيجة عدم إدراج مخصصات مالية كافية لسداد المتأخرات السيادية المتراكمة لعام 2026 ."
        },
        "forecast": [-1200000, -3400000, -4800000, -6200000, -2100000, 500000],
        "audit_user": "مدير إدارة التفتيش المالي بمديرية الشباب والرياضة"
    },
    "نادي الإسكندرية الرياضي": {
        "metrics": {"budget": "85,000,000 ج.م", "spent": "81,400,000 ج.م", "liquidity": "3,600,000 ج.م", "compliance": "95 %"},
        "budget_data": {
            "عقود وعمولات اللاعبين": {"مخطط": 40000000, "فعلي": 39200000, "متبقي": 800000, "نسبة": 98.0},
            "صيانة وإيجار الملاعب": {"مخطط": 25000000, "فعلي": 23800000, "متبقي": 1200000, "نسبة": 95.2},
            "الأجور ومرتبات العاملين": {"مخطط": 15000000, "فعلي": 14900000, "متبقي": 100000, "نسبة": 99.3},
            "المصروفات النثرية والإدارية": {"مخطط": 5000000, "فعلي": 3500000, "متبقي": 1500000, "نسبة": 70.0}
        },
        "alerts": {
            "critical": "🟢 الوضع مستقر نظامياً - لا توجد انحرافات حرجة نشطة : \nكافة مسارات الصرف الحالية بنادي الإسكندرية الرياضي مطابقة للربط المالي للائحة المالية الموحدة ، مع تسجيل كامل محاضر مجلس الإدارة رقمياً بنسبة امتثال 95 % .",
            "warning": "🟡 تنبيه استباقي - تدقيق عقود الرعاية السنوية :\nالنظام يوصي بتسريع إجراءات المراجعة القانونية لملف التجديد الخاص بمزايدة حقول الإعلانات لتفادي فجوة تدفقات نقدية في الربع المالي القادم ."
        },
        "forecast": [4500000, 5200000, 3100000, 3600000, 6800000, 8000000],
        "audit_user": "المراقب المالي المقيم لوزارة الشباب والرياضة"
    }
}

# 4. القائمة الجانبية المتقدمة للتنقل وتحديد النادي
st.sidebar.markdown("<h2 style='color:#38bdf8; text-align:center;'>🛡️ نظام EWS الذكي</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align:center; color:#94a3b8; font-size:12px;'>حوكمة الإدارة المالية بالهيئات الرياضية</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

st.sidebar.subheader("⚙️ محددات النظام والنادي")
selected_club = st.sidebar.selectbox("اختر الهيئة الرياضية المستهدفة :", list(clubs_database.keys()))
financial_period = st.sidebar.selectbox("الفترة المالية الحالية :", ["الربع السنوي الحالي ( 2026 )", "الحساب الختامي المتوقع"])

st.sidebar.markdown("---")
st.sidebar.subheader("📌 قائمة التنقل الرئيسية")
page = st.sidebar.radio(
    "اختر الشاشة الرقابية :",
    ["🎛️ لوحة المؤشرات العامة", "🚨 محرك الإنذار المبكر", "📊 تحليلات بنود الموازنة", "🛡️ سجل التتبع والحوكمة ( Audit )"]
)

# استدعاء البيانات الخاصة بالنادي المحدد تلقائياً
current_data = clubs_database[selected_club]

# ==========================================
# الشاشة الأولى: لوحة المؤشرات العامة
# ==========================================
if page == "🎛️ لوحة المؤشرات العامة":
    st.markdown(f"<h1 style='color:#f8fafc;'>🎛️ لوحة المؤشرات المالية العامة</h1>", unsafe_allow_html=True)
    st.markdown(f"تحليل تدفقات مديونيات ومؤشرات الامتثال اللحظي لـ **{selected_club}** وفقاً لتقرير الفحص المالي والإداري الموحد .")
    st.markdown("---")
    
    # عرض البطاقات بأسلوب الكروت الاحترافي الديناميكي بناءً على النادي المختار
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-title">إجمالي الموازنة المعتمدة</div>
            <div class="metric-value">{current_data["metrics"]["budget"]}</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-title">إجمالي الصرف الفعلي</div>
            <div class="metric-value" style="color:#ef4444;">{current_data["metrics"]["spent"]}</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-title">السيولة النقدية المتاحة / العجز</div>
            <div class="metric-value" style="color:#10b981;">{current_data["metrics"]["liquidity"]}</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-title">معدل الامتثال والحوكمة الرقمية</div>
            <div class="metric-value" style="color:#38bdf8;">{current_data["metrics"]["compliance"]}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("### 📊 نظرة عامة على كفاءة بنود الصرف ومدى تجاوز مراكز التكلفة")
    
    # تحويل البيانات ديناميكياً للرسم البياني المتطور
    df_chart = pd.DataFrame.from_dict(current_data["budget_data"], orient='index').reset_index()
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
    fig.update_layout(font_family="Cairo", title_text=f"مقارنة الانحرافات المالية بين الصرف الفعلي والربط المعتمد - {selected_club}")
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# الشاشة الثانية: محرك الإنذار المبكر
# ==========================================
elif page == "🚨 محرك الإنذار المبكر":
    st.markdown("<h1 style='color:#ef4444;'>🚨 محرك التنبؤ ورصد الانحرافات اللحظي</h1>", unsafe_allow_html=True)
    st.markdown(f"فحص ومطابقة المخاطر المالية والإدارية المرصودة آلياً لنادي **{selected_club}** .")
    st.markdown("---")
    
    st.subheader("⚠️ سجل الإنذارات والمخالفات النشطة بالنادي")
    if "مستقر" in current_data["alerts"]["critical"]:
        st.success(current_data["alerts"]["critical"])
    else:
        st.error(current_data["alerts"]["critical"])
        
    st.warning(current_data["alerts"]["warning"])

# ==========================================
# الشاشة الثالثة: تحليلات بنود الموازنة
# ==========================================
elif page == "📊 تحليلات بنود الموازنة":
    st.markdown("<h1 style='color:#38bdf8;'>📊 التفاصيل التحليلية المتقدمة لبنود الموازنة</h1>", unsafe_allow_html=True)
    st.markdown(f"المطابقة الرقمية المفصلة لجداول المديونيات وحجم الوفر والعجز لـ **{selected_club}** .")
    st.markdown("---")
    
    df_table = pd.DataFrame.from_dict(current_data["budget_data"], orient='index').reset_index()
    df_table.columns = ['البند المالي المستهدف', 'الربط المالي المعتمد ( ج.م )', 'الصرف الفعلي اللحظي ( ج.م )', 'الوفر / العجز الحالي ( ج.م )', 'نسبة الاستهلاك %']
    
    st.subheader("📋 جدول المطابقة المالية والمديونيات التفصيلي")
    st.dataframe(df_table.style.format({
        'الربط المالي المعتمد ( ج.م )': '{:,.0f}',
        'الصرف الفعلي اللحظي ( ج.م )': '{:,.0f}',
        'الوفر / العجز الحالي ( ج.م )': '{:,.0f}',
        'نسبة الاستهلاك %': '{:.1f}%'
    }), use_container_width=True)
    
    st.markdown("---")
    st.subheader("🔮 النمذجة التنبؤية لحجم العجز والتدفقات النقدية القادمة")
    
    months = ['يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
    
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=months, y=current_data["forecast"], mode='lines+markers', name='السيولة المتوقعة', line=dict(color='#10b981', width=3)))
    fig_line.update_layout(template='plotly_dark', font_family="Cairo", title_text="محاكاة المنحنى التنبئي لحركة النقدية وسداد المديونيات للربع القادم")
    st.plotly_chart(fig_line, use_container_width=True)

# ==========================================
# الشاشة الرابعة: سجل التتبع والحوكمة
# ==========================================
elif page == "🛡️ سجل التتبع والحوكمة ( Audit )":
    st.markdown("<h1 style='color:#10b981;'>🛡️ سجل تتبع نزاهة البيانات والامتثال الرقمي</h1>", unsafe_allow_html=True)
    st.markdown(f"توثيق رادع وغير قابل للتعديل ( Audit Trail ) لكافة القرارات الإدارية والمالية بنادي **{selected_club}** .")
    st.markdown("---")
    
    audit_log = pd.DataFrame({
        'التوقيت والزمن اللحظي': ['2026-06-10 14:22:15', '2026-06-10 11:05:02', '2026-06-09 09:15:40', '2026-06-08 13:01:12'],
        'المستخدم / الكادر البشري': ['المراقب المالي المعتمد', 'نظام EWS ( خوارزمية تلقائية )', current_data["audit_user"], 'مفتش وزارة الشباب والرياضة'],
        'الإجراء المتخذ تفصيلاً': ['اعتماد مسار فحص مديونية التوريدات الإنشائية وعقود المقاولات', 'حجب معاملة قيد ارتباط مالي إضافي لصفقة لاعب لعدم وجود ربط موازنة', 'تغذية النظام بتقرير الفحص الميداني الخاص بالانحرافات الإدارية المستندية', 'ولوج كامل للرقابة الرقمية المباشرة ومطابقة الحسابات الختامية المقترحة بالمديرية'],
        'حالة الامتثال للائحة الموحدة': ['✅ متوافق وممتثل تشريعياً', '❌ تم الحجب والمنع الآلي للتجاوز المالي', '⚠️ مراجعة مستندية معلقة بقسم المراجعة', '✅ فحص وتفتيش نظامي سليم']
    })
    
    st.table(audit_log)
