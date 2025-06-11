import pygame
import random
import sys

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Begriffs-Quiz")
FONT = pygame.font.SysFont("consolas", 40)
SMALL_FONT = pygame.font.SysFont("consolas", 24)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
GREEN = (0, 200, 0)
ORANGE = (255, 165, 0)
RED = (200, 0, 0)
BLUE = (0, 100, 255)

# Wörterbücher für Themen
woerterbuecher = {
    "Python": {
        "class": "Ein Bauplan für Objekte.",
        "tuple": "Eine unveränderliche Liste.",
        "float": "Ein Datentyp für Dezimalzahlen.",
        "break": "Beendet eine Schleife vorzeitig.",
        "yield": "Erzeugt Werte in einer Generator-Funktion.",
        "async": "Markiert eine Funktion für asynchrone Ausführung.",
        "import": "Wird genutzt, um Module einzubinden.",
        "return": "Gibt einen Wert aus einer Funktion zurück.",
        "lambda": "Definiert eine anonyme Funktion.",
        "global": "Ermöglicht Zugriff auf Variablen außerhalb einer Funktion.",
        "dict": "Ein Mapping-Typ für Schlüssel-Wert-Paare.",
        "list": "Eine veränderliche Sammlung von Elementen.",
        "set": "Eine ungeordnete Sammlung einzigartiger Elemente.",
        "int": "Ein Datentyp für ganze Zahlen.",
        "str": "Ein Datentyp für Zeichenketten.",
        "def": "Deklariert eine Funktion.",
        "elif": "Eine zusätzliche Bedingung nach einer if-Abfrage.",
        "try": "Beginnt einen Block zur Fehlerbehandlung.",
        "except": "Fängt eine Ausnahme in einem try-Block ab.",
        "finally": "Wird immer nach try/except ausgeführt.",
        "for": "Eine Schleife, die über eine Sequenz iteriert.",
        "while": "Eine Schleife, die basierend auf einer Bedingung läuft.",
        "with": "Ermöglicht sicheres Ressourcenmanagement.",
        "pass": "Platzhalter ohne Funktion.",
        "continue": "Springt zur nächsten Iteration der Schleife.",
        "super": "Greift auf Methoden der Elternklasse zu.",
        "self": "Referenz auf die aktuelle Instanz einer Klasse.",
        "nonlocal": "Greift auf Variablen aus einer äußeren Funktion zu.",
        "is": "Vergleicht Identität zweier Objekte.",
        "not": "Logische Negation.",
        "or": "Logisches Oder.",
        "and": "Logisches Und.",
        "raise": "Wirft eine Ausnahme.",
        "del": "Löscht eine Variable oder ein Element.",
        "from": "Importiert Teile eines Moduls.",
        "as": "Vergibt einen Aliasnamen.",
        "assert": "Prüft eine Bedingung und wirft einen Fehler bei False.",
        "bool": "Ein Datentyp für Wahrheitswerte (True oder False).",
        "complex": "Ein Datentyp für komplexe Zahlen.",
        "bytes": "Ein Datentyp für Byte-Sequenzen.",
        "bytearray": "Eine veränderbare Byte-Sequenz.",
        "memoryview": "Ermöglicht speichereffizienten Zugriff auf Byte-Objekte.",
        "zip": "Fasst mehrere Listen zu Tupeln zusammen.",
        "map": "Wendet eine Funktion auf jedes Element einer Sequenz an.",
        "filter": "Filtert Elemente basierend auf einer Funktion.",
        "sorted": "Sortiert eine Sequenz.",
        "reversed": "Gibt eine umgekehrte Sequenz zurück.",
        "all": "Prüft, ob alle Elemente einer Sequenz True sind.",
        "any": "Prüft, ob mindestens ein Element einer Sequenz True ist.",
        "enumerate": "Erzeugt Paare aus Index und Wert.",
        "id": "Gibt die Speicheradresse eines Objekts zurück.",
        "type": "Bestimmt den Datentyp eines Objekts.",
        "format": "Formatiert Zeichenketten.",
        "chr": "Gibt das Zeichen zu einer Unicode-Nummer zurück.",
        "ord": "Gibt die Unicode-Nummer eines Zeichens zurück.",
        "bin": "Wandelt eine Zahl in eine Binärdarstellung um.",
        "hex": "Wandelt eine Zahl in eine Hexadezimaldarstellung um.",
        "oct": "Wandelt eine Zahl in eine Oktaldarstellung um.",
        "exec": "Führt dynamisch übergebenen Code aus.",
        "eval": "Wertet einen Ausdruck als Code aus.",
        "open": "Öffnet eine Datei.",
        "read": "Liest Daten aus einer Datei.",
        "write": "Schreibt Daten in eine Datei.",
        "append": "Hängt Daten an eine Datei an.",
        "close": "Schließt eine Datei.",
        "math": "Modul für mathematische Funktionen.",
        "random": "Modul für Zufallszahlen.",
        "time": "Modul für Zeitfunktionen.",
        "os": "Modul für Betriebssystem-Funktionen.",
        "sys": "Modul für System- und Interpreter-Funktionen.",
        "itertools": "Modul für effiziente Iterationstools.",
        "functools": "Modul für Funktionen höherer Ordnung.",
        "collections": "Modul mit erweiterten Datenstrukturen.",
        "threading": "Modul für parallele Threads.",
        "multiprocessing": "Modul für parallele Prozesse.",
        "asyncio": "Modul für asynchrone Programmierung.",
    },

    "C#": {
        "class": "Ein Bauplan für Objekte in C#.",
        "struct": "Ein Werttyp, ähnlich einer Klasse.",
        "interface": "Definiert eine Schnittstelle ohne Implementierung.",
        "namespace": "Gruppiert verwandte Klassen.",
        "using": "Bindet Namespaces ein.",
        "public": "Öffentliche Zugriffsmodifizierer.",
        "private": "Private Zugriffsmodifizierer.",
        "protected": "Geschützter Zugriffsmodifizierer.",
        "static": "Erzeugt eine statische Methode oder Variable.",
        "void": "Rückgabetyp für Methoden ohne Rückgabe.",
        "int": "Ganzzahliger Datentyp in C#.",
        "double": "Datentyp für Gleitkommazahlen.",
        "string": "Datentyp für Zeichenketten.",
        "bool": "Datentyp für Wahrheitswerte.",
        "new": "Erzeugt eine neue Instanz eines Objekts.",
        "return": "Gibt einen Wert aus einer Methode zurück.",
        "foreach": "Iteriert über eine Sammlung.",
        "if": "Bedingte Anweisung.",
        "else": "Alternative Anweisung zu if.",
        "try": "Beginnt einen Block zur Fehlerbehandlung.",
        "catch": "Fängt eine Ausnahme ab.",
        "finally": "Wird immer nach try/catch ausgeführt.",
        "throw": "Wirft eine Ausnahme.",
        "get": "Liest eine Eigenschaft.",
        "set": "Schreibt eine Eigenschaft.",
        "abstract": "Definiert eine abstrakte Klasse oder Methode.",
        "sealed": "Verhindert Vererbung.",
        "override": "Überschreibt eine Methode der Basisklasse.",
        "virtual": "Erlaubt das Überschreiben von Methoden.",
        "readonly": "Erlaubt Schreibzugriff nur im Konstruktor.",
        "const": "Deklariert eine Konstante.",
        "event": "Definiert ein Event.",
        "delegate": "Ermöglicht das Speichern von Methodenreferenzen.",
        "char": "Datentyp für einzelne Zeichen.",
        "decimal": "Datentyp für exakte Dezimalzahlen.",
        "var": "Deklariert eine Variable mit automatisch erkanntem Typ.",
        "dynamic": "Deklariert eine Variable mit dynamischem Typ.",
        "object": "Die Basisklasse aller Typen in C#.",
        "typeof": "Gibt den Typ eines Objekts zurück.",
        "sizeof": "Gibt die Größe eines Datentyps zurück.",
        "stackalloc": "Erzeugt einen Array-Speicherbereich auf dem Stack.",
        "lock": "Sichert einen Codeabschnitt für gleichzeitigen Zugriff.",
        "unsafe": "Erlaubt unsicheren Code mit direktem Speicherzugriff.",
        "fixed": "Ermöglicht das Arbeiten mit festen Speicheradressen.",
        "volatile": "Markiert eine Variable für nebenläufige Zugriffe.",
        "checked": "Überprüft Überläufe bei arithmetischen Operationen.",
        "unchecked": "Ignoriert Überläufe bei arithmetischen Operationen.",
        "nameof": "Gibt den Namen einer Variablen oder Methode als String zurück.",
        "default": "Gibt den Standardwert eines Typs zurück.",
        "base": "Greift auf die Basisklasse einer abgeleiteten Klasse zu.",
        "this": "Referenziert die aktuelle Instanz einer Klasse.",
        "params": "Erlaubt eine variable Anzahl von Argumenten.",
        "switch": "Ermöglicht Fallunterscheidungen.",
        "case": "Definiert einen Fall in einer switch-Anweisung.",
        "goto": "Springt zu einer bestimmten Code-Stelle.",
        "ref": "Ermöglicht Referenzübergabe von Variablen.",
        "out": "Ermöglicht Rückgabe mehrerer Werte aus einer Methode.",
        "in": "Verhindert Änderung eines übergebenen Werts.",
        "async": "Ermöglicht asynchrone Methoden.",
        "await": "Wartet auf das Ergebnis einer asynchronen Operation.",
        "yield": "Erzeugt einen Wert in einer Iterator-Methode.",
        "LINQ": "Modul für Abfragen auf Datenquellen.",
        "Task": "Repräsentiert eine asynchrone Operation.",
        "Tuple": "Struktur für mehrere Werte in einer Variable.",
        "record": "Definiert eine unveränderliche Datenstruktur.",
        "Span": "Bietet effizienten Zugriff auf Speicherbereiche.",
        "Memory": "Repräsentiert verwalteten Speicher.",
        "Func": "Delegat für Methoden mit Rückgabewert.",
        "Action": "Delegat für Methoden ohne Rückgabewert.",
        "Expression": "Ermöglicht Erstellung von Code als Objekte.",
        "Regex": "Modul für reguläre Ausdrücke.",
        "JsonSerializer": "Modul für JSON-Serialisierung.",
        "HttpClient": "Modul für HTTP-Anfragen.",
    },

    "Plank": {
        "1.616255*10^-35": "Planck-Länge",
        "5.391247*10^-44": "Planck-Zeit",
        "2.176434*10^-8": "Planck-Masse",
        "1.956*10^9": "Planck-Energie",
        "1.416784*10^32": "Planck-Temperatur",
        "1.8755459*10^-18": "Planck-Ladung",
        "5.15500*10^96": "Planck-Dichte",

    },

    "AWS": {
        "EC2": "Skaliere deine Anwendung automatisch bei wechselnder Last, um Kosten zu senken und Verfügbarkeit zu erhöhen.",
        "S3": "Sichere deine Daten vor versehentlichem Verlust durch eine Funktion, die frühere Zustände speichert.",
        "RDS": "Setze auf hohe Verfügbarkeit bei produktiven Datenbanken durch redundante Bereitstellung in verschiedenen Verfügbarkeitszonen.",
        "Lambda": "Beachte eine maximale Ausführungsdauer und optimiere deine Funktionen für schnelle Reaktionen.",
        "CloudFront": "Beschleunige die weltweite Auslieferung deiner Inhalte durch ein verteiltes Netzwerk nahe bei den Nutzern.",
        "VPC": "Schütze dein Netzwerk durch Kombination aus statischen und dynamischen Zugriffskontrollen.",
        "IAM": "Gewähre nur die absolut notwendigen Zugriffsrechte – ein Sicherheitsprinzip, das Risiken minimiert.",
        "CloudWatch": "Überwache deine Systeme mit Warnungen und visuellen Dashboards, um Fehler früh zu erkennen.",
        "ECS": "Führe containerisierte Anwendungen ohne eigene Serververwaltung aus, indem du serverlose Optionen nutzt.",
        "Route 53": "Leite den Verkehr nur an gesunde Endpunkte, um Ausfälle zu vermeiden.",
        "Elastic Beanstalk": "Automatisiere das Deployment und die Verwaltung von Webanwendungen ohne manuelle Infrastrukturarbeit.",
        "SNS": "Verteile Nachrichten an mehrere Empfänger gleichzeitig für effektive Benachrichtigungen.",
        "SQS": "Entkopple Komponenten deiner Architektur, um Lastspitzen abzufangen und zu puffern.",
        "EFS": "Teile persistenten Speicher über mehrere Recheninstanzen hinweg, um Datenkonsistenz zu gewährleisten.",
        "CloudFormation": "Beschreibe und verwalte deine Infrastruktur als wiederholbaren Code.",
        "Glue": "Automatisiere Datenaufbereitung und ETL-Prozesse ohne eigene Serververwaltung.",
        "Athena": "Analysiere große Datenmengen direkt im Speicher, ohne eine Datenbank zu betreiben.",
        "CodePipeline": "Erstelle automatisierte Abläufe für Software-Tests und Deployments.",
        "Secrets Manager": "Lagere geheime Zugangsdaten sicher aus und automatisiere deren Rotation.",
        "DynamoDB": "Wähle flexible Leistungsoptionen, um Kosten und Kapazität optimal zu steuern.",
        "SaaS": "Diese Cloud-Lösung liefert komplett fertige Anwendungen, die du direkt über das Internet nutzen kannst, ohne dich um Infrastruktur oder Wartung kümmern zu müssen.",
        "PaaS": "Hier bekommst du eine Entwicklungsumgebung und Tools in der Cloud, um Anwendungen zu programmieren und zu betreiben, ohne Server und Netzwerke selbst verwalten zu müssen.",
        "IaaS": "Dieses Modell stellt dir virtuelle Maschinen, Netzwerke und Speicher in der Cloud bereit, damit du Betriebssysteme und Anwendungen komplett selbst konfigurieren kannst."
    }
}

