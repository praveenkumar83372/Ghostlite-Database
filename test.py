import ghostlite

db = ghostlite.open("project")

print(
    db.query("SELECT * FROM users WHERE age = 25 LIMIT 2")
)