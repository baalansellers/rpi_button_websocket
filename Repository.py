import sqlite3

class Repository(object):
	def __init__(self):
		self.conn = 'countdown.db'

	def get_current_count(self):
		db = sqlite3.connect(self.conn, detect_types=sqlite3.PARSE_DECLTYPES)
		cursor = db.execute("""
			SELECT num_sales
			FROM tblCurrentCount
			WHERE id = 1;
		""")
		value = cursor.fetchall()[0][0]
		db.close()
		return value

	def set_count(self,index):
		db = sqlite3.connect(self.conn, detect_types=sqlite3.PARSE_DECLTYPES)
		db.execute('UPDATE tblCurrentCount SET num_sales = ' + str(index) + ' WHERE id = 1;')
		db.commit()
		db.close()
		return True