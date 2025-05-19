import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials

# Configuration des autorisations Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Ouvrir le Google Sheets
spreadsheet_id = "1R1Pk1jDeuInON_4HT8doLiiUja4d0lczkVnb-KN4XcA"
sheet = client.open_by_key(spreadsheet_id).worksheet("Réponses au formulaire 1")

# Récupérer la date actuelle au format correspondant à Google Sheets
today = datetime.datetime.today().strftime("%d/%m/%Y")  # Adapter si nécessaire

# Extraction des valeurs des colonnes A (Horodateur) et E (Numéros de téléphone)
timestamps = sheet.col_values(1)[1:]  # Colonne A (Horodateur), en ignorant l'en-tête
phone_numbers = sheet.col_values(5)[1:]  # Colonne E (Numéro de téléphone)

# Filtrer les numéros correspondant à la date d'aujourd'hui
filtered_numbers = [phone_numbers[i] for i in range(len(timestamps)) if timestamps[i].split(" ")[0] == today]

# Affichage des numéros filtrés
print("Numéros de téléphone extraits aujourd'hui :", filtered_numbers)
