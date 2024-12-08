import tkinter as tk
from Login import create_login_frame
from Book import load_books_from_csv


def show_frame(parent, frame):
    """Menampilkan frame tertentu."""
    # Menyembunyikan semua widget yang ada pada parent
    for widget in parent.winfo_children():
        widget.pack_forget()
    # Menampilkan frame yang baru
    frame.pack(expand=True, fill="both")


def main():
    global csv_file
    # Menentukan path ke file CSV
    csv_file = r"C:\Users\Rafi\Documents\Tubes prokom\Aplikasi-Peminjaman-Buku\data_buku.csv"
    load_books_from_csv(csv_file)  # Memuat data buku

    # Membuat window utama
    root = tk.Tk()
    root.title("Aplikasi Perpustakaan Pintar")
    root.geometry("1650x1080")
    root.configure(bg="#E0E0E0")

    # Inisialisasi frame pertama (login)
    login_frame = create_login_frame(root)

    # Menampilkan frame login
    show_frame(root, login_frame)

    # Menjalankan aplikasi
    root.mainloop()


if __name__ == "__main__":
    main()
