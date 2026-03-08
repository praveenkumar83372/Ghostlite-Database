# 👻 Ghostlite

Ghostlite is a **lightweight Python database** designed to make data storage simple and powerful for developers.

It allows you to store, query, and manage data directly in Python while providing built-in tools such as SQL querying, REST APIs, a web dashboard, an admin panel, and distributed database synchronization.

Ghostlite is perfect for **local applications, prototypes, learning databases, and lightweight backend services**.

---

# 🚀 Installation

Install Ghostlite using pip:

```
pip install ghostlite
```

---

# ⚡ Features

Ghostlite provides powerful capabilities while remaining lightweight.

### 🗄 Simple Data Storage

Create databases and tables easily using Python.

### 🧠 SQL Query Engine

Run SQL-like queries directly on your data.

### 🔍 Full Text Search

Search records using keywords.

### 🌐 REST API

Expose your database through a built-in API server.

### 📊 Web Dashboard

View tables and records directly in your browser.

### 👨‍💻 Admin Panel

Manage your database visually with a simple UI.

### 🔄 Distributed Mode

Synchronize multiple Ghostlite nodes for distributed databases.

### 🔐 Transaction Support

Basic transaction operations for safe updates.

---

# 🧑‍💻 Basic Example

```python
import ghostlite

# create or open database
db = ghostlite.open("mydatabase")

# access table
users = db["users"]

# insert records
users.insert(name="Alice", age=25)
users.insert(name="Bob", age=30)

# read data
print(users.all())
```

Output example:

```
[
 {'name': 'Alice', 'age': 25},
 {'name': 'Bob', 'age': 30}
]
```

---

# 🧾 SQL Query Example

Ghostlite supports SQL-style queries.

```python
import ghostlite

db = ghostlite.open("mydb")

result = db.query("SELECT * FROM users WHERE age=25")

print(result)
```

---

# 🌐 Running the Web Tools

### Start Admin Panel

```python
db.enable_admin()
```

Open in browser:

```
http://localhost:9000
```

---

### Start REST API

```python
db.enable_api()
```

Example endpoints:

```
http://localhost:5000/tables
http://localhost:5000/table/users
http://localhost:5000/query?sql=SELECT * FROM users
```

---

### Start Dashboard

```python
db.enable_dashboard()
```

Open:

```
http://localhost:8080
```

---

# 🔎 Full Text Search

```python
db.enable_search()

results = db.search("users", "Alice")

print(results)
```

---

# 🔄 Distributed Database Example

Ghostlite supports simple distributed database synchronization.

```python
db.enable_cluster([
    "http://node1:5000",
    "http://node2:5000"
])
```

---

# 💡 What You Can Build With Ghostlite

Ghostlite can be used for many types of projects:

• Local data storage applications
• Lightweight backend services
• Prototypes and MVPs
• Developer tools
• Learning database systems
• Offline-first applications

---

# 🔗 Links

### GitHub

https://github.com/praveenkumar83372

### Portfolio

https://praveenkumart-portfolio.web.app/

---

# 👨‍💻 Author

Praveen Kumar

Developer passionate about building innovative software tools and systems.

---

# 📜 License

MIT License
