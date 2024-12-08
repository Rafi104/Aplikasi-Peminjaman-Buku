import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import os

# Variabel global untuk menyimpan buku berdasarkan kategori
books_by_category = {}
book_status = {}
csv_file = r"E:\Aplikasi Peminjaman Buku\Aplikasi Peminjaman Buku\data_buku.csv"

# Fungsi untuk memuat buku berdasarkan kategori dari CSV
def load_books_from_csv(csv_file):
    global books_by_category, book_status
    books_by_category = {}
    book_status = {}

    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' tidak ditemukan.")
        return

    book_df = pd.read_csv(csv_file)
    for _, row in book_df.iterrows():
        category = row['kategori']
        book_title = row['judul_buku']
        status = row['status']

        if category not in books_by_category:
            books_by_category[category] = []
        books_by_category[category].append(book_title)

        book_status[book_title] = status

    return books_by_category

# Fungsi untuk menyimpan buku ke file CSV
def save_books_to_csv(csv_file):
    if not isinstance(csv_file, str):
        raise ValueError(f"csv_file harus berupa string, tetapi ditemukan {type(csv_file)}")
    book_list = []
    for category, books in books_by_category.items():
        for book in books:
            book_list.append({'judul_buku': book, 'kategori': category, 'status': book_status[book]})

    book_df = pd.DataFrame(book_list)
    book_df.to_csv(csv_file, index=False)

# Fungsi untuk menambahkan efek hover pada tombol
def add_hover_effect(button):
    button.bind('<Enter>', lambda e: button.configure(bg='#F0F0F0'))
    button.bind('<Leave>', lambda e: button.configure(bg='white'))

# Fungsi untuk membuat menu utama
# Fungsi untuk membuat menu utama
def create_home_menu(parent):
    from pinjambuku import create_borrow_book_frame
    from Main import show_frame
    from returnbook import create_return_book_frame
    """Buat frame untuk menu utama."""
    frame = tk.Frame(parent, bg='#E8F6F3')
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Frame utama
    content_frame = tk.Frame(frame, bg='#E8F6F3')
    content_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Frame sambutan
    welcome_frame = tk.Frame(content_frame, bg='#E8F6F3')
    welcome_frame.pack(fill="x", pady=(0, 30))
    tk.Label(
        welcome_frame,
        text="Selamat Datang,",
        font=("Helvetica", 32, "bold"),
        bg='#E8F6F3',
        fg='#FF6B6B'
    ).pack()

    # Tombol untuk melihat buku berdasarkan kategori
    btn_view_books = tk.Button(
        content_frame,
        text="Lihat Buku Berdasarkan Kategori",
        font=('Helvetica', 14),
        bg='white',
        fg='#2E86C1',
        width=30,
        height=2,
        relief='solid',
        bd=1,
        cursor="hand2",
        command=lambda: show_frame(parent, create_book_category_frame(parent, frame))  # Menambahkan semua argumen yang diperlukan
    )
    btn_view_books.pack(pady=10)
    add_hover_effect(btn_view_books)

    # Tombol untuk meminjam buku
    btn_borrow_book = tk.Button(
        content_frame,
        text="Pinjam Buku",
        font=('Helvetica', 14),
        bg='white',
        fg='#2E86C1',
        width=30,
        height=2,
        relief='solid',
        bd=1,
        cursor="hand2",
        command=lambda: show_frame(parent, create_borrow_book_frame(parent, frame,csv_file))  # Menambahkan semua argumen yang diperlukan untuk fitur pinjam buku
    )
    btn_borrow_book.pack(pady=10)
    add_hover_effect(btn_borrow_book)
    # Tombol untuk mengembalikan buku
    btn_return_book = tk.Button(
        content_frame,
        text="Kembalikan Buku",
        font=('Helvetica', 14),
        bg='white',
        fg='#2E86C1',
        width=30,
        height=2,
        relief='solid',
        bd=1,
        cursor="hand2",
        command=lambda: show_frame(parent, create_return_book_frame(parent,frame))  # Menambahkan semua argumen yang diperlukan untuk fitur kembalikan buku
    )
    btn_return_book.pack(pady=10)
    add_hover_effect(btn_return_book)

    return frame


    # Tombol untuk mengembalikan buku
    # btn_return_book = tk.Button(
    #     content_frame,
    #     text="Kembalikan Buku",
    #     font=('Helvetica', 14),
    #     bg='white',
    #     fg='#2E86C1',
    #     width=30,
    #     height=2,
    #     relief='solid',
    #     bd=1,
    #     cursor="hand2",
    #     command=lambda: show_frame(parent, create_return_book_frame(parent, frame))  # Menambahkan semua argumen yang diperlukan untuk fitur kembalikan buku
    # )
    # btn_return_book.pack(pady=10)
    # add_hover_effect(btn_return_book)

    return frame

