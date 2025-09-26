# BankingApp (Python)

Eine einfache Python-Konsolenanwendung zum Verwalten von Bankkonten mit Münzautomaten-Simulation.  
Die App ermöglicht es, Konten zu registrieren, sich einzuloggen, den Kontostand einzusehen, Geld einzuzahlen oder abzuheben.  
Alle Daten werden in einer lokalen JSON-Datei gespeichert.

---

## Features

- **Login & Registrierung**
  - Benutzer melden sich mit einer **8-stelligen Kontonummer** an oder registrieren ein neues Konto.
- **Persistente Speicherung**
  - Konten und Guthaben werden in `accounts.json` gespeichert.
- **Münzbasierte Darstellung**
  - Guthaben wird in Euro-Münzen (2 €, 1 €, 0,50 €, usw.) verwaltet.
- **Einzahlungen & Auszahlungen**
  - Beträge können flexibel eingegeben werden (z. B. `3,76` oder `3.76`).
  - Automatische Neuberechnung der Münzverteilung.
- **Übersicht**
  - Anzeige des aktuellen Kontostands in Tabellenform oder als Gesamtbetrag.

---

## Installation

1. **Repository klonen**  
   ```bash
   git clone https://github.com/<dein-benutzername>/BankingApp.git
   cd BankingApp
   ```

2. **Python-Version prüfen**  
   Stelle sicher, dass **Python 3.8+** installiert ist:  
   ```bash
   python --version
   ```

3. **App starten**  
   ```bash
   python main.py
   ```

---

## Nutzung

Nach dem Start der Anwendung erscheint ein Willkommensbildschirm:

```text
Willkommen beim Münzautomaten.

Bitte Kontonummer (8 Ziffern):
```

- **Neue Kontonummer eingeben** → Konto wird erstellt.  
- **Vorhandene Kontonummer eingeben** → Login ins bestehende Konto.  

### Hauptmenü

```text
Wie kann ich Ihnen helfen?
1 - Übersicht
2 - Einzahlen
3 - Auszahlen
4 - Logout
5 - Exit
```

#### 1 - Übersicht  
Zeigt den Kontostand in einer Münztabelle an.  

#### 2 - Einzahlen  
Eingabe eines Betrags, z. B.:  
```
3,76
```

#### 3 - Auszahlen  
Eingabe eines gewünschten Auszahlungsbetrags. Die App prüft, ob genügend Guthaben vorhanden ist.  

#### 4 - Logout  
Abmelden und mit einem anderen Konto einloggen.  

#### 5 - Exit  
Speichert alle Änderungen und beendet die Anwendung.  

---

## Dateien

- **main.py** – Hauptprogramm (Bankautomaten-Logik)  
- **accounts.json** – Speicherdatei mit allen Konten (automatisch angelegt)  

---

## Beispiel

```text
Willkommen beim Münzautomaten.

Bitte Kontonummer (8 Ziffern):
12345678

Kontonummer nicht gefunden.

Bitte wählen (Login | Register | Exit):
register
Bitte geben Sie Ihren Namen ein:
Max Mustermann
acc erfolgreich erstellt. Willkommen Max Mustermann.

Wie kann ich Ihnen helfen?
1 - Übersicht
2 - Einzahlen
3 - Auszahlen
4 - Logout
5 - Exit
```

---

## ToDo / Erweiterungen

- PIN-Schutz für Konten  
- Unterstützung für Banknoten  
- GUI-Version (z. B. mit Tkinter oder PyQt)  
- Unit Tests  
