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
orc_df = pd.read_excel("./orcamento/TABELA_PADRAO.xlsx")
# escolher qual tabela usar
def pesquisar(event=None):
    arquivo = filedialog.askopenfilename(initialdir="./orcamento",
                  title="Escolha uma tabela de orçamento",
                  filetypes=(("Excel files", "*.xlsx*"),("all files", "*.*")))
    psq_lbl['text'] = "Aquivo escolhido:\n " + arquivo
    orc_df = pd.read_excel(arquivo)
    #print(orc_df)

psq_btn = tk.Button(master=orc_frm, font="MsComicSans 14", text="Procurar Tabela")
psq_btn.bind("<Button>", pesquisar)
psq_btn.place(x=50, y=130)

psq_lbl = tk.Label(master=orc_frm, font="MsComicSans 14")
psq_lbl.place(x=50, y=80)

# ler a tabela no python
tst_btn = tk.Button(master=orc_frm, font="MsComicSans 14", text="teste", command=print(orc_df))

tst_btn.place(x=50, y=180)


# classe de acomodações
# master, cord de btn, capacidade, valor, imagem, pessoas, 
class Acomod:
    def __init__(self, nome, quantidade, capacidade, valor, cordX, cordY, ocupacao, cafe=0):
        self.cafe = cafe
        self.capacidade = capacidade
        self.cordX = cordX
        self.cordY = cordY
        self.estado = False
        self.nome = nome
        self.ocupacao = ocupacao
        self.quantidade = quantidade 
        self.valor = valor    

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
                print('valor total de 220')
            elif ( self.ocupacao == 2):
                print('valor total de 290')
            else:
                print(f'valor total de [duplo + cama extra * {self.ocupacao - 2}]')
    
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

# criando as acomod
suit = Acomod('Suíte', 1, 10, 10.00, 400 , 250, 0)

apto = Acomod('Apartamento', 1, 5, 10.00, 600, 250, 0)

cabn = Acomod('Cabana Americana', 1, 3, 10.00, 800, 250, 0)

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
            i.check()
            i.kpc['text'] = f'Quantidade: {i.quantidade} \n Capacidade: {i.capacidade} \n Ocupação: {i.ocupacao}'
            i.tot['text'] = f'Total R$:{i.custo()}'
            
def diminui(event=None):
    lista = [suit, apto, cabn, casa, swis, stan]
    for i in lista:
        if i.estado==True:
            if(i.ocupacao == 0):
                pass
            else:
                i.ocupacao-=1
            i.check()
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
