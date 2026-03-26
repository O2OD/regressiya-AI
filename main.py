import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Bashorat Tizimi", page_icon="📈", layout="wide")

st.sidebar.title("⚙️ Sozlamalar")
input_method = st.sidebar.radio(
    "Kiritish usulini tanlang:",
    ("12-Variant (Mustaqil ish)", "Tasodifiy (Random) kiritish")
)

st.sidebar.markdown("---")

if input_method == "12-Variant (Mustaqil ish)":
    n = np.arange(1, 11)
    x = np.array([5, 4, 2, 1.1, 3, 4, 5.3, 3.6, 2.6, 4.9])
    y = np.array([5.1, 3.8, 2.1, 1.3, 0.6, 4.0, 4.1, 2.6, 1.3, 3.7])
    future_steps = st.sidebar.slider("Kelajak qadami (X o'qi):", 1, 10, 3)
else:
    if st.sidebar.button("🔄 Yangi random yaratish"):
        st.session_state.random_seed = np.random.randint(0, 100000)
    if 'random_seed' not in st.session_state:
        st.session_state.random_seed = 42
    np.random.seed(st.session_state.random_seed)
    
    points_count = st.sidebar.slider("Nuqtalar soni (n):", 5, 50, 15)
    n = np.arange(1, points_count + 1)
    x = np.round(np.random.uniform(1, 100, points_count), 1)
    y = np.round(0.85 * x + 10 + np.random.normal(0, 15, points_count), 1)
    future_steps = st.sidebar.slider("Kelajak qadami (X o'qi):", 5, 50, 15)

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
    
    ax.set_xlabel("X o'qi", fontsize=10)
    ax.set_ylabel("Y o'qi", fontsize=10)
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    
    st.pyplot(fig)