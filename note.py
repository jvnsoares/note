import sqlite3 as lite
import os.path
import exceptions
import sys


##clss notes, within this classe are functions to read, list, write and delete notes using a sqlite database
class Notes:

    #default database
    database = "notes"

    def __init__(self):

        self.load()
        self.login()


    ##load function, load the default database
    def load(self):

        #verify is database exist, if not create a new one
        if  not os.path.exists("%s.db" % self.database):
            sys.stdout.write("You must create a new user and password\n")
            #create a new user
            sys.stdout.write("User ?")
            user = sys.stdin.readline().strip()
            #check if password and confirmation match
            while True:
                sys.stdout.write("password ?")
                pssw1 = sys.stdin.readline().strip()
                sys.stdout.write("confirm password ?")
                pssw2 = sys.stdin.readline().strip()

                if pssw1 == pssw2:
                    break
                else:
                    sys.stdout.write("password and confirmation are not the same, try again\n")

            #create the database and insert the user
            with lite.connect('%s.db' % (self.database )) as con:
                cur=con.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS notes(id  INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL UNIQUE, content TEXT, userId TEXT, FOREIGN KEY(userId) REFERENCES user(id) )")
                cur.execute("CREATE TABLE IF NOT EXISTS user(id  INTEGER PRIMARY KEY AUTOINCREMENT,login  TEXT NOT NULL, password TEXT NOT NULL UNIQUE)")
                cur.execute("INSERT INTO user(login,password) VALUES( '%s' , '%s' )" % (user,pssw1))

    #login
    def login(self):
        sys.stdout.write("login ?")
        login = sys.stdin.readline().strip()
        sys.stdout.write("password ?")
        pssw = sys.stdin.readline().strip()

        with lite.connect('%s.db' % (self.database )) as con:
            cur=con.cursor()
            cur.execute("SELECT user.id FROM user WHERE user.login = '%s' AND user.password = '%s' " % (login,pssw))
            result = cur.fetchone()
            self.userId =  result[0]


    ##read function, to read a note is necessary give the note title
    def read(self):
        sys.stdout.write("Title? ")
        title = sys.stdin.readline().strip()

        with lite.connect('%s.db' % (self.database )) as con:
            cur = con.cursor()
            cur.execute("SELECT notes.content FROM notes WHERE notes.title = '%s' AND notes.userId = '%s' " % (title,self.userId) )
            result = cur.fetchall()

            if not result:
                sys.stdout.write( "Note not found\n")

            else:
                for row in result:
                    sys.stdout.write( row[0] + '\n' )


    ##write function, to write a new note is necessary create a title and the content of the function.
    ##The id it is created automatically
    # todo: fix error when to users create a note with the same title
    def write(self):

        sys.stdout.write("Title: ")
        title = sys.stdin.readline().strip()

        sys.stdout.write("Content: ")
        content = sys.stdin.readline().strip()

        with lite.connect('%s.db' % (self.database )) as con:
            con.execute("INSERT INTO notes(title,content,userID) VALUES( '%s' , '%s' , '%s' )" % (title,content,self.userId))


    ##delete function, to delete a note is is necessary pass the note title
    # todo: include a way to delete a note using the note id
    def delete(self):

        sys.stdout.write("Title: ")
        title = sys.stdin.readline().strip()


        with lite.connect('%s.db' % (self.database )) as con:
            result=con.execute("DELETE FROM notes WHERE notes.title = '%s' AND notes.userId = '%s' " % (title,self.userId))
            for row in result:
                sys.stdout.write( row[0] + '\n' )


    ##list the notes in the database
    def list(self):

        with lite.connect('%s.db' % (self.database )) as con:
            result=con.execute(" SELECT notes.id, notes.title FROM notes WHERE notes.userId = '%s'" % (self.userId))
            for row in result:
                 sys.stdout.write( str( row[0] ) + '-' + row[1] + '\n')


    def persist(self):
        pass

    # todo:check if the user exist before try to create
    def newUser(self):
        sys.stdout.write("User ?")
        user = sys.stdin.readline().strip()
        #check if password and confirmation match
        while True:
            sys.stdout.write("password ?")
            pssw1 = sys.stdin.readline().strip()
            sys.stdout.write("confirm password ?")
            pssw2 = sys.stdin.readline().strip()

            if pssw1 == pssw2:
                break
            else:
                sys.stdout.write("password and confirmation are not the same, try again\n")
        with lite.connect('%s.db' % (self.database )) as con:
            cur=con.cursor()
            cur.execute("INSERT INTO user(login,password) VALUES( '%s' , '%s' )" % (user,pssw1))


    def changeUser(self):
        self.login()

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
            notes.delete()

        #elif action == 's':
        #    notes.persist()

        elif action == 'u':
            notes.newUser()

        elif action == 'c':
            notes.changeUser()

        #help
        elif action == 'h':
            sys.stdout.write("r \t read note\n" +
                             "l \t list notes \n" +
                             "w \t write note\n" +
                             "d \t delete note \n" +
                             "u \t create user \n" +
                             "c \t change user \n")

        #quit
        elif action == 'q':
            break

run()
