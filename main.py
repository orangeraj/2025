import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from tkinter import ttk, messagebox
from tkinter import *
from datetime import datetime
import os

class TiffinServiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tiffin Service Management System")
        self.root.geometry("1000x600")  # Standardized main window size
        
        # File path for storing order history
        self.history_file = "order_history.xlsx"
        
        # Static menu items list instead of Excel
        self.menu_items = [
            {"Item Name": "Dal Rice", "Price": 120},
            {"Item Name": "Veg Thali", "Price": 150},
            {"Item Name": "Roti Sabzi", "Price": 100},
            {"Item Name": "Paneer Special", "Price": 180},
            {"Item Name": "South Indian Thali", "Price": 200}
        ]
        
        # Initialize order items and load order history
        self.order_items = []
        self.order_history = self.load_order_history()
        
        # Create main menu
        self.create_menu()
        
        # Create main frames
        self.create_main_frames()
        
    def load_order_history(self):
        try:
            orders = []
            # Get all order history files
            files = [f for f in os.listdir() if f.startswith('order_history_') and f.endswith('.xlsx')]
            
            for file in files:
                if os.path.exists(file):
                    df = pd.read_excel(file)
                    for _, row in df.iterrows():
                        order = {
                            'date': row['Date'],
                            'items': eval(row['Items']),
                            'total': row['Total']
                        }
                        orders.append(order)
            return orders
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading order history: {str(e)}")
        return []
    
    def save_order_history(self):
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            filename = f"order_history_{today}.xlsx"
            
            # Load existing data for today if file exists
            existing_data = []
            if os.path.exists(filename):
                try:
                    df_existing = pd.read_excel(filename)
                    for _, row in df_existing.iterrows():
                        existing_data.append({
                            'Date': row['Date'],
                            'Items': row['Items'],
                            'Total': row['Total']
                        })
                except Exception:
                    pass

            # Add new orders from today
            data = existing_data
            for order in self.order_history:
                if order['date'].split()[0] == today:  # Only add today's orders
                    data.append({
                        'Date': order['date'],
                        'Items': str(order['items']),
                        'Total': order['total']
                    })

            # Save to Excel with proper formatting
            df = pd.DataFrame(data)
            if not df.empty:
                writer = pd.ExcelWriter(filename, engine='openpyxl')
                df.to_excel(writer, index=False, sheet_name='Orders')
                
                # Auto-adjust columns width
                worksheet = writer.sheets['Orders']
                for idx, col in enumerate(df.columns):
                    max_length = max(
                        df[col].astype(str).apply(len).max(),
                        len(col)
                    )
                    worksheet.column_dimensions[chr(65 + idx)].width = max_length + 2
                
                writer.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error saving order history: {str(e)}")

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Management Menu
        manage_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Management", menu=manage_menu)
        manage_menu.add_command(label="Customers", command=self.show_customers)
        manage_menu.add_command(label="Menu Items", command=self.show_menu)
        manage_menu.add_command(label="Orders", command=self.show_orders)
        
    def create_main_frames(self):
        # Welcome Frame
        self.welcome_frame = ttk.Frame(self.root, padding="10")
        self.welcome_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(self.welcome_frame, 
                 text="Welcome to Tiffin Service Management System",
                 font=('Helvetica', 16, 'bold')).grid(row=0, column=0, pady=20)
        
        # Style configuration for bigger buttons
        style = ttk.Style()
        style.configure('Big.TButton', font=('Helvetica', 12), padding=10)
        
        # Quick Actions Buttons
        ttk.Button(self.welcome_frame, 
                  text="New Order",
                  style='Big.TButton',
                  width=30,
                  command=self.new_order).grid(row=1, column=0, pady=15)
        
        ttk.Button(self.welcome_frame,
                  text="View Orders",
                  style='Big.TButton',
                  width=30,
                  command=self.show_orders).grid(row=2, column=0, pady=15)
        
        ttk.Button(self.welcome_frame,
                  text="Manage Customers",
                  style='Big.TButton',
                  width=30,
                  command=self.show_customers).grid(row=3, column=0, pady=15)
    
    def new_order(self):
        # Create new window for order
        order_window = Toplevel(self.root)
        order_window.title("New Order")
        order_window.geometry("1000x600")

        # Create frames
        item_frame = ttk.Frame(order_window, padding="10")
        item_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10)
        
        cart_frame = ttk.Frame(order_window, padding="10")
        cart_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10)

        # Menu Items List
        ttk.Label(item_frame, text="Menu Items", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, pady=5)
        
        # Create Treeview for menu items
        menu_tree = ttk.Treeview(item_frame, columns=('Item', 'Price'), show='headings', height=15)
        menu_tree.heading('Item', text='Item')
        menu_tree.heading('Price', text='Price')
        menu_tree.column('Item', width=200)  # Set column width
        menu_tree.column('Price', width=100)  # Set column width
        menu_tree.grid(row=1, column=0, pady=5)

        # Populate menu items
        for item in self.menu_items:
            menu_tree.insert('', 'end', values=(item['Item Name'], f"₹{item['Price']}"))

        # Cart List
        ttk.Label(cart_frame, text="Selected Items", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, pady=5)
        
        cart_tree = ttk.Treeview(cart_frame, columns=('Item', 'Price'), show='headings', height=10)
        cart_tree.heading('Item', text='Item')
        cart_tree.heading('Price', text='Price')
        cart_tree.column('Item', width=200)  # Set column width
        cart_tree.column('Price', width=100)  # Set column width
        cart_tree.grid(row=1, column=0, pady=5)

        # Total Price Label
        total_price = StringVar(value="Total: ₹0.00")
        ttk.Label(cart_frame, textvariable=total_price, font=('Helvetica', 12, 'bold')).grid(row=2, column=0, pady=10)

        def add_to_cart():
            selection = menu_tree.selection()
            if not selection:
                return
            
            item = menu_tree.item(selection[0])['values']
            cart_tree.insert('', 'end', values=item)
            
            # Update total price
            total = sum(float(cart_tree.item(item)['values'][1].replace('₹', '')) 
                       for item in cart_tree.get_children())
            total_price.set(f"Total: ₹{total:.2f}")

        def remove_from_cart():
            selection = cart_tree.selection()
            if not selection:
                return
            
            cart_tree.delete(selection[0])
            
            # Update total price
            total = sum(float(cart_tree.item(item)['values'][1].replace('₹', '')) 
                       for item in cart_tree.get_children())
            total_price.set(f"Total: ₹{total:.2f}")

        def place_order():
            if not cart_tree.get_children():
                messagebox.showwarning("Warning", "Please add items to cart!")
                return
            
            # Collect items from cart
            ordered_items = []
            total = 0
            for item_id in cart_tree.get_children():
                item = cart_tree.item(item_id)['values']
                ordered_items.append({
                    'Item Name': item[0],
                    'Price': float(item[1].replace('₹', ''))
                })
                total += float(item[1].replace('₹', ''))
            
            # Add to order history
            order = {
                'items': ordered_items,
                'total': total,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.order_history.append(order)
            
            # Save to Excel file
            self.save_order_history()
            
            messagebox.showinfo("Success", f"Order placed successfully!\nTotal Amount: ₹{total:.2f}")
            order_window.destroy()

        # Buttons
        ttk.Button(item_frame, text="Add to Cart", command=add_to_cart).grid(row=2, column=0, pady=5)
        ttk.Button(cart_frame, text="Remove Item", command=remove_from_cart).grid(row=3, column=0, pady=5)
        ttk.Button(cart_frame, text="Place Order", command=place_order).grid(row=4, column=0, pady=5)
    
    def show_orders(self):
        # Create new window for order history
        history_window = Toplevel(self.root)
        history_window.title("Order History")
        history_window.geometry("1000x600")

        # Create frame
        frame = ttk.Frame(history_window, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10)

        # Add date filter
        filter_frame = ttk.Frame(frame)
        filter_frame.grid(row=0, column=0, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Label(filter_frame, text="Select Date: ").pack(side=tk.LEFT, padx=5)
        
        # Get unique dates from order history
        dates = sorted(list(set([order['date'].split()[0] for order in self.order_history])), reverse=True)
        date_var = tk.StringVar()
        if dates:
            date_var.set(dates[0])  # Set to most recent date
        
        date_combo = ttk.Combobox(filter_frame, textvariable=date_var, values=dates)
        date_combo.pack(side=tk.LEFT, padx=5)

        # Create Treeview for orders
        tree = ttk.Treeview(frame, columns=('Date', 'Items', 'Total'), show='headings', height=15)
        tree.heading('Date', text='Date')
        tree.heading('Items', text='Items')
        tree.heading('Total', text='Total')
        
        tree.column('Date', width=200)
        tree.column('Items', width=550)
        tree.column('Total', width=150)
        
        tree.grid(row=1, column=0, pady=5)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=tree.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        tree.configure(yscrollcommand=scrollbar.set)

        def update_orders(*args):
            # Clear current items
            for item in tree.get_children():
                tree.delete(item)
                
            selected_date = date_var.get()
            
            # Populate orders for selected date
            for order in self.order_history:
                if order['date'].split()[0] == selected_date:
                    items_str = ", ".join([item['Item Name'] for item in order['items']])
                    tree.insert('', 'end', values=(
                        order['date'],
                        items_str,
                        f"₹{order['total']:.2f}"
                    ))

        date_combo.bind('<<ComboboxSelected>>', update_orders)
        
        # Initial population of orders
        if dates:
            update_orders()
    
    def show_customers(self):
        # Create new window for customers
        customers_window = Toplevel(self.root)
        customers_window.title("Customer Management")
        customers_window.geometry("1000x600")  # Standardized window size
        messagebox.showinfo("Customers", "Customer management will be implemented here")
    
    def show_menu(self):
        # Create new window for menu management
        menu_window = Toplevel(self.root)
        menu_window.title("Menu Management")
        menu_window.geometry("1000x600")  # Standardized window size
        messagebox.showinfo("Menu Items", "Menu management will be implemented here")

if __name__ == "__main__":
    root = tk.Tk()
    app = TiffinServiceApp(root)
    root.mainloop() 