import tkinter as tk
from tkinter import messagebox
import pandas as pd
from user_manager import read_users, write_user
from PIL import Image, ImageTk  # Mengimpor PIL untuk memuat gambar


# Fungsi untuk membuat form entry
def create_form_entry(parent, label_text, is_password=False):
    """Membuat label dan input field."""
    tk.Label(parent, text=label_text, font=("Arial", 12), bg="#87CEEB").pack(anchor="w", pady=(10, 5))
    entry = tk.Entry(parent, font=("Arial", 12), show="*" if is_password else "")
    entry.pack(pady=(0, 10))
    return entry


# Fungsi untuk pendaftaran
def register(name_entry, username_entry, password_entry, parent,frame, controller):
    from Main import show_frame
    """Logika untuk pendaftaran pengguna baru."""
    name = name_entry.get().strip()
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not all([name, username, password]):
        messagebox.showerror("Error", "Semua field harus diisi!")
        return

    users = read_users()
    if username in users['username'].values:
        messagebox.showerror("Error", "Username sudah terdaftar!")
        return

    write_user(username, password, name)
    messagebox.showinfo("Sukses", "Pendaftaran berhasil!")
    show_frame(parent,create_login_frame(parent, controller,frame))


# Fungsi untuk login
def login(username_entry, password_entry, parent,frame):
    from Main import show_frame
    from Book import create_home_menu  # Pastikan `create_home_menu` sudah didefinisikan dengan benar
    """Logika untuk login pengguna."""
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    users = read_users()

    if username in users['username'].values:
        stored_password = users.loc[users['username'] == username, 'password'].values[0]
        if password == stored_password:
            messagebox.showinfo("Sukses", f"Selamat datang, {username}!")
            show_frame(parent,create_home_menu(parent))  # Pastikan create_home_menu menerima parameter yang benar
        else:
            messagebox.showerror("Error", "Password salah!")
    else:
        messagebox.showerror("Error", "Username tidak ditemukan!")


# Fungsi untuk membuat frame registrasi
def create_register_frame(parent,frame):
    from Main import show_frame
    """Frame registrasi."""
    frame = tk.Frame(parent, bg="#FFF7E6")
    tk.Label(frame, text="PERPUSTAKAAN PINTAR", font=("Arial Bold", 32), fg="#D35400", bg="#FFF7E6").place(pady=15, padx=10)
    tk.Label(frame, text="DAFTAR AKUN BARU", font=("Arial Bold", 24), fg="#2E86C1", bg="#FFF7E6").pack(pady=10)

    form_frame = tk.Frame(frame, bg="#FFF7E6")
    form_frame.pack(pady=20)

    name_entry = create_form_entry(form_frame, "NAMA LENGKAP")
    username_entry = create_form_entry(form_frame, "USERNAME")
    password_entry = create_form_entry(form_frame, "PASSWORD", is_password=True)

    button_frame = tk.Frame(form_frame, bg="#FFF7E6")
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="DAFTAR", font=("Arial Bold", 14), bg="#2E86C1", fg="white", width=20, height=1,
              command=lambda: register(name_entry, username_entry, password_entry, parent)).pack(pady=(0, 10))
    tk.Button(button_frame, text="SUDAH PUNYA AKUN? MASUK", font=("Arial", 12), bg="#95A5A6", fg="white", width=28, height=2,
              command=lambda: show_frame(create_login_frame(parent,frame))).pack()

    return frame


def create_login_frame(parent):
    from Main import show_frame
    """Frame login dan registrasi dengan background gambar."""
    frame = tk.Frame(parent, bg="#87CEEB")
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Menambahkan canvas untuk latar belakang gambar
    canvas = tk.Canvas(frame, width=frame.winfo_width(), height=frame.winfo_height())
    canvas.pack(fill="both", expand=True)

    # Memuat gambar latar belakang
    bg_image = Image.open("E:\\Aplikasi Peminjaman Buku\\Aplikasi Peminjaman Buku\\Sign Up.png")  # Ganti dengan path gambar Anda
    bg_image = bg_image.resize((frame.winfo_width(), frame.winfo_height()), Image.ANTIALIAS)  # Resize sesuai ukuran frame
    bg_image = ImageTk.PhotoImage(bg_image)

    # Menambahkan gambar latar belakang ke canvas
    canvas.create_image(0, 0, image=bg_image, anchor="nw")
    
    # Label judul dan login form
    tk.Label(frame, text="PERPUSTAKAAN PINTAR", font=("Arial Bold", 32), fg="#D35400", bg="#87CEEB").pack(pady=10)
    tk.Label(frame, text="MASUK", font=("Arial Bold", 24), fg="#2E86C1", bg="#87CEEB").pack(pady=10)

    form_frame = tk.Frame(frame, bg="#87CEEB")
    form_frame.pack(pady=20)

    username_entry = create_form_entry(form_frame, "USERNAME")
    password_entry = create_form_entry(form_frame, "PASSWORD", is_password=True)

    button_frame = tk.Frame(form_frame, bg="#87CEEB")
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="MASUK", font=("Arial Bold", 14), bg="#2E86C1", fg="white", width=20, height=1,
              command=lambda: login(username_entry, password_entry, parent, frame)).pack(pady=(0, 10))
    tk.Button(button_frame, text="BELUM PUNYA AKUN? DAFTAR", font=("Arial", 12), bg="#95A5A6", fg="white", width=28, height=2,
              command=lambda: show_frame(create_register_frame(parent))).pack()

    return frame

