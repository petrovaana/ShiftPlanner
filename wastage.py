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

def add_wastage(title, classes):
    sql = "INSERT INTO wastage (title) VALUES (?)"
    db.execute(sql, [title])

    wastage_id = db.last_insert_id()

    sql = "INSERT INTO wastage_classes (wastage_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [wastage_id, class_title, class_value])
    
def get_classes(wastage_id):
    sql = "SELECT title, value FROM wastage_classes WHERE wastage_id = ?"
    result = db.query(sql, [wastage_id])
    return [{"title": res["title"], "value": res["value"]} for res in result]

def get_wastage():
    sql = "SELECT id, title FROM wastage ORDER BY id DESC"
    wastages = db.query(sql)

    result = []
    for wastage in wastages:
        classes = get_classes(wastage["id"])
        result.append({
            "id": wastage["id"],
            "title": wastage["title"],
            "classes": classes
        })
    return result