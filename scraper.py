import db_common
import sys


def db_operation():
    print("initialized database")
    db = db_common.database()
    db.db_init()
    return db

if __name__ == "__main__":
    # get args
    input_folder_name = sys.argv[1:]

    # init database operations
    db = db_operation()