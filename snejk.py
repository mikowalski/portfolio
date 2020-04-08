import pygame
import random
import tkinter as tk
import tkinter.ttk as ttk
from enum import Enum



class Kierunek(Enum):
    LEWO=1
    PRAWO=2
    GORA=3
    DOL=4


class CialoWeza:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def lokuj(self,nowa_x,nowa_y):
        self.x=nowa_x
        self.y=nowa_y


class Jedzenie:
    def __init__(self,x,y):
        self.x = x
        self.y = y




class menu_startowe():
    def graj(self):
        switcher_predkosci = {
            0: 7,
            1: 12,
            2: 22
        }
        switcher_jedzenia = {
            0: 1,
            1: 3,
            2: 15
        }
        self.wybor_predkosci = switcher_predkosci.get(self.predkosc.current())
        self.wybor_jedzenia = switcher_jedzenia.get(self.jedzenie.current())
        print(str(self.wybor_predkosci)+" -- "+str(self.wybor_jedzenia))
        self.okno_menu.destroy()

    def __init__(self):
        self.wybor_predkosci = 7
        self.wybor_jedzenia = 1

        self.okno_menu = tk.Tk()
        self.okno_menu.title("SNEJK")

        self.label1 = tk.Label(self.okno_menu,text="Predkosc weza")
        self.label1.pack(side=tk.TOP)
        self.pr_value = tk.StringVar()
        self.predkosc = ttk.Combobox(self.okno_menu, textvariable = self.pr_value )
        self.predkosc.pack()
        self.predkosc['values'] = ("wolna","średnia","szybka")
        self.predkosc.current(0)

        self.label2 = tk.Label(self.okno_menu, text="Ilość jedzenia na planszy")
        self.label2.pack(side=tk.TOP)
        self.je_value = tk.StringVar()
        self.jedzenie = ttk.Combobox(self.okno_menu, textvariable=self.je_value)
        self.jedzenie.pack()
        self.jedzenie['values'] = ("jedno", "trzy", "piętnaście")
        self.jedzenie.current(0)


        self.button = tk.Button(self.okno_menu, text = "GRAJ", command = self.graj)
        self.button.pack(side = tk.BOTTOM)


        tk.mainloop()
        print(self.wybor_predkosci,self.wybor_jedzenia)

    def wybierz_opcje(self):
        return (self.wybor_predkosci, self.wybor_jedzenia)




def okno_koniec_gry():
    global punkty
    okno = tk.Tk()
    tekst_koncowy = "Koniec gry! Twój wynik wynosi " + str(punkty) + " punktów"
    label = tk.Label(okno,text = tekst_koncowy, font = ("Tahoma", 16, "bold"))
    label.pack()
    tk.mainloop()














opcje = menu_startowe().wybierz_opcje()
pygame.init()
print("PO PYGAME INIT: " + str(opcje))

zakoncz_gre = False
rozmiar_okna = (600,600)
okno_gry = pygame.display.set_mode(rozmiar_okna)
pygame.display.set_caption("SNEJK")

glowa_x = 300
glowa_y = 300
glowa_kierunek = Kierunek.PRAWO

punkty = 0



lista_ciala_weza = []
for i in range(5):
    lista_ciala_weza.append(CialoWeza(glowa_x,glowa_y-(15*(i+1))))


lista_jedzenia = []
for i in range(opcje[1]+1):
    lista_jedzenia.append(Jedzenie(random.randint(0,40)*15,random.randint(0,40)*15))





def glowa_weza(k):
    global glowa_x, glowa_y

    if k==Kierunek.PRAWO:
        glowa_x+=15
    if k==Kierunek.DOL:
       glowa_y+=15
    if k==Kierunek.GORA:
        glowa_y-=15
    if k==Kierunek.LEWO:
        glowa_x-=15

    glowa_x%=600
    glowa_y%=600



def cialo_weza():
    global zakoncz_gre, glowa_x, glowa_y

    for c in lista_ciala_weza:
        if (c.x==glowa_x and c.y==glowa_y):
            zakoncz_gre = True

    c = lista_ciala_weza[len(lista_ciala_weza)-1]
    c.lokuj(glowa_x,glowa_y)
    lista_ciala_weza.remove(c)
    lista_ciala_weza.insert(0,c)


def jedzenie():
    global glowa_x, glowa_y, punkty

    for j in lista_jedzenia:
        if(j.x==glowa_x and j.y==glowa_y):
            c = CialoWeza(glowa_x - (15 * len(lista_ciala_weza)), glowa_y)
            lista_ciala_weza.append(c)
            lista_jedzenia.remove(j)
            lista_jedzenia.append(Jedzenie(random.randint(0,40)*15,random.randint(0,40)*15))
            punkty+=1









def petla_widoku():
    okno_gry.fill((225, 250, 215))
    for c in lista_ciala_weza:
        pygame.draw.rect(okno_gry, (0,255,0) , (c.x, c.y, 15, 15),  0 )
    for j in lista_jedzenia:
        pygame.draw.rect(okno_gry, (0,0,255),(j.x,j.y,15,15),0)
    pygame.draw.rect(okno_gry, (255, 0, 0), (glowa_x, glowa_y, 15, 15), 0)
    pygame.display.update()








def petla_gry():

    global zakoncz_gre, glowa_x, glowa_y, glowa_kierunek, opcje
    zegar = pygame.time.Clock()

    while not zakoncz_gre:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and glowa_kierunek!=Kierunek.LEWO:
                    glowa_kierunek=Kierunek.PRAWO
                if event.key == pygame.K_LEFT and glowa_kierunek!=Kierunek.PRAWO:
                    glowa_kierunek=Kierunek.LEWO
                if event.key == pygame.K_UP and glowa_kierunek!=Kierunek.DOL:
                    glowa_kierunek=Kierunek.GORA
                if event.key == pygame.K_DOWN and glowa_kierunek!=Kierunek.GORA:
                    glowa_kierunek=Kierunek.DOL



        jedzenie()
        glowa_weza(glowa_kierunek)
        cialo_weza()
        petla_widoku()
        zegar.tick(opcje[0])






petla_gry()
okno_koniec_gry()
quit()