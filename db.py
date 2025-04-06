import sqlite3

DB_ORDERS = 'orders.db'
DB_REVIEWS = 'reviews.db'


def get_orders_connection():
    return sqlite3.connect(DB_ORDERS)


def get_reviews_connection():
    return sqlite3.connect(DB_REVIEWS)


def init_db():
    # Створення таблиці для замовлень
    with get_orders_connection() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                is_done INTEGER DEFAULT 0
            )
        ''')
        conn.commit()

    # Створення таблиці для відгуків
    with get_reviews_connection() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                review_type TEXT NOT NULL CHECK(review_type IN ('positive', 'negative'))
            )
        ''')
        conn.commit()


def get_reviews():
    with get_reviews_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM reviews')
        return c.fetchall()


def add_review(title, review_type):
    if review_type not in ['positive', 'negative']:
        raise ValueError("review_type must be 'positive' or 'negative'")
    
    with get_reviews_connection() as conn:
        c = conn.cursor()
        c.execute('INSERT INTO reviews (title, review_type) VALUES (?, ?)', (title, review_type))
        conn.commit()


def add_order(title):
    with get_orders_connection() as conn:
        c = conn.cursor()
        c.execute('INSERT INTO orders (title) VALUES (?)', (title,))
        conn.commit()