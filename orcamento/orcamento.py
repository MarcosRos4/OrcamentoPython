import tkinter as tk
from tkinter import filedialog
import pandas as pd

# janela do orçamento
janela = tk.Tk()
janela.title('HOTEL')
janela.geometry('1920x1080+0+0')
janela.maxsize(1920, 1080)

# frame do orcamento
orc_frm = tk.Frame(janela, height=1080, width=1920)
orc_frm['bg'] = 'gray'
orc_frm.pack()

# puxando a tabela
# escolher qual tabela usar

arquivo = filedialog.askopenfilename(initialdir="./orcamento",
              title="Escolha uma tabela de orçamento",
              filetypes=(("Excel files", "*.xlsx*"),("all files", "*.*")))
orc_df = pd.read_excel(arquivo)
print(orc_df)

psq_lbl = tk.Label(master=orc_frm, font="MsComicSans 14")
psq_lbl['text'] = "Aquivo escolhido:\n " + arquivo
psq_lbl.place(x=50, y=80)

# classe de acomodações
# master, cord de btn, capacidade, valor, imagem, pessoas, 
class Acomod:
    def __init__(self, nome, quantidade, capacidade,cordX, cordY, ocupacao):
        self.capacidade = capacidade
        self.cordX = cordX
        self.cordY = cordY
        self.estado = False
        self.nome = nome
        self.ocupacao = ocupacao
        self.quantidade = quantidade 
        self.valor = 0   

        # label de ocupação
        self.kpc = tk.Label(master=orc_frm, text=f'Quantidade: {self.quantidade} \n Capacidade: {self.capacidade} \n Ocupação: {self.ocupacao}', font='Arial 14')
        self.kpc.place(x=self.cordX, y=self.cordY-80)
        # label de custo
        self.tot = tk.Label(master=orc_frm, text=f"Total R$:{self.custo()}", font='MsComicSans 14')
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
        elif(self.ocupacao <= 0 ):
            return 1
        else:
            return 0

    def custo(self):
        if(self.check()==1):
            return '---------'
        else:
            if (self.ocupacao == 1):
                self.valor =  orc_df[self.nome][0]
            elif ( self.ocupacao == 2):
                self.valor = orc_df[self.nome][1]
            else:
                self.valor = (orc_df[self.nome][1] + (orc_df[self.nome][2] * (self.ocupacao - 2)))
    
    def paste(self):
        copypasta = f"_*{self.nome}*_\nR$ {self.custo()} (valor de 24h)\nR${self.custo()*1.9} (valor de 48h)\n"
        janela.clipboard_append(copypasta)
        
    def stt_change(self, event):
        if(self.estado==False):
            self.btn['bg']='light green'
            self.estado=True
        else:
            self.btn['bg']='white'
            self.estado=False

    def aumenta(self, event=None):
        if (self.estado==True):
            self.ocupacao+=1
            self.check()
            self.custo()
            self.kpc['text'] = f'Quantidade: {self.quantidade} \n Capacidade: {self.capacidade} \n Ocupação: {self.ocupacao}'
            self.tot['text'] = f'Total R$:{self.valor}'
            
    def diminui(self, event=None):
        if (self.estado==True):
            if(self.ocupacao == 0):
                pass
            else:
                self.ocupacao-=1
                self.check()
                self.custo()
                self.kpc['text'] = f'Quantidade: {self.quantidade} \n Capacidade: {self.capacidade} \n Ocupação: {self.ocupacao}'
                self.tot['text'] = f'Total R$:{self.valor}'

# criando as acomod
# parametros nome, quantidade, capacidade,cordX, cordY, ocupacao
suit = Acomod('suit', 1, 10, 400 , 250, 0)

apto = Acomod("apto", 1, 5, 600, 250, 0)

cabn = Acomod('cabn', 1, 3, 800, 250, 0)

casa = Acomod('casa', 1, 5, 1000, 250, 0)

swis = Acomod('swis', 1, 3, 1200, 250, 0)

stan = Acomod('stan', 1, 8, 1400, 250, 0)


# icone label
ico_lbl = tk.Label(orc_frm, font='MsComicSans 14', text='PESSOA')
ico_lbl.place(x=870, y=550)

#alterar o numero de pessoas na acomod


# adicionar pessoas
mais_btn = tk.Button(orc_frm, font='MsComicSans 14',  text='+')
mais_btn.bind('<Button>', suit.aumenta, add="+")
mais_btn.bind('<Button>', apto.aumenta, add="+")
mais_btn.bind('<Button>', cabn.aumenta, add="+")
mais_btn.bind('<Button>', swis.aumenta, add="+")
mais_btn.bind('<Button>', casa.aumenta, add="+")
mais_btn.bind('<Button>', stan.aumenta, add="+")
mais_btn.place(x=950, y=550)

# subtrair pessoas
mens_btn = tk.Button(orc_frm, font='MsComicSans 14', text='-')
mens_btn.bind('<Button>', suit.diminui, add="+")
mens_btn.bind('<Button>', apto.diminui, add="+")
mens_btn.bind('<Button>', cabn.diminui, add="+")
mens_btn.bind('<Button>', swis.diminui, add="+")
mens_btn.bind('<Button>', casa.diminui, add="+")
mens_btn.bind('<Button>', stan.diminui, add="+")
mens_btn.place(x=850, y=550)

# copy to clipboard
def copia(envent=None):
    lista = [suit, apto, cabn, casa, swis, stan]
    janela.clipboard_clear()
    janela.clipboard_append("Segue orçamento que corresponde a quantidade de pessoas e as acomodações disponíveis para a data. " +
    "Caso queira saber valores para mais diárias, pode nos avisar, ok? (o orçamento terá validade de 15 dias)\n"+
    "\n*DIÁRIA COM CAFÉ DA MANHÃ*\n")
    for i in lista:
        if i.estado==True:
            i.paste()

cp_btn = tk.Button(orc_frm, font='MsComicSans 14', text='copy to clipboard')
cp_btn.bind('<Button>', copia)
cp_btn.place(x=1000, y=550)

# abrir tela de configurações
def config(event=None):
    cfg_win = tk.Toplevel()
    cfg_win.title('HOTEL')
    cfg_win.geometry('1920x1080+0+0')
    cfg_win.maxsize(1920, 1080)
    cfg_frm = tk.Frame(master=cfg_win, height=1080, width=1920)
    
# botão para as configurações
cfg_btn = tk.Button(orc_frm, font='MsComicSans 14', text='Configurações')
cfg_btn.bind('<Button>', config)
cfg_btn.place(x=1750, y=0)

# janela das configurações

# frame das configurações

janela.mainloop()
