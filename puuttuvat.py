import db

def add_puuttuva(tuote, paiva):
    sql = "INSERT INTO items (tuote, paiva) VALUES (?, ?)"
    db.execute(sql, [tuote, paiva])

def get_puuttuvat():
    sql = "SELECT tuote, paiva FROM puuttuvat ORDER BY DESC"
    return db.query(sql)

def get_puuttuva(tuote):
    sql = """SELECT tuote
            FROM puuttuvat
            WHERE tuote = ?"""
    return db.query(sql, [tuote])[0]