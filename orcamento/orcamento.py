import math
from multiprocessing import Event
from re import S
import re
import tkinter as tk
import pyperclip as cp

janela = tk.Tk()
janela.title('HOTEL')
janela.geometry('1920x1080+0+0')
janela.maxsize(1920, 1080)

# frame do orcamento
orc_frm = tk.Frame(janela, height=1080, width=1920)
orc_frm['bg'] = 'gray'
orc_frm.pack()

# classe de acomodações
# master, cord de btn, capacidade, valor, imagem, pessoas, 
class Acomod:
    def __init__(self, nome, quantidade, capacidade, valor, cordX, cordY, ocupacao=0):
        self.nome = nome
        self.quantidade = quantidade 
        self.capacidade = capacidade
        self.valor = valor
        self.ocupacao = ocupacao
        self.cordX = cordX
        self.cordY = cordY
        self.estado = False
    
        # label de ocupação
        self.kpc = tk.Label(master=orc_frm, text=f'Quantidade: {self.quantidade} \n Capacidade: {self.capacidade} \n Ocupação: {self.ocupacao}', font='Arial 14')
        self.kpc.place(x=self.cordX, y=self.cordY-80)
        # label de custo
        self.tot = tk.Label(master=orc_frm, text=f'Total R$:{self.custo()}', font='MsComicSans 14')
        self.tot.place(x=self.cordX, y=self.cordY+150)
        self.butao()


    def butao(self):
        self.btn = tk.Button(orc_frm, text=self.nome, height=5, width=18, font='MsComicSans 14')
        self.btn.bind('<Button>', self.stt_change)
        self.btn.place(x=self.cordX, y=self.cordY)
        

    def check(self):
        if(self.ocupacao > self.capacidade):
            self.quantidade += 1
            self.capacidade*=2
        elif(self.ocupacao<=self.capacidade/2 and self.quantidade>1):
            self.capacidade/=2
            self.quantidade-=1
        elif(self.ocupacao < 0):
            return 1
        else:
            return 0

    def custo(self):
        
        if(self.check()==1):
            return 'valor negativo'
        else:
            return self.ocupacao * self.valor 
    
    def paste(self):
        return f'{self.custo()} e mais algumas coisas para fazer sentido'

    def stt_change(self, event):
        if(self.estado==False):
            self.btn['bg']='light green'
            self.estado=True
        else:
            self.btn['bg']='white'
            self.estado=False


# criando as acomod
suit = Acomod('Suíte', 1, 10, 10.00, 400 , 250, 0)


apto = Acomod('Apartamento', 1, 5, 10.00, 600, 250, 0)


cabn = Acomod('CabanaAmericana', 1, 3, 10.00, 800, 250, 0)


casa = Acomod('Casarão', 1, 5, 10.00, 1000, 250, 0)


swis = Acomod('Suíço', 1, 3, 10.00, 1200, 250, 0)


stan = Acomod('Standart', 1, 8, 10.00, 1400, 250, 0)

# icone label
ico_lbl = tk.Label(orc_frm, font='MsComicSans 14', text='PESSOA')
ico_lbl.place(x=870, y=550)

#alterar o numero de pessoas na acomod
def aumenta(event=None):
    lista = [suit, apto, cabn, casa, swis, stan]
    for i in lista:
        if i.estado==True:
            i.ocupacao+=1
            i.kpc['text'] = f'Quantidade: {i.quantidade} \n Capacidade: {i.capacidade} \n Ocupação: {i.ocupacao}'
            i.tot['text'] = f'Total R$:{i.custo()}'
            
def diminui(event=None):
    lista = [suit, apto, cabn, casa, swis, stan]
    for i in lista:
        if i.estado==True:
            i.ocupacao-=1
            i.kpc['text'] = f'Quantidade: {i.quantidade} \n Capacidade: {i.capacidade} \n Ocupação: {i.ocupacao}'
            i.tot['text'] = f'Total R$:{i.custo()}'

# adicionar pessoas
mais_btn = tk.Button(orc_frm, font='MsComicSans 14',  text='+')
mais_btn.bind('<Button>', aumenta)
mais_btn.place(x=950, y=550)

# subtrair pessoas
mens_btn = tk.Button(orc_frm, font='MsComicSans 14', text='-')
mens_btn.bind('<Button>', diminui)
mens_btn.place(x=850, y=550)

# copy to clipboard
def copia(envent=None):
    lista = [suit, apto, cabn, casa, swis, stan]
    for i in lista:
        if i.estado==True:
            print(i.paste())
    return 0

cp_btn = tk.Button(orc_frm, font='MsComicSans 14', text='copy to clipboard')
cp_btn.bind('<Button>', copia)
cp_btn.place(x=1000, y=550)

janela.mainloop()
