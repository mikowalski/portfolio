from enum import Enum
import tkinter as tk
from tkinter import ttk

import pygame
import random

SZEROKOSC_PLANSZY=(600,600)

granie = True
lista_smug = {}
opcje = []

class Kierunek(Enum):
    LEWO=1
    PRAWO=2
    GORA=3
    DOL=4


class Gracz():
    def __init__(self,x,y,kierunek):
        self.x = x
        self.y = y
        self.kierunek = kierunek
        self.kolor_smugi = (random.uniform(0,255),random.uniform(0,255),random.uniform(0,255))

class Wrog():
    def __init__(self,x,y,kierunek):
        self.x = x
        self.y = y
        self.kierunek = kierunek
        self.kolor_smugi = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
    def sprawdz_czy_skrecic(self):
        if self.kierunek==Kierunek.LEWO:
            odleglosc_gora = 0
            odleglosc_dol = 0
            if (self.x-5,self.y) in lista_smug:
                for i in range(self.y,0,-5):
                    if (self.x,abs(self.y - i)) in lista_smug.keys():
                        break
                    odleglosc_gora = abs(self.y-i)
                for i in range(self.y, SZEROKOSC_PLANSZY[1], 5):
                    if (self.x,abs(self.y - i)) in lista_smug.keys():
                        break
                    odleglosc_dol = abs(self.y - i)
                print("LEWO: "+str(odleglosc_gora) + " UP VS DOWN " + str(odleglosc_dol))
                if odleglosc_dol>odleglosc_gora:
                    self.kierunek=Kierunek.DOL
                    print("WYBIERAM DOL")
                else:
                    self.kierunek=Kierunek.GORA
                    print("WYBIERAM GORA")
                return
        if self.kierunek==Kierunek.GORA:
            odleglosc_lewo = 0
            odleglosc_prawo = 0
            if (self.x,self.y-5) in lista_smug:
                for i in range(self.x,0,-5):
                    if (abs(self.x-i),self.y) in lista_smug.keys():
                        break
                    odleglosc_lewo = abs(self.x-i)
                for i in range(self.x, SZEROKOSC_PLANSZY[0], 5):
                    if (abs(self.x-i),self.y) in lista_smug.keys():
                        break
                    odleglosc_prawo = abs(self.x - i)
                print("GORA: "+str(odleglosc_lewo) + " VS " + str(odleglosc_prawo))

                if odleglosc_lewo>odleglosc_prawo:
                    self.kierunek=Kierunek.LEWO
                    print("WYBIERAM LEWO")
                else:
                    self.kierunek=Kierunek.PRAWO
                    print("WYBIERAM PRAWO")
                return
        if self.kierunek==Kierunek.DOL:
            odleglosc_lewo = 0
            odleglosc_prawo = 0
            if (self.x,self.y+5) in lista_smug:
                for i in range(self.x,0,-5):
                    if (abs(self.x-i),self.y) in lista_smug.keys():
                        break
                    odleglosc_lewo = abs(self.x-i)
                for i in range(self.x, SZEROKOSC_PLANSZY[0], 5):
                    if (abs(self.x-i),self.y) in lista_smug.keys():
                        break
                    odleglosc_prawo = abs(self.x - i)
                print("DOL: "+str(odleglosc_lewo) + " VS " + str(odleglosc_prawo))
                if odleglosc_lewo>odleglosc_prawo:
                    self.kierunek=Kierunek.LEWO
                    print("WYBIERAM LEWO")
                else:
                    self.kierunek=Kierunek.PRAWO
                    print("WYBIERAM PRAWO")
                return
        if self.kierunek==Kierunek.PRAWO:
            if (self.x+5,self.y) in lista_smug:
                odleglosc_gora = 0
                odleglosc_dol = 0
                for i in range(self.y,0,-5):
                    if (self.x,abs(self.y - i)) in lista_smug.keys():
                        break
                    odleglosc_gora = abs(self.y - i)
                for i in range(self.y, SZEROKOSC_PLANSZY[1], 5):
                    if (self.x,abs(self.y - i)) in lista_smug.keys():
                        break
                    odleglosc_dol = abs(self.y - i)
                print("PRAWO: "+str(odleglosc_gora) + " UP VS DOWN " + str(odleglosc_dol))
                if odleglosc_dol>odleglosc_gora:
                    self.kierunek=Kierunek.DOL
                    print("WYBIERAM DOL")
                else:
                    self.kierunek=Kierunek.GORA
                    print("WYBIERAM GORA")
                return

