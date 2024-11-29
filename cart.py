import json
import os
import customtkinter as ctk

class Cart:
    def __init__(self, cart_file="cart.json"):
        self.cart_file = cart_file
        self.cart = self.load_cart()

    def load_cart(self):
        """Load the cart from the JSON file."""
        if os.path.exists(self.cart_file):
            with open(self.cart_file, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    print("Error: Cart file is corrupted. Initializing a new cart.")
                    return {}
        return {}
    
    def view_cart(self):
        """Display the cart in a new window."""
        cart_window = ctk.CTkToplevel(self.root)
        cart_window.title("View Cart")
        cart_window.geometry("400x400")

        c=self.get_cart()
        row = 0
        for item, details in c.items():
            ctk.CTkLabel(cart_window, text=f"{item} - Qty: {details['quantity']} - ${details['price']:.2f}").grid(
                row=row, column=0, padx=10, pady=5, sticky="w"
            )
            row += 1

        total_price = self.cart.calculate_total_price()
        ctk.CTkLabel(cart_window, text=f"Total Price: ${total_price:.2f}", font=("Arial", 14, "bold")).grid(
            row=row, column=0, padx=10, pady=20, sticky="w"
        )

    def save_cart(self):
        """Save the cart to the JSON file."""
        with open(self.cart_file, "w") as file:
            json.dump(self.cart, file)

    def add_item(self, item_name, item_price):
        """Add an item to the cart."""
        if item_name in self.cart:
            self.cart[item_name]["quantity"] += 1
        else:
            self.cart[item_name] = {"quantity": 1, "price": item_price}
        self.save_cart()

    def remove_item(self, item_name):
        """Remove an item from the cart."""
        if item_name in self.cart:
            self.cart[item_name]["quantity"] -= 1
            if self.cart[item_name]["quantity"] <= 0:
                del self.cart[item_name]
            self.save_cart()

    def calculate_total_price(self):
        """Calculate the total price of the cart."""
        return sum(item["quantity"] * item["price"] for item in self.cart.values())

    def get_cart(self):
        """Return the current cart."""
        return self.cart
