import tkinter as tk
from tkinter import messagebox, ttk
from Main import show_frame
from Book import create_home_menu
from datetime import datetime  # Import datetime untuk mendapatkan tanggal peminjaman

def create_borrow_book_frame(parent, frame, csv_file="data_buku.csv"):
    from Book import book_status, books_by_category
    """Buat frame untuk daftar buku yang bisa dipinjam."""
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
    def update_book_list():
        """Fungsi untuk memperbarui daftar buku berdasarkan kategori yang dipilih."""
        selected = selected_category.get()  # Ambil kategori yang dipilih
        book_listbox.delete(0, tk.END)  # Hapus daftar lama

        # Cek kategori yang dipilih dan tampilkan buku yang sesuai
        if selected == "Dipinjam":  # Tampilkan buku yang tidak tersedia
            for category in books_by_category:
                for book in books_by_category[category]:
                    if book_status.get(book) == "Tidak Tersedia":  # Buku dipinjam
                        book_listbox.insert(tk.END, book)
        elif selected == "Semua":  # Tampilkan semua buku yang tersedia
            for category in books_by_category:
                for book in books_by_category[category]:
                    if book_status.get(book) == "Tersedia":  # Buku tersedia
                        book_listbox.insert(tk.END, book)
        else:  # Tampilkan buku berdasarkan kategori yang tersedia
            if selected in books_by_category:
                for book in books_by_category[selected]:
                    if book_status.get(book) == "Tersedia":  # Buku tersedia
                        book_listbox.insert(tk.END, book)

    def borrow_selected_book():
        """Fungsi untuk meminjam buku yang dipilih."""
        try:
            selected_index = book_listbox.curselection()  # Ambil indeks buku yang dipilih
            if not selected_index:
                messagebox.showwarning("Peringatan", "Pilih buku terlebih dahulu!")
                return

            selected_book = book_listbox.get(selected_index)  # Ambil judul buku berdasarkan indeks

            # Menyimpan tanggal peminjaman saat buku dipinjam
            borrow_date = datetime.now().strftime("%Y-%m-%d")  # Mengambil tanggal hari ini
            if borrow_book(selected_book, csv_file, borrow_date):  # Panggil fungsi borrow_book dengan tanggal peminjaman
                # Perbarui tampilan Listbox setelah buku dipinjam
                update_book_list()
        except IndexError:
            messagebox.showwarning("Peringatan", "Pilih buku terlebih dahulu!")

    def borrow_book(selected_book, csv_file, borrow_date):
        from Book import save_books_to_csv
        """Fungsi untuk meminjam buku yang dipilih."""
        if book_status[selected_book] == "Tersedia":
            book_status[selected_book] = "Tidak Tersedia"  # Mengubah status buku menjadi Tidak Tersedia
            book_status[f"{selected_book}_tanggal_peminjaman"] = borrow_date  # Menyimpan tanggal peminjaman
            save_books_to_csv(csv_file)  # Simpan perubahan ke file CSV
            messagebox.showinfo("Sukses", f"Buku '{selected_book}' berhasil dipinjam pada {borrow_date}!")
            return True  # Berhasil dipinjam
        else:
            messagebox.showerror("Gagal", f"Buku '{selected_book}' sedang tidak tersedia!")
            return False  # Gagal dipinjam

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

    selected_category = tk.StringVar()
    category_dropdown = ttk.Combobox(
        category_frame,
        textvariable=selected_category,
        values=["Semua"] + list(books_by_category.keys()),  # Tambahkan opsi "Semua"
        state="readonly",
        font=("Arial", 12),
        width=30
    )
    category_dropdown.pack(side=tk.LEFT, padx=10)

    # Hubungkan dropdown kategori dengan fungsi update
    selected_category.trace("w", lambda *args: update_book_list())

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
        command=lambda: show_frame(parent, create_home_menu(parent,frame))
    ).pack(pady=20)

    return frame
