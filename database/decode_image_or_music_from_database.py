import sqlite3


class Db():
    def __init__(self):
        pass

    def take_musik_from_bd(self, db_name, file_format='.png', index):
        con = sqlite3.connect(db_name)

        cur = con.cursor()

        result = cur.execute("""SELECT * FROM image WHERE id == ?""", (index,)).fetchall()

        con.close()

        name = result[0][1] + file_format
        with open(name, mode='wb') as musik_file:
            musik_file.write(result[0][2])


Db.take_musik_from_bd(input('Database name '), input('File format '), int(input('Столбец ')))