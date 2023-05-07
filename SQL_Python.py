import mysql.connector
mydb=mysql.connector.connect(host='localhost',user='root',password='@09June2003',database='Inventory_Management')
c=mydb.cursor()
c.execute('''CREATE TABLE manufacture
             (manufacture_id INT PRIMARY KEY,
             item_name VARCHAR(255) NOT NULL,
             color VARCHAR(255) NOT NULL,
             manufacturer_name VARCHAR(255) NOT NULL,
             number_of_items_required INT NOT NULL,
             defective_items INT)''')
print("manufacture table was created")

c.execute('''CREATE TABLE goods
             (goods_id INT PRIMARY KEY,
             manufacture_id INT NOT NULL,
             manufacture_date DATE NOT NULL,
             price REAL NOT NULL,
             FOREIGN KEY(manufacture_id) REFERENCES manufacture(manufacture_id))''')
print("goods table was created")

c.execute('''CREATE TABLE purchase
             (purchase_id INT PRIMARY KEY,
             goods_id INT NOT NULL,
             store_name VARCHAR(255),
             purchase_date DATE NOT NULL,
             purchase_amount REAL NOT NULL,
             FOREIGN KEY(goods_id) REFERENCES goods(goods_id))''')
print("purchase table was created")

c.execute('''CREATE TABLE sale
             (sale_id INT PRIMARY KEY,
             store_name VARCHAR(255),
             goods_id INT NOT NULL,
             sale_date DATE NOT NULL,
             profit_margin REAL NOT NULL,
             FOREIGN KEY(goods_id) REFERENCES goods(goods_id))''')
print("sale table was created")
mydb.commit()

manufacture_data = [(1, 'chair', 'wooden','ABC', 100, 5),
                    (2, 'chair', 'metal','ABC', 50, 7),
                    (3, 'table', 'wooden','SS_Export', 75, 8),
                    (4, 'table', 'metal','SS_Export', 25, 9),
                    (5, 'toy', 'red','Toyco' ,200, 4),
                    (6, 'toy', 'blue','Toyco',150, 0),
                    (7, 'shirt', 'white','Clothing',300, 0),
                    (8, 'shirt', 'black','Clothing', 200, 4)]
c.executemany("INSERT INTO manufacture VALUES (%s,%s,%s,%s,%s,%s)", manufacture_data)

goods_data = [(101, 1, '2023-04-01', 50.0),
              (102, 1, '2023-04-01', 50.0),
              (103, 2, '2023-04-02', 75.0),
              (104, 3, '2023-04-03', 100.0),
              (105, 3, '2023-04-03', 100.0),
              (106, 4, '2023-04-04', 150.0),
              (107, 5, '2023-04-05', 5.0),
              (108, 6, '2023-04-06', 2.5),
              (109, 7, '2023-04-07', 10.0),
              (110, 8, '2023-05-01', 12.5)]
c.executemany("INSERT INTO goods VALUES (%s,%s,%s,%s)", goods_data)

purchase_data = [(201, 101, 'OnlineStore', '2023-04-01', 500.0),
                 (202, 103, 'OfflineStore', '2023-04-02', 750.0),
                 (203, 105, 'MyCare', '2023-04-03', 1000.0),
                 (204, 106, 'MyCare', '2023-04-04', 1500.0),
                 (205, 107, 'MyKids', '2023-04-05', 50.0),
                 (206, 108, 'Mykids', '2023-04-06', 25.0),
                 (207, 109, 'ORay', '2023-04-07', 100.0),
                 (208, 110, 'ORay', '2023-05-01', 125.0)]
c.executemany("INSERT INTO purchase VALUES (%s,%s,%s,%s,%s)", purchase_data)

sale_data = [(301, 'OnlineStore', 101, '2023-04-01', 75.0, 10.0),
             (302, 'OfflineStore', 103, '2023-04-02', 75.0, 10.0),
             (303, 'MyCare', 105, '2023-04-04', 112.5, 15.0),
             (304, 'ORay',109, '2023-04-07', 150.0, 20.0)]
c.executemany("INSERT INTO sale VALUES (%s,%s,%s,%s,%s,%s)", sale_data)
mydb.commit()

c.execute('''DELETE FROM manufacture
             WHERE item_name = 'shirt' AND color = 'black' AND defective_items > 0
             AND manufacture_id IN (SELECT manufacture_id
                                    FROM goods
                                    WHERE goods_id IN (SELECT goods_id
                                                       FROM purchase
                                                       WHERE purchase_date = '2023-05-01' AND purchase_amount = 125.0))''')
c.execute("SELECT*FROM manufacture")
myresult1=c.fetchall()
print(myresult1)
mydb.commit()


c.execute('''UPDATE manufacture
             SET number_of_items_required = 50
             WHERE item_name = 'toy' AND color = 'red'
             AND manufacture_id IN (SELECT manufacture_id
                                    FROM goods
                                    WHERE goods_id IN (SELECT goods_id
                                                       FROM purchase
                                                       WHERE purchase_date = '2023-04-05' AND purchase_amount = 5.0)
                                    AND manufacture_id IN (SELECT manufacture_id
                                                           FROM manufacture
                                                           WHERE item_name = 'toy' AND color = 'red'))''')
c.execute("SELECT*FROM manufacture")
myresult2=c.fetchall()
print(myresult2)
mydb.commit()

c.execute('''SELECT * FROM manufacture
             WHERE item_name = 'chair' AND color = 'wooden' AND manufacture_date < '2023-05-01' ''')
rows = c.fetchall()
for row in rows:
    print(row)
mydb.commit()

c.execute('''SELECT sale.profit_margin 
            FROM sale 
            JOIN goods ON sale.goods_id = goods.goods_id 
            JOIN manufacture ON goods.manufacture_id = manufacture.manufacture_id 
            WHERE manufacture.item_name = 'table' 
            AND manufacture.color = 'wooden' 
            AND sale.store_name = 'MyCare' 
            AND manufacture.manufacturer_name = 'SS Export' ''')
row = c.fetchone()
if row:
    print("The profit margin of the wooden table sold by MyCare store and manufactured by SS Export company is:", row[0])
else:
    print("No result found.")





