import constants
import sqlite3

class database:
    def __init__(self, database_name=constants.sqlite_db_name):
       self.conn = sqlite3.connect(database_name, check_same_thread=False)
       self.cursor = self.conn.cursor()
    
    def db_table_exist(self):
        #get the count of tables with the name
        try:
            self.cursor.execute('Select * from accounts')
            return True
        except Exception as e:        
            return False
    
    def db_close(self):
        self.conn.close()

    def db_init(self):
        if self.db_table_exist() == False:
            self.cursor.execute('''CREATE TABLE accounts
                (id INTEGER PRIMARY KEY autoincrement,                
                account_name        CHAR(400),
                status              CHAR(20),
                followers          TEXT,
                new_followers_account          TEXT);''')
            print("Table created successfully")

    def last_record(self):
        self.cursor.execute("SELECT * FROM accounts ORDER BY ID DESC LIMIT 1;")
        return self.cursor.fetchone()

    # get all records from this table
    def get_twitter_accounts(self):
        self.cursor.execute("SELECT * FROM accounts WHERE status = 'completed' OR status = 'PENDING';")
        return self.cursor.fetchall()

    # get all records from this table
    def get_twitter_accounts_for_details(self):
        self.cursor.execute("SELECT * FROM accounts WHERE status = 'waiting for process';")
        return self.cursor.fetchall()

    # getting new Twitter accounts
    def get_new_twitter_accounts(self):
        self.cursor.execute("SELECT * FROM accounts WHERE status = 'PENDING';")
        return self.cursor.fetchall()

    # updating new_followers_account column
    def update_new_followers_account_byid(self, id, new_followers_links):
        self.cursor.execute("UPDATE accounts SET new_followers_account = ? WHERE id = ?",(', '.join(new_followers_links), id))
        self.conn.commit()
        print(f'Updated new_follower_accounts for Id {id}.')

    # updating follwoers column here
    def update_account_fromfollowers_stringobj_byid(self, id, new_followers):
        self.cursor.execute("UPDATE accounts SET followers = '{}' WHERE id = {}".format(new_followers, id))
        self.conn.commit()
        print(f'updated follower_accounts for Id {id}.')


    def update_account_fromfollowers_listobject_byid(self, id, new_followers):
        self.cursor.execute("UPDATE accounts SET followers = '{}' WHERE id = {}".format(', '.join(new_followers), id))
        self.conn.commit()
        print(f'update follower_accounts for {id}.')

    # updating status column here
    def update_currentstatus_byid(self, id, status):               
        self.cursor.execute("UPDATE accounts SET status = '{}' WHERE id = {}".format(status, id))
        self.conn.commit()
        print(f'updated status for ID {id}.')

    def insert_new_account(self, account_name, status):        
        self.cursor.execute(
            "insert into accounts (account_name, status) values (?, ?)",
            (account_name, status)
        )
        self.conn.commit()
        print(f'insert data, {account_name} {status}.')

    # inserting follwoers into table from initial_datascraper file
    def insert_into_accounts_by_id(self, id, followers_links):
        self.cursor.execute("UPDATE accounts SET followers = ? WHERE id = ?", (', '.join(followers_links), id))
        self.conn.commit()
        print(f'inserted followers for ID {id}.')

    def get_highest_number_of_follower_account(self,id):
        self.cursor.execute("SELECT new_followers_account FROM accounts WHERE id = ?", (id,))
        row = self.cursor.fetchone()
        followers_count = len(row[0].split(', '))
        return followers_count

    def remove_duplicates(self):
        self.cursor.execute("UPDATE accounts SET new_followers_account = REPLACE(LOWER(new_followers_account), 'mamakirani2', '') WHERE LOWER(new_followers_account) LIKE '%mamakirani2%';")
        self.conn.commit()
        print("Duplicates removed.")    
    
 

db=database()
db.remove_duplicates()


