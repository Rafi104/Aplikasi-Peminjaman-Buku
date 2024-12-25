import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from tkcalendar import DateEntry
from logika import authenticate_user, books_by_category, book_status,borrow_book,write_user,return_book,update_book_list,read_books_from_csv,calculate_fine, write_books_to_csv
from datetime import datetime

books_by_category = {}
book_status = {}
csv_file = "data_buku.csv"

def show_frame(parent, frame):
    """Menampilkan frame tertentu."""
    for widget in parent.winfo_children():
        widget.pack_forget()
    frame.pack(expand=True, fill="both")

def create_register_frame(parent):
    """Membuat frame untuk pendaftaran pengguna baru."""
    frame = tk.Frame(parent, bg="#F7F9F9")
    frame.pack(expand=True, fill="both")

    # Label Judul
    tk.Label(frame, text="Pendaftaran Pengguna Baru", font=("Arial", 20), fg="#2E86C1", bg="#F7F9F9").pack(pady=20)

    # Frame untuk form input
    form_frame = tk.Frame(frame, bg="#F7F9F9")
    form_frame.pack(pady=20)

    # Label dan input untuk nama
    tk.Label(form_frame, text="Nama Lengkap", font=("Arial", 14), fg="#333333", bg="#F7F9F9").grid(row=0, column=0, sticky="w", pady=5)
    name_entry = tk.Entry(form_frame, font=("Arial", 14), width=40)
    name_entry.grid(row=0, column=1, pady=5)

    # Label dan input untuk username
    tk.Label(form_frame, text="Username", font=("Arial", 14), fg="#333333", bg="#F7F9F9").grid(row=1, column=0, sticky="w", pady=5)
    username_entry = tk.Entry(form_frame, font=("Arial", 14), width=40)
    username_entry.grid(row=1, column=1, pady=5)

    # Label dan input untuk password
    tk.Label(form_frame, text="Password", font=("Arial", 14), fg="#333333", bg="#F7F9F9").grid(row=2, column=0, sticky="w", pady=5)
    password_entry = tk.Entry(form_frame, font=("Arial", 14), width=40, show="*")
    password_entry.grid(row=2, column=1, pady=5)

    # Fungsi untuk mendaftar pengguna baru
    def register_user():
        name = name_entry.get()
        username = username_entry.get()
        password = password_entry.get()

        if not name or not username or not password:
            messagebox.showerror("Error", "Semua kolom harus diisi!")
            return

        # Mendaftar pengguna baru
        write_user(username, password, name)

        # Menampilkan pesan sukses dan kembali ke login
        messagebox.showinfo("Pendaftaran Berhasil", f"Pengguna {name} berhasil didaftarkan!")
        # Kembali ke frame login setelah berhasil mendaftar
        show_frame(parent, create_login_frame(parent))

    # Tombol untuk mendaftar
    register_button = tk.Button(frame, text="Daftar", font=("Arial", 14), command=register_user)
    register_button.pack(pady=10)

    # Tombol untuk kembali ke halaman login
    back_button = tk.Button(frame, text="Kembali ke Login", font=("Arial", 14), command=lambda: show_frame(parent, create_login_frame(parent)))
    back_button.pack(pady=10)

    return frame

# gui.py

def create_login_frame(parent):
    """Membuat frame login."""
    frame = tk.Frame(parent, bg="#E8F6F3")
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text="Login Aplikasi Peminjaman Buku Perpustakaan", font=("Arial", 20), fg="#2E86C1", bg="#E8F6F3").pack(pady=20)

    username_label = tk.Label(frame, text="Username:", font=("Arial", 14), bg="#E8F6F3")
    username_label.pack(pady=5)
    username_entry = tk.Entry(frame, font=("Arial", 14))
    username_entry.pack(pady=5)

    password_label = tk.Label(frame, text="Password:", font=("Arial", 14), bg="#E8F6F3")
    password_label.pack(pady=5)
    password_entry = tk.Entry(frame, font=("Arial", 14), show="*")
    password_entry.pack(pady=5)

    def login():
        """Fungsi untuk memverifikasi login pengguna."""
        username = username_entry.get()
        password = password_entry.get()

        if authenticate_user(username, password):
            messagebox.showinfo("Login Sukses", "Login berhasil!")
            # Setelah login berhasil, tampilkan frame home
            home_frame = create_home_menu(parent)  # Pastikan fungsi create_home_menu ada
            show_frame(parent, home_frame)  # Pastikan show_frame sudah terdefinisi
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah!")

    login_button = tk.Button(frame, text="Login", font=("Arial", 14), bg="#FF6B6B", fg="white", command=login)
    login_button.pack(pady=20)

    register_button = tk.Button(frame, text="Register", font=("Arial", 14), bg="#FF6B6B", fg="white", command=lambda: show_frame(parent, create_register_frame(parent)))
    register_button.pack(pady=20)

    return frame

