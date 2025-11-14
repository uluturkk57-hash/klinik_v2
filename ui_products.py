import tkinter as tk
from tkinter import ttk
import db_core


class ProductsPage:
    def __init__(self, parent, conn):
        self.conn = conn
        self.frame = ttk.Frame(parent)

        # --- ÜST BAŞLIK ---
        title = ttk.Label(self.frame, text="Ürün Yönetimi", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # --- ANA ALAN ---
        content = ttk.Frame(self.frame)
        content.pack(fill="both", expand=True)

        # Sol: Ürün formu
        self.left = ttk.LabelFrame(content, text="Ürün Ekle / Güncelle")
        self.left.pack(side="left", fill="y", padx=10, pady=10)

        # Sağ: Ürün tablosu
        self.right = ttk.LabelFrame(content, text="Ürün Listesi")
        self.right.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # -------------------
        # FORM ALANLARINI OLUŞTUR
        # -------------------
        ttk.Label(self.left, text="Ürün Adı:").pack(anchor="w", pady=2)
        self.entry_name = ttk.Entry(self.left, width=30)
        self.entry_name.pack(anchor="w", pady=2)

        ttk.Label(self.left, text="Alış Fiyatı (₺):").pack(anchor="w", pady=2)
        self.entry_buy = ttk.Entry(self.left, width=15)
        self.entry_buy.pack(anchor="w", pady=2)

        ttk.Label(self.left, text="Satış Fiyatı (₺):").pack(anchor="w", pady=2)
        self.entry_sell = ttk.Entry(self.left, width=15)
        self.entry_sell.pack(anchor="w", pady=2)

        ttk.Label(self.left, text="Stok Adedi:").pack(anchor="w", pady=2)
        self.entry_stock = ttk.Entry(self.left, width=10)
        self.entry_stock.pack(anchor="w", pady=2)

        ttk.Label(self.left, text="Kategori:").pack(anchor="w", pady=2)
        self.entry_cat = ttk.Entry(self.left, width=20)
        self.entry_cat.pack(anchor="w", pady=2)

        # -------------------
        # Hedef Kar %
        # -------------------
        ttk.Label(self.left, text="Hedef Kâr %:").pack(anchor="w", pady=2)
        self.entry_target = ttk.Entry(self.left, width=10)
        self.entry_target.pack(anchor="w", pady=2)

        # Canlı Hesaplama Sonucu
        self.label_calc = ttk.Label(self.left, text="Önerilen Satış: -", foreground="blue")
        self.label_calc.pack(anchor="w", pady=5)

        # "Uygula" butonu – satış fiyatına yazar
        self.btn_apply = ttk.Button(
            self.left, text="Uygula", command=self.apply_target_price
        )
        self.btn_apply.pack(anchor="w", pady=5)

        # KAYDET Butonu
        self.btn_save = ttk.Button(self.left, text="Kaydet", command=self.save_product)
        self.btn_save.pack(anchor="w", pady=10)

        # -------------------
        # TABLO OLUŞTUR
        # -------------------
        columns = ("id", "name", "buy", "sell", "stock", "cat")
        self.table = ttk.Treeview(self.right, columns=columns, show="headings")

        self.table.heading("id", text="ID")
        self.table.heading("name", text="Ürün Adı")
        self.table.heading("buy", text="Alış ₺")
        self.table.heading("sell", text="Satış ₺")
        self.table.heading("stock", text="Stok")
        self.table.heading("cat", text="Kategori")

        self.table.pack(fill="both", expand=True)

        # İlk liste
        self.refresh_table()

    # -------------------------------------
    # HEDEF KAR % → ÖNERİLEN FİYAT HESABI
    # -------------------------------------
    def apply_target_price(self):
        try:
            buy = float(self.entry_buy.get())
            target = float(self.entry_target.get())

            suggested = buy + (buy * target / 100)

            # Etikette göster
            self.label_calc.config(text=f"Önerilen Satış: {suggested:.2f} ₺")

            # Satış fiyatı kutusuna yaz
            self.entry_sell.delete(0, tk.END)
            self.entry_sell.insert(0, f"{suggested:.2f}")

        except:
            self.label_calc.config(text="Hata: değerleri kontrol et!")

    # -------------------------------------
    # ÜRÜN KAYIT
    # -------------------------------------
    def save_product(self):
        try:
            name = self.entry_name.get()
            buy = float(self.entry_buy.get())
            sell = float(self.entry_sell.get())
            stock = int(self.entry_stock.get())
            cat = self.entry_cat.get()

            db_core.add_product(self.conn, name, buy, sell, stock, cat)

            self.refresh_table()

        except Exception as e:
            print("Kayıt Hatası:", e)

    # -------------------------------------
    # TABLO YENİLEME
    # -------------------------------------
    def refresh_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM products ORDER BY id DESC")
        rows = cursor.fetchall()

        for r in rows:
            self.table.insert("", "end", values=(
                r["id"], r["name"], r["buy_price"], r["sell_price"], r["stock"], r["category"]
            ))     # -------------------------------------
    # FORM SIFIRLAMA
    # -------------------------------------
    def clear_form(self):
        self.entry_name.delete(0, tk.END)
        self.entry_buy.delete(0, tk.END)
        self.entry_sell.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        self.entry_cat.delete(0, tk.END)
        self.entry_target.delete(0, tk.END)
        self.label_calc.config(text="Önerilen Satış: -")

    # -------------------------------------
    # TABLODAN ÜRÜN SEÇME
    # -------------------------------------
    def on_select_product(self, event):
        try:
            selected = self.table.selection()
            if not selected:
                return

            values = self.table.item(selected[0], "values")
            prod_id, name, buy, sell, stock, cat = values

            self.selected_id = prod_id

            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, name)

            self.entry_buy.delete(0, tk.END)
            self.entry_buy.insert(0, buy)

            self.entry_sell.delete(0, tk.END)
            self.entry_sell.insert(0, sell)

            self.entry_stock.delete(0, tk.END)
            self.entry_stock.insert(0, stock)

            self.entry_cat.delete(0, tk.END)
            self.entry_cat.insert(0, cat)

        except Exception as e:
            print("Seçim hatası:", e)

    # -------------------------------------
    # ÜRÜN GÜNCELLE
    # -------------------------------------
    def update_product(self):
        try:
            prod_id = self.selected_id
            name = self.entry_name.get()
            buy = float(self.entry_buy.get())
            sell = float(self.entry_sell.get())
            stock = int(self.entry_stock.get())
            cat = self.entry_cat.get()

            c = self.conn.cursor()
            c.execute("""
            UPDATE products
            SET name=?, buy_price=?, sell_price=?, stock=?, category=?
            WHERE id=?
            """, (name, buy, sell, stock, cat, prod_id))
            self.conn.commit()

            self.refresh_table()

        except Exception as e:
            print("Güncelleme hatası:", e)

    # -------------------------------------
    # STOK ARTIRMA
    # -------------------------------------
    def add_stock(self):
        try:
            prod_id = self.selected_id
            qty = int(self.entry_stock_change.get())
            db_core.update_stock(self.conn, prod_id, qty)
            self.refresh_table()
        except:
            pass

    # -------------------------------------
    # STOK AZALTMA
    # -------------------------------------
    def remove_stock(self):
        try:
            prod_id = self.selected_id
            qty = int(self.entry_stock_change.get())
            db_core.update_stock(self.conn, prod_id, -qty)
            self.refresh_table()
        except:
            pass

    # -------------------------------------
    # ARAMA FİLTRESİ
    # -------------------------------------
    def search_products(self, *args):
        query = self.entry_search.get().lower()

        for row in self.table.get_children():
            self.table.delete(row)

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()

        for r in rows:
            if query in r["name"].lower():
                self.table.insert("", "end", values=(
                    r["id"], r["name"], r["buy_price"], r["sell_price"],
                    r["stock"], r["category"]
                ))

