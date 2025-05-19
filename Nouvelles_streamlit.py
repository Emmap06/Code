import streamlit as st
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

# Interface Streamlit
st.title("📊 Suivi des nouvelles entrées dans Google Sheets")
st.write("Ce programme détecte en temps réel l'ajout de nouvelles données.")

# Bouton pour stopper le script
stop_script = st.button("Arrêter la surveillance")

# Fonction de détection des nouvelles entrées
def extract_new_entries():
    global previous_last_row, start_time
    
    all_values = sheet.get_all_values()
    current_last_row = len(all_values)

    if current_last_row > previous_last_row:
        new_rows = range(previous_last_row, current_last_row)

        for row in new_rows:
            timestamp = all_values[row][0]  # Colonne A (Horodateur)
            phone_number = all_values[row][4]  # Colonne E (Numéro de téléphone)

            st.write(f"🆕 **Nouvelle entrée détectée !** 📅 {timestamp} | 📞 {phone_number}")
        
        previous_last_row = current_last_row
        start_time = time.time()
    elif time.time() - start_time > 3600:
        st.warning("🚨 Aucune nouvelle entrée après 15 secondes. Arrêt du script.")
        st.stop()

# Boucle d'attente continue avec Streamlit
while not stop_script:
    extract_new_entries()
    time.sleep(5)  # Vérification toutes les 5 secondes

if __name__ == "__main__":
    st.run()
