import sqlite3

connection = sqlite3.connect("initiate_db.db")
cursor = connection.cursor()

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Products(
# id INTEGER PRIMARY KEY,
# title TEXT NOT NULL,
# description TEXT,
# price INTEGER NOT NULL
# )
# ''')
#
# products_data = [
#     ('Центрум', 'Мультивитаминный комплекс', 100),
#     ('B COMPLEX', 'Комплекс витамина В', 200),
#     ('VITAGOLD', 'Витамин D3', 300),
#     ('Витамины В', 'Витамины группы В', 400),
# ]
#
# cursor.executemany('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)', products_data)

def get_all_products():
    connection = sqlite3.connect("initiate_db.db")  # Создаем соединение внутри функции
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()

    connection.close()

    return [{'title': title, 'description': description, 'price': price} for id, title, description, price in products]

connection.commit()
connection.close()