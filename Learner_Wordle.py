import pygame
import random
import sys
import json
import pyperclip
import os


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

titel_eingabe = ""
wort_hinweis_eingabe = ""
active_input = None

def resource_path(relative_path):
    """Gibt den absoluten Pfad zurück, auch wenn PyInstaller das Programm packt."""
    if hasattr(sys, '_MEIPASS'):
        # Im gepackten Zustand ist _MEIPASS der temporäre Ordner mit allen Dateien
        return os.path.join(sys._MEIPASS, relative_path)
    # Beim normalen Ausführen ist der Pfad relativ zum Skript
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), relative_path)


pfad = resource_path('hinweise/hinweise.json')

with open(pfad, 'r', encoding='utf-8') as f:
    woerterbuecher = json.load(f)


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

def zeichne_button2():
    return zeichne_button("Creat", WIDTH // 2 - 100, HEIGHT - 100, 200, 50)

def zeichne_creat_fenster():
    global titel_eingabe, wort_hinweis_eingabe, active_input

    screen.fill(WHITE)

    info = SMALL_FONT.render("Gib Thema (Titel) ein und mehrere 'Wort, Hinweis' Zeilen. Klick auf SAVE", True, BLACK)
    screen.blit(info, (50, 50))

    # Eingabefeld Titel
    pygame.draw.rect(screen, ORANGE if active_input == "titel" else GRAY, (50, 100, 600, 40))
    pygame.draw.rect(screen, BLACK, (50, 100, 600, 40), 2)
    titel_text = SMALL_FONT.render(titel_eingabe, True, BLACK)
    screen.blit(titel_text, (55, 105))

    # Eingabefeld für Wörter + Hinweise (mehrzeilig)
    box_rect = pygame.Rect(50, 160, 600, 200)
    pygame.draw.rect(screen, ORANGE if active_input == "wort" else GRAY, box_rect)
    pygame.draw.rect(screen, BLACK, box_rect, 2)

    # Mehrzeilige Darstellung:
    zeilen = wort_hinweis_eingabe.split("\n")
    for i, zeile in enumerate(zeilen):
        zeilentext = SMALL_FONT.render(zeile, True, BLACK)
        screen.blit(zeilentext, (55, 165 + i * 25))

    # Save-Button
    save_button = zeichne_button("SAVE", 50, 380, 200, 50)

    # Dummy Button rechts neben Textbox
    paste_button = zeichne_button("Paste", 660, 160, 120, 50)

    return save_button, paste_button



def zeichne_menu():
    screen.fill(WHITE)
    titel = FONT.render("Wähle ein Thema:", True, BLACK)
    screen.blit(titel, (WIDTH // 2 - titel.get_width() // 2, 100))

    buttons = []
    themen = list(woerterbuecher.keys()) + ["Create"]

    button_width = 200
    button_height = 60
    spacing_x = 40
    spacing_y = 20
    start_y = 200

    # Berechne, wie viele Zeilen vertikal auf den Screen passen
    max_rows = (HEIGHT - start_y - 50) // (button_height + spacing_y)

    # Berechne, wie viele Spalten wir brauchen
    num_columns = (len(themen) + max_rows - 1) // max_rows  # Rundung nach oben

    # Gesamtbreite aller Spalten inklusive Abstand
    total_width = num_columns * button_width + (num_columns - 1) * spacing_x

    # Start-x für Zentrierung
    start_x = WIDTH // 2 - total_width // 2

    for index, thema in enumerate(themen):
        col = index // max_rows
        row = index % max_rows
        x = start_x + col * (button_width + spacing_x)
        y = start_y + row * (button_height + spacing_y)
        rect = zeichne_button(thema, x, y, button_width, button_height)
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
    elif state == "Create":
        zeichne_creat_fenster()

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
                state = "menu"
            elif event.key == pygame.K_DELETE:
                pygame.quit()
                sys.exit()


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

        if state == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
            for rect, thema in button_list:
                if rect.collidepoint(event.pos):
                    if thema == "Create":
                        state = "Create"
                    else:
                        starte_spiel(thema)

        # Seite 2: Eingabe
        if state == "Create":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(50, 100, 600, 40).collidepoint(event.pos):
                    active_input = "titel"
                elif pygame.Rect(50, 160, 600, 200).collidepoint(event.pos):
                    active_input = "wort"
                else:
                    active_input = None

                # Save-Button gedrückt?
                if pygame.Rect(50, 380, 200, 50).collidepoint(event.pos):
                    if titel_eingabe:
                        if titel_eingabe not in woerterbuecher:
                            woerterbuecher[titel_eingabe] = {}
                        zeilen = wort_hinweis_eingabe.split("\n")
                        for i, zeile in enumerate(zeilen):
                            if zeile.strip() == "":
                                zeile = " "  # Leerzeichen statt leerer String
                            zeilentext = SMALL_FONT.render(zeile, True, BLACK)
                            screen.blit(zeilentext, (55, 165 + i * 25))
                        for zeile in wort_hinweis_eingabe.split("\n"):
                            if "," in zeile:
                                wort, hinweis = map(str.strip, zeile.split(",", 1))
                                woerterbuecher[titel_eingabe][wort] = hinweis

                        # JSON speichern
                        with open(pfad, "w", encoding="utf-8") as f:
                            json.dump(woerterbuecher, f, indent=4, ensure_ascii=False)

                        wort_hinweis_eingabe = ""  # Eingabe zurücksetzen
                elif pygame.Rect(660, 160, 120, 50).collidepoint(event.pos):

                    clipboard_text = pyperclip.paste()
                    wort_hinweis_eingabe += clipboard_text

            if event.type == pygame.KEYDOWN:
                if active_input == "titel":
                    if event.key == pygame.K_BACKSPACE:
                        titel_eingabe = titel_eingabe[:-1]
                    elif event.unicode.isprintable():
                        titel_eingabe += event.unicode
                elif active_input == "wort":
                    if event.key == pygame.K_BACKSPACE:
                        wort_hinweis_eingabe = wort_hinweis_eingabe[:-1]
                    elif event.key == pygame.K_RETURN:
                        wort_hinweis_eingabe += "\n"
                    elif event.unicode.isprintable():
                        wort_hinweis_eingabe += event.unicode



    if state == "spiel" and (geraten or len(versuche) >= max_versuche):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if neustart_button.collidepoint(event.pos):
                    state = "menu"


    pygame.display.flip()
    clock.tick(60)