# Spielzustände
state = "menu"
eingabe = ""
wort = ""
hinweis = ""
wortlen = 0
versuche = []
max_versuche = 6
geraten = False

def zeichne_versuche():
    spacing = 10
    box_size = 60
    start_y = HEIGHT // 2 - 180

    for idx, versuch in enumerate(versuche):
        start_x = (WIDTH - (wortlen * (box_size + spacing) - spacing)) // 2
        y = start_y + idx * (box_size + spacing)

        for i in range(wortlen):
            x = start_x + i * (box_size + spacing)
            buchstabe = versuch[i]
            if buchstabe == wort[i]:
                farbe = GREEN
            elif buchstabe in wort:
                farbe = ORANGE
            else:
                farbe = RED

            pygame.draw.rect(screen, farbe, (x, y, box_size, box_size))
            pygame.draw.rect(screen, BLACK, (x, y, box_size, box_size), 2)
            buchstabenbild = FONT.render(buchstabe.upper(), True, BLACK)
            bx = x + (box_size - buchstabenbild.get_width()) // 2
            by = y + (box_size - buchstabenbild.get_height()) // 2
            screen.blit(buchstabenbild, (bx, by))

def zeichne_aktuelle_eingabe():
    spacing = 10
    box_size = 60
    y = HEIGHT // 2 + (max_versuche // 2) * (box_size + spacing)
    start_x = (WIDTH - (wortlen * (box_size + spacing) - spacing)) // 2

    for i in range(wortlen):
        x = start_x + i * (box_size + spacing)
        pygame.draw.rect(screen, GRAY, (x, y, box_size, box_size))
        pygame.draw.rect(screen, BLACK, (x, y, box_size, box_size), 2)
        if i < len(eingabe):
            buchstabenbild = FONT.render(eingabe[i].upper(), True, BLACK)
            bx = x + (box_size - buchstabenbild.get_width()) // 2
            by = y + (box_size - buchstabenbild.get_height()) // 2
            screen.blit(buchstabenbild, (bx, by))

