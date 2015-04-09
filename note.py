import sqlite3 as lite
import exceptions
import sys


##clss notes, within this classe are functions to read, list, write and delete notes using a sqlite database
class Notes:


    def __init__(self):

        self.load()


    ##load function, it is possible to choose between the default database or create/use a new one
    def load(self):

        sys.stdout.write("Database name? ")
        self.database = sys.stdin.readline().strip()

        if self.database == "":
            sys.stdout.write("Default database loaded \n")
            self.database="note"

        with lite.connect('%s.db' % (self.database )) as con:
            cur=con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS notes(id  INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL UNIQUE, content TEXT)")

    ##read function, to read a note is necessary give the note title
    def read(self):
        sys.stdout.write("Title? ")
        title = sys.stdin.readline().strip()

        with lite.connect('%s.db' % (self.database )) as con:
            cur = con.cursor()
            cur.execute("SELECT notes.content FROM notes WHERE notes.title = '%s' " % (title) )
            result = cur.fetchall()

            if not result:
                sys.stdout.write( "Note not found\n")

            for row in result:
                sys.stdout.write( row[0] + '\n' )


    ##write function, to write a new note is necessary create a title and the content of the function.
    ##The id it is created automatically
    def write(self):

        sys.stdout.write("Title: ")
        title = sys.stdin.readline().strip()

        sys.stdout.write("Content: ")
        content = sys.stdin.readline().strip()

        with lite.connect('note.db') as con:
            result=con.execute("INSERT INTO notes(title,content) VALUES( '%s' , '%s' )" % (title,content))


    ##delet function, to delet a note is is necessary pass the note title
    # todo: include a way to delet a note using the note id
    def delet(self):

        sys.stdout.write("Title: ")
        title = sys.stdin.readline().strip()


        with lite.connect('%s.db' % (self.database )) as con:
            result=con.execute("DELETE FROM notes WHERE notes.title = '%s' " % (title))
            for row in result:
                sys.stdout.write( row[0] + '\n' )


    ##list the notes in the database
    def list(self):
       with lite.connect('%s.db' % (self.database )) as con:
            result=con.execute(" SELECT notes.id, notes.title FROM notes ")
            for row in result:
                 sys.stdout.write( str( row[0] ) + '-' + row[1] + '\n')


    def persist(self):
        pass


#read, list, write, delete, save

def run():
    notes = Notes()
    while True:
        sys.stdout.write("what? ")
        action = sys.stdin.readline().strip()
        if action == 'r':
            notes.read()
        elif action == 'l':
            notes.list()
        elif action == 'w':
            notes.write()
        elif action == 'd':
            notes.delet()
        #elif action == 's':
        #    notes.persist()
        elif action == 'q':
            break

run()
