import random
import time

restricted_accounts = ['0x00Sik', 'WaseembadamiFa9', 'bilal_mahrvi', 'MoonisElahi6', 'realdogen', 'Naya__Pakistan_',
                       'dao_times', 'navalbukhari3', 'RaiMAliPTI', 'UnderCsPaksitani', 'Mianjan09052208', 'ShkhRasheed', 'SdqJaan', 'AnwarLodhi', 'FarrukhHabibISF','siasatpk']


def get_followers_list(links):
    followers_links = set()
    for link in links:
        href = link.get_attribute('href')
        if href not in followers_links:
            account_username = href.split('/')[-1]
            if account_username not in restricted_accounts:
                followers_links.add(account_username)
            else:
                continue

    return followers_links

def pause_program_after_sometime(id):
    if id % 15 ==0:
        sleep=random.randint(60,90)
        print("Pausing program for ", sleep, "seconds before next account...")
        time.sleep(sleep)


