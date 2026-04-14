import io
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sklearn.cluster import KMeans

st.set_page_config(page_title="AI Data Suite", page_icon="🧠", layout="wide")

st.sidebar.title("🛠️ Platforma Menyusi")
app_mode = st.sidebar.radio(
    "AI vositasini tanlang:",
    ["1. 🔍 K-Means (Klasterlash)", "2. 📈 Regressiya (Bashorat)"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("📥 Ma'lumot kiritish")
uploaded_file = st.sidebar.file_uploader("CSV yoki Excel yuklang", type=['csv', 'xlsx'])
manual_entry = st.sidebar.toggle("✍️ Fayl yo'qmi? Qo'lda kiritish")

if app_mode == "1. 🔍 K-Means (Klasterlash)":
    st.title("🔍 K-Means: Avtomatik Guruhlash")
    st.sidebar.markdown("---")
    k_clusters = st.sidebar.number_input("K = (Guruhlar sonini kiriting, Max: 5)", min_value=2, max_value=5, value=3, step=1)
    
    data_ready = False
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            if len(df.columns) >= 2:
                df = df.iloc[:, :2]
                x_name, y_name = df.columns[0], df.columns[1]
                data_ready = True
            else:
                st.error("Faylda kamida 2 ta ustun bo'lishi kerak!")
        except Exception:
            st.error("Faylni o'qishda xatolik.")
    elif manual_entry:
        x_name, y_name = "Mijoz yoshi", "Xarid summasi ($)"
        df = pd.DataFrame({x_name: [22, 25, 24, 45, 50, 48, 30, 32, 29, 60], y_name: [15, 20, 18, 80, 95, 85, 45, 50, 48, 120]})
        data_ready = True

    if data_ready:
        col1, col2 = st.columns([1.3, 3.7])
        with col1:
            st.subheader("✍️ Ma'lumotlar")
            edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, hide_index=True, height=400)
        
        clean_df = edited_df.dropna()
        
        with col2:
            if len(clean_df) < k_clusters:
                st.warning(f"Hisoblash uchun kamida {k_clusters} ta qator kerak.")
            else:
                x_vals = clean_df.iloc[:, 0].values
                y_vals = clean_df.iloc[:, 1].values
                
                kmeans = KMeans(n_clusters=k_clusters, random_state=42, n_init=10)
                clusters = kmeans.fit_predict(list(zip(x_vals, y_vals)))
                centroids = kmeans.cluster_centers_
                
                clean_df['Klaster'] = clusters + 1
                
                st.subheader("📊 Klasterlash Natijasi")
                fig, ax = plt.subplots(figsize=(10, 4.5))
                scatter = ax.scatter(x_vals, y_vals, c=clusters, cmap='viridis', s=100, alpha=0.8, edgecolors='w')
                ax.scatter(centroids[:, 0], centroids[:, 1], c='red', s=250, marker='X', label='Markazlar')
                ax.set_xlabel(x_name, fontsize=10)
                ax.set_ylabel(y_name, fontsize=10)
                ax.legend()
                ax.grid(True, linestyle='--', alpha=0.5)
                st.pyplot(fig)
                
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    clean_df.to_excel(writer, index=False, sheet_name="Klaster_Natijalari")
                st.download_button("📥 Natijani Excelga yuklash", data=buffer.getvalue(), file_name="KMeans_Natija.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.info("👈 Ishlashni boshlash uchun chap paneldan fayl yuklang yoki 'Qo'lda kiritish'ni yoqing.")

elif app_mode == "2. 📈 Regressiya (Bashorat)":
    st.title("📈 Regressiya: Kelajakni Bashorat qilish")
    st.sidebar.markdown("---")
    future_steps = st.sidebar.slider("Kelajakni necha qadam oldinga bashorat qilamiz?", 1, 30, 5)
    
    data_ready = False
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            if len(df.columns) >= 2:
                df = df.iloc[:, :2]
                x_name, y_name = df.columns[0], df.columns[1]
                data_ready = True
            else:
                st.error("Faylda kamida 2 ta ustun bo'lishi kerak!")
        except Exception:
            st.error("Faylni o'qishda xatolik.")
    elif manual_entry:
        x_name, y_name = "X (Qadam / Yil)", "Y (Qiymat)"
        df = pd.DataFrame({x_name: [1, 2, 3, 4, 5], y_name: [12.1, 15.3, 19.2, 24.5, 29.8]})
        data_ready = True

    if data_ready:
        col1, col2 = st.columns([1.3, 3.7])
        with col1:
            st.subheader("✍️ Ma'lumotlar")
            edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, hide_index=True, height=400)
        
        clean_df = edited_df.dropna()
        
        with col2:
            if len(clean_df) < 2:
                st.warning("Hisob-kitob qilish uchun kamida 2 ta qator kerak.")
            else:
                x = clean_df.iloc[:, 0].to_numpy(dtype=float)
                y = clean_df.iloc[:, 1].to_numpy(dtype=float)
                a, b = np.polyfit(x, y, 1)
                
                st.subheader("📈 Natija va Grafik")
                st.success(f"Regressiya tenglamasi: y = {a:.4f}x {'+' if b>0 else '-'} {abs(b):.4f}")
                
                fig, ax = plt.subplots(figsize=(10, 4.5))
                ax.scatter(x, y, color='#1f77b4', s=60, alpha=0.8, label="Faktlar")
                x_line = np.linspace(np.min(x), np.max(x), 100)
                ax.plot(x_line, a * x_line + b, color='#d62728', linewidth=2.5, label="Regressiya")
                future_x = np.linspace(np.max(x), np.max(x) + future_steps, 20)
                future_y = a * future_x + b
                ax.plot(future_x, future_y, color='#2ca02c', linestyle='dashed', linewidth=2.5, label="Bashorat")
                ax.scatter(future_x[-1], future_y[-1], color='#ff7f0e', s=120, zorder=5, label="Yakuniy nuqta")
                
                if np.min(x) > 1000 and np.max(x) < 3000:
                    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda val, pos: f"{int(val)}"))
                
                ax.set_xlabel(x_name, fontsize=10)
                ax.set_ylabel(y_name, fontsize=10)
                ax.legend(loc='lower right', fontsize=10)
                ax.grid(True, linestyle='--', alpha=0.5)
                st.pyplot(fig)
                
                future_report = pd.DataFrame({'Holat': ['Bashorat'] * len(future_x), x_name: np.round(future_x, 2), y_name: np.round(future_y, 2)})
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    clean_df.to_excel(writer, index=False, sheet_name="Faktlar")
                    future_report.to_excel(writer, index=False, sheet_name="Bashoratlar")
                st.download_button("📥 Hisobotni yuklash (.xlsx)", data=buffer.getvalue(), file_name="Bashorat_Natija.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.info("👈 Ishlashni boshlash uchun chap paneldan fayl yuklang yoki 'Qo'lda kiritish'ni yoqing.")