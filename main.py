import customtkinter as ctk
from tkinter import messagebox
import sys
from natija import FinalApp

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tizimga kirish")
        self.geometry("400x300")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("dark")
        
        self.label = ctk.CTkLabel(self, text="TATU Smart System", font=("Arial", 20, "bold"))
        self.label.pack(pady=30)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Parolni kiriting", show="*", width=200)
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self, text="KIRISH", command=self.check_password)
        self.login_button.pack(pady=20)

    def check_password(self):
        if self.password_entry.get() == "1111":
            self.destroy()
            self.open_main_app()
        else:
            messagebox.showerror("Xato", "Parol noto'g'ri!")

    def open_main_app(self):
        main_app = FinalApp()
        main_app.mainloop()

if __name__ == "__main__":
   
    if getattr(sys, 'frozen', False):
       
        login = LoginWindow()
        login.mainloop()
    else:
   
        app = FinalApp()
        app.mainloop()