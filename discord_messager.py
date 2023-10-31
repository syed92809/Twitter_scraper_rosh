from selenium.webdriver.common.by import By
import db_common
import sys
import time
import message_sender
import constants
import common
import twitter_monitor
import utilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def start_scraping_new_account_details(driver=None):

    while True:
        # step 1: create instance of database class
        db_obj = db_common.database()

        #step 2: get new followers record form database
        accounts = db_obj.get_twitter_accounts_for_details()

        for account in accounts:
            id = account[0]
            followed_by=account[1]
            new_followers = account[4]
            get_each_follower_name=new_followers.split(', ')

            # getting new_followers_account counts here
            get_follower_count = db_obj.get_highest_number_of_follower_account(id)


            # step 3: separate each follower in a row
            for follower in get_each_follower_name:

                print(f'Followers for ID: {id}')


                # step 3: open each account to get their details

                try:

                    # Pausing program for sometime after every 15 accounts to prevent account ban
                    utilities.pause_program_after_sometime(id)

                    # Opening the Twitter account
                    account_url=(f'https://twitter.com/{follower}')
                    driver.get(account_url)
                    time.sleep(10)

                    try:
                        # Getting No. of Tweets
                        tweet_element = WebDriverWait(driver, 60).until(
                            EC.presence_of_element_located((By.XPATH, '//div[@class="css-1dbjc4n r-1habvwh"]'))
                        )
                        tweet_text = tweet_element.text

                        # Extract the number of posts from the text
                        tweet = tweet_text.split('\n')[-1].split()[0]
                        print("Number of Posts:", tweet)
                    except:
                        print("No tweets found")


                    # Getting Image Link
                    try:
                        find_img_element=driver.find_element(By.XPATH, "//div[@aria-label='Opens profile photo']")
                        image_element = find_img_element.find_element(By.XPATH, ".//img[@alt='Opens profile photo']")
                        account_profile_image = image_element.get_attribute("src")
                        print(account_profile_image)

                    except:
                        print("No profile image found")

                    # Getting No. of Followers
                    followers = driver.find_elements(By.XPATH, f'//a[@href="/{follower}/followers"]')
                    for inner_spans in followers:
                        num_of_followers=inner_spans.text
                        print(num_of_followers)

                    # Get Description
                    desc = driver.find_elements(By.XPATH, '//div[@data-testid="UserDescription"]')
                    for inner_span in desc:
                        account_description=inner_span.text.strip()
                        print(account_description)

                    # Get User Join Date
                    date = driver.find_elements(By.XPATH, '//span[@data-testid="UserJoinDate"]')
                    for inner_spane in date:
                        created_date=inner_spane.text
                        print(created_date)

                    print("********************")

                    # Step 4: send account details to their respective discord channel

                    if get_follower_count >= 5:
                        message_sender.send_account_details_to_hot_accounts_channel(follower,account_url,followed_by,account_profile_image,num_of_followers,tweet,account_description,created_date)
                    else:
                        message_sender.send_account_details_to_raw_feed(follower,account_url,followed_by,account_profile_image,num_of_followers,tweet,account_description,created_date)

                    time.sleep(300)

                except Exception as e:
                    print(e)

            # calling update status fucntion here
            db_obj.update_currentstatus_byid(id, "completed")


if __name__ == "__main__":

    # step 1: check if database exist
    if twitter_monitor.db_checking():

        # step 2: get chrome driver from common.py file
        driver_obj=common.get_driver2()

        # step 3: perform login operation
        common.platform_login(driver=driver_obj)

        # step4: start scraping of new accounts
        start_scraping_new_account_details(driver=driver_obj)