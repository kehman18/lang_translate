import os
from dotenv import load_dotenv
import tweepy
from googletrans import Translator

# Twitter API credentials
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ACCESS_TOKEN = os.getenv('ACESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')

# Authenticate with Twitter API
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Initialize the Google Translate API
translator = Translator()

# Function to process mentions
def process_mentions():
    mentions = api.mentions_timeline(count=5)
    
    for mention in mentions:
        print(f"Bot mentioned by: @{mention.user.screen_name}")
        print(f"Tweet: {mention.text}")

        # Checks to see if the comment is part of a section
        if mention.in_reply_to_status_id:
            original_tweet = api.get_status(mention.in_reply_to_status_id)
            print(f"Original tweet by: @{original_tweet.user.screen_name}")
            print(f"Original tweet text: {original_tweet.text}")

            # Detect language
            detected_lang = translator.detect(original_tweet.text).lang

            # Translate if not in English
            if detected_lang != 'en':
                translated = translator.translate(original_tweet.text, dest='en')
                print(f"Translated tweet: {translated.text}")

                # Reply to the tweet with the translation
                api.update_status(f"@{mention.user.screen_name} @{original_tweet.user.screen_name} {translated.text}", in_reply_to_status_id=mention.id)
        else:
            # If no reply-to tweet, just translate the mention itself
            detected_lang = translator.detect(mention.text).lang

            if detected_lang != 'en':
                translated = translator.translate(mention.text, dest='en')
                api.update_status(f"@{mention.user.screen_name} {translated.text}", in_reply_to_status_id=mention.id)

# Call the function to process bot mentions
process_mentions()
