import tkinter as tk
from tkinter import ttk, messagebox
import re

class PerpustakaanPintar:
    def _init_(self, root):
        self.root = root
        self.root.title("Perpustakaan Pintar")
        self.root.geometry("400x600")
        self.root.configure(bg="#FFF7E6")
        
        # Create container for frames
        self.container = tk.Frame(root, bg="#FFF7E6")
        self.container.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Dictionary to store frames
        self.frames = {}
        
        # Create register and login frames
        for F in (RegisterFrame, LoginFrame):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.pack(fill="both", expand=True)
            
        # Show register frame initially
        self.show_frame(RegisterFrame)
        
    def show_frame(self, frame_class):
        # Hide all frames
        for frame in self.frames.values():
            frame.pack_forget()
        # Show selected frame
        frame = self.frames[frame_class]
        frame.pack(fill="both", expand=True)

class RegisterFrame(tk.Frame):
    def _init_(self, parent, controller):
        tk.Frame._init_(self, parent, bg="#FFF7E6")
        self.controller = controller
        
        # Title
        title_label = tk.Label(
            self,
            text="PERPUSTAKAAN\nPINTAR",
            font=("Arial Bold", 24),
            fg="#D35400",
            bg="#FFF7E6",
            justify="center"
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(
            self,
            text="DAFTAR AKUN BARU",
            font=("Arial Bold", 16),
            fg="#2E86C1",
            bg="#FFF7E6"
        )
        subtitle_label.pack(pady=10)
        
        # Form Frame
        form_frame = tk.Frame(self, bg="#FFF7E6")
        form_frame.pack(pady=20)
        
        # Full Name
        tk.Label(
            form_frame,
            text="NAMA LENGKAP",
            font=("Arial", 12),
            fg="#E74C3C",
            bg="#FFF7E6"
        ).pack(anchor="w")
        self.name_entry = tk.Entry(form_frame, width=40)
        self.name_entry.pack(pady=(5, 15), ipady=5)
        
        # Email
        tk.Label(
            form_frame,
            text="EMAIL",
            font=("Arial", 12),
            fg="#E74C3C",
            bg="#FFF7E6"
        ).pack(anchor="w")
        self.email_entry = tk.Entry(form_frame, width=40)
        self.email_entry.pack(pady=(5, 15), ipady=5)
        
        # Password
        tk.Label(
            form_frame,
            text="PASSWORD",
            font=("Arial", 12),
            fg="#E74C3C",
            bg="#FFF7E6"
        ).pack(anchor="w")
        self.password_entry = tk.Entry(form_frame, width=40, show="*")
        self.password_entry.pack(pady=(5, 20), ipady=5)
        
        # Register Button
        register_button = tk.Button(
            form_frame,
            text="DAFTAR",
            font=("Arial Bold", 12),
            bg="#2E86C1",
            fg="white",
            width=20,
            command=self.register
        )
        register_button.pack(pady=10)
        
        # Login Link
        login_button = tk.Button(
            form_frame,
            text="SUDAH PUNYA AKUN? MASUK",
            font=("Arial", 10),
            bg="#95A5A6",
            fg="white",
            width=25,
            command=lambda: controller.show_frame(LoginFrame)
        )
        login_button.pack(pady=10)
    
    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def register(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not all([name, email, password]):
            messagebox.showerror("Error", "Semua field harus diisi!")
            return
            
        if not self.validate_email(email):
            messagebox.showerror("Error", "Format email tidak valid!")
            return
            
        if len(password) < 6:
            messagebox.showerror("Error", "Password minimal 6 karakter!")
            return
            
        messagebox.showinfo("Sukses", "Pendaftaran berhasil!")
        self.clear_form()
        
    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

class LoginFrame(tk.Frame):
    def _init_(self, parent, controller):
        tk.Frame._init_(self, parent, bg="#FFF7E6")
        self.controller = controller
        
        # Title
        title_label = tk.Label(
            self,
            text="PERPUSTAKAAN\nPINTAR",
            font=("Arial Bold", 24),
            fg="#D35400",
            bg="#FFF7E6",
            justify="center"
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(
            self,
            text="MASUK",
            font=("Arial Bold", 16),
            fg="#2E86C1",
            bg="#FFF7E6"
        )
        subtitle_label.pack(pady=10)
        
        # Form Frame
        form_frame = tk.Frame(self, bg="#FFF7E6")
        form_frame.pack(pady=20)
        
        # Email
        tk.Label(
            form_frame,
            text="EMAIL",
            font=("Arial", 12),
            fg="#E74C3C",
            bg="#FFF7E6"
        ).pack(anchor="w")
        self.email_entry = tk.Entry(form_frame, width=40)
        self.email_entry.pack(pady=(5, 15), ipady=5)
        
        # Password
        tk.Label(
            form_frame,
            text="PASSWORD",
            font=("Arial", 12),
            fg="#E74C3C",
            bg="#FFF7E6"
        ).pack(anchor="w")
        self.password_entry = tk.Entry(form_frame, width=40, show="*")
        self.password_entry.pack(pady=(5, 20), ipady=5)
        
        # Login Button
        login_button = tk.Button(
            form_frame,
            text="MASUK",
            font=("Arial Bold", 12),
            bg="#2E86C1",
            fg="white",
            width=20,
            command=self.login
        )
        login_button.pack(pady=10)
        
        # Register Link
        register_button = tk.Button(
            form_frame,
            text="BELUM PUNYA AKUN? DAFTAR",
            font=("Arial", 10),
            bg="#95A5A6",
            fg="white",
            width=25,
            command=lambda: controller.show_frame(RegisterFrame)
        )
        register_button.pack(pady=10)
    
    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not all([email, password]):
            messagebox.showerror("Error", "Semua field harus diisi!")
            return
            
        # Untuk demo, gunakan kredensial sederhana
        if email == "admin@perpustakaan.com" and password == "admin123":
            messagebox.showinfo("Sukses", "Login berhasil!")
            self.clear_form()
        else:
            messagebox.showerror("Error", "Email atau password salah!")
    
    def clear_form(self):
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

if _name_ == "_main_":
    root = tk.Tk()
    app = PerpustakaanPintar(root)
    root.mainloop()