from discordwebhook import Discord
import constants
import utilities

raw_feed_discord = Discord(url=constants.RAW_FEED_DISCORD_CHANNEL)
hot_account_discord=Discord(url=constants.HOT_ACCOUNTS_DISCORD_CHANNEL)


# function for raw feed accounts
def send_account_details_to_raw_feed(account_name,account_url,followed_by,account_profile_image,number_of_followers,number_of_tweets,description,account_created_date):
    reverse_search_text = "Profile Image"
    raw_feed_discord.post(

        embeds=[
            {
                "author": {
                    "name": f"{account_name}",
                    "url": f"{account_url}",
                    "icon_url": f"{account_profile_image}",
                },
                # "title": "Embed Title",
                "description": f"{description}",
                "fields": [
                    {"name": "Followers", "value": f"{number_of_followers}", "inline": True},
                    {"name": "Tweets", "value": f"{number_of_tweets}", "inline": True},
                    {"name": "Followed by", "value": f"{followed_by}", "inline": True},
                    {"name": "Created", "value": f"{account_created_date}", "inline": True},
                    {"name": "\u200b", "value": "\u200b", "inline": True},  # Empty field for alignment
                    {"name": "Reverse search", "value": f"[{reverse_search_text}]({account_profile_image})",
                     "inline": True},

                ],
                "thumbnail": {"url": f"{account_profile_image}"},
                # "image": {"url": "https://picsum.photos/400/300"},
                # "footer": {
                #     "text": "Embed Footer",
                #     "icon_url": "https://picsum.photos/20/20",
                # },
            }
        ],)

# function for hot accounts
def send_account_details_to_hot_accounts_channel(account_name,account_url,followed_by,account_profile_image,number_of_followers,number_of_tweets,description,account_created_date):

    reverse_search_text = "Profile Image"

    hot_account_discord.post(

        embeds=[
            {
                "author": {
                    "name": f"{account_name}",
                    "url": f"{account_url}",
                    "icon_url": f"{account_profile_image}",
                },
                # "title": "Embed Title",
                "description": f"{description}",
                "fields": [
                    {"name": "Followers", "value": f"{number_of_followers}", "inline": True},
                    {"name": "Tweets", "value": f"{number_of_tweets}", "inline": True},
                    {"name": "Followed by", "value": f"{followed_by}", "inline": True},
                    {"name": "Created", "value": f"{account_created_date}", "inline": True},
                    {"name": "\u200b", "value": "\u200b", "inline": True},  # Empty field for alignment
                    {"name": "Reverse search", "value": f"[{reverse_search_text}]({account_profile_image})",
                     "inline": True},

                ],
                "thumbnail": {"url": f"{account_profile_image}"},
                # "image": {"url": "https://picsum.photos/400/300"},
                # "footer": {
                #     "text": "Embed Footer",
                #     "icon_url": "https://picsum.photos/20/20",
                # },
            }
        ],
    )

