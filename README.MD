# MTG Search Tool

Tento nástroj umožňuje automaticky vyhledat kusové karty na webu [cernyrytir.cz](https://cernyrytir.cz) a uložit výsledky do CSV.

## 🧩 Funkce
- Automatické vyhledávání karet podle CSV vstupu
- Získání dostupnosti, ceny a názvu
- Uložení výsledků a výběr nejlepší nabídky do CSV
- Automatické stažení kompatibilního Microsoft Edge WebDriveru

## 📁 Struktura projektu
```
MTG-Search-Tool/
├── mtg_search.py                  # hlavní skript
├── prepare_driver.py              # stáhne msedgedriver odpovídající nainstalované verzi Edge
├── cards.csv                      # seznam karet (jeden název na řádek)
├── driver/                        # sem se uloží msedgedriver.exe
├── out/                           # výstupní CSV soubory
├── installer.iss                  # instalační skript pro Inno Setup
├── README.md                      # tento soubor
└── .gitignore                     # ignoruje nepotřebné soubory
```

## ▶️ Použití

### 1. Stáhni WebDriver
```bash
python prepare_driver.py
```

### 2. Spusť hlavní skript
```bash
python mtg_search.py
```

### 3. Sestavení .exe (volitelné)
```bash
pyinstaller --onefile --add-data "driver/msedgedriver.exe;." mtg_search.py
```

### 4. Vytvoření instalačního balíčku (Inno Setup)
1. Otevři `installer.iss` v Inno Setup
2. Klikni na "Compile"
3. Najdeš `mtg_search_setup.exe` v `OutputDir`

## 📦 Závislosti
- Python 3.8+
- `selenium`
- `pyinstaller` (volitelné)

## 📄 Licence
Tento projekt přibaluje `msedgedriver.exe`, který je součástí Microsoft Edge WebDriver a je distribuován v souladu s jeho licencí.

---

✉️ Pro jakékoli dotazy nebo úpravy mě neváhej kontaktovat.
