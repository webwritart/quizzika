from UI import App
import sqlite3


con = sqlite3.connect("data.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS questions(category, chapter, question, answer)")
con.commit()
con.close()

