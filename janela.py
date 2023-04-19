"""
Constrói a janela
"""

import sys
import tkinter as tk
from tkinter import ttk
from boletos import importar_boletos


class App(tk.Tk):
    """
    Cria janela com retorno para o usuário
    """

    def __init__(self):
        super().__init__()

        # Largura da Janela
        self.labelradio = None
        self.cotaunica = None
        self.data1 = None
        self.data2 = None
        self.data3 = None

        w = 450
        # Altura da Janela
        h = 152

        # Define a janela como não exclusiva (outras janelas podem sobrepor ela)
        self.acertaconfjanela(False)
        # Adiciona o cabeçalho da janela
        self.title('Andamento Extração')

        self.minsize(w, h)
        # Desenha a janela com a largura e altura definida e na posição calculada, ou seja, no centro da tela
        self.center()

        # Label número cliente
        self.labelcodigocliente = ttk.Label(self, text='Arquivo:            ', font="Arial 15 bold")
        self.labelcodigocliente.place(x=0, y=0, width=self.winfo_width())
        self.labelcodigocliente.configure(anchor='center')

        # Label número da inscrição
        self.labelinscricao = ttk.Label(self, text='', font="Arial 15")
        self.labelinscricao.place(x=0, y=30, width=self.winfo_width())
        self.labelinscricao.configure(anchor='center')

        # ProgressBar de Quantidade de Transações (Views)
        self.barraextracao = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.barraextracao.place(x=75, y=60, width=300)

        # Label de quantidade de extrações
        self.labelquantidade = ttk.Label(self, text='', font="Arial 10")
        self.labelquantidade.place(x=0, y=90, width=self.winfo_width())
        self.labelquantidade.configure(anchor='center')

        # Label de status do sistema
        self.labelstatus = ttk.Label(self, text='', font="Arial 15")
        self.labelstatus.place(x=0, y=110, width=self.winfo_width())
        self.labelstatus.configure(anchor='center')

        # button Iniciar Extração
        self.executar = ttk.Button(self, text='Executar')
        self.executar['command'] = self.executar_clicked
        self.executar.place(x=10, rely=(1 / 10) * 8)

        # button Fechar a Janela
        self.fechar = ttk.Button(self, text='Fechar')
        self.fechar['command'] = self.fechar_clicked
        self.fechar.place(x=self.winfo_width() - 90, rely=(1 / 10) * 8)

    def executar_clicked(self):
        """
        Ação do botão
        """
        importar_boletos(self)

    def fechar_clicked(self):
        """
        Ação do botão
        """
        self.destroy()
        sys.exit()

    def mudartexto(self, nomelabel, texto):
        """
        :param nomelabel: nome do label a ter o texto alterado
        :param texto: texto a ser inserido
        """
        self.__getattribute__(nomelabel).config(text=texto)
        self.atualizatela()

    def configurarbarra(self, nomebarra, maximo, indicador):
        """
        :param nomebarra: nome da barra a ser atualizada.
        :param maximo: limite máximo da barra de progresso.
        :param indicador: variável
        """
        self.__getattribute__(nomebarra).config(maximum=maximo, value=indicador)
        self.atualizatela()

    def acertaconfjanela(self, exclusiva):
        """
        :param exclusiva: se a janela fica na frente das outras ou não
        """
        self.attributes("-topmost", exclusiva)
        self.atualizatela()

    def atualizatela(self):
        """
        Dá um 'refresh' na tela para modificar com alterações realizadas
        """
        self.update()

    def center(self):
        """
        :param: the main window or Toplevel window to center

        Apparently a common hack to get the window size. Temporarily hide the
        window to avoid update_idletasks() drawing the window in the wrong
        position.
        """

        self.update_idletasks()  # Update "requested size" from geometry manager

        # define window dimensions width and height
        width = self.winfo_width()
        frm_width = self.winfo_rootx() - self.winfo_x()
        win_width = width + 2 * frm_width

        height = self.winfo_height()
        titlebar_height = self.winfo_rooty() - self.winfo_y()
        win_height = height + titlebar_height + frm_width

        # Get the window position from the top dynamically as well as position from left or right as follows
        x = self.winfo_screenwidth() // 2 - win_width // 2
        y = self.winfo_screenheight() // 2 - win_height // 2

        # this is the line that will center your window
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        # This seems to draw the window frame immediately, so only call deiconify()
        # after setting correct window position
        self.deiconify()
