import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. إعدادات الصفحة الكلية بأسلوب احترافي مرن
st.set_page_config(
    page_title="نظام الإنذار المبكر الذكي - EWS",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"  # جعل القائمة الجانبية مخفية تلقائياً في الموبايل لتوفير مساحة رؤية
)

# 2. حقن الـ CSS المتقدم والمحسن ليتوافق مع الشاشات الصغيرة (Responsive)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght=400;600;700&display=swap');
    
    html, body, [data-testid="stSidebar"], .stApp, p, div, h1, h2, h3, h4, h5, h6 {
        font-family: 'Cairo', sans-serif !important;
        direction: RTL !important;
        text-align: right !important;
    }
    
    /* تنسيق البطاقات المالية الرقمية لتكون مرنة */
    .metric-card {
        background-color: #1e293b;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 10px;
        width: 100%;
    }
    .metric-title {
        color: #94a3b8;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .metric-value {
        color: #f8fafc;
        font-size: 20px;
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
    
    /* تحسين عرض الجداول في الهواتف */
    .stDataFrame, div[data-testid="stTable"] {
        width: 100% !important;
        overflow-x: auto !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. قاعدة البيانات الشاملة المستمدة من تقرير المديونيات
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
            "warning": "🟡 إنذار استباقي - تراكم مديونيات هيئة الأوقاف والضرائب :\nالنظام يتوقع صدور حكم قضائي بالحجز على الحسابات الجارية للنادي نتيجة عدم إدراج مخصصات مالية كافية لسداد المتأخرات السياسية المتراكمة لعام 2026 ."
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

selected_club = st.sidebar.selectbox("اختر الهيئة الرياضية المستهدفة :", list(clubs_database.keys()))
financial_period = st.sidebar.selectbox("الفترة المالية الحالية :", ["الربع السنوي الحالي ( 2026 )", "الحساب الختامي المتوقع"])

st.sidebar.markdown("---")
page = st.sidebar.radio(
    "اختر الشاشة الرقابية :",
    ["🎛️ لوحة المؤشرات العامة", "🚨 محرك الإنذار المبكر", "📊 تحليلات بنود الموازنة", "🛡️ سجل التتبع والحوكمة ( Audit )"]
)

current_data = clubs_database[selected_club]

# ==========================================
# الشاشة الأولى: لوحة المؤشرات العامة
# ==========================================
if page == "🎛️ لوحة المؤشرات العامة":
    st.markdown(f"<h3 style='color:#f8fafc; font-size:22px;'>🎛️ لوحة المؤشرات المالية العامة</h3>", unsafe_allow_html=True)
    st.markdown(f"تحليل مديونيات ومؤشرات الامتثال لـ **{selected_club}** .")
    st.markdown("---")
    
    # استخدام حاويات مرنة بدلاً من استجابة الأعمدة الصلبة لتناسب الشاشات الصغيرة
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"""<div class="metric-card"><div class="metric-title">إجمالي الموازنة المعتمدة</div><div class="metric-value">{current_data["metrics"]["budget"]}</div></div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="metric-card"><div class="metric-title">إجمالي الصرف الفعلي</div><div class="metric-value" style="color:#ef4444;">{current_data["metrics"]["spent"]}</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card"><div class="metric-title">السيولة النقدية / العجز</div><div class="metric-value" style="color:#10b981;">{current_data["metrics"]["liquidity"]}</div></div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="metric-card"><div class="metric-title">معدل الامتثال والحوكمة</div><div class="metric-value" style="color:#38bdf8;">{current_data["metrics"]["compliance"]}</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 كفاءة بنود الصرف")
    
    df_chart = pd.DataFrame.from_dict(current_data["budget_data"], orient='index').reset_index()
    df_chart.columns = ['البند المالي', 'المخطط', 'الفعلي', 'المتبقي', 'النسبة']
    
    fig = px.bar(
        df_chart, 
        x='البند المالي', 
        y=['المخطط', 'الفعلي'], 
        barmode='group',
        template='plotly_dark',
        color_discrete_sequence=['#38bdf8', '#ef4444'],
        labels={'value': 'المبلغ', 'variable': 'البيان'}
    )
    fig.update_layout(
        font_family="Cairo", 
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# الشاشة الثانية: محرك الإنذار المبكر
# ==========================================
elif page == "🚨 محرك الإنذار المبكر":
    st.markdown("<h3 style='color:#ef4444; font-size:22px;'>🚨 محرك التنبؤ ورصد الانحرافات اللحظي</h3>", unsafe_allow_html=True)
    st.markdown(f"تنبيهات الذكاء الاصطناعي لنادي **{selected_club}** .")
    st.markdown("---")
    
    if "مستقر" in current_data["alerts"]["critical"]:
        st.success(current_data["alerts"]["critical"])
    else:
        st.error(current_data["alerts"]["critical"])
        
    st.warning(current_data["alerts"]["warning"])

# ==========================================
# الشاشة الثالثة: تحليلات بنود الموازنة
# ==========================================
elif page == "📊 تحليلات بنود الموازنة":
    st.markdown("<h3 style='color:#38bdf8; font-size:22px;'>📊 التفاصيل التحليلية لبنود الموازنة</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    df_table = pd.DataFrame.from_dict(current_data["budget_data"], orient='index').reset_index()
    df_table.columns = ['البند المستهدف', 'الربط المعتمد', 'الصرف الفعلي', 'الوفر/العجز', 'الاستهلاك %']
    
    st.subheader("📋 جدول المطابقة المالي")
    st.dataframe(df_table, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🔮 النمذجة التنبؤية لحركة النقدية")
    
    months = ['يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=months, y=current_data["forecast"], mode='lines+markers', line=dict(color='#10b981', width=3)))
    fig_line.update_layout(template='plotly_dark', font_family="Cairo", margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_line, use_container_width=True)

# ==========================================
# الشاشة الرابعة: سجل التتبع والحوكمة
# ==========================================
elif page == "🛡️ سجل التتبع والحوكمة ( Audit )":
    st.markdown("<h3 style='color:#10b981; font-size:22px;'>🛡️ سجل تتبع نزاهة البيانات والامتثال</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    audit_log = pd.DataFrame({
        'التوقيت': ['14:22', '11:05', '09:15', '13:01'],
        'المستخدم': ['المراقب المالي', 'نظام EWS الآلي', current_data["audit_user"], 'مفتش الوزارة'],
        'الإجراء المتخذ تفصيلاً': ['فحص مديونية التوريدات وعقود المقاولات', 'حجب معاملة قيد ارتباط إضافي لصفقة لاعب', 'تغذية تقرير الانحرافات الإدارية المستندية', 'ولوج الرقابة الرقمية ومطابقة الحسابات الختامية'],
        'الامتثال': ['✅ ممتثل', '❌ محجوب', '⚠️ معلق', '✅ سليم']
    })
    st.dataframe(audit_log, use_container_width=True)
