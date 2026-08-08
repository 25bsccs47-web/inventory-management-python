import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

CSV_FILE = 'inventory.csv'

def load_items():
    items = []
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'quantity', 'price'])
        return items
    with open(CSV_FILE, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                items.append({
                    'id': int(row['id']),
                    'name': row['name'],
                    'quantity': int(row['quantity']),
                    'price': float(row['price'])
                })
            except Exception:
                continue
    return items

def save_items(items):
    with open(CSV_FILE, 'w', newline='') as f:
        fieldnames = ['id', 'name', 'quantity', 'price']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for it in items:
            writer.writerow({'id': it['id'], 'name': it['name'], 'quantity': it['quantity'], 'price': it['price']})

def next_id(items):
    if not items:
        return 1
    return max(i['id'] for i in items) + 1

class InventoryApp:
    def __init__(self, root):
        self.root = root
        root.title("Inventory Management")
        self.items = load_items()

        frame = ttk.Frame(root, padding=10)
        frame.pack(fill='both', expand=True)

        self.tree = ttk.Treeview(frame, columns=('Name','Qty','Price'), show='headings', selectmode='browse')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Qty', text='Quantity')
        self.tree.heading('Price', text='Price')
        self.tree.column('Name', width=200)
        self.tree.column('Qty', width=80, anchor='center')
        self.tree.column('Price', width=100, anchor='e')
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.tree.pack(fill='both', expand=True)

        form = ttk.Frame(frame, padding=(0,10))
        form.pack(fill='x')
        ttk.Label(form, text="Name").grid(row=0,column=0,sticky='w')
        self.name_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.name_var).grid(row=0,column=1,sticky='ew')
        ttk.Label(form, text="Quantity").grid(row=1,column=0,sticky='w')
        self.qty_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.qty_var).grid(row=1,column=1,sticky='ew')
        ttk.Label(form, text="Price").grid(row=2,column=0,sticky='w')
        self.price_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.price_var).grid(row=2,column=1,sticky='ew')
        form.columnconfigure(1, weight=1)

        btns = ttk.Frame(frame)
        btns.pack(fill='x')
        ttk.Button(btns, text="Add Item", command=self.add_item).pack(side='left', padx=5)
        ttk.Button(btns, text="Update Item", command=self.update_item).pack(side='left', padx=5)
        ttk.Button(btns, text="Delete Item", command=self.delete_item).pack(side='left', padx=5)
        ttk.Button(btns, text="Refresh", command=self.refresh).pack(side='left', padx=5)

        self.status = ttk.Label(frame, text="")
        self.status.pack(fill='x', pady=(8,0))

        self.refresh()

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.items = load_items()
        for it in self.items:
            status = "LOW" if it['quantity'] < 10 else "OK"
            self.tree.insert('', 'end', iid=str(it['id']), values=(it['name'], it['quantity'], f"{it['price']:.2f}"))
        self.status.config(text=f"Loaded {len(self.items)} items.")

    def add_item(self):
        name = self.name_var.get().strip()
        try:
            qty = int(self.qty_var.get())
            price = float(self.price_var.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Quantity must be integer and price must be a number.")
            return
        if not name:
            messagebox.showerror("Invalid input", "Name cannot be empty.")
            return
        item = {'id': next_id(self.items), 'name': name, 'quantity': qty, 'price': price}
        self.items.append(item)
        save_items(self.items)
        self.refresh()
        self.name_var.set(''); self.qty_var.set(''); self.price_var.set('')
        self.status.config(text=f"✅ {name} added.")

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        item = next((it for it in self.items if str(it['id'])==iid), None)
        if item:
            self.name_var.set(item['name'])
            self.qty_var.set(str(item['quantity']))
            self.price_var.set(str(item['price']))

    def update_item(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select item", "Please select an item to update.")
            return
        iid = sel[0]
        try:
            qty = int(self.qty_var.get())
            price = float(self.price_var.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Quantity must be integer and price must be a number.")
            return
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Invalid input", "Name cannot be empty.")
            return
        for it in self.items:
            if str(it['id'])==iid:
                it['name']=name; it['quantity']=qty; it['price']=price
                break
        save_items(self.items)
        self.refresh()
        self.status.config(text="✅ Item updated.")

    def delete_item(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select item", "Please select an item to delete.")
            return
        iid = sel[0]
        confirm = messagebox.askyesno("Confirm", "Delete selected item?")
        if not confirm: return
        self.items = [it for it in self.items if str(it['id'])!=iid]
        save_items(self.items)
        self.refresh()
        self.name_var.set(''); self.qty_var.set(''); self.price_var.set('')
        self.status.config(text="✅ Item deleted.")

def main():
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()