import DBConnection
from Basic_Classes import *


class Interface(tkinter.Frame):
    """
        Classe base de interface para interagir com usuario

        metodos:
            __init__:
                inicia interface grafica

                instancia outras classes:
                    self.BD:
                        instancia classe que faz conexao com banco de dados
                    self.con:
                        instancia classe que faz a autenticacao no banco de dados
                    self.ins:
                        instancia classe que faz as insercoes no banco de dados
                    self.rem:
                        instancia classe que faz as remocoes no banco de dados
                    self.up:
                        instancia classe que faz as alteracoes no banco de dados
                    self.cons:
                        instancia classe que faz as consultas no banco de dados

            create_widget_first:
                cria os botoes da primeira interface,
                botao de conectar, inserir, remover, alterar e consultar

            change_color_connect:
                altera a cor do botao conectar :
                    verde se conectado
                    vermelho se desconectado

            error_window (menssage):
                abre uma nova janela(pop-up) para mostrar ao usuario
                algum erro
                metodo chamado sempre que um error ocorrer

                    menssage:
                        string que sera mostrada na janela que ira abrir

            disconnect:
                desconecta do banco de dados

            fecha_erro:
                fecha a janela criada por error_window
                Eh chamada quando o usuario clica em "fechar" na janela que o error_window abre

            close:
                disconecta do banco de dados e fecha a janela principal


    """
    def __init__(self):
        self.master = tkinter.Tk()
        self.master.title('Banco de Dados')
        tkinter.Frame.__init__(self, self.master)
        self.grid()
        self.BD = DBConnection.DBConnection()
        self.con = Connection(self.BD, self.error_window, self.change_color_connect)
        self.ins = Insert(self.BD, self.error_window)
        self.rem = Remove(self.BD, self.error_window)
        self.up = Update(self.BD, self.error_window)
        self.cons = Consult(self.BD, self.error_window)
        self.login = None
        self.senha = None
        self.button_add_field = None
        self.number_table_fields = 0
        self.new_win = None
        self.fields_table = []
        self.create_widget_first()

    def create_widget_first(self):
        # botao connect
        self.connect = tkinter.Button(self, text='Conectar', font=40, background='red', command=self.con.connect)
        self.connect.grid(row=0, column=1, ipadx=20, ipady=20)

        # Botao Insert
        self.insert = tkinter.Button(self, text='Inserir Novos\n Dados', font=40, command=self.ins.insert)
        self.insert.grid(row=1, column=0, ipadx=15, ipady=15, padx=10, pady=10)

        # Botao remover
        self.remove = tkinter.Button(self, text='Remover Dados', font=40, command=self.rem.remove)
        self.remove.grid(row=1, column=3, ipadx=15, ipady=15, padx=10, pady=10)

        # Botao atualizar
        self.update = tkinter.Button(self, text='Atualizar Dados', font=40, command=self.up.update)
        self.update.grid(row=2, column=0, ipadx=15, ipady=15, padx=10, pady=10)

        # Botao consultar
        self.consult = tkinter.Button(self, text='Consultar Dados', font=40, command=self.cons.consult)
        self.consult.grid(row=2, column=3, ipadx=15, ipady=15, padx=10, pady=10)

    def change_color_connect(self):
        if self.connect['background'] == 'red':
            self.connect['background'] = 'green'
        else:
            self.connect['background'] = 'red'

    def error_window(self, menssage):
        self.new_window = tkinter.Toplevel()
        self.new_window.title('Error')
        self.new_window.geometry('300x100')
        tkinter.Label(self.new_window, text=menssage, font=25).grid(row=0)
        tkinter.Button(self.new_window, text='Fechar', command=self.fecha_erro).grid(row=2)

    def disconnect(self):
        self.BD.stop_connection()

    def fecha_erro(self):
        self.new_window.destroy()

    def close(self):
        self.BD.stop_connection()
        exit()


def main():
    a = Interface()
    a.mainloop()


if __name__ == '__main__':
    main()
