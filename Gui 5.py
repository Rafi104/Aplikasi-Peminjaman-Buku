import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class PerpustakaanPintar:
    def __init__(self, root):
        self.root = root
        self.root.title("Perpustakaan Pintar")
        
        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Calculate window size (80% of screen)
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        
        # Calculate position
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set window size and position
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        self.root.minsize(800, 600)
        
        # Configure grid weight
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Initialize data structures
        self.users = {}
        self.current_user = None
        self.borrowed_books = {}  # Format: {username: [{book: str, borrow_date: datetime, return_date: datetime}]}
        self.books_by_category = {
            "All": ["Kalkulus dan Geometri", "Analitis", "Fisika Dasar", 
                "Kimia Organik", "Pemrograman Python untuk Pemula", 
                 "Sejarah Indonesia", "Atlas Dunia", "Algoritma dan Struktur Data", "Pengantar Psikologi", "Laskar Pelangi", "5 Cm", "Bumi Manusia",
                "Harry Potter and the Philosopher's Stone",
                "The Great Gatsby", "Sang Pemimpi",
                "Tenggelamnya Kapal Van der Wijck", "Arah Langkah", "Naruto: Volume 1", "One Piece: East Blue",
                "Dragon Ball: Z Saga", "Attack on Titan: Volume 1",
                "Doraemon: Petualangan", "My Hero Academia",
                "Demon Slayer", "Jujutsu Kaisen", "Slamdunk, Haikyuu",
                "Crayoon Shinchan"
            ],
            "Pelajaran": [
                "Kalkulus dan Geometri", "Analitis", "Fisika Dasar", 
                "Kimia Organik", "Pemrograman Python untuk Pemula",
                "Sejarah Indonesia", "Atlas Dunia", 
                "Algoritma dan Struktur Data", "Pengantar Psikologi"
            ],
            "Novel": [
                "Laskar Pelangi", "5 Cm", "Bumi Manusia",
                "Harry Potter and the Philosopher's Stone",
                "The Great Gatsby", "Sang Pemimpi",
                "Tenggelamnya Kapal Van der Wijck", "Arah Langkah"
            ],
            "Komik": [
                "Naruto: Volume 1", "One Piece: East Blue",
                "Dragon Ball: Z Saga", "Attack on Titan: Volume 1",
                "Doraemon: Petualangan", "My Hero Academia",
                "Demon Slayer", "Jujutsu Kaisen", "Slamdunk, Haikyuu",
                "Crayon Shinchan", ""
            ]
        }
        
        # Create container
        self.container = tk.Frame(root)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Create and store frames
        self.frames = {}
        for F in (RegisterFrame, LoginFrame, HomeMenu, BookCategoryFrame, BorrowBookFrame, BookReturnFrame):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(RegisterFrame)
    
    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()
        
    def add_user(self, username, password, name):
        self.users[username] = {
            'password': password,
            'name': name
        }
    
    def check_user(self, username, password):
        return username in self.users and self.users[username]['password'] == password

    def get_username_by_name(self, name):
        for username, data in self.users.items():
            if data['name'] == name:
                return username
        return None

class BorrowBookFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#E8F6F3")
        
        # Main content frame
        content_frame = tk.Frame(self, bg="#E8F6F3")
        content_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Title
        tk.Label(
            content_frame,
            text="PEMINJAMAN BUKU",
            font=("Arial Bold", 24),
            fg="#2E86C1",
            bg="#E8F6F3"
        ).pack(pady=20)

        # Info label
        self.info_label = tk.Label(
            content_frame,
            text="Silakan pilih kategori dan buku yang ingin dipinjam",
            font=("Arial", 12),
            fg="#2E86C1",
            bg="#E8F6F3"
        )
        self.info_label.pack(pady=10)
        
        # Category selection frame
        category_frame = tk.Frame(content_frame, bg="#E8F6F3")
        category_frame.pack(fill="x", pady=10)
        
        tk.Label(
            category_frame,
            text="Pilih Kategori:",
            font=("Arial", 14),
            bg="#E8F6F3"
        ).pack(side=tk.LEFT, padx=10)
        
        self.selected_category = tk.StringVar()
        category_dropdown = ttk.Combobox(
            category_frame,
            textvariable=self.selected_category,
            values=list(controller.books_by_category.keys()),
            state="readonly",
            font=("Arial", 12),
            width=30
        )
        category_dropdown.pack(side=tk.LEFT, padx=10)
        
        # Book list frame with title
        book_list_frame = tk.Frame(content_frame, bg="#E8F6F3")
        book_list_frame.pack(fill="both", expand=True, pady=10)
        
        tk.Label(
            book_list_frame,
            text="Daftar Buku:",
            font=("Arial", 14),
            bg="#E8F6F3"
        ).pack(anchor="w", padx=10, pady=(0, 5))
        
        # Book list with scrollbar
        book_frame = tk.Frame(book_list_frame, bg="#E8F6F3")
        book_frame.pack(fill="both", expand=True)
        
        self.book_listbox = tk.Listbox(
            book_frame,
            font=("Arial", 12),
            width=50,
            height=15,
            selectmode=tk.SINGLE
        )
        self.book_listbox.pack(side=tk.LEFT, pady=10, padx=10)
        
        scrollbar = ttk.Scrollbar(book_frame, orient="vertical", command=self.book_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.book_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Button frame
        button_frame = tk.Frame(content_frame, bg="#E8F6F3")
        button_frame.pack(pady=20)
        
        # Borrow button
        self.borrow_button = tk.Button(
            button_frame,
            text="PINJAM BUKU",
            font=("Arial Bold", 14),
            bg="#2E86C1",
            fg="white",
            width=20,
            height=2,
            cursor="hand2",
            command=self.borrow_book,
            state=tk.DISABLED  # Disabled by default until book is selected
        )
        self.borrow_button.pack(pady=10)
        
        # Back button
        tk.Button(
            button_frame,
            text="KEMBALI KE MENU UTAMA",
            font=("Arial", 12),
            bg="#95A5A6",
            fg="white",
            width=25,
            height=2,
            cursor="hand2",
            command=lambda: controller.show_frame(HomeMenu)
        ).pack()
        
        # Bind events
        self.selected_category.trace("w", self.update_book_list)
        self.book_listbox.bind('<<ListboxSelect>>', self.on_book_select)
    
    def on_book_select(self, event):
        """Handle book selection event"""
        selection = self.book_listbox.curselection()
        if selection:
            selected_book = self.book_listbox.get(selection[0])
            if "(Tersedia)" in selected_book:
                self.borrow_button.config(state=tk.NORMAL)
                self.info_label.config(text="Klik 'PINJAM BUKU' untuk meminjam buku yang dipilih")
            else:
                self.borrow_button.config(state=tk.DISABLED)
                self.info_label.config(text="Buku ini sedang dipinjam, silakan pilih buku lain")
        else:
            self.borrow_button.config(state=tk.DISABLED)
    
    def update_book_list(self, *args):
        """Update the book list when category changes"""
        self.book_listbox.delete(0, tk.END)
        self.borrow_button.config(state=tk.DISABLED)
        self.info_label.config(text="Silakan pilih buku yang ingin dipinjam")
        
        selected = self.selected_category.get()
        if selected in self.controller.books_by_category:
            # Get all currently borrowed books
            borrowed_books = set()
            for user_books in self.controller.borrowed_books.values():
                for book_data in user_books:
                    borrowed_books.add(book_data["book"])
            
            # Update listbox with availability status
            for book in self.controller.books_by_category[selected]:
                status = " (Dipinjam)" if book in borrowed_books else " (Tersedia)"
                self.book_listbox.insert(tk.END, book + status)
    
    def borrow_book(self):
        """Handle book borrowing process"""
        if not self.controller.current_user:
            messagebox.showerror("Error", "Silakan login terlebih dahulu!")
            self.controller.show_frame(LoginFrame)
            return
        
        selection = self.book_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Silakan pilih buku terlebih dahulu!")
            return
        
        selected_item = self.book_listbox.get(selection[0])
        selected_book = selected_item.split(" (")[0]  # Remove status from book title
        
        username = self.controller.get_username_by_name(self.controller.current_user)
        
        # Check if user has reached maximum allowed books (e.g., 3 books)
        if username in self.controller.borrowed_books:
            if len(self.controller.borrowed_books[username]) >= 3:
                messagebox.showerror("Error", "Anda telah mencapai batas maksimal peminjaman (3 buku)!")
                return
        
        # Initialize borrowed books for user if not exists
        if username not in self.controller.borrowed_books:
            self.controller.borrowed_books[username] = []
        
        # Set borrow and return dates
        borrow_date = datetime.now()
        return_date = borrow_date + timedelta(days=7)
        
        # Add book to borrowed books
        self.controller.borrowed_books[username].append({
            "book": selected_book,
            "borrow_date": borrow_date,
            "return_date": return_date
        })
        
        # Show success message
        message = (
            f"Buku berhasil dipinjam!\n\n"
            f"Judul: {selected_book}\n"
            f"Tanggal Peminjaman: {borrow_date.strftime('%d-%m-%Y')}\n"
            f"Tanggal Pengembalian: {return_date.strftime('%d-%m-%Y')}\n\n"
            f"Catatan:\n"
            f"- Maksimal peminjaman 3 buku\n"
            f"- Denda keterlambatan Rp 5.000/hari"
        )
        messagebox.showinfo("Sukses", message)
        
        # Update the book list to reflect the new status
        self.update_book_list()
        self.borrow_button.config(state=tk.DISABLED)
        self.info_label.config(text="Silakan pilih buku lain yang ingin dipinjam")

class RegisterFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#FFF7E6")
        
        # Create main content frame
        content_frame = tk.Frame(self, bg="#FFF7E6")
        content_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Title and subtitle
        title_frame = tk.Frame(content_frame, bg="#FFF7E6")
        title_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="PERPUSTAKAAN PINTAR",
            font=("Arial Bold", 32),
            fg="#D35400",
            bg="#FFF7E6"
        ).pack(pady=10)
        
        tk.Label(
            title_frame,
            text="DAFTAR AKUN BARU",
            font=("Arial Bold", 24),
            fg="#2E86C1",
            bg="#FFF7E6"
        ).pack()
        
        # Form frame
        form_frame = tk.Frame(content_frame, bg="#FFF7E6")
        form_frame.pack(expand=True, pady=20)
        
        # Form fields
        labels = ["NAMA LENGKAP", "USERNAME", "PASSWORD"]
        entries = []
        
        for i, text in enumerate(labels):
            tk.Label(
                form_frame,
                text=text,
                font=("Arial", 14),
                fg="#E74C3C",
                bg="#FFF7E6"
            ).pack(anchor="w", pady=(10, 5))
            
            entry = tk.Entry(
                form_frame,
                font=("Arial", 12),
                width=50
            )
            if text == "PASSWORD":
                entry.configure(show="*")
            entry.pack(pady=(0, 10), ipady=5)
            entries.append(entry)
        
        self.name_entry, self.username_entry, self.password_entry = entries
        
        # Buttons frame
        button_frame = tk.Frame(form_frame, bg="#FFF7E6")
        button_frame.pack(pady=20)
        
        tk.Button(
            button_frame,
            text="DAFTAR",
            font=("Arial Bold", 14),
            bg="#2E86C1",
            fg="white",
            width=20,
            height=1,
            cursor="hand2",
            command=self.register
        ).pack(pady=(0, 10))
        
        tk.Button(
            button_frame,
            text="SUDAH PUNYA AKUN? MASUK",
            font=("Arial", 12),
            bg="#95A5A6",
            fg="white",
            width=28,
            height=2,
            cursor="hand2",
            command=lambda: controller.show_frame(LoginFrame)
        ).pack()
    
    def register(self):
        name = self.name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not all([name, username, password]):
            messagebox.showerror("Error", "Semua field harus diisi!")
            return
            
        if len(username) < 4:
            messagebox.showerror("Error", "Username minimal 4 karakter!")
            return
            
        if len(password) < 6:
            messagebox.showerror("Error", "Password minimal 6 karakter!")
            return
            
        if username in self.controller.users:
            messagebox.showerror("Error", "Username sudah terdaftar!")
            return
        
        self.controller.add_user(username, password, name)
        messagebox.showinfo("Sukses", "Pendaftaran berhasil!")
        self.clear_form()
        self.controller.show_frame(LoginFrame)
    
    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#FFF7E6")
        
        # Create main content frame
        content_frame = tk.Frame(self, bg="#FFF7E6")
        content_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Title and subtitle
        title_frame = tk.Frame(content_frame, bg="#FFF7E6")
        title_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="PERPUSTAKAAN PINTAR",
            font=("Arial Bold", 32),
            fg="#D35400",
            bg="#FFF7E6"
        ).pack(pady=10)
        
        tk.Label(
            title_frame,
            text="MASUK",
            font=("Arial Bold", 24),
            fg="#2E86C1",
            bg="#FFF7E6"
        ).pack()
        
        # Form frame
        form_frame = tk.Frame(content_frame, bg="#FFF7E6")
        form_frame.pack(expand=True, pady=20)
        
        # Username field
        tk.Label(
            form_frame,
            text="USERNAME",
            font=("Arial", 14),
            fg="#E74C3C",
            bg="#FFF7E6"
        ).pack(anchor="w", pady=(10, 5))
        
        self.username_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            width=50
        )
        self.username_entry.pack(pady=(0, 10), ipady=5)
        
        # Password field with show/hide toggle
        tk.Label(
            form_frame,
            text="PASSWORD",
            font=("Arial", 14),
            fg="#E74C3C",
            bg="#FFF7E6"
        ).pack(anchor="w", pady=(10, 5))
        
        # Create a frame for password entry and toggle button
        password_frame = tk.Frame(form_frame, bg="#FFF7E6")
        password_frame.pack(fill="x", pady=(0, 10))
        
        self.password_entry = tk.Entry(
            password_frame,
            font=("Arial", 12),
            width=47,
            show="*"
        )
        self.password_entry.pack(side=tk.LEFT, ipady=5)
        
        # Add toggle password visibility button
        self.show_password = tk.BooleanVar()
        self.show_password.set(False)
        
        self.toggle_btn = tk.Button(
            password_frame,
            text="👁️",
            font=("Arial", 12),
            bg="#95A5A6",
            fg="white",
            width=3,
            cursor="hand2",
            command=self.toggle_password_visibility
        )
        self.toggle_btn.pack(side=tk.LEFT, padx=(5, 0), ipady=4)
        
        # Buttons frame
        button_frame = tk.Frame(form_frame, bg="#FFF7E6")
        button_frame.pack(pady=20)
        
        tk.Button(
            button_frame,
            text="MASUK",
            font=("Arial Bold", 14),
            bg="#2E86C1",
            fg="white",
            width=20,
            height=1,
            cursor="hand2",
            command=self.login
        ).pack(pady=(0, 10))
        
        tk.Button(
            button_frame,
            text="BELUM PUNYA AKUN? DAFTAR",
            font=("Arial", 12),
            bg="#95A5A6",
            fg="white",
            width=28,
            height=2,
            cursor="hand2",
            command=lambda: controller.show_frame(RegisterFrame)
        ).pack()
    
    def toggle_password_visibility(self):
        """Toggle password visibility between show and hide"""
        if self.password_entry.cget('show') == '*':
            self.password_entry.configure(show='')
            self.toggle_btn.configure(bg="#2E86C1")  # Highlight button when password is visible
        else:
            self.password_entry.configure(show='*')
            self.toggle_btn.configure(bg="#95A5A6")  # Return to normal color when password is hidden
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not all([username, password]):
            messagebox.showerror("Error", "Semua field harus diisi!")
            return
        
        if self.controller.check_user(username, password):
            self.controller.current_user = self.controller.users[username]['name']
            messagebox.showinfo("Sukses", f"Selamat datang, {self.controller.users[username]['name']}!")
            self.clear_form()
            self.controller.frames[HomeMenu].update_welcome_message()
            self.controller.show_frame(HomeMenu)
        else:
            messagebox.showerror("Error", "Username atau password salah!")
    
    def clear_form(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        # Reset password visibility to hidden when clearing form
        self.password_entry.configure(show='*')
        self.toggle_btn.configure(bg="#95A5A6")

class BookCategoryFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#E8F6F3")
        
        # Create main content frame
        content_frame = tk.Frame(self, bg="#E8F6F3")
        content_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Title
        tk.Label(
            content_frame,
            text="DAFTAR BUKU BERDASARKAN KATEGORI",
            font=("Arial Bold", 24),
            fg="#2E86C1",
            bg="#E8F6F3"
        ).pack(pady=20)
        
        # Category selection frame
        category_frame = tk.Frame(content_frame, bg="#E8F6F3")
        category_frame.pack(fill="x", pady=10)
        
        tk.Label(
            category_frame,
            text="Pilih Kategori:",
            font=("Arial", 14),
            bg="#E8F6F3"
        ).pack(side=tk.LEFT, padx=10)
        
        self.selected_category = tk.StringVar()
        category_dropdown = ttk.Combobox(
            category_frame,
            textvariable=self.selected_category,
            values=list(controller.books_by_category.keys()),
            state="readonly",
            font=("Arial", 12),
            width=30
        )
        category_dropdown.pack(side=tk.LEFT, padx=10)
        
        # Book list
        self.book_listbox = tk.Listbox(
            content_frame,
            font=("Arial", 12),
            width=50,
            height=15,
            selectmode=tk.SINGLE
        )
        self.book_listbox.pack(pady=20)
        
        # Back button
        tk.Button(
            content_frame,
            text="KEMBALI KE MENU UTAMA",
            font=("Arial", 12),
            bg="#95A5A6",
            fg="white",
            width=25,
            height=2,
            cursor="hand2",
            command=lambda: controller.show_frame(HomeMenu)
        ).pack(pady=20)
        
        # Bind category selection to update book list
        self.selected_category.trace('w', self.update_book_list)
    
    def update_book_list(self, *args):
        self.book_listbox.delete(0, tk.END)  # Hapus semua item dalam listbox
        selected = self.selected_category.get()  # Ambil kategori yang dipilih
        
        # Periksa apakah kategori ada dalam dictionary buku
        if selected in self.controller.books_by_category:
            # Dapatkan daftar buku untuk kategori yang dipilih
            books_in_category = self.controller.books_by_category[selected]
            borrowed_books = {
                book['book'] for user_books in self.controller.borrowed_books.values()
                for book in user_books
            }
            
            for book in books_in_category:
                # Tentukan status ketersediaan
                status = " (Dipinjam)" if book in borrowed_books else " (Tersedia)"
                self.book_listbox.insert(tk.END, book + status)
                

class KonfirmasiPeminjamanDialog(tk.Toplevel):
    def __init__(self, parent, book_title, borrow_date, return_date):
        super().__init__(parent)
        self.title("Konfirmasi Peminjaman")
        self.result = False
        self.controller = parent.controller
        
        # Window settings
        self.configure(bg="#E8F6F3")
        self.resizable(False, False)
        
        # Center the dialog
        window_width = 400
        window_height = 350
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Create main frame
        main_frame = tk.Frame(self, bg="#E8F6F3", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")
        
        # Title
        tk.Label(
            main_frame,
            text="Konfirmasi Peminjaman Buku",
            font=("Arial Bold", 16),
            fg="#2E86C1",
            bg="#E8F6F3"
        ).pack(pady=(0, 20))
        
        # Book details
        details_frame = tk.Frame(main_frame, bg="#E8F6F3")
        details_frame.pack(fill="x", pady=10)
        
        # Book information
        info_text = f"""
Judul Buku: {book_title}

Tanggal Peminjaman: {borrow_date.strftime('%d-%m-%Y')}
Tanggal Pengembalian: {return_date.strftime('%d-%m-%Y')}

Ketentuan:
- Maksimal peminjaman 7 hari
- Denda keterlambatan Rp 5.000/hari
- Maksimal peminjaman 3 buku per anggota
"""
        
        tk.Label(
            details_frame,
            text=info_text,
            font=("Arial", 12),
            justify=tk.LEFT,
            bg="#E8F6F3"
        ).pack(pady=10)
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg="#E8F6F3")
        button_frame.pack(pady=20)
        
        # Confirm button
        self.confirm_button = tk.Button(
            button_frame,
            text="KONFIRMASI",
            font=("Arial Bold", 12),
            bg="#2ECC71",
            fg="white",
            width=20,
            height=1,
            cursor="hand2",
            command=self.konfirmasi_dan_lanjutkan
        )
        self.confirm_button.pack(pady=(0, 10))
        
        # Back to main menu button
        self.menu_button = tk.Button(
            button_frame,
            text="KEMBALI KE MENU",
            font=("Arial", 12),
            bg="#3498DB",
            fg="white",
            width=20,
            height=1,
            cursor="hand2",
            command=self.kembali_ke_menu
        )
        self.menu_button.pack(pady=(0, 10))
        
        # Cancel button
        self.cancel_button = tk.Button(
            button_frame,
            text="BATAL",
            font=("Arial", 12),
            bg="#95A5A6",
            fg="white",
            width=20,
            height=1,
            cursor="hand2",
            command=self.batal
        )
        self.cancel_button.pack()
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)
    
    def konfirmasi_dan_lanjutkan(self):
        """Konfirmasi peminjaman dan lanjut ke menu utama"""
        self.result = True
        messagebox.showinfo("Konfirmasi", "Peminjaman buku telah dikonfirmasi!")
        self.destroy()
        self.controller.show_frame(HomeMenu)
    
    def kembali_ke_menu(self):
        """Batalkan peminjaman dan kembali ke menu utama"""
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin kembali ke menu utama?\nPeminjaman buku akan dibatalkan."):
            self.result = False
            self.destroy()
            self.controller.show_frame(HomeMenu)
    
    def batal(self):
        """Batalkan dialog peminjaman"""
        self.result = False
        self.destroy()

