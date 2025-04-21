import db
from datetime import datetime

def add_item(title, description, booked_space, guests, payment, start_price, date, user_id):
    sql = "INSERT INTO items (title, description, booked_space, guests, payment, start_price, date, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    db.execute(sql, [title, description, booked_space, guests, payment, start_price, date, user_id])

def add_information(item_id, user_id, description):
    sql = "INSERT INTO edits (item_id, user_id, description) VALUES (?, ?, ?)"
    db.execute(sql, [item_id, user_id, description])

def get_information(item_id):
    sql = """SELECT edits.description, users.id user_id, users.username
            FROM edits, users
            WHERE edits.item_id = ? AND edits.user_id = users.id
            ORDER BY edits.id"""
    return db.query(sql, [item_id])

def get_items():
    sql = "SELECT id, title, date FROM items ORDER BY date DESC"
    return db.query(sql)

def get_items_indexpage():
    sql = """SELECT id, title, date 
            FROM items 
            ORDER BY CASE
                WHEN date = ? THEN 0
                ELSE 1
            END, date ASC
            LIMIT 7"""
    today = datetime.today().date()
    return db.query(sql, [today])

def get_item(item_id):
    sql = """SELECT items.id, 
                    items.title,
                    items.description,
                    items.date,
                    items.payment,
                    items.booked_space,
                    items.start_price,
                    items.guests,
                    users.id user_id,
                    users.username 
            FROM items, users
            WHERE items.user_id = users.id 
            AND items.id = ?"""
    result = db.query(sql, [item_id])
    if result:
        return result[0]
    else:
        return None

def update_item(item_id, title, description, booked_space, guests, payment, start_price, date):
    sql = """UPDATE items SET title = ?,
                            description = ?,
                            booked_space = ?,
                            guests = ?,
                            payment = ?,
                            start_price = ?,
                            date = ?
                        WHERE id = ?"""
    db.execute(sql, [title, description, booked_space, guests, payment, start_price, date, item_id])

def remove_item(item_id):
    sql = "DELETE FROM edits WHERE item_id = ?"
    db.execute(sql, [item_id])

    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

def find_items(query):
    sql = """SELECT id, title, date
            FROM items
            WHERE LOWER(title) LIKE LOWER(?) 
                OR LOWER(description) LIKE LOWER(?) 
                OR LOWER(booked_space) LIKE LOWER(?)
            ORDER BY id DESC"""
    like = "%" + query + "%"
    results = db.query(sql, [like, like, like])
    return results
