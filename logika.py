import pandas as pd
import os
from collections import defaultdict
import csv
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Variabel global untuk menyimpan data buku dan status buku
books_by_category = {}
book_status = {}

csv_file = "data_buku.csv"
user_csv_file = "users.csv"

def save_books_to_csv():
    """Menyimpan status buku ke file CSV."""
    book_list = []
    for category, books in books_by_category.items():
        for book in books:
            book_title, status = book.split(" - ")  # Pisahkan judul dan status
            book_list.append({'title': book_title, 'category': category, 'status': status})

    book_df = pd.DataFrame(book_list)
    book_df.to_csv(csv_file, index=False)


def borrow_book(selected_book):
    """Meminjam buku yang dipilih dan mencatat tanggal peminjaman."""
    try:
        # Memeriksa status buku
        if selected_book in book_status and book_status[selected_book] == "Tersedia":
            book_status[selected_book] = "Tidak Tersedia"  # Ubah status buku menjadi tidak tersedia
            borrow_date = datetime.now().strftime("%Y-%m-%d")  # Mengambil tanggal peminjaman
            book_status[f"{selected_book}_tanggal_peminjaman"] = borrow_date
            save_books_to_csv()  # Simpan perubahan ke CSV
            return True, borrow_date
        else:
            return False, "Buku sedang tidak tersedia!"
    except Exception as e:
        return False, f"Terjadi kesalahan: {e}"


def return_book(selected_book):
    """Mengembalikan buku yang dipilih, menghitung denda dan memperbarui status buku."""
    try:
        if selected_book in book_status and book_status[selected_book] == "Tidak Tersedia":
            borrowed_date = book_status.get(f"{selected_book}_tanggal_peminjaman")
            if borrowed_date:
                borrowed_date = datetime.strptime(borrowed_date, "%Y-%m-%d")
                return_date = datetime.now()
                max_borrow_days = 3
                overdue_days = (return_date - borrowed_date).days - max_borrow_days
                fine = max(0, overdue_days * 5000)  # Denda dihitung jika terlambat
                book_status[selected_book] = "Tersedia"
                book_status[f"{selected_book}_tanggal_pengembalian"] = return_date.strftime("%Y-%m-%d")
                book_status[f"{selected_book}_denda"] = fine
                save_books_to_csv()  # Simpan perubahan ke CSV
                return fine, return_date.strftime("%Y-%m-%d")
            else:
                return None, "Tanggal peminjaman tidak ditemukan!"
        else:
            return None, "Buku tidak sedang dipinjam!"
    except Exception as e:
        return None, f"Terjadi kesalahan: {e}"


def read_users():
    """Membaca data pengguna dari file CSV."""
    try:
        users = pd.read_csv(user_csv_file)  # Pastikan file ini ada di direktori yang benar
        return users
    except FileNotFoundError:
        print("File 'users.csv' tidak ditemukan.")
        return pd.DataFrame(columns=['username', 'password', 'name'])


def authenticate_user(username, password):
    """Autentikasi pengguna berdasarkan username dan password yang tersimpan di CSV."""
    users = read_users()

    username = username.strip().lower()
    password = password.strip().lower()

    if username in users['username'].values:
        stored_password = users.loc[users['username'] == username, 'password'].values[0]
        stored_password = str(stored_password).strip().lower()  # Ubah menjadi string dan bersihkan spasi

        if password == stored_password:
            return True
    return False


def write_user(username, password, name):
    """Menulis data pengguna baru ke file CSV."""
    users = read_users()
    new_user = pd.DataFrame([[username, password, name]], columns=['username', 'password', 'name'])
    users = pd.concat([users, new_user], ignore_index=True)
    users.to_csv(user_csv_file, index=False)


import csv
from collections import defaultdict

# Fungsi untuk membaca buku dari CSV dengan path yang diberikan
def load_books_from_csv(csv_file):
    global books_by_category, book_status
    books_by_category = {}
    book_status = {}

    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' tidak ditemukan.")
        return

    book_df = pd.read_csv(csv_file)
    for _, row in book_df.iterrows():
        category = row['category']
        book_title = row['title']
        status = row['status']

        if category not in books_by_category:
            books_by_category[category] = []
        books_by_category[category].append(book_title)

        book_status[book_title] = status

    return books_by_category

# Menggunakan path file yang Anda berikan
file_path = r"C:\Users\Rafi\Documents\Tubes prokom\Aplikasi-Peminjaman-Buku\data_buku.csv"

# Membaca buku dari file CSV menggunakan pandas
books_by_category = load_books_from_csv(file_path)

def read_books_from_csv(csv_file="data_buku.csv"):
    """Membaca data buku dari CSV dan mengembalikannya dalam bentuk list of dict."""
    books = []
    try:
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                books.append(row)
    except FileNotFoundError:
        print(f"File {csv_file} tidak ditemukan.")
    except Exception as e:
        print(f"Error reading from CSV: {e}")
    return books

def borrow_book(book_title, csv_file):
    books = read_books_from_csv(csv_file)
    
    # Cari buku berdasarkan judul
    selected_book = None
    for book in books:
        if book['title'] == book_title and book['status'] == 'Tersedia':
            selected_book = book
            break
    
    if selected_book is None:
        return False, None
    
    # Update status buku menjadi "Dipinjam"
    selected_book['status'] = 'Dipinjam'
    
    # Menyimpan tanggal peminjaman saat ini
    selected_book['tanggal_peminjaman'] = datetime.now().strftime("%Y-%m-%d")
    
    # Set denda menjadi 0 pada saat peminjaman
    selected_book['denda'] = '0'
    
    # Menyimpan perubahan ke CSV
    write_books_to_csv(books, csv_file)
    
    return True, selected_book

def write_books_to_csv(books, csv_file="data_buku.csv"):
    """Menulis daftar buku yang sudah diperbarui ke file CSV."""
    try:
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["title", "book_id", "category", "status", "tanggal_peminjaman", "tanggal_pengembalian", "denda"])
            writer.writeheader()
            for book in books:
                writer.writerow(book)
        print("File CSV berhasil diperbarui.")
    except Exception as e:
        print(f"Error writing to CSV: {e}")
        
# Fungsi untuk memperbarui daftar buku yang tersedia
def update_book_list(book_listbox, selected_category, csv_file):
    books = read_books_from_csv(csv_file)
    
    # Menampilkan hanya buku yang tersedia (status = "Tersedia")
    book_listbox.delete(0, tk.END)
    
    filtered_books = []
    if selected_category == "Semua":
        filtered_books = [book for book in books if book['status'] == "Tersedia"]
    else:
        filtered_books = [book for book in books if book['status'] == "Tersedia" and book['category'] == selected_category]
    
    for book in filtered_books:
        book_listbox.insert(tk.END, book['title'])

def calculate_fine(borrow_date, return_date):
    """Menghitung denda berdasarkan tanggal peminjaman dan tanggal pengembalian."""
    try:
        borrow_date_obj = datetime.strptime(borrow_date, "%Y-%m-%d")
        return_date_obj = datetime.strptime(return_date, "%Y-%m-%d")

        # Menghitung selisih hari antara tanggal peminjaman dan pengembalian
        overdue_days = (return_date_obj - borrow_date_obj).days

        if overdue_days > 3:  # Denda hanya berlaku jika terlambat lebih dari 3 hari
            fine = (overdue_days - 3) * 5000  # Denda 5.000 per hari setelah 3 hari
        else:
            fine = 0

        return fine

    except ValueError:
        return 0  # Mengembalikan 0 jika ada kesalahan dalam format tanggal