def pinjam_buku(self):
    if not self.controller.current_user:
        messagebox.showerror("Error", "Silakan login terlebih dahulu!")
        self.controller.show_frame(LoginFrame)
        return
        
    selection = self.book_listbox.curselection()
    if not selection:
        messagebox.showerror("Error", "Silakan pilih buku terlebih dahulu!")
        return
    
    selected_book = self.book_listbox.get(selection[0]).split(" (")[0]
    username = self.controller.get_username_by_name(self.controller.current_user)
    
    # Check maximum books limit
    if username in self.controller.borrowed_books:
        if len(self.controller.borrowed_books[username]) >= 3:
            messagebox.showerror("Error", "Anda telah mencapai batas maksimal peminjaman (3 buku)!")
            return
    
    borrow_date = datetime.now()
    return_date = borrow_date + timedelta(days=7)
    
    # Show confirmation dialog
    dialog = KonfirmasiPeminjamanDialog(
        self,
        selected_book,
        borrow_date,
        return_date
    )
    
    if dialog.result:
        if username not in self.controller.borrowed_books:
            self.controller.borrowed_books[username] = []
        
        self.controller.borrowed_books[username].append({
            "book": selected_book,
            "borrow_date": borrow_date,
            "return_date": return_date
        })
        
        self.update_book_list()
        self.borrow_button.config(state=tk.DISABLED)
        self.info_label.config(text="Silakan pilih buku lain yang ingin dipinjam")

class BookReturnFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#E8F6F3")
        
        # Create main content frame
        content_frame = tk.Frame(self, bg="#E8F6F3")
        content_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Title
        tk.Label(
            content_frame,
            text="PENGEMBALIAN BUKU",
            font=("Arial Bold", 24),
            fg="#FF6B6B",
            bg="#E8F6F3"
        ).pack(pady=(0, 20))
        
        tk.Label(
            content_frame,
            text="Terimakasih telah mengembalikan buku nya kembali",
            font=("Arial", 14),
            fg="#2E86C1",
            bg="#E8F6F3"
        ).pack(pady=(0, 30))
        
        # Borrowed books frame
        book_frame = tk.Frame(content_frame, bg="#E8F6F3")
        book_frame.pack(fill="both", expand=True, pady=10)
        
        tk.Label(
            book_frame,
            text="Daftar buku yang dipinjam:",
            font=("Arial Bold", 14),
            fg="#2E86C1",
            bg="#E8F6F3"
        ).pack(anchor="w", padx=10, pady=(0, 10))
        
        # Book list
        self.book_listbox = tk.Listbox(
            book_frame,
            font=("Arial", 12),
            width=50,
            height=8,
            selectmode=tk.SINGLE
        )
        self.book_listbox.pack(side=tk.LEFT, pady=10, padx=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(book_frame, orient="vertical", command=self.book_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.book_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Return details frame
        details_frame = tk.Frame(content_frame, bg="#E8F6F3")
        details_frame.pack(fill="x", pady=20)
        
        # Book details
        labels = ["Tanggal Peminjaman:", "Tanggal Pengembalian:", "Denda:"]
        self.detail_labels = {}
        
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
            self.detail_labels[label] = value_label
        
        # Buttons frame
        button_frame = tk.Frame(content_frame, bg="#E8F6F3")
        button_frame.pack(pady=20)
        
        tk.Button(
            button_frame,
            text="KONFIRMASI PENGEMBALIAN",
            font=("Arial Bold", 14),
            bg="#2E86C1",
            fg="white",
            width=25,
            height=2,
            cursor="hand2",
            command=self.return_book
        ).pack(pady=10)
        
        tk.Button(
            button_frame,
            text="KEMBALI KE MENU UTAMA",
            font=("Arial", 12),
            bg="#95A5A6",
            fg="white",
            width=25,
            height=2,
            cursor="hand2",
            command=lambda: controller.show_frame(HomeMenu)
        ).pack()
        
        # Bind selection event
        self.book_listbox.bind('<<ListboxSelect>>', self.update_book_details)
    
    def update_borrowed_books_list(self):
        self.book_listbox.delete(0, tk.END)
        username = self.controller.get_username_by_name(self.controller.current_user)
        if username in self.controller.borrowed_books:
            for book_data in self.controller.borrowed_books[username]:
                self.book_listbox.insert(tk.END, book_data['book'])
    
    def calculate_fine(self, borrow_date, return_date):
        actual_return = datetime.now()
        if actual_return > return_date:
            days_late = (actual_return - return_date).days
            return days_late * 5000  # Rp 5.000 per day
        return 0
    
    def update_book_details(self, event):
        selection = self.book_listbox.curselection()
        if not selection:
            return
            
        username = self.controller.get_username_by_name(self.controller.current_user)
        selected_book = self.book_listbox.get(selection[0])
        
        # Find book data
        book_data = None
        for book in self.controller.borrowed_books[username]:
            if book['book'] == selected_book:
                book_data = book
                break
        
        if book_data:
            self.detail_labels["Tanggal Peminjaman:"].config(
                text=book_data['borrow_date'].strftime('%d-%m-%Y')
            )
            self.detail_labels["Tanggal Pengembalian:"].config(
                text=book_data['return_date'].strftime('%d-%m-%Y')
            )
            
            fine = self.calculate_fine(book_data['borrow_date'], book_data['return_date'])
            self.detail_labels["Denda:"].config(
                text=f"Rp {fine:,}" if fine > 0 else "Rp 0"
            )
    
    def return_book(self):
        selection = self.book_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Silakan pilih buku yang akan dikembalikan!")
            return
        
        username = self.controller.get_username_by_name(self.controller.current_user)
        selected_book = self.book_listbox.get(selection[0])
        
        # Remove book from borrowed books
        self.controller.borrowed_books[username] = [
            book for book in self.controller.borrowed_books[username]
            if book['book'] != selected_book
        ]
        
        messagebox.showinfo("Sukses", "Buku berhasil dikembalikan!")
        self.update_borrowed_books_list()
        
        # Reset detail labels
        for label in self.detail_labels.values():
            label.config(text="-")

class HomeMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#E8F6F3')
        
        # Create main content frame
        content_frame = tk.Frame(self, bg='#E8F6F3')
        content_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Welcome frame
        welcome_frame = tk.Frame(content_frame, bg='#E8F6F3')
        welcome_frame.pack(fill="x", pady=(0, 30))
        
        tk.Label(
            welcome_frame,
            text="Selamat Datang,",
            font=("Helvetica", 32, "bold"),
            bg='#E8F6F3',
            fg='#FF6B6B'
        ).pack()
        
        self.user_label = tk.Label(
            welcome_frame,
            text="",
            font=("Helvetica", 24),
            bg='#E8F6F3',
            fg='#2E86C1'
        )
        self.user_label.pack(pady=(10, 0))
        
        # Menu buttons frame
        menu_frame = tk.Frame(content_frame, bg='#E8F6F3')
        menu_frame.pack(expand=True)
        
        buttons = [
            ("Lihat Buku Berdasarkan Kategori", lambda: controller.show_frame(BookCategoryFrame), "#2E86C1"),
            ("Pinjam Buku", lambda: controller.show_frame(BorrowBookFrame), "#2E86C1"),
            ("Kembalikan Buku", self.kembalikan_buku, "#2E86C1"),
            ("Keluar", self.konfirmasi_keluar, "#95A5A6")
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                menu_frame,
                text=text,
                font=('Helvetica', 14),
                bg='white',
                fg=color,
                width=30,
                height=2,
                relief='solid',
                bd=1,
                cursor="hand2",
                command=command
            )
            btn.pack(pady=10)
            self.add_hover_effect(btn)

    def update_welcome_message(self):
        if self.controller.current_user:
            self.user_label.config(text=self.controller.current_user)

    def add_hover_effect(self, button):
        button.bind('<Enter>', lambda e: button.configure(bg='#F0F0F0'))
        button.bind('<Leave>', lambda e: button.configure(bg='white'))

    def kembalikan_buku(self):
        username = self.controller.get_username_by_name(self.controller.current_user)
        if username not in self.controller.borrowed_books or not self.controller.borrowed_books[username]:
            messagebox.showinfo("Info", "Anda tidak memiliki buku yang dipinjam")
            return
        
        self.controller.frames[BookReturnFrame].update_borrowed_books_list()
        self.controller.show_frame(BookReturnFrame)

    def konfirmasi_keluar(self):
        if messagebox.askyesno("Konfirmasi Keluar", "Apakah Anda yakin ingin keluar?"):
            self.controller.current_user = None
            self.user_label.config(text="")
            self.controller.show_frame(LoginFrame)

if __name__ == "__main__":
    root = tk.Tk()
    app = PerpustakaanPintar(root)
    root.mainloop()