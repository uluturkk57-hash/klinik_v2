import tkinter as tk
from tkinter import ttk

# Modüller (bunlar dosyaları oluşturunca çalışacak)
import db_core
import ui_products
import ui_sales
import ui_customers
import ui_treatments
import ui_reports

class KlinikApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Klinik Yönetim Sistemi v2")
        self.root.geometry("1200x700")

        # Veritabanı bağlantısı
        self.conn = db_core.get_connection()
        db_core.init_db(self.conn)

        # ----- Üst Menü -----
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Çıkış", command=self.on_close)
        menubar.add_cascade(label="Dosya", menu=file_menu)

        # ----- Sekme Sistemi -----
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # ----- Sayfaları Yükle -----
        self.page_products = ui_products.ProductsPage(self.notebook, self.conn)
        self.notebook.add(self.page_products.frame, text="Ürün / Stok")

        self.page_sales = ui_sales.SalesPage(self.no
