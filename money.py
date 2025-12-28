import customtkinter as ctk
import requests
import pyperclip
from datetime import datetime

class SalliConverterFinal(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Settings
        self.title("Salli Converter Pro - Ultimate")
        self.geometry("500x800")
        self.resizable(False, False)
        
        # Default Theme Settings
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        # --- Main UI Container ---
        self.container = ctk.CTkFrame(self, corner_radius=30, border_width=2, border_color="#2ECC71")
        self.container.pack(pady=20, padx=20, fill="both", expand=True)

        # Theme Switch (Light/Dark)
        self.theme_switch = ctk.CTkSwitch(self.container, text="Dark Mode", command=self.change_theme)
        self.theme_switch.pack(pady=(15, 0), padx=20, anchor="ne")

        # Header Section
        self.title_label = ctk.CTkLabel(self.container, text="Money Converter", 
                                        font=("Segoe UI", 36, "bold"), text_color="#27AE60")
        self.title_label.pack(pady=(20, 5))
        
        self.status_label = ctk.CTkLabel(self.container, text="Ready to Convert", 
                                         font=("Arial", 12), text_color="gray")
        self.status_label.pack()

        # Input Field
        self.amount_entry = ctk.CTkEntry(self.container, placeholder_text="Enter the amount", 
                                         width=360, height=65, font=("Arial", 22),
                                         border_width=2, corner_radius=15, justify="center")
        self.amount_entry.pack(pady=35)
        self.amount_entry.focus()

        # Currency Selection
        self.sel_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.sel_frame.pack(pady=5)

        currencies = ["USD", "LKR", "EUR", "GBP", "INR", "AUD", "CAD", "JPY", "SGD", "AED"]

        self.from_cb = ctk.CTkComboBox(self.sel_frame, values=currencies, width=135, height=45)
        self.from_cb.set("USD")
        self.from_cb.grid(row=0, column=0, padx=10)

        self.swap_btn = ctk.CTkButton(self.sel_frame, text="⇄", width=50, height=45, font=("Arial", 24),
                                      fg_color="#2ECC71", hover_color="#27AE60", command=self.swap)
        self.swap_btn.grid(row=0, column=1)

        self.to_cb = ctk.CTkComboBox(self.sel_frame, values=currencies, width=135, height=45)
        self.to_cb.set("LKR")
        self.to_cb.grid(row=0, column=2, padx=10)

        # Live Rate Mini Display
        self.rate_info = ctk.CTkLabel(self.container, text="", font=("Arial", 12), text_color="#7F8C8D")
        self.rate_info.pack(pady=5)

        # Convert Button
        self.conv_btn = ctk.CTkButton(self.container, text="Convert Now", 
                                      command=self.convert, width=240, height=60,
                                      font=("Arial", 20, "bold"), corner_radius=18)
        self.conv_btn.pack(pady=30)

        # Result Area
        self.res_box = ctk.CTkFrame(self.container, corner_radius=25, height=150, width=400)
        self.res_box.pack_propagate(False)
        self.res_box.pack(pady=10)

        self.res_val = ctk.CTkLabel(self.res_box, text="Result: ---", 
                                    font=("Segoe UI", 38, "bold"), text_color="#27AE60")
        self.res_val.pack(expand=True)

        # Copy Link
        self.copy_btn = ctk.CTkButton(self.container, text="📋 Copy to Clipboard", font=("Arial", 13), 
                                      fg_color="transparent", text_color="#27AE60", hover=False,
                                      command=self.copy)
        self.copy_btn.pack(pady=15)

        # Key Bindings
        self.bind('<Return>', lambda e: self.convert())

    def change_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def swap(self):
        f, t = self.from_cb.get(), self.to_cb.get()
        self.from_cb.set(t)
        self.to_cb.set(f)

    def convert(self):
        try:
            amt = float(self.amount_entry.get())
            f, t = self.from_cb.get(), self.to_cb.get()
            self.res_val.configure(text="...", text_color="#f1c40f")
            self.update()

            data = requests.get(f"https://api.exchangerate-api.com/v4/latest/{f}").json()
            rate = data["rates"][t]
            res = amt * rate
            
            self.res_val.configure(text=f"{t} {res:,.2f}", text_color="#27AE60")
            self.rate_info.configure(text=f"Live Rate: 1 {f} = {rate:,.2f} {t}")
            self.status_label.configure(text=f"Last updated: {datetime.now().strftime('%I:%M %p')}")
            
        except:
            self.res_val.configure(text="Check Input!", text_color="#e74c3c")

    def copy(self):
        txt = self.res_val.cget("text")
        if "Result" not in txt and "Check" not in txt:
            pyperclip.copy(txt)
            self.copy_btn.configure(text="✅ Copied!")
            self.after(2000, lambda: self.copy_btn.configure(text="📋 Copy to Clipboard"))

if __name__ == "__main__":
    app = SalliConverterFinal()
    app.mainloop()