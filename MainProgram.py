import os
import csv
from datetime import datetime, timedelta

# Kelas Mahasiswa, Buku, Peminjaman, dan Admin
class Mahasiswa:
    def __init__(self, nama, nim):
        self.nama = nama
        self.nim = nim

class Buku:
    def __init__(self, judul, penulis):
        self.judul = judul
        self.penulis = penulis
        self.status = "Tersedia"  # Default status

class Peminjaman:
    def __init__(self, mahasiswa, buku, durasi_pinjam=7):
        self.mahasiswa = mahasiswa
        self.buku = buku
        self.tanggal_pinjam = datetime.now()
        self.tanggal_kembali = self.tanggal_pinjam + timedelta(days=durasi_pinjam)
        self.status = "Dipinjam"
        self.tanggal_pengembalian = None
        # Set status buku menjadi "Tidak Tersedia"
        self.buku.status = "Tidak Tersedia"

    def info_peminjaman(self):
        print("\n--- Info Peminjaman ---")
        print(f"Nama Mahasiswa: {self.mahasiswa.nama}")
        print(f"NIM: {self.mahasiswa.nim}")
        print(f"Judul Buku: {self.buku.judul}")
        print(f"Penulis Buku: {self.buku.penulis}")
        print(f"Tanggal Peminjaman: {self.tanggal_pinjam.strftime('%Y-%m-%d')}")
        print(f"Estimasi Pengembalian: {self.tanggal_kembali.strftime('%Y-%m-%d')}")
        print("Catatan: Denda Rp5000/hari jika terlambat mengembalikan buku.")

class Admin:
    def __init__(self):
        self.data_peminjaman = []

    def simpan_data_peminjaman(self, peminjaman):
        self.data_peminjaman.append(peminjaman)

    def kembalikan_buku(self, buku):
        for peminjaman in self.data_peminjaman:
            if peminjaman.buku == buku and peminjaman.status == "Dipinjam":
                peminjaman.status = "Dikembalikan"
                peminjaman.tanggal_pengembalian = datetime.now()
                buku.status = "Tersedia"
                return True
        return False

# Fungsi utilitas
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def welcome_message():
    clear_screen()
    print("===================== WELCOME =====================")
    print("        Selamat datang di Perpustakaan Pintar! ")
    print("===================================================")

buku_list = []
    # Kategori Komik
    Buku("Naruto: Volume 1", "Masashi Kishimoto"),
    Buku("One Piece: East Blue", "Eiichiro Oda"),
    Buku("Dragon Ball: Z Saga", "Akira Toriyama"),
    Buku("Attack on Titan: Volume 1", "Hajime Isayama"),
    Buku("Doraemon: Petualangan", "Fujiko F. Fujio"),
    Buku("My Hero Academia", "Kohei Horikoshi"),
    Buku("Demon Slayer", "Koyoharu Gotouge"),
    Buku("Jujutsu Kaisen", "Gege Akutami"),
    # Kategori Pelajaran
    Buku("Kalkulus dan Geometri Analitis", "Edwin J Purcell, Dale Varberg"),
    Buku("Fisika Dasar", "Halliday dan Resnick"),
    Buku("Kimia Organik", "Paula Bruice"),
    Buku("Pemrograman Python untuk Pemula", "John Doe"),
    Buku("Sejarah Indonesia", "M.C. Ricklefs"),
    Buku("Atlas Dunia", "National Geographic"),
    Buku("Bahasa Indonesia", "Abdul Chaer"),
    Buku("English Grammar in Use", "Raymond Murphy"),
    Buku("Pengantar Psikologi", "Rita L. Atkinson"),
    Buku("Algoritma dan Struktur Data", "Jane Smith"),
    # Kategori Novel
    Buku("Laskar Pelangi", "Andrea Hirata"),
    Buku("5 Cm", "Donny Dhirgantoro"),
    Buku("Bumi", "Tere Liye"),
    Buku("Harry Potter and the Philosopher's Stone", "J.K. Rowling"),
    Buku("The Great Gatsby", "F. Scott Fitzgerald"),
    Buku("Sang Pemimpi", "Andrea Hirata"),
    Buku("Tenggelamnya Kapal Van der Wijck", "Hamka"),
    Buku("Arah Langkah", "Fiersa Besari")
    Buku("Tapak Jejak", "Fiersa Besari")
]

