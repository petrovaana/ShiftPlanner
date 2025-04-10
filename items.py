import db

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)
    
    return classes

def add_item(title, description, pax, maksutapa, start_price, pvm, user_id, classes):
    all_classes = get_all_classes()

    sql = "INSERT INTO items (title, description, pax, maksutapa, start_price, pvm, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)"
    db.execute(sql, [title, description, pax, maksutapa, start_price, pvm, user_id])

    item_id = db.last_insert_id()

    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [item_id, title, value])


#Muokkauksiin just et kuka muokannu viimesimmän kerran liittyvät tiedot
def add_tiedot(item_id, user_id, description):
    sql = "INSERT INTO muokkaukset (item_id, user_id, description) VALUES (?, ?, ?)"
    db.execute(sql, [item_id, user_id, description])

def get_tiedot(item_id):
    sql = """SELECT muokkaukset.description, users.username
            FROM muokkaukset, users
            WHERE muokkaukset.item_id = ? AND muokkaukset.user_id = users.id
            ORDER BY muokkaukset.id DESC"""
    return db.query(sql, [item_id])

def get_classes(item_id):
    sql = "SELECT title, value FROM item_classes WHERE item_id = ?"
    return db.query(sql, [item_id])


def get_items():
    sql = "SELECT id, title, tila, pvm FROM items ORDER BY DESC"
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.title, 
                    items.id,
                    items.description,
                    items.tila,
                    items.pax,
                    items.maksutapa,
                    items.start_price,
                    users.id user_id,
                    users.username 
            FROM items, users
            WHERE items.user_id = users.id 
            AND items.id = ?"""
    result = db.query(sql, [item_id])
    return result[0] if result else None


def update_item(item_id, title, description, pax, maksutapa, start_price, pvm, classes):
    sql = """UPDATE items SET title = ?,
                            description = ?,
                            pax = ?,
                            maksutapa = ?,
                            start_price = ?,
                            pvm = ?
                        WHERE id = ?"""
    db.execute(sql, [title, description, pax, maksutapa, start_price, pvm, item_id])

    sql = "DELETE FROM item_classes WHERE item_id = ?"
    db.execute(sql, [item_id])

    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [item_id, title, value])

#Poistaa yksärin
def remove_item(item_id):
    sql = "DELETE FROM item_classes WHERE item_id = ?"
    db.execute(sql, [item_id])

    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

#Pystyy ettii yksärii nimen, description tai tilan perusteella
def find_items(query):
    sql = """SELECT id, title
            FROM items
            WHERE title LIKE ? OR description LIKE ? OR tila LIKE ?
            ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.execute(sql, [like, like])