def add_hover_effect(button):
    button.bind('<Enter>', lambda e: button.configure(bg='#F0F0F0'))
    button.bind('<Leave>', lambda e: button.configure(bg='white'))
    
def create_home_menu(parent):
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
        text="Selamat Datang!",
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
        command=lambda: show_frame(parent, create_book_category_frame(parent))  # Menambahkan semua argumen yang diperlukan
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
        command=lambda: show_frame(parent, create_borrow_book_frame(parent))  # Menambahkan semua argumen yang diperlukan untuk fitur pinjam buku
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
        command=lambda: show_frame(parent, create_return_book_frame(parent))  # Menambahkan semua argumen yang diperlukan untuk fitur kembalikan buku
    )
    btn_return_book.pack(pady=10)
    add_hover_effect(btn_return_book)

    # Tombol untuk keluar
    btn_exit = tk.Button(
        content_frame,
        text="Keluar",
        font=('Helvetica', 14),
        bg='white',
        fg='#FF6B6B',
        width=30,
        height=2,
        relief='solid',
        bd=1,
        cursor="hand2",
        command=parent.quit  # Menghentikan aplikasi
    )
    btn_exit.pack(pady=10)
    add_hover_effect(btn_exit)

    return frame

# Fungsi untuk membaca data buku dari CSV
def load_books_from_csv(filename):
    # Membaca file CSV dengan pandas
    try:
        df = pd.read_csv(filename)
        # Mengelompokkan buku berdasarkan kategori
        books_by_category = df.groupby('category').apply(lambda x: list(zip(x['title'], x['status']))).to_dict()
        return books_by_category
    except FileNotFoundError:
        print(f"File {filename} tidak ditemukan!")
        return {}

# Contoh path file
file_path = r"C:\Users\Rafi\Documents\Tubes prokom\Aplikasi-Peminjaman-Buku\data_buku.csv"

# Memuat data buku dari CSV
books_by_category = load_books_from_csv(file_path)

def create_book_category_frame(parent):
    """Buat frame untuk daftar buku berdasarkan kategori."""
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

    # Dropdown kategori dengan pilihan kategori
    selected_category = tk.StringVar()
    category_dropdown = ttk.Combobox(
        category_frame,
        textvariable=selected_category,
        values=["Semua"] + list(books_by_category.keys()),  # Pastikan "Semua" ada di awal kategori
        state="readonly",
        font=("Arial", 12),
        width=30
    )
    category_dropdown.pack(side=tk.LEFT, padx=10)

    # Listbox untuk menampilkan buku
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
        command=lambda: show_frame(parent, create_home_menu(parent))  # Placeholder, sesuaikan dengan aksi yang tepat
    ).pack(pady=20)

    # Fungsi untuk memperbarui daftar buku berdasarkan kategori yang dipilih
    def update_book_list(event):
        selected_category_value = selected_category.get()

        # Bersihkan listbox
        book_listbox.delete(0, tk.END)

        # Menampilkan buku berdasarkan kategori yang dipilih
        if selected_category_value == "Semua":
            # Menampilkan semua buku dari semua kategori
            for category, books in books_by_category.items():
                for book_title, book_status in books:
                    book_listbox.insert(tk.END, f"{book_title} - {book_status}")
        else:
            # Menampilkan buku dari kategori yang dipilih
            books = books_by_category.get(selected_category_value, [])
            for book_title, book_status in books:
                book_listbox.insert(tk.END, f"{book_title} - {book_status}")

    # Bind perubahan kategori pada combobox untuk memperbarui daftar buku
    category_dropdown.bind("<<ComboboxSelected>>", update_book_list)

    # Memanggil fungsi untuk pertama kali agar menampilkan buku berdasarkan kategori default
    update_book_list(None)

    return frame

