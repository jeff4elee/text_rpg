import sqlite3
import simplejson as json

#stores connection to database
con = sqlite3.connect('data.db')

#cursor traverses the records of the table
cur = con.cursor()
playerId = None

#cur.execute('''DROP TABLE Users''')

#cur.execute('''CREATE TABLE Users(User_Id INTEGER PRIMARY KEY,''' 
#            '''Username TEXT, Password TEXT)''')

#cur.execute('''DROP TABLE UserData''')

#cur.execute('''CREATE TABLE UserData(UserData_Id INTEGER PRIMARY KEY,''' 
#            '''json_value TEXT, User_Id INTEGER,'''
#            '''FOREIGN KEY(User_Id) REFERENCES Users(User_Id))''')
                
def prompt_registration():
    """ Prompts the user to register a username/password for
        future plays """
    
    user = raw_input("Enter a username\n").lower()

    #queries the username and determines if it already exists
    cur.execute('''SELECT * FROM Users WHERE Username = ?''', (user,))

    #if record exists, repeat the prompt until a unique username is provided
    while(cur.fetchone() is not None):
        
        user = raw_input("Username taken. Enter another\n").lower()
        cur.execute('''SELECT Username FROM Users WHERE Username = ?''', (user,))

    if(user == 'quit()'):
        return
    
    #if record does not exist, proceed to prompt for a password
    password = raw_input("Enter a password\n")


    if(password == 'quit()'):
        return
        
    #inserts the unique record into the database
    cur.execute('''INSERT INTO Users(Username, Password) VALUES(?, ?)''', (user, password,))
    print "Registered successfully"

def prompt_login():
    """ Prompts the user for login info and
        loads their associated save file """
    
    user = raw_input("Enter your username\n").lower()
    
    #queries the username and determines if it exists
    cur.execute('''SELECT * FROM Users WHERE Username = ?''', (user,))

    #if record does not exist, repeat the prompt until a valid username is provided    
    while(cur.fetchone() is None):
        if(user == 'quit()'):
            return
        user = raw_input("Invalid Username. Enter a valid one\n",).lower()
        cur.execute('''SELECT Username FROM Users WHERE Username = ?''', (user,))

    #if record exists, proceed to prompt for a password
    password = raw_input("Enter your password\n")

    cur.execute('''SELECT * FROM Users WHERE Username = ? AND Password = ?''', (user, password,))    
    while(cur.fetchone() is None):
        if(password == 'quit()'):
            return
        password = raw_input("Invalid password. Try again\n")
        cur.execute('''SELECT * FROM Users WHERE Username = ? AND Password = ?''', (user, password,))    

    global playerId

    query = cur.execute('''SELECT * FROM Users WHERE Username = ? AND Password = ?''', (user, password,))    

    #assigns the playerId as the User_Id int
    playerId = query.fetchone()[0]
    print "Login successful" 

    try:
        #retrieves the jsonfile from the UserData table 
        query = cur.execute('''SELECT json_value FROM UserData WHERE User_Id = ?''', (playerId,))    
        json_file = query.fetchone()[0]
        print "Save file loaded"
        return json_file
    except:
        #creates a new row in the Userdata table for the new player
        print "No previous save file\n"
        cur.execute('''INSERT INTO UserData(User_Id) VALUES(?)''', (playerId,))
        print "A new file has been created"        
        return None

def save(json_file, data):
    """ Saves the current game by updating the user's table row
        with the new data """
    
    with open(json_file, 'w') as fp:
        saved_file = json.dumps(data, fp)
        print saved_file
        cur.execute('''UPDATE UserData SET json_value=? WHERE User_Id = ?''', (saved_file, playerId,))
        fp.close()

def displayUserInfo():
    """ Displays the user's play data """
    
    cur.execute('''SELECT * FROM UserData WHERE User_Id = ?''', (playerId,))

    data = cur.fetchone()

    for col in data:
        print col

def displayUserTable():
    """ Displays all the users/passwords """

    cur.execute('''SELECT * FROM Users''')

    data = cur.fetchall()
    for row in data:
        for col in row:
            print col,
        print '\n'
