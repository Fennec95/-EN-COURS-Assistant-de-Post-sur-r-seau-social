from ensembledata.api import EDClient

# Mets ton vrai token ici
client = EDClient("AgAbsqPqxhVbr0YV")

# TikTok - data d’un utilisateur public
tiktok_data = client.tiktok.user_info_from_username(username="daviddobrik")
print("TikTok:", tiktok_data.data)

# Instagram - data d’un compte public
insta_data = client.instagram.user_info(username="nasa")
print("Instagram:", insta_data.data)

# YouTube - subscribers d’une chaîne publique
yt_data = client.youtube.channel_subscribers(channel_id="UCnQghMm3Z164JFhScQYFTBw")
print("YouTube:", yt_data.data)

print("🔵 TikTok:")
print("Nom:", tiktok_data.data["user"]["nickname"])
print("Followers:", tiktok_data.data["stats"]["followerCount"])
print("Likes:", tiktok_data.data["stats"]["heartCount"])

print("\n🟣 Instagram:")
print("Nom:", insta_data.data["full_name"])
print("Followers: [non inclus dans réponse trial]")

print("\n🔴 YouTube:")
print("Abonnés:", yt_data.data)

