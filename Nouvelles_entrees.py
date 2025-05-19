import gspread
import time
import datetime
from oauth2client.service_account import ServiceAccountCredentials

# Configuration des autorisations Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Ouvrir le Google Sheets
spreadsheet_id = "1R1Pk1jDeuInON_4HT8doLiiUja4d0lczkVnb-KN4XcA"
sheet = client.open_by_key(spreadsheet_id).worksheet("Réponses au formulaire 1")

# Stocker la dernière ligne connue
previous_last_row = len(sheet.get_all_values())
start_time = time.time()

def extract_new_entries():
    global previous_last_row, start_time
    
    # Récupérer toutes les valeurs de la feuille
    all_values = sheet.get_all_values()
    current_last_row = len(all_values)

    if current_last_row > previous_last_row:
        # Identifier les nouvelles lignes ajoutées
        new_rows = range(previous_last_row, current_last_row)

        for row in new_rows:
            timestamp = all_values[row][0]  # Colonne A (Horodateur)
            phone_number = all_values[row][4]  # Colonne E (Numéro de téléphone)

            print(f"Nouvelle entrée détectée - Horodateur : {timestamp}, Numéro : {phone_number}")
        
        # Mettre à jour la dernière ligne connue et réinitialiser le timer
        previous_last_row = current_last_row
        start_time = time.time()
    elif time.time() - start_time > 15:
        print("Aucune nouvelle entrée après 15 secondes. Arrêt du script.")
        exit()

# Boucle d'attente continue pour détecter les nouvelles entrées
while True:
    extract_new_entries()
    time.sleep(5)  # Vérification toutes les 5 secondes
