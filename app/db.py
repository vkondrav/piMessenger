import datetime
import sqlite3
import os

class Database:
	
	basedir = os.path.abspath(os.path.dirname(__file__))

	DATABASE = basedir + "/app.db"
	
	def __init__(self, app):
		self.app = app
	
	def getDb(self):
		db = getattr(self.app, '_database', None)
		if db is None:
			db = self.app._database = sqlite3.connect(self.DATABASE)
			
		db.row_factory = makeDicts
		return db
					
	def getMessages(self):
		return self.queryDb("SELECT * FROM messages ORDER BY timestamp DESC LIMIT 10")

	def queryDb(self, query, args=(), one=False):
		con = self.getDb()
		cur = con.cursor().execute(query, args)
		rv = cur.fetchall()
		return (rv[0] if rv else None) if one else rv
		
	def addMessage(self, message):  
		con = self.getDb()
		cur = con.cursor().execute("INSERT INTO messages (timestamp, message) VALUES (?,?)",(getCurrentTimestamp(), message))
		cur.close()
		con.commit()
		
def makeDicts(cursor, row):
	return dict((cursor.description[idx][0], value)
				for idx, value in enumerate(row))			
		
def getCurrentTimestamp():
	return round(datetime.datetime.now().timestamp(), 0)