admin = Admin()

def tampilkan_daftar_buku():
    print("\n--- Daftar Buku di Perpustakaan ---")
    for i, buku in enumerate(buku_list, start=1):
        status_text = "Tersedia" if buku.status == "Tersedia" else "Tidak Tersedia"
        print(f"{i}. {buku.judul} oleh {buku.penulis} - Status: {status_text}")
    pilih_peminjaman(username)

def tampilkan_daftar_buku_berdasarkan_kategori():
    print("\n--- Daftar Buku Berdasarkan Kategori ---")
    print("\nKategori: Komik")
    for buku in buku_list[:5]:
        status_text = "Tersedia" if buku.status == "Tersedia" else "Tidak Tersedia"
        print(f"- {buku.judul} oleh {buku.penulis} - Status: {status_text}")

    print("\nKategori: Pelajaran")
    for buku in buku_list[5:10]:
        status_text = "Tersedia" if buku.status == "Tersedia" else "Tidak Tersedia"
        print(f"- {buku.judul} oleh {buku.penulis} - Status: {status_text}")

    print("\nKategori: Novel")
    for buku in buku_list[10:]:
        status_text = "Tersedia" if buku.status == "Tersedia" else "Tidak Tersedia"
        print(f"- {buku.judul} oleh {buku.penulis} - Status: {status_text}")

def tampilkan_buku_kategori(kategori):
    if kategori == "Komik":
        return buku_list[:5]
    elif kategori == "Pelajaran":
        return buku_list[5:10]
    elif kategori == "Novel":
        return buku_list[10:]
    return []

def aplikasi_peminjaman():
    print("\n--- Peminjaman Buku ---")
    print("Pilih kategori buku:")
    print("1. Komik")
    print("2. Pelajaran")
    print("3. Novel")
    kategori_pilihan = input("Masukkan nomor kategori (1/2/3): ")

    if kategori_pilihan == '1':
        kategori = "Komik"
    elif kategori_pilihan == '2':
        kategori = "Pelajaran"
    elif kategori_pilihan == '3':
        kategori = "Novel"
    else:
        print("Pilihan kategori tidak valid.")
        return

    buku_kategori = tampilkan_buku_kategori(kategori)
    if not buku_kategori:
        print("Tidak ada buku dalam kategori ini.")
        return

    print(f"\n--- Daftar Buku {kategori} ---")
    for i, buku in enumerate(buku_kategori, start=1):
        status_text = "Tersedia" if buku.status == "Tersedia" else "Tidak Tersedia"
        print(f"{i}. {buku.judul} oleh {buku.penulis} - Status: {status_text}")

    pilihan = input("Pilih nomor buku yang ingin Anda pinjam: ")
    try:
        pilihan = int(pilihan) - 1
        if pilihan < 0 or pilihan >= len(buku_kategori):
            print("Pilihan tidak valid.")
            return
        buku = buku_kategori[pilihan]
        if buku.status == "Tidak Tersedia":
            print("Maaf, buku ini sedang tidak tersedia karena sedang dipinjam.")
            return

        nama = input("Masukkan Nama Anda: ")
        nim = input("Masukkan NIM Anda: ")
        mahasiswa = Mahasiswa(nama, nim)

        konfirmasi = input(f"Apakah Anda yakin ingin meminjam buku '{buku.judul}' oleh {buku.penulis}? (ya/tidak): ").lower()
        if konfirmasi != "ya":
            print("Peminjaman dibatalkan.")
            return

        peminjaman = Peminjaman(mahasiswa, buku)
        admin.simpan_data_peminjaman(peminjaman)
        peminjaman.info_peminjaman()
        print("\nPeminjaman berhasil! Data telah disimpan.")
    except ValueError:
        print("Input tidak valid. Harap masukkan angka.")

