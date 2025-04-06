from ensembledata.api import EDClient
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ENSEMBLEDATA_API_KEY")
client = EDClient(API_KEY)


def get_instagram_info(username: str):
    result = client.instagram.user_info(username=username)
    return result.data

def get_tiktok_info(username: str):
    result = client.tiktok.user_info_from_username(username=username)
    return result.data

def get_youtube_subscribers(channel_id: str):
    result = client.youtube.channel_subscribers(channel_id=channel_id)
    return result.data
