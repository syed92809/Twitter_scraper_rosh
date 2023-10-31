import db_common
import sys
import time
import pandas as pd
from pathlib import Path
import constants
import common
import utilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# step 1.
def db_operation():
    print("initialized database")
    db = db_common.database()
    db.db_init()
    return db

# step 2.
def dump_csv_into_database(file_name="users_20230726-032240.csv", database=None):
    print("starting inserting data into database")
    path = Path(file_name)
    if path.is_file():
        dataframe = pd.read_csv(file_name)
        # on each trend title
        for index, row in dataframe.iterrows():
            database.insert_new_account(row[0],constants.DB_STATUS_PENDING)
    else:
        print("Twitter Account is missing.")


# step 4.
def get_account_followers(driver=None, database=None):
    accounts = database.get_twitter_accounts()
    for account in accounts:
        id = account[0]
        account_name = account[1]
        print(f'Id : {id} Account_name : {account_name}')

        try:
            # Pausing program for sometime after every 15 accounts to prevent account ban
            utilities.pause_program_after_sometime(id)

            # Opening the Twitter account
            driver.get(f'https://twitter.com/{account_name}/followers')
            time.sleep(10)

            # step 1. Getting followers links from the portal
            # Wait for the 'find_followers_div' element to be located and visible
            find_followers_div = WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "//div[@class='css-1dbjc4n r-1oszu61 r-1niwhzg r-18u37iz r-16y2uox r-1wtj0ep r-2llsf r-13qz1uu']"))
            )

            # Find elements within the 'find_followers_div' using a wait
            links = WebDriverWait(find_followers_div, 60).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, './/a[@class="css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l"]'))
            )

            # step 2. get all link in set object form
            followers_links = utilities.get_followers_list(links)
            #complete followers
            print("--------------")
            print(followers_links)

            # step 3. update followers for respective the account
            database.insert_into_accounts_by_id(id, followers_links)
            time.sleep(30)
        except Exception as e:
            print("Account not found:", e)

if __name__ == "__main__":
    # get args
    option_string = sys.argv[1:]
    db = None
    print(option_string[0])
    #"RefreshDB_Execution", "ExistingDB_Execution"
    if option_string[0] == constants.DB_Refresh_Execution:
        # step 1. init database operations
        db = db_operation()
        # step 2. read csv file and dump into database
        dump_csv_into_database(file_name="users_20230726-032240.csv", database=db)
    # step 2.a get chrome driver
    driver_obj = common.get_driver2()
    # step 3. login on the platform
    common.platform_login(driver=driver_obj)
    # step 4. get account follower and save in the database
    get_account_followers(driver=driver_obj, database=db)