def pengembalian_buku():
    print("\n--- Pengembalian Buku ---")
    if not admin.data_peminjaman:
        print("Tidak ada buku yang sedang dipinjam.")
        return

    print("\nDaftar Buku yang Sedang Dipinjam:")
    peminjaman_aktif = [p for p in admin.data_peminjaman if p.status == "Dipinjam"]
    if not peminjaman_aktif:
        print("Tidak ada buku yang sedang dipinjam.")
        return

    for i, peminjaman in enumerate(peminjaman_aktif, start=1):
        print(f"{i}. {peminjaman.buku.judul} - Dipinjam oleh {peminjaman.mahasiswa.nama}")

    try:
        pilihan = int(input("\nPilih nomor buku yang akan dikembalikan: ")) - 1
        if 0 <= pilihan < len(peminjaman_aktif):
            peminjaman = peminjaman_aktif[pilihan]
            if admin.kembalikan_buku(peminjaman.buku):
                print(f"\nBuku '{peminjaman.buku.judul}' berhasil dikembalikan.")
                print(f"Tanggal pengembalian: {peminjaman.tanggal_pengembalian.strftime('%Y-%m-%d')}")
            else:
                print("Gagal mengembalikan buku.")
        else:
            print("Pilihan tidak valid.")
    except ValueError:
        print("Input tidak valid. Harap masukkan angka.")

def main_menu(username):
    while True:
        clear_screen()
        print(f"Selamat datang, {username}!")
        print("1. Pinjam Buku")
        print("2. Lihat Semua Buku")
        print("3. Lihat Buku Berdasarkan Kategori")
        print("4. Kembalikan Buku")
        print("5. Keluar")
        choice = input("Pilih menu (1/2/3/4/5): ")

        if choice == '1':
            aplikasi_peminjaman()
        elif choice == '2':
            tampilkan_daftar_buku()
        elif choice == '3':
            tampilkan_daftar_buku_berdasarkan_kategori()
        elif choice == '4':
            pengembalian_buku()
        elif choice == '5':
            print("Terima kasih telah menggunakan aplikasi ini!")
            exit()
        else:
            print("Pilihan tidak valid.")
        
        input("\nTekan Enter untuk melanjutkan...")
        
def pilih_peminjaman(username):
    while True:
        print("=====================================")
        print("1. Pinjam Buku")
        print("2. Kembali")
        choice = input("Pilih menu (1/2): ")

        if choice == '1':
            aplikasi_peminjaman()
        elif choice == '2':
            main_menu(username)
        elif choice == '5':
            print("Terima kasih telah menggunakan aplikasi ini!")
            exit()
        else:
            print("Pilihan tidak valid.")

def login():
    global username
    welcome_message()
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")

    try:
        with open('akun.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2 and row[0] == username and row[1] == password:
                    print("Login berhasil!")
                    main_menu(username)
                    return
            print("Username atau password salah.")
    except FileNotFoundError:
        print("Database akun tidak ditemukan. Silakan sign up terlebih dahulu.")
        with open('akun.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'password'])
    input("Tekan Enter untuk kembali ke menu...")
    main()

def sign_up():
   welcome_message()
   username = input("Masukkan username baru: ")
   password = input("Masukkan password baru (minimal 8 karakter, kombinasi huruf dan angka): ")
   while not (len(password) >= 8 and password.isalnum()):
       print("Password tidak valid. Harus minimal 8 karakter dengan kombinasi huruf dan angka.")
       password = input("Masukkan kembali password: ")

   try:
       with open('akun.csv', 'r') as file:
           reader = csv.reader(file)
           for row in reader:
               if row[0] == username:
                   print("Username sudah terdaftar.")
                   input("Tekan Enter untuk kembali ke menu...")
                   main()
                   return
               
   except FileNotFoundError:
       pass

   with open('akun.csv', 'a', newline='') as file:
       writer = csv.writer(file)
       writer.writerow([username, password])
   print("Akun berhasil dibuat!")
   input("Tekan Enter untuk login...")
   main()

def main():
    while True:
        clear_screen()
        print("1. Login")
        print("2. Sign Up")
        print("3. Keluar")
        choice = input("Pilih menu (1/2/3): ")

        if choice == '1':
            login()
        elif choice == '2':
            sign_up()
        elif choice == '3':
            print("Terima kasih telah menggunakan aplikasi ini!")
            exit()
        else:
            print("Pilihan tidak valid.")
            input("Tekan Enter untuk kembali...")

if __name__ == "__main__":
    main()