# Fungsi untuk memperbarui daftar buku berdasarkan kategori yang dipilih
# Fungsi untuk memperbarui daftar buku berdasarkan kategori yang dipilih
# Fungsi untuk memperbarui daftar buku berdasarkan kategori yang dipilih
def update_book_list(event, book_listbox, selected_category):
    """Fungsi untuk memperbarui daftar buku berdasarkan kategori yang dipilih."""
    selected = selected_category.get()  # Ambil kategori yang dipilih
    book_listbox.delete(0, tk.END)  # Hapus daftar lama

    if selected == "Semua":  # Jika kategori yang dipilih adalah "Semua"
        # Menampilkan semua buku
        for category in books_by_category:
            for book in books_by_category[category]:
                status = book_status.get(book, "Tersedia")  # Ambil status buku, default Tersedia
                book_listbox.insert(tk.END, f"{book} ({status})")
    elif selected in books_by_category:  # Jika kategori tertentu dipilih
        for book in books_by_category[selected]:
            status = book_status.get(book, "Tersedia")  # Ambil status buku
            book_listbox.insert(tk.END, f"{book} ({status})")  # Tampilkan judul dan status buku

# Fungsi untuk membuat frame kategori buku (Hanya melihat buku)
def create_book_category_frame(parent, frame):
    from Main import show_frame
    """Buat frame untuk daftar buku berdasarkan kategori (Hanya melihat buku)."""
    frame = tk.Frame(parent, bg="#E8F6F3")
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Judul
    tk.Label(
        frame,
        text="DAFTAR BUKU BERDASARKAN KATEGORI",
        font=("Arial Bold", 24),
        fg="#2E86C1",
        bg="#E8F6F3"
    ).pack(pady=20)

    # Frame kategori
    category_frame = tk.Frame(frame, bg="#E8F6F3")
    category_frame.pack(fill="x", pady=10)

    tk.Label(
        category_frame,
        text="Pilih Kategori:",
        font=("Arial", 14),
        bg="#E8F6F3"
    ).pack(side=tk.LEFT, padx=10)

    # Dropdown kategori
    selected_category = tk.StringVar()
    category_dropdown = ttk.Combobox(
        category_frame,
        textvariable=selected_category,
        values=["Semua"] + list(books_by_category.keys()),  # Menambahkan "Semua" di depan kategori
        state="readonly",
        font=("Arial", 12),
        width=30
    )
    category_dropdown.pack(side=tk.LEFT, padx=10)

    # Listbox untuk buku
    book_listbox = tk.Listbox(
        frame,
        font=("Arial", 12),
        width=50,
        height=15,
        selectmode=tk.SINGLE
    )
    book_listbox.pack(pady=20)

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
        command=lambda: show_frame(parent, create_home_menu(parent, frame))
    ).pack(pady=20)

    # Perbarui daftar buku pertama kali setelah kategori dipilih
    category_dropdown.bind("<<ComboboxSelected>>", lambda event: update_book_list(event, book_listbox, selected_category))

    return frame

