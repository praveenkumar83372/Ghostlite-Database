import ghostlite

# open database
db = ghostlite.open("project")

# enable search engine
db.enable_search()

# enable dashboard
db.enable_dashboard()