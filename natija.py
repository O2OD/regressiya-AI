import customtkinter as ctk
from tkinter import filedialog, messagebox
import data
import subprocess
import threading
import sys

class FinalApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.original_df = None
        self.filtered_df = None
        self.current_fac = "Barcha"
        self.current_cat = "Barcha talabalar"
        
        self.fac_buttons = {}
        self.cat_buttons = {}
        
        self.title("TATU Smart Analytics System")
        self.geometry("1400x850")
        ctk.set_appearance_mode("dark")

        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="AMALLAR", font=("Arial", 18, "bold")).pack(pady=(20,10))
        ctk.CTkButton(self.sidebar, text="📥 IMPORT DATA", fg_color="#10B981", height=45, command=self.import_file).pack(pady=5, padx=20)
        ctk.CTkButton(self.sidebar, text="📤 EXPORT RESULTS", fg_color="#D97706", height=45, command=self.export_file).pack(pady=5, padx=20)
        
      
        self.exe_btn = ctk.CTkButton(self.sidebar, text="🛠 EXE FAYL YARATISH", fg_color="#7C3AED", height=45, command=self.start_exe_thread)
        self.exe_btn.pack(pady=5, padx=20)


        if getattr(sys, 'frozen', False):
            self.exe_btn.pack_forget()

        ctk.CTkLabel(self.sidebar, text="ID BILAN QIDIRUV", font=("Arial", 14, "bold")).pack(pady=(30,5))
        self.id_search_entry = ctk.CTkEntry(self.sidebar, placeholder_text="ID kiriting...", height=35)
        self.id_search_entry.pack(pady=5, padx=20)
        ctk.CTkButton(self.sidebar, text="🆔 ID BO'YICHA IZLASH", fg_color="#3B82F6", command=self.run_search_id).pack(pady=2, padx=20)

        ctk.CTkLabel(self.sidebar, text="ISM BILAN QIDIRUV", font=("Arial", 14, "bold")).pack(pady=(20,5))
        self.name_search_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Ism kiriting...", height=35)
        self.name_search_entry.pack(pady=5, padx=20)
        ctk.CTkButton(self.sidebar, text="👤 ISM BO'YICHA IZLASH", fg_color="#6366F1", command=self.run_search_name).pack(pady=2, padx=20)

        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        self.fac_frame = ctk.CTkFrame(self.main_area)
        self.fac_frame.pack(fill="x", pady=(0,10))
        
        facs = ["Barcha", "KI", "DI", "AX", "TT"]
        for f in facs:
            btn = ctk.CTkButton(self.fac_frame, text=f, width=110, height=35, command=lambda x=f: self.filter_fac(x))
            btn.pack(side="left", padx=5, pady=5)
            self.fac_buttons[f] = btn

        self.filter_frame = ctk.CTkFrame(self.main_area)
        self.filter_frame.pack(fill="x", pady=(0,10))
        
        cats = ["Barcha talabalar", "Yiqilayotganlar", "3 ga o'qiydiganlar", "4-5 ga o'qiydiganlar"]
        for c in cats:
            btn = ctk.CTkButton(self.filter_frame, text=c, fg_color="#4B5563", height=35, command=lambda x=c: self.filter_cat(x))
            btn.pack(side="left", padx=5, pady=5)
            self.cat_buttons[c] = btn

        self.table_box = ctk.CTkTextbox(self.main_area, font=("Consolas", 13), wrap="none")
        self.table_box.pack(fill="both", expand=True)
        
        self.update_button_colors()

    def update_button_colors(self):
        for name, btn in self.fac_buttons.items():
            if name == self.current_fac:
                btn.configure(fg_color="#2563EB", border_width=2, border_color="white")
            else:
                btn.configure(fg_color="#3B82F6", border_width=0)
        for name, btn in self.cat_buttons.items():
            if name == self.current_cat:
                btn.configure(fg_color="#1D4ED8", border_width=2, border_color="white")
            else:
                btn.configure(fg_color="#4B5563", border_width=0)

    def start_exe_thread(self):
        self.exe_btn.configure(state="disabled", text="YIG'ILMOQDA...")
        threading.Thread(target=self.make_exe, daemon=True).start()

    def make_exe(self):
        try:
            cmd = ["pyinstaller", "--noconsole", "--onefile", "--collect-all", "customtkinter", "--name", "TATU_Database_System", "main.py"]
            subprocess.run(cmd, check=True)
            messagebox.showinfo("Tayyor", "EXE yaratildi! 'dist' papkasidan olishingiz mumkin.")
        except Exception as e:
            messagebox.showerror("Xato", f"Xato yuz berdi: {e}")
        finally:
            self.exe_btn.configure(state="normal", text="🛠 EXE FAYL YARATISH")

    def import_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.original_df = data.process_data(path)
            self.filtered_df = self.original_df.copy()
            self.show_data(self.filtered_df)

    def filter_fac(self, fac):
        if self.original_df is not None:
            self.current_fac = fac
            self.update_button_colors()
            self.filtered_df = data.apply_filters(self.original_df, faculty=fac, category=self.current_cat)
            self.show_data(self.filtered_df)

    def filter_cat(self, cat):
        if self.original_df is not None:
            self.current_cat = cat
            self.update_button_colors()
            self.filtered_df = data.apply_filters(self.original_df, faculty=self.current_fac, category=cat)
            self.show_data(self.filtered_df)

    def run_search_id(self):
        if self.original_df is not None:
            self.filtered_df = data.search_by_id(self.original_df, self.id_search_entry.get())
            self.show_data(self.filtered_df)

    def run_search_name(self):
        if self.original_df is not None:
            self.filtered_df = data.search_by_name(self.original_df, self.name_search_entry.get())
            self.show_data(self.filtered_df)

    def show_data(self, dframe):
        self.table_box.delete("1.0", "end")
        if dframe is not None:
            col_widths = {'ID': 15, 'Ism': 35, 'Viloyat': 25, 'Kurs': 10, 'Guruh': 15, 'GPA': 5}
            header = ""
            for col, width in col_widths.items():
                if col in dframe.columns:
                    header += f"{col:<{width}}"
            self.table_box.insert("end", header + "\n" + "-"*110 + "\n")
            for _, row in dframe.iterrows():
                row_str = ""
                for col, width in col_widths.items():
                    if col in dframe.columns:
                        val = str(row[col])
                        if len(val) > width - 2: val = val[:width-5] + "..."
                        row_str += f"{val:<{width}}"
                self.table_box.insert("end", row_str + "\n")

    def export_file(self):
        if self.filtered_df is not None:
            path = filedialog.asksaveasfilename(defaultextension=".xlsx")
            if path:
                self.filtered_df.to_excel(path, index=False)
                messagebox.showinfo("OK", "Muvaffaqiyatli saqlandi!")