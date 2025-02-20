import ijson
import json
import re
import os

# Lista województw bez polskich znaków
wojewodztwa = [
    "dolnoslaskie", "kujawsko_pomorskie", "lubelskie", "lubuskie", "lodzkie", "malopolskie", 
    "mazowieckie", "opolskie", "podkarpackie", "podlaskie", "pomorskie", "slaskie", 
    "swietokrzyskie", "warminsko_mazurskie", "wielkopolskie", "zachodniopomorskie", "other"
]

# Funkcja czyszcząca JSON z błędnych znaków sterujących
def clean_json(text):
    return re.sub(r'[\x00-\x1F\x7F]', '', text)  # Usuwanie znaków sterujących

# Przetwarzanie plików dla wszystkich województw
for idx, woj in enumerate(wojewodztwa, start=1):
    input_file = f"data_all_{woj}.json"
    output_file = f"data_{woj}.json"
    temp_file = f"temp_cleaned_{woj}.json"
    
    if not os.path.exists(input_file):
        print(f"⚠️ Plik {input_file} nie istnieje, pomijam.")
        continue

    try:
        # Otwórz plik i usuń ewentualne błędne znaki
        with open(input_file, "r", encoding="utf-8-sig") as f:
            raw_text = f.read()
            cleaned_text = clean_json(raw_text)

        # Zapisz oczyszczony JSON do tymczasowego pliku
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

        # Otwórz oczyszczony JSON i przetwarzaj go strumieniowo
        with open(temp_file, "r", encoding="utf-8") as f:
            parser = ijson.items(f, "tblBusinessEntityStats.Detail_Collection.item")
            filtered_records = [record for record in parser if record.get("GlownyKodPkd") == "4776Z"]

        # Tworzenie nowej struktury JSON i zapis do pliku
        filtered_json = {"tblBusinessEntityStats": {"Detail_Collection": filtered_records}}

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(filtered_json, f, ensure_ascii=False, indent=4)

        # Usunięcie pliku tymczasowego
        os.remove(temp_file)
        
        # Usunięcie pliku wejściowego po udanej akcji
        os.remove(input_file)

        print(f"✅ {woj}: przetworzono pomyślnie ({idx}/{len(wojewodztwa)})")
    
    except Exception as e:
        print(f"❌ Błąd podczas przetwarzania {woj}: {e}")