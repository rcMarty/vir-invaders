# Dokumentace projektu: Vánoční Space Invaders & "Grinch" Ransomware

## 1. Úvod a cíl projektu
Tento projekt byl vytvořen v rámci předmětu **PVBPS**. Cílem bylo demonstrovat komplexní scénář útoku, který využívá techniky **sociálního inženýrství** (vánoční tématika) v kombinaci s moderní exfiltrací dat řízenou **umělou inteligencí (LLM)**.

Aplikace se navenek prezentuje jako hra _**Vánoční Space Invaders**_, zatímco na pozadí operuje ransomware, který inteligentně vytěžuje data a šifruje soubory.

---

## 2. Architektura řešení

Systém je rozdělen do tří hlavních logických celků:

1.  **Klient (Payload):**
    * **Main Wrapper:** Spouštěč, který detekuje prostředí.
    * **Hra:** Interaktivní část pro odvedení pozornosti.
    * **Malware:** Ransomware běžící na pozadí.
2.  **LLM Rozhraní:** Externí API pro sémantickou analýzu citlivosti dat.
3.  **C2 Server (Command & Control):** FastAPI server pro sběr exfiltrovaných dat.

---

## 3. Technická specifikace

### 3.1 Spouštěcí logika (Main Wrapper)
Vstupní bod aplikace (`main.py`) funguje jako orchestrátor procesů.

* **Detekce lokalizace:** Skript kontroluje systémové nastavení jazyka.
    * `if locale.startswith('cs')`: Spouští se **Hra** i **Malware**.
    * `else`: Spouští se **pouze Hra**.
    * *Účel:* Cílení útoku pouze na ČR a ochrana před analýzou v zahraničních sandboxech.
* **Multiprocessing:** Hra a malware běží ve dvou oddělených subprocesech. To zajišťuje, že akce ransomwaru při šifrování nezpůsobí "sekání" hry, což by mohlo uživatele varovat (uživatel by si sice mohl myslet, že hra je v UE5, ale i tak by to mohlo být podezřelé)

### 3.2 Vánoční Space Invaders (Krycí aplikace)
* **Žánr:** 2D Arkáda.
* **Gameplay:** Hráč ovládá postavu "Grinche" a střílí vánoční dárky po přibližujících se naštvaných dětech.
* **Platforma:** Python (PyGame), funkční na Windows i Linux.

### 3.3 Ransomware s LLM analýzou
Škodlivý kód prochází rekurzivně souborový systém od domovského adresáře aktuálního uživatele.

#### Workflow zpracování souboru:
1.  **Kontrola stavu:** Malware zkontroluje hlavičku souboru na přítomnost vlastního markeru (signatury). Pokud je soubor již zašifrován, je přeskočen.
2.  **LLM Triage (Analýza citlivosti):**
    * Před zašifrováním se odešlou metadata (název, cesta, velikost) a prvních **100 bytů** obsahu do LLM.
    * **Dotaz na LLM (zjednodušeně):** *"Je tento soubor na základě názvu a obsahu pravděpodobně citlivý?"*
3.  **Exfiltrace dat:**
    * Pokud LLM odpoví kladně, soubor se odesílá na C2 server.
    * Odesílání probíhá ve **streamu po 1MB chuncích** (prevence zaplnění RAM).
4.  **Šifrování:**
    * Soubor je zašifrován (AES) a označen markerem (prepend).
    * Původní obsah je přepsán šifrovanými daty.

### 3.4 C2 Server (Backend)
Server je napsán v frameworku **FastAPI** pro vysoký výkon a asynchronní zpracování requestů.

* **Ukládání dat:**
    * Server vytváří pro každého klienta unikátní složku (na základě klientem generovaného UUID).
    * Zachovává originální adresářovou strukturu exfiltrovaných souborů.
* **Endpoint:** Přijímají streamovaná data a rekonstruují binární soubory na disku serveru.

---

## 4. Bezpečnostní a implementační detaily

* **Multiplatformní podpora:** Kód je navržen tak, aby fungoval na OS Windows i Linux.
* **Streamování:** Odesílání velkých souborů po částech (chunks) zajišťuje stabilitu i na pomalejším připojení a snižuje nápadnost síťového provozu.
* **Selektivní útok:** Díky LLM se neodesílá "smetí" (systémové soubory, instalátory her), ale pouze potenciálně hodnotná data, což snižuje riziko detekce a zvyšuje efektivitu útoku.

