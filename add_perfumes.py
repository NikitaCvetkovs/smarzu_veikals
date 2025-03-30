import sqlite3

DB_NAME = 'shop.db'

perfumes = [
    ("Dior Sauvage", 100, 85),
    ("Bleu de Chanel", 100, 110),
    ("Creed Aventus", 100, 350),
    ("Acqua di Gio Profumo", 75, 95),
    ("YSL Y EDP", 100, 95),
    ("Jean Paul Gaultier Le Male", 125, 75),
    ("Versace Eros", 100, 70),
    ("Tom Ford Ombre Leather", 100, 180),
    ("Armani Code Profumo", 100, 110),
    ("Paco Rabanne 1 Million", 100, 65),
    ("Paco Rabanne Invictus", 100, 70),
    ("Stronger With You Intensely", 100, 90),
    ("Dolce & Gabbana The One", 100, 80),
    ("Burberry Hero", 100, 85),
    ("Hugo Boss Bottled", 100, 60),
    ("Givenchy Gentleman EDP", 100, 95),
    ("Prada Luna Rossa Carbon", 100, 90),
    ("Valentino Uomo Born in Roma", 100, 95),
    ("Mercedes-Benz Club Black", 100, 55),
    ("YSL La Nuit de l'Homme", 100, 85),
    ("Tom Ford Noir Extreme", 100, 150),
    ("Azzaro Wanted By Night", 100, 70),
    ("Mancera Cedrat Boise", 120, 110),
    ("Mont Blanc Explorer", 100, 65),
    ("Bvlgari Man in Black", 100, 80),
    ("Ralph Lauren Polo Blue", 100, 75),
    ("Issey Miyake L'Eau d'Issey", 125, 60),
    ("John Varvatos Vintage", 125, 50),
    ("Bentley for Men Intense", 100, 45),
    ("Lacoste Blanc", 100, 55)
]

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

c.executemany("INSERT INTO perfumes (name, volume, price) VALUES (?, ?, ?)", perfumes)

conn.commit()
conn.close()

print("Smaržas pievienotas!")
