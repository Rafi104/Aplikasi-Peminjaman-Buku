import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Class Agenda")
root.geometry("600x450")
root.configure(bg="#f0f0f0")

# Membuat frame-frame
frame_category = tk.Frame(root, bg="#f0f0f0")
frame_book_list = tk.Frame(root, bg="#f0f0f0")

# Membuat label dan dropdown untuk kategori buku
label_category = tk.Label(frame_category, text="Pilih kategori buku:", bg="#f0f0f0", font=("Arial", 14, "bold"))
label_category.pack(side=tk.LEFT, padx=10)

category_options = ["Pelajaran", "Novel", "Komik"]
selected_category = tk.StringVar()
dropdown_category = ttk.Combobox(frame_category, textvariable=selected_category, values=category_options, font=("Arial", 12), state="readonly")
dropdown_category.pack(side=tk.LEFT, padx=10)

# Membuat listbox untuk daftar buku
listbox_books = tk.Listbox(frame_book_list, width=50, font=("Arial", 12), selectbackground="#007bff", selectforeground="white", bg="#fff", bd=1, relief=tk.SOLID)
listbox_books.pack(pady=20)

# Menampilkan buku-buku berdasarkan kategori yang dipilih
def update_book_list(*args):
    listbox_books.delete(0, tk.END)
    selected = selected_category.get()
    if selected == "Pelajaran":
        for book in ["Kalkulus dan Geometri", "Analitis", "Fisika Dasar", "Kimia Organik", "Pemrograman Python untuk Pemula", "Sejarah Indonesia", "Atlas Dunia", "Algoritma dan Struktur Data", "Pengantar Psikologi"]:
            listbox_books.insert(tk.END, book)
    elif selected == "Novel":
        for book in ["Laskar Pelangi", "5 Cm", "Bumi Manusia", "Harry Potter and the Philosopher's Stone", "The Great Gatsby", "Sang Pemimpi", "Tenggelamnya Kapal Van der Wijck", "Arah Langkah"]:
            listbox_books.insert(tk.END, book)
    elif selected == "Komik":
        for book in ["Naruto: Volume 1", "One Piece: East Blue", "Dragon Ball: Z Saga", "Attack on Titan: Volume 1", "Doraemon: Petualangan", "My Hero Academia", "Demon Slayer", "Jujutsu Kaisen", "Slamdunk"]:
            listbox_books.insert(tk.END, book)

selected_category.trace("w", update_book_list)

# Tata letak
frame_category.pack(pady=20)
frame_book_list.pack(pady=20)

root.mainloop()