from UI import App
import sqlite3
from brain import DATABASE_URI


con = sqlite3.connect(DATABASE_URI)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS questions(category, chapter, question, answer)")
con.commit()
con.close()

App('QUIZZIKA', (1800, 1000))
