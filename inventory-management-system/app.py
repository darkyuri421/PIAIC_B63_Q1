import getpass
import json
import os

# User and Role Management
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'role': self.role
        }

# Product Management
class Product:
    def __init__(self, product_id, name, category, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'stock_quantity': self.stock_quantity
        }

# Inventory System
class InventorySystem:
    def __init__(self, users_file='users.json', products_file='products.json'):
        self.products = {}
        self.users = []
        self.current_user = None
        self.low_stock_threshold = 5
        self.users_file = users_file
        self.products_file = products_file
        self.load_users()
        self.load_products()

    # User Management
    def add_user(self, username, password, role):
        self.users.append(User(username, password, role))
        self.save_users()

    def authenticate_user(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                return True
        return False

    # Product Management
    def add_product(self, product_id, name, category, price, stock_quantity):
        if self.current_user.role == "Admin":
            self.products[product_id] = Product(product_id, name, category, price, stock_quantity)
            print(f"Product {name} added successfully!")
            self.save_products()
        else:
            print("Access denied: Only admins can add products.")

    def edit_product(self, product_id, **kwargs):
        if self.current_user.role == "Admin":
            product = self.products.get(product_id)
            if product:
                product.name = kwargs.get('name', product.name)
                product.category = kwargs.get('category', product.category)
                product.price = kwargs.get('price', product.price)
                product.stock_quantity = kwargs.get('stock_quantity', product.stock_quantity)
                print(f"Product {product_id} updated successfully!")
                self.save_products()
            else:
                print("Product not found.")
        else:
            print("Access denied: Only admins can edit products.")

    def delete_product(self, product_id):
        if self.current_user.role == "Admin":
            if product_id in self.products:
                del self.products[product_id]
                print(f"Product {product_id} deleted successfully!")
                self.save_products()
            else:
                print("Product not found.")
        else:
            print("Access denied: Only admins can delete products.")

    def view_products(self):
        if not self.products:
            print("No products available.")
            return
        for product in self.products.values():
            print(f"ID: {product.product_id}, Name: {product.name}, Category: {product.category}, "
                  f"Price: ${product.price}, Stock: {product.stock_quantity}")

    def search_product(self, name=None, category=None):
        for product in self.products.values():
            if (name and product.name.lower() == name.lower()) or (category and product.category.lower() == category.lower()):
                print(f"ID: {product.product_id}, Name: {product.name}, Category: {product.category}, "
                      f"Price: ${product.price}, Stock: {product.stock_quantity}")

    def adjust_stock(self, product_id, amount):
        product = self.products.get(product_id)
        if product:
            product.stock_quantity += amount
            print(f"Stock adjusted for {product.name}. New stock: {product.stock_quantity}")
            if product.stock_quantity <= self.low_stock_threshold:
                print("Warning: Low stock level! Consider restocking.")
            self.save_products()
        else:
            print("Product not found.")

    # Save and Load JSON Data
    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                users_data = json.load(f)
                self.users = [User(**user) for user in users_data]

    def save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump([user.to_dict() for user in self.users], f, indent=4)

    def load_products(self):
        if os.path.exists(self.products_file):
            with open(self.products_file, 'r') as f:
                products_data = json.load(f)
                self.products = {product['product_id']: Product(**product) for product in products_data}

    def save_products(self):
        with open(self.products_file, 'w') as f:
            json.dump([product.to_dict() for product in self.products.values()], f, indent=4)

# Error handling
def main():
    system = InventorySystem()
    
    # Adding sample users if no users exist
    if not system.users:
        system.add_user("admin", "admin123", "Admin")
        system.add_user("user", "user123", "User")

    # Login simulation
    print("Welcome to the Inventory Management System!")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    if not system.authenticate_user(username, password):
        print("Authentication failed! Please try again.")
        return
    
    print(f"Login successful! Logged in as {system.current_user.role}.")

    while True:
        print("\nOptions:")
        print("1. Add Product")
        print("2. Edit Product")
        print("3. Delete Product")
        print("4. View Products")
        print("5. Search Product")
        print("6. Adjust Stock")
        print("7. Logout")
        
        choice = input("Choose an option: ")

        try:
            if choice == "1":
                product_id = input("Enter Product ID: ")
                name = input("Enter Product Name: ")
                category = input("Enter Category: ")
                price = float(input("Enter Price: "))
                stock_quantity = int(input("Enter Stock Quantity: "))
                system.add_product(product_id, name, category, price, stock_quantity)

            elif choice == "2":
                product_id = input("Enter Product ID to edit: ")
                name = input("Enter New Product Name (leave blank to skip): ")
                category = input("Enter New Category (leave blank to skip): ")
                price = input("Enter New Price (leave blank to skip): ")
                stock_quantity = input("Enter New Stock Quantity (leave blank to skip): ")
                
                kwargs = {}
                if name: kwargs['name'] = name
                if category: kwargs['category'] = category
                if price: kwargs['price'] = float(price)
                if stock_quantity: kwargs['stock_quantity'] = int(stock_quantity)
                
                system.edit_product(product_id, **kwargs)

            elif choice == "3":
                product_id = input("Enter Product ID to delete: ")
                system.delete_product(product_id)

            elif choice == "4":
                system.view_products()

            elif choice == "5":
                name = input("Enter Product Name to search (leave blank to skip): ")
                category = input("Enter Category to search (leave blank to skip): ")
                system.search_product(name=name, category=category)

            elif choice == "6":
                product_id = input("Enter Product ID to adjust stock: ")
                amount = int(input("Enter amount to adjust (+ for restock, - for sale): "))
                system.adjust_stock(product_id, amount)

            elif choice == "7":
                print("Logging out...")
                break

            else:
                print("Invalid option. Please try again.")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
