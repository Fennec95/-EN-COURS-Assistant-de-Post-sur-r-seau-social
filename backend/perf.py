import os
import csv
from datetime import datetime
from collections import defaultdict
import tkinter as tk
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt

# Configuration
CSV_FILENAME = "historique_publications.csv"
DAYS_FR = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# Initialiser Tkinter (mode silencieux)
root = tk.Tk()
root.withdraw()

# Demander le nombre de publications
try:
    num_points = int(simpledialog.askstring(
        "Nombre de données",
        "Combien de publications veux-tu entrer ?"
    ))
except (TypeError, ValueError):
    messagebox.showerror("Erreur", "Tu dois entrer un nombre valide.")
    exit()

# Collecte des données utilisateur
posts_data = []

for i in range(num_points):
    try:
        date_str = simpledialog.askstring(
            "Date de publication",
            f"Date/heure de la publication #{i + 1} (format : jj/mm/aaaa) :"
        )
        dt = datetime.strptime(date_str, "%d/%m/%Y")
        timestamp = int(dt.timestamp())

        likes = int(simpledialog.askstring(
            "Likes",
            f"Nombre de likes pour la publication #{i + 1} :"
        ))

        posts_data.append({
            "jour de publication": timestamp,
            "date lisible": dt.strftime('%d/%m/%Y'),
            "stats": {"likes": likes}
        })

    except (TypeError, ValueError):
        messagebox.showwarning("Saisie ignorée", "Valeurs invalides, ce point sera ignoré.")
        continue

# Sauvegarde dans un fichier CSV
file_exists = os.path.isfile(CSV_FILENAME)
with open(CSV_FILENAME, mode='a', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    if not file_exists:
        writer.writerow(["timestamp", "date lisible", "likes"])
    for post in posts_data:
        writer.writerow([
            post["jour de publication"],
            post["date lisible"],
            post["stats"]["likes"]
        ])

# Analyse des publications par jour de la semaine
likes_par_jour = defaultdict(list)

for post in posts_data:
    dt = datetime.fromtimestamp(post["jour de publication"])
    jour = dt.weekday()  # 0 = lundi, 6 = dimanche
    likes_par_jour[jour].append(post["stats"]["likes"])

# Calcul de la moyenne des likes par jour
meilleur_jour = None
meilleure_moyenne = 0

print("\nMoyenne des likes par jour de la semaine :\n")

for i in range(7):
    likes = likes_par_jour[i]
    moyenne = sum(likes) / len(likes) if likes else 0
    print(f"{DAYS_FR[i]} : {moyenne:.2f} likes")
    
    if moyenne > meilleure_moyenne:
        meilleure_moyenne = moyenne
        meilleur_jour = DAYS_FR[i]

# Résultat
if meilleur_jour is not None:
    print(f"\nMeilleur jour pour publier : {meilleur_jour} (en moyenne {meilleure_moyenne:.2f} likes)")
else:
    print("\nPas de données disponibles pour déterminer le meilleur jour.")

# Affichage du graphique des likes par jour de la semaine
jours = [DAYS_FR[i] for i in range(7)]
moyenne_par_jour = [sum(likes_par_jour[i]) / len(likes_par_jour[i]) if likes_par_jour[i] else 0 for i in range(7)]

plt.figure(figsize=(10, 5))
plt.bar(jours, moyenne_par_jour, color='green')
plt.xlabel("Jour de la semaine")
plt.ylabel("Moyenne des likes")
plt.title("Moyenne des likes par jour de la semaine")
plt.tight_layout()
plt.show()
