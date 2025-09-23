from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import json
import os

# Datei mit allen Accounts (JSON-Speicher)
ACCOUNTS_FILE = 'accounts.json'
accounts = {}
active_acc = None
acc_coins = None

# --- JSON-Funktionen ---
# Laden
def load_accounts():
  global accounts
  if os.path.exists(ACCOUNTS_FILE):
    try:
      with open(ACCOUNTS_FILE, 'r') as f:
        accounts = json.load(f)
    except json.JSONDecodeError:
      print('Fehlerhafte JSON-Datei. Starte mit leeren Accounts.')

# Speichern
def save_accounts():
  with open(ACCOUNTS_FILE, 'w') as f:
    json.dump(accounts, f, indent=2)

# Neuen Account erstellen
def create_acc(acc_number, name):
  accounts[acc_number] = {
    "name": name,
    "acc_coins": {k: 0 for k in COINS_TEMPLATE}
  }
  save_accounts()

# Login- oder Registrierungsdialog
def login_or_register():
  while True:
    acc = ask_acc_number()

    if acc in accounts:
      # Login
      acc_coins = accounts[acc]['acc_coins']
      name = accounts[acc].get('name', 'Unbekannt')
      print(f"Hallo {name}.")
      return acc, acc_coins, name
    else:
      # acc nicht gefunden → Optionen
      choice = input('Kontonummer nicht gefunden.\n\nBitte wählen (Login | Register | Exit):\n').strip().lower()
      if choice == 'login':
        # zurück zum Start
        continue
      elif choice == 'register':
        name = input('Bitte geben Sie Ihren Namen ein:\n').strip()
        create_acc(acc, name)
        print(f'acc erfolgreich erstellt. Willkommen {name}.')
        acc_coins = accounts[acc]['acc_coins']
        return acc, acc_coins, name
      elif choice == 'exit':
        print('Vielen Dank. Auf Wiedersehen.')
        exit()
      else:
        print('Ungültige Eingabe. Bitte "Login", "Register" oder "Exit" eingeben.')

# --- Alte Version der Kontonummer-Abfrage ---
# Diese Version funktioniert ohne JSON-Datei und prüft nur eine 8-stellige Zahl.
# 
# print('Bitte Kontonummer eingeben:')
# while True:
#   try:
#     acc = input('')
#     if acc.isdigit():
#       if len(acc) == 8:
#         print('Willkommen!')
#         break
#       else:
#         print('Eine Kontonummer besteht aus 8 Ziffern.')
#   except ValueError:
#     print('Ungültige Eingabe! Bitte nur Ziffern eingeben.')

# --- Account Coins-Template und Werte ---
COINS_TEMPLATE = {
  '2': 0,
  '1': 0,
  '0.5': 0,
  '0.2': 0,
  '0.1': 0,
  '0.05': 0,
  '0.02': 0,
  '0.01': 0
}
labels = {
  '2': '2.00 €',
  '1': '1.00 €',
  '0.5': '0.50 €',
  '0.2': '0.20 €',
  '0.1': '0.10 €',
  '0.05': '0.05 €',
  '0.02': '0.02 €',
  '0.01': '0.01 €'
}
values = {
  '2': 200,
  '1': 100,
  '0.5': 50,
  '0.2': 20,
  '0.1': 10,
  '0.05': 5,
  '0.02': 2,
  '0.01': 1
}
denom_list = list(values.items())

# Betrag als Euro-Betrag mit 2 Nachkommastellen formatieren
def format_eur(amount):
  return str(Decimal(amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)).replace('.', ',')

# Eingabe einer gültigen Kontonummer (8-stellig)
def ask_acc_number():
  while True:
    acc = input('Bitte Kontonummer (8 Ziffern):\n').strip()
    if acc.isdigit() and len(acc) == 8:
      return acc
    print("Ungültige Eingabe. Eine Kontonummer muss genau 8 Ziffern enthalten.")

# Gesamtkontostand in Cent berechnen
def get_total_cents():
  return sum(acc_coins[k] * values[k] for k in acc_coins)

