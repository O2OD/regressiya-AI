import io
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Bashorat Tizimi", page_icon="📈", layout="wide")

st.sidebar.title("⚙️ Sozlamalar")
input_method = st.sidebar.radio(
    "Kiritish usulini tanlang:",
    ("12-Variant (Mustaqil ish)", "Sun'iy AI ma'lumotlari (Tasodifiy)")
)

st.sidebar.markdown("---")

if input_method == "12-Variant (Mustaqil ish)":
    n = np.arange(1, 11)
    x = np.array([5, 4, 2, 1.1, 3, 4, 5.3, 3.6, 2.6, 4.9])
    y = np.array([5.1, 3.8, 2.1, 1.3, 0.6, 4.0, 4.1, 2.6, 1.3, 3.7])
    future_steps = st.sidebar.slider("Kelajak qadami (X o'qi):", 1, 10, 3)
    y_label = "Y o'qi"
    x_label = "X o'qi"

else:
    dataset_type = st.sidebar.selectbox(
        "Bashorat sohasini tanlang:",
        [
            "Samarqand markazida uy narxlari ($)",
            "Kiberhujumlar zarari (Mln $)",
            "Elektromobillar savdosi hajmi (dona)",
            "Xalqaro aviachiptalar narxi ($)",
            "IT Dasturchilar maoshi ($)"
        ]
    )

    if st.sidebar.button("🔄 Yangi ma'lumot yaratish"):
        st.session_state.random_seed = np.random.randint(0, 100000)
    if 'random_seed' not in st.session_state:
        st.session_state.random_seed = 42
    np.random.seed(st.session_state.random_seed)
    
    points_count = st.sidebar.slider("Ma'lumotlar hajmi (Yillar):", 5, 30, 15)
    n = np.arange(1, points_count + 1)
    x = np.arange(2025 - points_count, 2025)
    
    if dataset_type == "Samarqand markazida uy narxlari ($)":
        y = np.round(35000 + (x - x[0]) * 2000 + np.random.normal(0, 3000, points_count), 0)
    elif dataset_type == "Kiberhujumlar zarari (Mln $)":
        y = np.round(10 + (x - x[0]) * 8 + np.random.normal(0, 4, points_count), 1)
    elif dataset_type == "Elektromobillar savdosi hajmi (dona)":
        y = np.round(200 + (x - x[0]) * 1500 + np.random.normal(0, 500, points_count), 0)
    elif dataset_type == "Xalqaro aviachiptalar narxi ($)":
        y = np.round(200 + (x - x[0]) * 15 + np.random.normal(0, 25, points_count), 0)
    else:
        y = np.round(300 + (x - x[0]) * 180 + np.random.normal(0, 50, points_count), 0)

    future_steps = st.sidebar.slider("Kelajak bashorati (Yil):", 2, 15, 5)
    y_label = dataset_type
    x_label = "Yillar"

df = pd.DataFrame({'n': n, 'x': x, 'y': y})
a, b = np.polyfit(x, y, 1)

st.title("📊 Regressiya va Bashorat Tizimi")
st.success(f"**Regressiya tenglamasi:** y = {a:.4f}x {'+' if b>0 else '-'} {abs(b):.4f}")

col1, col2 = st.columns([1.2, 3.8])

with col1:
    st.subheader("📋 Ma'lumotlar")
    st.dataframe(df, use_container_width=True, hide_index=True, height=380)

with col2:
    st.subheader("📈 Grafik")
    fig, ax = plt.subplots(figsize=(10, 4.5))
    
    ax.scatter(x, y, color='#1f77b4', s=60, alpha=0.8, label="Haqiqiy nuqtalar")
    
    x_line = np.linspace(np.min(x), np.max(x), 100)
    ax.plot(x_line, a * x_line + b, color='#d62728', linewidth=2.5, label="Regressiya chizig'i")
    
    future_x = np.linspace(np.max(x), np.max(x) + future_steps, 20)
    future_y = a * future_x + b
    
    ax.plot(future_x, future_y, color='#2ca02c', linestyle='dashed', linewidth=2.5, label="Bashorat (Kelajak)")
    ax.scatter(future_x[-1], future_y[-1], color='#ff7f0e', s=120, zorder=5, label="Yakuniy nuqta")
    
    ax.set_xlabel(x_label, fontsize=10)
    ax.set_ylabel(y_label, fontsize=10)
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    
    st.pyplot(fig)

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='Natijalar')

st.download_button(
    label="📥 Excelga yuklash (.xlsx)",
    data=buffer.getvalue(),
    file_name="bashorat.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)