def zeige_hinweis(text):
    hinweis_text = SMALL_FONT.render("Hinweis: " + text, True, BLACK)
    screen.blit(hinweis_text, (WIDTH // 2 - hinweis_text.get_width() // 2, 40))

def zeige_gewonnen():
    gewonnen_text = FONT.render("Richtig! Das Wort war: " + wort, True, GREEN)
    screen.blit(gewonnen_text, (WIDTH // 2 - gewonnen_text.get_width() // 2, HEIGHT - 140))

def zeige_verloren():
    verloren_text = FONT.render("Leider falsch. Das Wort war: " + wort, True, RED)
    screen.blit(verloren_text, (WIDTH // 2 - verloren_text.get_width() // 2, HEIGHT - 140))

def zeichne_button(text, x, y, w, h):
    pygame.draw.rect(screen, BLUE, (x, y, w, h))
    pygame.draw.rect(screen, BLACK, (x, y, w, h), 2)
    label = FONT.render(text, True, WHITE)
    screen.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))
    return pygame.Rect(x, y, w, h)

def zeichne_menu():
    screen.fill(WHITE)
    titel = FONT.render("Wähle ein Thema:", True, BLACK)
    screen.blit(titel, (WIDTH // 2 - titel.get_width() // 2, 100))
    buttons = []
    themen = list(woerterbuecher.keys())
    for i, thema in enumerate(themen):
        rect = zeichne_button(thema, WIDTH // 2 - 100, 200 + i * 100, 200, 60)
        buttons.append((rect, thema))
    return buttons

def starte_spiel(thema):
    global state, wort, hinweis, wortlen, eingabe, geraten, versuche
    state = "spiel"
    eingabe = ""
    geraten = False
    versuche = []
    wort, hinweis = random.choice(list(woerterbuecher[thema].items()))
    wort = wort.lower()
    wortlen = len(wort)

def zeichne_neustart_button():
    return zeichne_button("Neustart", WIDTH // 2 - 100, HEIGHT - 100, 200, 50)


# Hauptloop
clock = pygame.time.Clock()

while True:
    screen.fill(WHITE)

    if state == "menu":
        button_list = zeichne_menu()

    elif state == "spiel":
        zeige_hinweis(hinweis)
        zeichne_versuche()
        if not geraten and len(versuche) < max_versuche:
            zeichne_aktuelle_eingabe()

        if geraten:
            zeige_gewonnen()
            neustart_button = zeichne_neustart_button()
        elif len(versuche) >= max_versuche:
            zeige_verloren()
            neustart_button = zeichne_neustart_button()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if state == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
            for rect, thema in button_list:
                if rect.collidepoint(event.pos):
                    starte_spiel(thema)

        if state == "spiel" and not geraten and len(versuche) < max_versuche:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    eingabe = eingabe[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(eingabe) == wortlen:
                        versuche.append(eingabe)
                        if eingabe == wort:
                            geraten = True
                        eingabe = ""
                elif len(eingabe) < wortlen and event.unicode.isprintable():
                    eingabe += event.unicode.lower()

    if state == "spiel" and (geraten or len(versuche) >= max_versuche):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if neustart_button.collidepoint(event.pos):
                    state = "menu"


    pygame.display.flip()
    clock.tick(60)
