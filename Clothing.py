import mainpage
import customtkinter as ctk
from PIL import Image
from cart import Cart


class ClothingPage:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Commerce Product List")
        self.root.geometry("700x600")
        ctk.set_appearance_mode("dark")

        # Initialize cart
        self.cart = Cart()

        # Item data
        self.items = {
            "Jeans": 100.00,
            "T-Shirt": 150.00,
            "Tank top": 500.00,
            "Belt": 300.00,
            "Heels": 50.00,
            "Off shoulder top": 200.00,
            "Skirt": 400.00,
            "Blazer": 20.00,
        }

        self.cart_labels = {}
        self.placeholder_img = self.create_ctk_image((100, 100))

        # Build the UI
        self.create_title()
        self.create_item_list()
        self.create_view_cart_button()
        self.create_return_button()
        self.create_total_price_label()

        # Update the UI with initial cart data
        self.update_cart_ui()

    def create_title(self):
        """Create the title label."""
        title_label = ctk.CTkLabel(self.root, text="Clothing Section", font=("Diamonds", 24, "bold"))
        title_label.pack(pady=10)

    def create_ctk_image(self, size):
        """Create a placeholder image as CTkImage."""
        placeholder = Image.new("RGB", size, color=(200, 200, 200))
        return ctk.CTkImage(light_image=placeholder, dark_image=placeholder, size=size)

    def create_item_list(self):
        """Create a scrollable frame with items."""
        scrollable_frame = ctk.CTkScrollableFrame(self.root, width=650, height=500)
        scrollable_frame.pack(pady=20, padx=20, fill="both", expand=True)

        for i, (item, price) in enumerate(self.items.items()):
            item_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10)
            item_frame.grid(row=i, column=0, pady=10, padx=10, sticky="ew")

            # Image placeholder
            image_label = ctk.CTkLabel(item_frame, image=self.placeholder_img, text="")
            image_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

            # Item title
            item_label = ctk.CTkLabel(item_frame, text=item, font=("Arial", 14, "bold"))
            item_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

            # Item price
            price_label = ctk.CTkLabel(item_frame, text=f"Price: ${price:.2f}", font=("Arial", 12))
            price_label.grid(row=1, column=1, padx=10, sticky="w")

            # Remove button
            remove_button = ctk.CTkButton(
                item_frame, text="-", width=30, fg_color="#fd5c63", hover_color="red",
                command=lambda i=item: self.remove_from_cart(i)
            )
            remove_button.grid(row=0, column=2, padx=10, sticky="E")

            # Add button
            add_button = ctk.CTkButton(
                item_frame, text="+", width=30, command=lambda i=item: self.add_to_cart(i)
            )
            add_button.grid(row=0, column=3, padx=10, sticky="E")

            # Quantity label
            cart_label = ctk.CTkLabel(item_frame, text="Quantity: 0", font=("Arial", 12))
            cart_label.grid(row=0, column=4, padx=10, sticky="E")

            self.cart_labels[item] = cart_label

    def create_view_cart_button(self):
        """Create the View Cart button."""
        view_cart_button = ctk.CTkButton(
            self.root, text="View Cart", fg_color="#007FFF", hover_color="blue", command=self.view_cart
        )
        view_cart_button.pack(pady=10)

    def create_return_button(self):
        """Create the Return to Main Page button."""
        return_button = ctk.CTkButton(
            self.root, text="Return to Main Page", fg_color="#FF8C00", hover_color="orange", command=self.return_to_main
        )
        return_button.pack(pady=0, padx=20)

    def create_total_price_label(self):
        """Create a dynamic total price label."""
        self.total_price_label = ctk.CTkLabel(self.root, text="Total Price: $0.00", font=("Arial", 14, "bold"))
        self.total_price_label.pack(pady=5, side="bottom", anchor="se")

    def add_to_cart(self, item):
        """Add an item to the cart."""
        self.cart.add_item(item, self.items[item])
        self.update_cart_ui()

    def remove_from_cart(self, item):
        """Remove an item from the cart."""
        self.cart.remove_item(item)
        self.update_cart_ui()

    def update_cart_ui(self):
        """Update the UI to reflect the cart state."""
        cart = self.cart.get_cart()
        for item, label in self.cart_labels.items():
            quantity = cart.get(item, {}).get("quantity", 0)
            label.configure(text=f"Quantity: {quantity}")
        self.update_total_price()

    def update_total_price(self):
        """Update the total price label."""
        total_price = self.cart.calculate_total_price()
        self.total_price_label.configure(text=f"Total Price: ${total_price:.2f}")

    def view_cart(self):
        """Display the cart in a new window."""
        cart_window = ctk.CTkToplevel(self.root)
        cart_window.title("View Cart")
        cart_window.geometry("400x400")

        cart = self.cart.get_cart()
        row = 0
        for item, details in cart.items():
            ctk.CTkLabel(cart_window, text=f"{item} - Qty: {details['quantity']} - ${details['price']:.2f}").grid(
                row=row, column=0, padx=10, pady=5, sticky="w"
            )
            row += 1

        total_price = self.cart.calculate_total_price()
        ctk.CTkLabel(cart_window, text=f"Total Price: ${total_price:.2f}", font=("Arial", 14, "bold")).grid(
            row=row, column=0, padx=10, pady=20, sticky="w"
        )

    def return_to_main(self):
        self.root.destroy()
        root = ctk.CTk()
        mainpage.MainPage(root)
        root.mainloop()


if __name__ == "__main__":
    root = ctk.CTk()
    app = ClothingPage(root)
    root.mainloop()