# Kontostand in Coins neu aufteilen
def redistribute(total_cents):
  for k in acc_coins:
    acc_coins[k] = 0
  remaining = total_cents
  for key, val in denom_list:
    use = remaining // val
    if use > 0:
      acc_coins[key] = use
      remaining -= use * val

# Aktuellen Kontostand anzeigen
def show_acc(show_table=True):
  total_cents = get_total_cents()
  if show_table:
    print("\nAktueller Kontostand:\n")
    print("Wert      |  Anzahl")
    print("-------------------")
    for key, _ in denom_list:
      print(f"{labels[key]:<8}  |  {acc_coins[key]:>6}")
    print("-------------------")
    print(f"Gesamt: {format_eur(total_cents/100)} €")
  else:
    print(f"{format_eur(total_cents/100)} €")

# Einzahlung
def deposit():
  global acc_coins
  raw = input('\nWelchen Betrag möchten Sie einzahlen (z.B. 3,76 / 3.76):\n').strip().replace(',', '.')
  try:
    amount_dec = Decimal(raw).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
  except InvalidOperation:
    print('Ungültiger Betrag.')
    return
  if amount_dec <= 0:
    print('Betrag muss größer als 0 sein.')
    return

  add_cents = int((amount_dec * Decimal('100')).to_integral_value(rounding=ROUND_HALF_UP))
  total_cents = get_total_cents() + add_cents
  redistribute(total_cents)
  accounts[active_acc]['acc_coins'] = acc_coins
  save_accounts()

  print('\nEinzahlung erfolgreich.')
  print('-------------------')
  print(f"Gesamt: {format_eur(add_cents/100)} €")
  print("===================\n")
  print('Neuer Kontostand:\n-------------------')
  show_acc(show_table=False)

# Auszahlung
def withdraw():
  global acc_coins
  total_cents = get_total_cents()
  print('\n\nAktueller Kontostand:\n-------------------')
  show_acc(show_table=False)

  raw = input('\nWelchen Betrag möchten Sie auszahlen (z.B. 3,76 / 3.76):\n').strip().replace(',', '.')
  try:
    amount_dec = Decimal(raw).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
  except InvalidOperation:
    print('Ungültiger Betrag.')
    return
  if amount_dec <= 0:
    print('Betrag muss größer als 0 sein.')
    return

  cents = int((amount_dec * Decimal("100")).to_integral_value(rounding=ROUND_HALF_UP))
  if cents > total_cents:
    print('Auszahlung fehlgeschlagen.\nNicht genügend Guthaben.')
    return

  new_total = total_cents - cents
  redistribute(new_total)
  accounts[active_acc]['acc_coins'] = acc_coins
  save_accounts()

  print('\nAuszahlung erfolgreich.')
  print('-------------------')
  print(f"Gesamt: {format_eur(cents/100)} €")
  print("===================\n")
  print('Neuer Kontostand:\n-------------------')
  show_acc(show_table=False)

# ---- Login / Registrierung ----
load_accounts()
print('Willkommen beim Münzautomaten.\n')
active_acc, acc_coins, name = login_or_register()

# ---- Hauptmenü ----
while True:
  print('\nWie kann ich Ihnen helfen?')
  print('1 - Übersicht')
  print('2 - Einzahlen')
  print('3 - Auszahlen')
  print('4 - Logout')
  print('5 - Exit')
  print('Bitte wählen:')

  try:
    choice = int(input(''))
  except ValueError:
    print('Bitte eine Zahl eingeben.')
    continue

  if choice == 1:
    show_acc(show_table=True)
  elif choice == 2:
    deposit()
  elif choice == 3:
    withdraw()
  elif choice == 4:
    save_accounts()
    print('Sie wurden ausgeloggt.\n')
    active_acc, acc_coins, name = login_or_register()
  elif choice == 5:
    save_accounts()
    print('Vielen Dank. Auf Wiedersehen!')
    break
  else:
    print('Ungültige Auswahl. Bitte 1-5 wählen.')
