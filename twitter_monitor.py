from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import db_common
import sys
import time
from pathlib import Path
import constants
import common
import utilities

# Core database object
db_obj = None


# step 1.
def db_checking():
    print("Checking database")
    db_obj = db_common.database()
    return db_obj.db_table_exist()


# step 3.
def start_account_crawling(driver=None):

    while True:
        db_obj = db_common.database()
        accounts = db_obj.get_twitter_accounts()

        for account in accounts:
            try:
                id = account[0]
                account_name = account[1]
                followers_str = account[3]
                print(f'Id : {id} Account_name : {account_name}')


                # Pausing program for sometime after every 15 accounts to prevent account ban
                utilities.pause_program_after_sometime(id)

                # Opening the Twitter account
                driver.get(f'https://twitter.com/{account_name}')
                time.sleep(2)

                # Clicking on the following button
                followersButton = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Followers")]')))
                followersButton.click()
                time.sleep(5)

                # step 1. Getting followers links from the portal
                # Wait for the 'find_followers_div' element to be located and visible
                find_followers_div = WebDriverWait(driver, 60).until(
                    EC.visibility_of_element_located((By.XPATH,
                                                      "//div[@class='css-1dbjc4n r-1oszu61 r-1niwhzg r-18u37iz r-16y2uox r-1wtj0ep r-2llsf r-13qz1uu']"))
                )

                # Find elements within the 'find_followers_div' using a wait
                links = WebDriverWait(find_followers_div, 60).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH,
                         './/a[@class="css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l"]'))
                )

                # step 2. get all link in list
                new_followers_links = utilities.get_followers_list(links)
                followers_set_obj = set(followers_str.split(', '))

                # step 3:separating new followers from previous ones here
                new_followers_links -= followers_set_obj

                if new_followers_links:
                    print(f"New followers for account '{account_name}':")

                    for follower in new_followers_links:
                        print(follower)

                    new_followers = ', '.join([followers_str] + list(new_followers_links))
                    # updating existing followers in the database
                    db_obj.update_account_fromfollowers_stringobj_byid(id, new_followers)

                    # adding new followers into table's new_followers_account column
                    db_obj.update_new_followers_account_byid(id, list(new_followers_links))

                    # step 4: updating status column here
                    db_obj.update_currentstatus_byid(id,"waiting for process")

                else:
                    print(f"No New followers found for account '{account_name}':")

                print("******************************\n******************************")

                time.sleep(60)

            except:
                print("Account not found")
                continue


if __name__ == "__main__":
    # get args
    option_string = sys.argv[1:]

    # step 1. Check database is existed
    if db_checking():
        # step 2. get chrome driver
        driver_obj = common.get_driver2()
        # step 3. login on the platform
        common.platform_login(driver=driver_obj)
        # step 4.
        start_account_crawling(driver=driver_obj)

    else:
        print("Unable to find database.")