def create_borrow_book_frame(parent, csv_file="data_buku.csv"):
    selected_category = tk.StringVar()  # Declare as StringVar
    frame = tk.Frame(parent, bg="#E8F6F3")
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Title
    tk.Label(
        frame,
        text="DAFTAR BUKU YANG TERSEDIA UNTUK DIPINJAM",
        font=("Arial Bold", 24),
        fg="#2E86C1",
        bg="#E8F6F3"
    ).pack(pady=20)

    # Listbox for available books
    book_listbox = tk.Listbox(
        frame,
        font=("Arial", 12),
        width=50,
        height=15,
        selectmode=tk.SINGLE
    )
    book_listbox.pack(pady=20)

    # Function to borrow selected book
    def borrow_selected_book():
        
        try:
            selected_index = book_listbox.curselection()  # Get selected book index
            if not selected_index:
                messagebox.showwarning("Peringatan", "Pilih buku terlebih dahulu!")
                return

            selected_item = book_listbox.get(selected_index)  # Get selected item text

            # Call the borrow function using the title instead of ID
            success, book = borrow_book(selected_item, csv_file)

            if success:
                messagebox.showinfo("Sukses", f"Buku '{book['title']}' berhasil dipinjam!\nTanggal Peminjaman: {book['tanggal_peminjaman']}")
            else:
                messagebox.showerror("Gagal", f"Buku '{book['title']}' sedang tidak tersedia!")

            # Update book list
            update_book_list(book_listbox, selected_category.get(), csv_file)

        except IndexError:
            messagebox.showwarning("Peringatan", "Pilih buku terlebih dahulu!")


    # Category dropdown
    category_frame = tk.Frame(frame, bg="#E8F6F3")
    category_frame.pack(fill="x", pady=10)

    tk.Label(
        category_frame,
        text="Pilih Kategori: ",
        font=("Arial", 14),
        bg="#E8F6F3"
    ).pack(side=tk.LEFT, padx=10)

    selected_category.set("Semua")  # Default category "Semua"

    category_dropdown = ttk.Combobox(
        category_frame,
        textvariable=selected_category,
        values=["Semua"],  # Default categories
        state="readonly",
        font=("Arial", 12),
        width=30
    )
    category_dropdown.pack(side=tk.LEFT, padx=10)

    # Update dropdown with categories from CSV
    books = read_books_from_csv(csv_file)
    categories = set(book['category'] for book in books)
    category_dropdown['values'] = ["Semua"] + list(categories)

    # Connect category dropdown with update function
    selected_category.trace("w", lambda *args: update_book_list(book_listbox, selected_category.get(), csv_file))

    # Button to borrow selected book
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

    # Button to return to main menu
    tk.Button(
        frame,
        text="KEMBALI KE MENU UTAMA",
        font=("Arial", 12),
        bg="#95A5A6",
        fg="white",
        width=25,
        height=2,
        cursor="hand2",
        command=lambda: show_frame(parent, create_home_menu(parent))  # Function to return to main menu (not implemented)
    ).pack(pady=20)

    # Initial book list update
    update_book_list(book_listbox, selected_category.get(), csv_file)
    
    return frame

