import db

def add_missing(title, date, user_id):
    sql = "INSERT INTO missing_items (title, date, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [title, date, user_id])

def get_missing_indexpage():
    sql = "SELECT id, title, date FROM missing_items ORDER BY id DESC LIMIT 10"
    return db.query(sql)

def get_missing():
    sql = "SELECT id, title, date FROM missing_items ORDER BY id DESC"
    return db.query(sql)

def get_missings(missing_id):
    sql = """SELECT id, title, date, user_id
            FROM missing_items
            WHERE id = ?"""
    result = db.query(sql, [missing_id])
    if result:
        return result[0]
    else:
        return None

def remove_missing(missing_id):
    sql = "DELETE FROM missing_items WHERE id = ?"
    db.execute(sql, [missing_id])

def find_missing(query):
    sql = """SELECT id, title
            FROM missing_items
            WHERE LOWER(title) LIKE LOWER(?)
            ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like])
