from datetime import datetime
import matplotlib.pyplot as plt

# Exemple de données simulées (remplace ça par tes vraies données de l’API)
posts_data = [
    {"jour de publication": 1712505600, "stats": {"likes": 12000}},
    {"jour de publication": 1712512800, "stats": {"likes": 9000}},
    {"jour de publication": 1712520000, "stats": {"likes": 15000}},
    {"jour de publication": 1712527200, "stats": {"likes": 4000}},
    # Ajoute ici les données de tous tes posts TikTok/Instagram
]

# On extrait l’heure et les likes
hours = []
likes = []

for post in posts_data:
    timestamp = post["jour de publication"]
    dt = datetime.fromtimestamp(timestamp)
    hours.append(dt.hour)
    likes.append(post["stats"]["likes"])

# On affiche le graphique
plt.scatter(hours, likes, color='green')
plt.xlabel("Heure de publication (0-23)")
plt.ylabel("Nombre de likes")
plt.title("Engagement (likes) par heure de publication")
plt.grid(True)
plt.show()
