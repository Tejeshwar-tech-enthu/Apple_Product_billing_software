import mysql.connector
import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime

#CREATE DATABASE bill;
#USE bill;
#CREATE TABLE cart_items(customer_name varchar(35), product_name varchar(30), quantity int, price_per_unit int);

class Product:
    def __init__(self, code, name, price):
        self.code = code
        self.name = name
        self.price = price


class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity


class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, cart_item):
        self.items.append(cart_item)

    def remove_item(self, cart_item):
        self.items.remove(cart_item)

    def calculate_total(self):
        total = sum(item.product.price * item.quantity for item in self.items)
        return total


class Invoice:
    def generate_invoice(self, cart):
        invoice_text = "Invoice:\n"
        for item in cart.items:
            invoice_text += f"{item.product.name} x {item.quantity} - ${item.product.price * item.quantity:.2f}\n"
        invoice_text += f"Total: ${cart.calculate_total():.2f}"
        return invoice_text


def display_products(products):
    product_list = "Available Products:\n"
    for product in products:
        product_list += f"{product.code}: {product.name} - ${product.price:.2f}\n"
    return product_list


def add_to_cart(cart, selected_product, quantity):
    cart.add_item(CartItem(selected_product, quantity))
    return f"{quantity} {selected_product.name}(s) added to cart."


def main():
    products = [
        Product("P01", "Mapple Laptop", 1088.08),
        Product("P02", "Mapple Mphone 14 Pro Max ", 1670.25),
        Product("P03", "Mapple MAC STUDIO", 2000),
        Product("P04", "Mapple MAirPods ", 278.38),
        Product("P05", "Mapple Watch Series 8", 1027.57),
        Product("P06", "Mapple MPad Pro M2 Chip", 1000),
    ]

    # Connect to the MySQL database
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tiger",
        database="bill",
    )

    def update_cart_preview():
        cart_preview_text = "Cart Preview:\n"
        for item in cart.items:
            cart_preview_text += f"{item.product.name} x {item.quantity}\n"
        cart_preview_text += f"Total: ${cart.calculate_total():.2f}"
        #  cart_preview_label.config(text=cart_preview_text)

    def display_products_command():
        product_list = display_products(products)
        display_label.config(text=product_list)

    def add_to_cart_command():
        product_list = display_products(products)
        display_label.config(text=product_list)
        product_code = product_code_entry.get()
        quantity = int(quantity_entry.get())
        selected_product = next((p for p in products if p.code == product_code), None)
        if selected_product:
            result = add_to_cart(cart, selected_product, quantity)
            messagebox.showinfo("Success", result)
        else:
            messagebox.showerror("Error", "Invalid product code.")

    def generate_invoice_command():
        if cart.items:
            # Ask for customer name
            customer_name = simpledialog.askstring("Name", "Enter Customer name:")
            if customer_name is None or customer_name.strip() == "":
                messagebox.showerror("Error", "Customer name cannot be empty.")
                return

            # Get the current date and time
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            invoice_text = f"Customer: {customer_name}\n"
            invoice_text += f"Date and Time: {current_datetime}\n\n"
            invoice_text += "Invoice:\n"
            for item in cart.items:
                invoice_text += f"{item.product.name} x {item.quantity} - ${item.product.price * item.quantity:.2f}\n"
            invoice_text += f"Total: ${cart.calculate_total():.2f}"

            # Show the invoice as a message box
            messagebox.showinfo("Invoice", invoice_text)

            # Insert cart data, customer name, and date/time into MySQL table
            cursor = db_connection.cursor()
            for item in cart.items:
                query = "INSERT INTO cart_items (customer_name, product_name, quantity, price_per_unit) VALUES (%s, %s, %s, %s)"
                values = (customer_name, item.product.name, item.quantity, item.product.price)
                cursor.execute(query, values)
            db_connection.commit()
            cursor.close()

            # Clear the cart and update cart preview
            cart.items.clear()
            update_cart_preview()
        else:
            messagebox.showerror("Error", "Cart is empty. Please add items to generate an invoice.")

    def exit_command():
        db_connection.close()
        root.destroy()

    root = tk.Tk()
    root.state('zoomed')
    root.title("Online MApple Store")
    cart = Cart()
    invoice = Invoice()
    display_label = tk.Label(root, text="Welcome to Online MApple Store", font=("Helvetica", 16))
    display_label.pack(pady=10)
    display_button = tk.Button(root, text="Display Products", command=display_products_command)
    display_button.pack()
    product_code_label = tk.Label(root, text="Product Code:")
    product_code_label.pack()
    product_code_entry = tk.Entry(root)
    product_code_entry.pack()
    quantity_label = tk.Label(root, text="Quantity:")
    quantity_label.pack()
    quantity_entry = tk.Entry(root)
    quantity_entry.pack()
    add_to_cart_button = tk.Button(root, text="Add to Cart", command=add_to_cart_command)
    add_to_cart_button.pack()
    generate_invoice_button = tk.Button(root, text="Generate Invoice", command=generate_invoice_command)
    generate_invoice_button.pack()
    exit_button = tk.Button(root, text="Exit", command=exit_command)
    exit_button.pack()

    root.mainloop()


if True:
    main()
