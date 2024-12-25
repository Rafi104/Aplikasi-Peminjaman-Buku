from tkinter import Tk
from Interface import create_login_frame, show_frame
from logika import load_books_from_csv

file_path = r"C:\Users\Rafi\Documents\Tubes prokom\Aplikasi-Peminjaman-Buku\data_buku.csv"
def main():
    # Memuat data buku dari CSV
    load_books_from_csv(file_path)

    # Membuat window utama
    root = Tk()
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