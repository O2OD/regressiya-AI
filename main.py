import io
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

st.set_page_config(page_title="Universal Bashorat Platformasi", page_icon="📊", layout="wide")

st.sidebar.title("📥 Ma'lumot yuklash")
uploaded_file = st.sidebar.file_uploader("CSV yoki Excel (.xlsx) fayl tanlang", type=['csv', 'xlsx'])

st.sidebar.markdown("---")
manual_entry = st.sidebar.toggle("✍️ Fayl yo'qmi? Qo'lda kiritish")

st.sidebar.markdown("---")
future_steps = st.sidebar.slider("Kelajakni necha qadam oldinga bashorat qilamiz?", 1, 30, 5)

st.title("📊 Universal AI Bashorat Platformasi")

data_ready = False

# 1. Ma'lumot yuklangan yoki qo'lda kiritish yoqilganini tekshiramiz
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        if len(df.columns) >= 2:
            x_name = df.columns[0]
            y_name = df.columns[1]
            df = df.iloc[:, :2] 
            data_ready = True
        else:
            st.error("Faylda kamida 2 ta ustun bo'lishi kerak!")
    except Exception:
        st.error("Faylni o'qishda xatolik yuz berdi.")

elif manual_entry:
    x_name = "Yil (Qadam)"
    y_name = "Natija (Qiymat)"
    df = pd.DataFrame({
        x_name: [2021, 2022, 2023], 
        y_name: [12.5, 18.2, 24.8]
    })
    data_ready = True

# 2. Agar ma'lumot bo'lsa (Fayl yoki Qo'lda kiritish), tizimni ishga tushiramiz
if data_ready:
    col1, col2 = st.columns([1.3, 3.7])

    with col1:
        st.subheader("✍️ Ma'lumotlar jadvali")
        st.info("Katakni bosib qiymatlarni o'zgartiring.")
        
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            height=400
        )

    clean_df = edited_df.dropna()

    with col2:
        if len(clean_df) < 2:
            st.warning("Hisob-kitob qilish uchun jadvalda kamida 2 ta to'liq qator bo'lishi kerak.")
        else:
            x = clean_df.iloc[:, 0].to_numpy(dtype=float)
            y = clean_df.iloc[:, 1].to_numpy(dtype=float)

            a, b = np.polyfit(x, y, 1)

            st.subheader("📈 Natija va Grafik")
            st.success(f"**Regressiya tenglamasi:** y = {a:.4f}x {'+' if b>0 else '-'} {abs(b):.4f}")

            fig, ax = plt.subplots(figsize=(10, 4.5))
            ax.scatter(x, y, color='#1f77b4', s=60, alpha=0.8, label="Kiritilgan faktlar")

            x_line = np.linspace(np.min(x), np.max(x), 100)
            ax.plot(x_line, a * x_line + b, color='#d62728', linewidth=2.5, label="Regressiya chizig'i")

            future_x = np.linspace(np.max(x), np.max(x) + future_steps, 20)
            future_y = a * future_x + b

            ax.plot(future_x, future_y, color='#2ca02c', linestyle='dashed', linewidth=2.5, label="AI Bashorati")
            ax.scatter(future_x[-1], future_y[-1], color='#ff7f0e', s=120, zorder=5, label="Yakuniy nuqta")

            if np.min(x) > 1000 and np.max(x) < 3000:
                 ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda val, pos: f"{int(val)}"))

            ax.set_xlabel(x_name, fontsize=10)
            ax.set_ylabel(y_name, fontsize=10)
            ax.legend(loc='lower right', fontsize=10)
            ax.grid(True, linestyle='--', alpha=0.5)

            st.pyplot(fig)

            future_report = pd.DataFrame({
                'Holat': ['AI Bashorati (Kelajak)'] * len(future_x),
                x_name: np.round(future_x, 2),
                y_name: np.round(future_y, 2)
            })

            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                clean_df.to_excel(writer, index=False, sheet_name="Faktlar")
                future_report.to_excel(writer, index=False, sheet_name="Bashoratlar")

            st.download_button(
                label="📥 To'liq hisobotni Excelga yuklash (.xlsx)",
                data=buffer.getvalue(),
                file_name="Universal_Bashorat_Hisoboti.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# 3. Agar ma'lumot kiritilmagan bo'lsa, "Kutish ekrani" (Landing Page) ko'rsatamiz
else:
    st.markdown("### 👋 Tizimga xush kelibsiz!")
    st.write("Bu sun'iy intellektga asoslangan biznes tahlil platformasi. U o'tmishdagi ma'lumotlarni tahlil qilib, **Regressiya algoritmi** orqali kelajakdagi aniq natijalarni bashorat qilib beradi.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("#### 📁 1-Usul: Fayl yuklash\nChap tomondagi menyudan o'zingizning tayyor **Excel** yoki **CSV** faylingizni yuklang. Dastur uni o'qib avtomatik tahlilni boshlaydi.")
    with col_b:
        st.success("#### ✍️ 2-Usul: Qo'lda kiritish\nAgar tayyor faylingiz bo'lmasa, chap menyudagi **'Qo'lda kiritish'** tugmasini yoqing va qiymatlarni to'g'ridan-to'g'ri saytga yozing.")
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.warning("👈 Iltimos, ishlashni boshlash uchun chap paneldan yuqoridagi usullardan birini tanlang!")