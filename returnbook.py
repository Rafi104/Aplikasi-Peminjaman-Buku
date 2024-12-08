import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from Book import books_by_category, book_status, save_books_to_csv
from Main import show_frame

csv_file = r"C:\Users\Rafi\Documents\Tubes prokom\Aplikasi-Peminjaman-Buku\data_buku.csv"

def borrow_book(selected_book, csv_file):
    """Fungsi untuk meminjam buku yang dipilih dan mencatat tanggal peminjaman."""
    try:
        # Validasi path CSV
        if not isinstance(csv_file, str):
            raise ValueError(f"csv_file harus berupa string, tetapi ditemukan {type(csv_file)}")

        # Cek apakah buku tersedia untuk dipinjam
        if book_status.get(selected_book) == "Tersedia":
            book_status[selected_book] = "Tidak Tersedia"  # Ubah status buku menjadi tidak tersedia

            # Ambil tanggal peminjaman
            borrow_date = datetime.now().strftime("%Y-%m-%d")  # Mengambil tanggal hari ini

            # Simpan tanggal peminjaman
            book_status[f"{selected_book}_tanggal_peminjaman"] = borrow_date
            save_books_to_csv(csv_file)  # Simpan ke file CSV

            messagebox.showinfo("Sukses", f"Buku '{selected_book}' berhasil dipinjam pada {borrow_date}!")
            return True  # Berhasil dipinjam
        else:
            messagebox.showerror("Gagal", f"Buku '{selected_book}' sedang tidak tersedia!")
            return False  # Gagal dipinjam
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
        return False

def return_book(selected_book, csv_file):
    """Fungsi untuk mengembalikan buku yang dipilih dengan tanggal peminjaman dan tanggal pengembalian serta perhitungan denda."""
    try:
        # Validasi path CSV
        if not isinstance(csv_file, str):
            raise ValueError(f"csv_file harus berupa string, tetapi ditemukan {type(csv_file)}")

        if selected_book in book_status and book_status[selected_book] == "Tidak Tersedia":
            # Ambil tanggal peminjaman
            borrowed_date = book_status.get(f"{selected_book}_tanggal_peminjaman")
            
            if borrowed_date:  # Pastikan tanggal peminjaman ada
                borrowed_date = datetime.strptime(borrowed_date, "%Y-%m-%d")
                return_date = datetime.now()  # Ambil tanggal pengembalian sekarang

                # Hitung denda jika terlambat
                max_borrow_days = 7
                overdue_days = (return_date - borrowed_date).days - max_borrow_days
                if overdue_days > 0:
                    fine = overdue_days * 5000
                    messagebox.showinfo("Denda", f"Buku dikembalikan terlambat {overdue_days} hari. Denda: Rp {fine}")
                else:
                    fine = 0

                # Update status buku
                book_status[selected_book] = "Tersedia"  # Ubah status buku
                book_status[f"{selected_book}_tanggal_pengembalian"] = return_date.strftime("%Y-%m-%d")  # Tanggal pengembalian
                book_status[f"{selected_book}_denda"] = fine  # Simpan denda
                save_books_to_csv(csv_file)  # Simpan ke file CSV

                messagebox.showinfo("Sukses", f"Buku '{selected_book}' berhasil dikembalikan!\nDenda: Rp {fine}")
                return fine, return_date.strftime("%Y-%m-%d")  # Return denda dan tanggal pengembalian
            else:
                messagebox.showerror("Error", "Tanggal peminjaman tidak ditemukan!")
                return None, None
        else:
            messagebox.showerror("Gagal", f"Buku '{selected_book}' tidak sedang dipinjam!")
            return None, None

    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
        return None, None

def create_return_book_frame(parent, container):  # Ganti frame ke container
    from Book import create_home_menu

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
    detail_labels = {}  # Menggunakan dictionary untuk menyimpan label detail

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
        detail_labels[label] = value_label  # Menyimpan label dalam dictionary

    def update_book_list():
        """Memperbarui daftar buku yang sedang dipinjam."""
        book_listbox.delete(0, tk.END)
        for category in books_by_category:
            for book in books_by_category[category]:
                if book_status.get(book) == "Tidak Tersedia":  # Menampilkan hanya buku yang sedang dipinjam
                    book_listbox.insert(tk.END, book)

    def return_selected_book():
        try:
            selected_index = book_listbox.curselection()
            if not selected_index:
                messagebox.showerror("Error", "Pilih buku terlebih dahulu!")
                return

            selected_book = book_listbox.get(selected_index)
            fine, return_date = return_book(selected_book, csv_file)

            # Update labels with borrow and return details
            if fine is not None:
                borrowed_date = book_status.get(f"{selected_book}_tanggal_peminjaman")
                denda = book_status.get(f"{selected_book}_denda", 0)
                detail_labels["Tanggal Peminjaman:"].config(text=borrowed_date)
                detail_labels["Tanggal Pengembalian:"].config(text=return_date)
                detail_labels["Denda:"].config(text=f"Rp {denda}")

            update_book_list()
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
        command=lambda: show_frame(parent, create_home_menu(parent,frame))
    ).pack(pady=20)

    update_book_list()
    return frame
