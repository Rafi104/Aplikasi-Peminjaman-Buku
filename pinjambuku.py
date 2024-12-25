import tkinter as tk
from tkinter import messagebox, ttk
from Main import show_frame
from Book import create_home_menu
from datetime import datetime  # Import datetime untuk mendapatkan tanggal peminjaman

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import csv

# Fungsi untuk membaca data buku dari file CSV
def read_books_from_csv(csv_file):
    books = []
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            books.append(row)
    return books

# Fungsi untuk menyimpan data buku ke file CSV
def save_books_to_csv(csv_file, books):
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['book_id', 'title', 'category', 'status', 'borrow_date']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for book in books:
            writer.writerow(book)

# Fungsi untuk memperbarui daftar buku yang ditampilkan di Listbox
def update_book_list(book_listbox, selected_category, csv_file):
    books = read_books_from_csv(csv_file)
    book_listbox.delete(0, tk.END)  # Hapus daftar lama

    # Filter buku berdasarkan kategori dan status
    for book in books:
        if selected_category == "Semua" or selected_category == book['category']:
            if book['status'] == "Tersedia":
                book_listbox.insert(tk.END, f"{book['title']} - ID: {book['book_id']}")

# Fungsi untuk meminjam buku berdasarkan ID
def borrow_book(selected_book_id, csv_file):
    books = read_books_from_csv(csv_file)
    
    for book in books:
        if book['book_id'] == selected_book_id:
            if book['status'] == "Tersedia":
                # Update status buku menjadi 'Tidak Tersedia'
                book['status'] = "Tidak Tersedia"
                book['borrow_date'] = datetime.now().strftime("%Y-%m-%d")
                save_books_to_csv(csv_file, books)  # Simpan perubahan ke CSV
                return True, book
            else:
                return False, book
    return False, None  # Buku tidak ditemukan

# Fungsi utama untuk membuat frame peminjaman buku
def create_borrow_book_frame(parent, frame, csv_file="data_buku.csv"):
    selected_category = tk.StringVar()  # Deklarasikan sebagai StringVar
    frame = tk.Frame(parent, bg="#E8F6F3")
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Judul
    tk.Label(
        frame,
        text="DAFTAR BUKU YANG TERSEDIA UNTUK DIPINJAM",
        font=("Arial Bold", 24),
        fg="#2E86C1",
        bg="#E8F6F3"
    ).pack(pady=20)

    # Listbox untuk buku yang tersedia
    book_listbox = tk.Listbox(
        frame,
        font=("Arial", 12),
        width=50,
        height=15,
        selectmode=tk.SINGLE
    )
    book_listbox.pack(pady=20)

    # Menampilkan buku yang tersedia
    def borrow_selected_book():
        """Fungsi untuk meminjam buku yang dipilih."""
        try:
            selected_index = book_listbox.curselection()  # Ambil indeks buku yang dipilih
            if not selected_index:
                messagebox.showwarning("Peringatan", "Pilih buku terlebih dahulu!")
                return

            selected_item = book_listbox.get(selected_index)  # Ambil teks yang dipilih
            title, book_id = selected_item.split(" - ID: ")  # Pisahkan judul dan ID

            # Panggil fungsi untuk meminjam buku berdasarkan ID
            success, book = borrow_book(book_id, csv_file)

            if success:
                messagebox.showinfo("Sukses", f"Buku '{book['title']}' berhasil dipinjam pada {book['borrow_date']}!")
            else:
                messagebox.showerror("Gagal", f"Buku '{book['title']}' sedang tidak tersedia!")
            
            # Perbarui daftar buku
            update_book_list(book_listbox, selected_category.get(), csv_file)

        except IndexError:
            messagebox.showwarning("Peringatan", "Pilih buku terlebih dahulu!")

    # Dropdown kategori
    category_frame = tk.Frame(frame, bg="#E8F6F3")
    category_frame.pack(fill="x", pady=10)

    tk.Label(
        category_frame,
        text="Pilih Kategori: ",
        font=("Arial", 14),
        bg="#E8F6F3"
    ).pack(side=tk.LEFT, padx=10)

    selected_category.set("Semua")  # Set kategori default "Semua"

    category_dropdown = ttk.Combobox(
        category_frame,
        textvariable=selected_category,
        values=["Semua"],  # Kategori default
        state="readonly",
        font=("Arial", 12),
        width=30
    )
    category_dropdown.pack(side=tk.LEFT, padx=10)

    # Update dropdown dengan kategori yang ada di file CSV
    books = read_books_from_csv(csv_file)
    categories = set(book['category'] for book in books)
    category_dropdown['values'] = ["Semua"] + list(categories)

    # Hubungkan dropdown kategori dengan fungsi update
    selected_category.trace("w", lambda *args: update_book_list(book_listbox, selected_category.get(), csv_file))

    # Tombol untuk meminjam buku
    tk.Button(
        frame,
        text="PINJAM BUKU",
        font=("Arial", 12),
        bg="#FF6B6B",
        fg="white",
        width=15,
        height=2,
        cursor="hand2",
        command=borrow_selected_book
    ).pack(pady=10)

    # Tombol untuk kembali ke menu utama
    tk.Button(
        frame,
        text="KEMBALI KE MENU UTAMA",
        font=("Arial", 12),
        bg="#95A5A6",
        fg="white",
        width=25,
        height=2,
        cursor="hand2",
        command=lambda: None  # Fungsi kembali ke menu utama
    ).pack(pady=20)

    # Perbarui daftar buku awal
    update_book_list(book_listbox, selected_category.get(), csv_file)

    return frame