class Smuga():
    def __init__(self,x,y,kolor):
        self.x=x
        self.y=y
        self.kolor=kolor


def graj(okno, predkosc):
    global opcje
    switcher_predkosci={"wolna":12,"średnia":22,"szybka":32}
    opcje = (switcher_predkosci.get(predkosc.get()),1)
    okno.destroy()
def menu_gry():
    global opcje
    okno = tk.Tk()
    tytul = tk.Label(okno, text="TRON", font=("Tahoma",13,"bold"))
    tytul.pack(side=tk.TOP)

    label1 = tk.Label(okno, text="Predkosc gry")
    label1.pack(side=tk.TOP)
    pr_value = tk.StringVar()
    predkosc = ttk.Combobox(okno, textvariable=pr_value)
    predkosc.pack()
    predkosc['values'] = ("wolna", "średnia", "szybka")
    predkosc.current(0)

    przycisk_graj = tk.Button(okno, text="GRAJ", command=lambda: graj(okno, predkosc))
    przycisk_graj.pack(side=tk.BOTTOM)

    tk.mainloop()


def petla_widoku(okno,gracze):
    okno.fill((0,25,0))
    for s in lista_smug.values():
        pygame.draw.rect(okno,s.kolor,(s.x,s.y,5,5))
    for g in gracze:
        pygame.draw.rect(okno,(255,0,0),(g.x,g.y,5,5))
    pygame.display.update()

def petla_ruchu(gracz):
    global granie
    if gracz.kierunek==Kierunek.PRAWO:
        gracz.x+=5
    if gracz.kierunek==Kierunek.LEWO:
        gracz.x-=5
    if gracz.kierunek==Kierunek.GORA:
        gracz.y-=5
    if gracz.kierunek==Kierunek.DOL:
        gracz.y+=5
    gracz.x%=SZEROKOSC_PLANSZY[0]
    gracz.y%=SZEROKOSC_PLANSZY[1]
    if (gracz.x,gracz.y) in lista_smug.keys():
        print("GEJM OłWER")
        granie = False


def petla_smugi(gracz):
    smuga = Smuga(gracz.x,gracz.y,gracz.kolor_smugi)
    lista_smug[(gracz.x,gracz.y)]=smuga

def petla_wrogow(wrog):
    petla_smugi(wrog)
    petla_ruchu(wrog)
    wrog.sprawdz_czy_skrecic()

def petla_gry():
    global granie, opcje
    okno = pygame.display.set_mode(SZEROKOSC_PLANSZY)
    pygame.display.set_caption("TRĄN")
    zegar = pygame.time.Clock()


    gracz = Gracz(0,220,Kierunek.PRAWO)
    wrog = Wrog(590,575,Kierunek.LEWO)

    while granie:
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                granie = False
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_w:
                    gracz.kierunek=Kierunek.GORA
                if e.key==pygame.K_s:
                    gracz.kierunek=Kierunek.DOL
                if e.key==pygame.K_a:
                    gracz.kierunek=Kierunek.LEWO
                if e.key==pygame.K_d:
                    gracz.kierunek=Kierunek.PRAWO

        petla_smugi(gracz)
        petla_ruchu(gracz)
        petla_wrogow(wrog)
        petla_widoku(okno,[gracz,wrog])
        zegar.tick(opcje[0])




menu_gry()
petla_gry()

okno = tk.Tk()
tytul = tk.Label(okno, text="GAME OVER!!!", font=("Tahoma",13,"bold"))
tytul.pack(side=tk.TOP)
tk.mainloop()


pygame.quit()