def create_return_book_frame(parent, csv_file="data_buku.csv"):

    frame = tk.Frame(parent, bg="#E8F6F3")
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    tk.Label(
        frame,
        text="KEMBALIKAN BUKU",
        font=("Arial Bold", 24),
        fg="#2E86C1",
        bg="#E8F6F3"
    ).pack(pady=20)

    book_listbox = tk.Listbox(
        frame,
        font=("Arial", 12),
        width=50,
        height=15,
        selectmode=tk.SINGLE
    )
    book_listbox.pack(pady=20)

    # Membuat container untuk menampilkan detail peminjaman dan pengembalian
    labels = ["Tanggal Peminjaman:", "Tanggal Pengembalian:", "Denda:"]
    detail_labels = {}

    details_frame = tk.Frame(frame, bg="#E8F6F3")
    details_frame.pack(pady=10)

    for label in labels:
        container = tk.Frame(details_frame, bg="#E8F6F3")
        container.pack(fill="x", pady=5)

        tk.Label(
            container,
            text=label,
            font=("Arial", 12),
            bg="#E8F6F3",
            width=20,
            anchor="w"
        ).pack(side=tk.LEFT, padx=10)

        value_label = tk.Label(
            container,
            text="-",
            font=("Arial", 12),
            bg="#E8F6F3",
            anchor="w"
        )
        value_label.pack(side=tk.LEFT, padx=10)
        detail_labels[label] = value_label

    # Input untuk tanggal pengembalian menggunakan DateEntry dari tkcalendar
    tk.Label(frame, text="Tanggal Pengembalian:", font=("Arial", 12), bg="#E8F6F3").pack(pady=5)
    return_date_entry = DateEntry(
        frame,
        font=("Arial", 12),
        width=20,
        background='darkblue',
        foreground='white',
        borderwidth=2,
        date_pattern='yyyy-mm-dd'  # Format tanggal yang diinginkan
    )
    return_date_entry.pack(pady=10)

    def update_book_list_return(books):
        """Memperbarui daftar buku yang sedang dipinjam."""
        book_listbox.delete(0, tk.END)
        for book in books:
            if book['status'] == "Dipinjam":  # Menampilkan hanya buku yang sedang dipinjam
                book_listbox.insert(tk.END, book['title'])

    def return_selected_book():
        try:
            selected_index = book_listbox.curselection()
            if not selected_index:
                messagebox.showerror("Error", "Pilih buku terlebih dahulu!")
                return

            selected_book_title = book_listbox.get(selected_index)
            books = read_books_from_csv(csv_file)

            # Cari buku yang dipilih berdasarkan judul
            selected_book = None
            for book in books:
                if book['title'] == selected_book_title:
                    selected_book = book
                    break

            if not selected_book:
                messagebox.showerror("Error", "Buku tidak ditemukan!")
                return

            borrow_date = selected_book['tanggal_peminjaman']

            # Periksa apakah tanggal peminjaman ada dan valid
            if not borrow_date:
                messagebox.showerror("Error", f"Buku '{selected_book_title}' belum dipinjam.")
                return

            # Ambil tanggal pengembalian dari input user (menggunakan DateEntry)
            return_date = return_date_entry.get_date()  # Mendapatkan tanggal yang dipilih
            if not return_date:
                messagebox.showerror("Error", "Masukkan tanggal pengembalian!")
                return

            # Format tanggal pengembalian menjadi string
            return_date_str = return_date.strftime("%Y-%m-%d")

            # Hitung denda
            fine = calculate_fine(borrow_date, return_date_str)

            # Update status buku dan tanggal peminjaman
            selected_book['status'] = "Tersedia"
            selected_book['tanggal_pengembalian'] = return_date_str
            selected_book['denda'] = fine

            # Pastikan tanggal peminjaman ada untuk seluruh buku yang dipinjam
            for book in books:
                if book['status'] == "Dipinjam":
                    if 'tanggal_peminjaman' not in book or not book['tanggal_peminjaman']:
                        messagebox.showerror("Error", "Beberapa buku tidak memiliki tanggal peminjaman yang valid!")
                        return

            # Menyimpan perubahan ke CSV
            write_books_to_csv(books, csv_file)

            # Update detail labels
            detail_labels["Tanggal Peminjaman:"].config(text=borrow_date)
            detail_labels["Tanggal Pengembalian:"].config(text=return_date_str)
            detail_labels["Denda:"].config(text=f"Rp {fine}")

            # Update list buku yang dipinjam
            update_book_list_return(books)

            # Informasi sukses
            messagebox.showinfo("Sukses", f"Buku '{selected_book_title}' berhasil dikembalikan!\nDenda: Rp {fine}")

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    tk.Button(
        frame,
        text="KEMBALIKAN BUKU",
        font=("Arial", 12),
        bg="#5DADE2",
        fg="white",
        cursor="hand2",
        command=return_selected_book
    ).pack(pady=10)

    tk.Button(
        frame,
        text="KEMBALI KE MENU UTAMA",
        font=("Arial", 12),
        bg="#95A5A6",
        fg="white",
        width=25,
        height=2,
        cursor="hand2",
        command=lambda: show_frame(parent, create_home_menu(parent))
    ).pack(pady=20)

    books = read_books_from_csv(csv_file)
    update_book_list_return(books)  # Update the list of borrowed books when the frame is created
    return frame