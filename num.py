import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuration des autorisations Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Ouvrir le Google Sheets avec l'ID du document
spreadsheet_id = "1R1Pk1jDeuInON_4HT8doLiiUja4d0lczkVnb-KN4XcA"
sheet = client.open_by_key(spreadsheet_id).worksheet("Réponses au formulaire 1")  # Nom corrigé !

# Extraction des numéros de téléphone depuis la colonne E
phone_numbers = sheet.col_values(5)[1:]  # Colonne E (index 5), en ignorant l'en-tête

# Affichage des numéros extraits
print("Numéros de téléphone extraits :", phone_numbers)
