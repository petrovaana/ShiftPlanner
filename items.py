import db

def add_yksari(title, description, start_price, pvm, user_id):
    sql = "INSERT INTO items (title, description, start_price, pvm, user_id) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [title, description, start_price, pvm, user_id])

def get_yksarit():
    sql = "SELECT id, title, pvm FROM items ORDER BY DESC"
    return db.query(sql)

def get_yksari(item_id):
    sql = """SELECT items.title, 
                    items.id,
                    items.description, 
                    items.start_price,
                    users.id user_id,
                    users.username 
            FROM items, users
            WHERE items.user_id = users.id 
            AND items.id = ?"""
    return db.query(sql, [item_id])[0]

def update_yksari(item_id, title, description, start_price, pvm):
    sql = """UPDATE items SET title = ?,
                            description = ?
                            start_price = ?
                            pvm = ?
                        WHERE id = ?"""
    db.execute(sql, [title, description, start_price, pvm, item_id])