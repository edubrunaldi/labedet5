import tkinter
from pprint import pprint

import cx_Oracle


class Connection:
    """
        Classe que faz as autenticacoes no banco de dados

        metodos:

            __init__(BD, error_window, change_color_connect):
                BD:
                    interage com o banco de dados
                error_window:
                    metodo do Interface que criar um pop-up com um mensagem de erro
                change_color_connect:
                    metodo do Interface que altera a cor do botao Conectar

            connect:
                cria uma nova janela pedindo login e senha para se conectar

            try_connect:
                com o login e senha fornecido tenta se conectar com o banco de dados
    """
    def __init__(self, BD, error_window, change_color_connect):
        self.BD = BD
        self.error_window = error_window
        self.change_color_connect = change_color_connect
        # self.root = root

    def connect(self):
        if self.BD.is_connect():
            if self.BD.stop_connection():
                self.change_color_connect()
            return
        self.new_win = tkinter.Toplevel()
        self.new_win.title('Connection')
        self.new_win.geometry('350x150')
        tkinter.Label(self.new_win, text='ID: ', font=30).grid(row=0, column=0, ipady=2)
        tkinter.Label(self.new_win, text='password: ', font=30).grid(row=1, column=0, ipady=2)
        self.login = tkinter.Entry(self.new_win)
        self.login.grid(row=0, column=1, sticky=tkinter.W, ipadx=20, ipady=3)
        self.senha = tkinter.Entry(self.new_win, show='*')
        self.senha.grid(row=1, column=1, sticky=tkinter.W, ipadx=20, ipady=3)
        tkinter.Button(self.new_win, text='Connect', font=30, command=self.try_connection).grid(row=2, column=1)

    def try_connection(self):
        login = self.login.get()
        senha = self.senha.get()
        try:
            self.BD.start_connection(login, senha)
            self.change_color_connect()
        except cx_Oracle.DatabaseError as ee:
            if 'ORA-01017' in str(ee):
                #ORA-01017 erro que indica que o usuario ou senha esta errado
                self.error_window('Erro ao tentar fazer o login\nUsuario ou Senha errado!!')
        else:
            self.new_win.destroy()


class Insert:
    """
        Classe que faz as insercoes no banco de dados

        metodo:

            __init__(BD, error_window):
                BD:
                    interage com o banco de dados
                error_window:
                    metodo do Interface que criar um pop-up com um mensagem de erro

            insert:
                procura todas as tabelas no banco de dados
                cria uma nova janela com todas as tabelas para
                que o usuario escolha uma para fazer a insercao

            insert_into_table(name_table):
                cria uma nova janela com todos atributos e seus campos para adiciona-lo
                se o atributo for not null entao o nome do atributo sera apresentado em vermelho

                    name_table:
                        string contendo o nome da tabela escolhido no metodo insert

            insert_into( list_attributes, name_table):
                cria um dicionario com o nome do atributo e seu conteudo
                e verifica para cada atributo coloca se esta de modo correto
                utilizando o metodo validate_attributes
                ex: se em NUMBER foi dado um inteiro ou entao
                    se em DATETIME esta mm/dd/aaaa



                    list_attributes:
                        lista do nome de todos atributos da tabela escolhida

                    name_table:
                        nome da tabela escolhida

            validate_attributes(self, list_attributes, insert_tuple):
                dado o nome do atributo ( list_attributes) e o
                nome conteudo do atributo( insert_tuple) verifica
                se o atributo eh valido

    """
    def __init__(self, BD, error_window):
        self.BD = BD
        self.error_window = error_window

    def insert(self):
        if not self.BD.is_connect():
            self.error_window('Conexao nao ativa!')
            return
        self.new_win = tkinter.Toplevel()
        self.new_win.title('Insercao')
        tables = self.BD.get_all_tables()
        self.tables_buttons = []
        tkinter.Label(self.new_win, text='Escolha\n uma\ntabela').grid(row=0, column=1)
        for i in range(len(tables)):
            if i % 2 == 1:
                self.tables_buttons.append(
                    tkinter.Button(self.new_win, text=tables[i], command=lambda x=i: self.insert_into_table(tables[x]))
                )
                self.tables_buttons[i].grid(row=i, column=0, padx=8, pady=8)
            else:
                self.tables_buttons.append(
                    tkinter.Button(self.new_win, text=tables[i], command=lambda x=i: self.insert_into_table(tables[x]))
                )
                self.tables_buttons[i].grid(row=i + 1, column=2, padx=8, pady=8, ipadx=20)

    def insert_into_table(self, name_table):
        list_attributes = self.BD.get_attributes_from_table(name_table)
        new_win = tkinter.Toplevel()
        new_win.title('Inserir na tabela ' + name_table)
        self.texts_attributes = []
        for i in range(len(list_attributes)):
            if list_attributes[i][3]:
                tkinter.Label(
                    new_win,
                    text=list_attributes[i][0] + '(' + list_attributes[i][1] + ')'
                ).grid(
                    row=i,
                    column=0
                )
            else:
                tkinter.Label(
                    new_win,
                    text=list_attributes[i][0] + '(' + list_attributes[i][1] + ')',
                    fg='red'
                ).grid(
                    row=i,
                    column=0
                )
            if list_attributes[i][1] == 'DATETIME':
                self.texts_attributes.append(tkinter.Entry(new_win))
                self.texts_attributes[i].insert(tkinter.END, 'mm/dd/aaaa')
            else:
                self.texts_attributes.append(tkinter.Entry(new_win))
            self.texts_attributes[i].grid(
                row=i,
                column=1,
                sticky=tkinter.W,
                ipadx=20,
                ipady=2,
                padx=8,
                pady=8
            )
        button_insert = tkinter.Button(new_win, text='Inserir', font=30,
                                       command=lambda: self.insert_into(list_attributes, name_table))
        button_insert.grid(row=len(list_attributes), column=1)

    def insert_into(self, list_attributes, name_table):
        insert_tuple = {}
        for i in range(len(list_attributes)):
            text_attribute = self.texts_attributes[i].get()
            insert_tuple[list_attributes[i]] = text_attribute
        if self.validate_attributes(list_attributes, insert_tuple):
            try:
                self.BD.insert_into_table(insert_tuple, name_table)
            except Exception as ee:
                print(ee)
                # TODO tratar excecoes do inserte nas tabelas
                pass

    def validate_attributes(self, list_attributes, insert_tuple):
        for type_att in list_attributes:
            """
                Para cada tipo de atributo  verifica se
                 o conteudo passado pelo usuario esta correto.
                Se nao estiver entao um pop-up com o erro encontrado eh mostrado.
            """
            # print(type_att[1])
            if type_att[1] == 'NUMBER':
                try:
                    if insert_tuple[type_att] != '':
                        insert_tuple[type_att] = int(insert_tuple[type_att])
                        # verficiar quantidade de numeros possiveis
                        if len(str(insert_tuple[type_att])) >= type_att[2]:
                            self.error_window(
                                type_att[0] + ' deve ter\n no maximo ' + str(type_att[2] - 1) + ' numeros')
                    elif not type_att[3]:  # se o atributo deve ser not null
                        self.error_window(type_att[0] + ' nao pode ser nulo')
                        return False
                except ValueError:
                    self.error_window(type_att[0] + ' deve ser \n' + type_att[1])
                    return False
            elif type_att[1] == 'FIXED_CHAR':
                if insert_tuple[type_att] != '':
                    # verifica quantidade de caracteres possiveis
                    if len(insert_tuple[type_att]) > type_att[2]:
                        self.error_window(type_att[0] + ' deve ter\n no maximo ' + str(type_att[2]) + ' caracteres')
                        return False
                    insert_tuple[type_att] = '\'' + insert_tuple[type_att] + '\''
                elif not type_att[3]:  # se o atributo deve ser not null
                    self.error_window(type_att[0] + ' nao pode ser nulo')
                    return False
            elif type_att[1] == 'STRING':
                if insert_tuple[type_att] != '':
                    # verifica quantidade de caracteres possiveis
                    if len(insert_tuple[type_att]) > type_att[2]:
                        self.error_window(type_att[0] + ' deve ter\n no maximo ' + str(type_att[2]) + ' caracteres')
                        return False
                    insert_tuple[type_att] = '\'' + insert_tuple[type_att] + '\''
                elif not type_att[3]:  # se o atributo deve ser not null
                    self.error_window(type_att[0] + ' nao pode ser nulo')
                    return False
            elif type_att[1] == 'DATETIME':
                try:
                    mm, dd, aaaa = insert_tuple[type_att].split('/')
                    insert_tuple[type_att] = 'TO_DATE(\'' + insert_tuple[type_att] + '\', \'mm/dd/yyy\')'
                except ValueError:
                    self.error_window('Um erro acontceu na data. ex. data:\n mm/dd/aaaa')

        return True


class Remove:
    """
        Classe que faz as remocoes no banco de dados

        metodo:

            __init__(BD, error_window):
                BD:
                    interage com o banco de dados
                error_window:
                    metodo do Interface que criar um pop-up com um mensagem de erro

            remove:
                procura todas as tabelas no banco de dados
                cria uma nova janela com todas as tabelas para
                que o usuario escolha uma para fazer a remocao

            choose_tuple(name_table):
                apresenda toda as tuplas da tabela escolhida
                com um checkbutton para escolher qual tupla deve ser removida

                    name_table:
                        string contendo o nome da tabela escolhida
    """
    def __init__(self, BD, error_window):
        self.BD = BD
        self.error_window = error_window
        self.tuple_remove = None

    def remove(self):
        '''if not self.BD.is_connect():
            self.error_window('Conexao nao ativa!')
            return'''
        self.new_win = tkinter.Toplevel()
        self.new_win.title('Remocao')
        tables = self.BD.get_all_tables()
        self.tables_buttons = []
        tkinter.Label(self.new_win, text='Escolha\n uma\ntabela').grid(row=0, column=1)
        for i in range(len(tables)):
            if i % 2 == 1:
                self.tables_buttons.append(
                    tkinter.Button(self.new_win, text=tables[i], command=lambda x=i: self.choose_tuple(tables[x]))
                )
                self.tables_buttons[i].grid(row=i, column=0, padx=8, pady=8)
            else:
                self.tables_buttons.append(
                    tkinter.Button(self.new_win, text=tables[i], command=lambda x=i: self.choose_tuple(tables[x]))
                )
                self.tables_buttons[i].grid(row=i + 1, column=2, padx=8, pady=8, ipadx=20)

    def choose_tuple(self, name_table):
        list_tuples = self.BD.get_tuples(name_table)
        root = tkinter.Tk()
        root.geometry('500x500')
        TableShow(root, list_tuples, self.error_window, choose=True, variavel=self.tuple_choosed).pack(fill='both', expand=True)
        root.mainloop()
        pprint(self.tuple_remove)
        # TODO enviar para o BD fazer remove

    def tuple_choosed(self, value):
        self.tuple_remove = value

class Update:
    # TODO tudo - copiar do remove
    """Classe que faz as alteracoes no banco de dados

        metodo:

            __init__(BD, error_window):
                BD:
                    interage com o banco de dados
                error_window:
                    metodo do Interface que criar um pop-up com um mensagem de erro

            update:
                procura todas as tabelas no banco de dados
                cria uma nova janela com todas as tabelas para
                que o usuario escolha uma para fazer a alteracao
    """
    def __init__(self, BD, error_window):
        self.BD = BD
        self.error_window = error_window
        self.tuple_update = None

    def update(self):
        '''if not self.BD.is_connect():
            self.error_window('Conexao nao ativa!')
            return'''
        self.new_win = tkinter.Toplevel()
        self.new_win.title('Atualizacao')
        tables = self.BD.get_all_tables()
        self.tables_buttons = []
        tkinter.Label(self.new_win, text='Escolha\n uma\ntabela').grid(row=0, column=1)
        for i in range(len(tables)):
            if i % 2 == 1:
                self.tables_buttons.append(
                    tkinter.Button(self.new_win, text=tables[i], command=lambda x=i: self.choose_tuple(tables[x]))
                )
                self.tables_buttons[i].grid(row=i, column=0, padx=8, pady=8)
            else:
                self.tables_buttons.append(
                    tkinter.Button(self.new_win, text=tables[i], command=lambda x=i: self.choose_tuple(tables[x]))
                )
                self.tables_buttons[i].grid(row=i + 1, column=2, padx=8, pady=8, ipadx=20)

    def choose_tuple(self, name_table):
        list_tuples = self.BD.get_tuples(name_table)
        root = tkinter.Tk()
        root.geometry('500x500')
        TableShow(root, list_tuples, self.error_window, choose=True, variavel=self.tuple_choosed).pack(fill='both', expand=True)
        root.mainloop()
        pprint(self.tuple_update)
        # TODO enviar para o BD fazer update

    def tuple_choosed(self, value):
        self.tuple_remove = value


class Consult:
    """
        Classe que faz as consultas no banco de dados

        metodo:

            __init__(BD, error_window):
                BD:
                    interage com o banco de dados
                error_window:
                    metodo do Interface que criar um pop-up com um mensagem de erro

            consult:
                procura todas as tabelas no banco de dados
                cria uma nova janela com todas as tabelas para
                que o usuario escolha uma para fazer a consulta

            consult_table(name_table):
                apresenta todas as tuplas da tabela escolhida

                    name_table:
                        string contendo o nome da tabela escolhida
    """
    def __init__(self, BD, error_window):
        self.BD = BD
        self.error_window = error_window

    def consult(self):
        '''if not self.BD.is_connect():
            self.error_window('Conexao nao ativa!')
            return'''
        self.new_win = tkinter.Toplevel()
        self.new_win.title('Consulta')
        tables = self.BD.get_all_tables()
        self.tables_buttons = []
        tkinter.Label(self.new_win, text='Escolha\n uma\ntabela').grid(row=0, column=1)
        for i in range(len(tables)):
            if i % 2 == 1:
                self.tables_buttons.append(
                    tkinter.Button(self.new_win, text=tables[i], command=lambda x=i: self.consult_table(tables[x]))
                )
                self.tables_buttons[i].grid(row=i, column=0, padx=8, pady=8)
            else:
                self.tables_buttons.append(
                    tkinter.Button(self.new_win, text=tables[i], command=lambda x=i: self.consult_table(tables[x]))
                )
                self.tables_buttons[i].grid(row=i + 1, column=2, padx=8, pady=8, ipadx=20)

    def consult_table(self, name_table):
        list_tuples = self.BD.get_tuples(name_table)
        root = tkinter.Tk()
        root.geometry('500x500')
        TableShow(root, list_tuples).pack(fill='both', expand=True)
        root.mainloop()





class TableShow(tkinter.Frame):
    """
        Classe que cria uma janela para apresentar a tabela pega no banco de dados

        __init__(root, list_tuples, chooose=False):
            Criar uma nova Janela mostrando todas as tuplas(list_tuples)

                root:
                    Criador da janela

                list_tuples:
                    lista de todas as tuplas contidas em uma tabela

                choose:
                    se eh para apenas imprimir a tabela (False)
                    ou
                    imprimir e poder escolher uma das tuplas (True)

        onFrameConfigure(event):
            fazer scroll em toda tabela

                event:
                    instancia do evento dado

    """
    def __init__(self, root, list_tuples, error_window, choose=False, variavel=None, **kwargs):
        tkinter.Frame.__init__(self, root, **kwargs)
        self.choose = choose
        self.variavel = variavel
        self.root = root
        self.error_window = error_window

        self.canvas = tkinter.Canvas(root, borderwidth=0, background="#ffffff")
        self.table = tkinter.Frame(self.canvas, background="#ffffff")
        scrollbar_v = tkinter.Scrollbar(self.canvas, orient='vertical', command=self.canvas.yview)
        scrollbar_h = tkinter.Scrollbar(self.canvas, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

        scrollbar_v.pack(side='right', fill='y')
        scrollbar_h.pack(side='bottom', fill='x')
        self.canvas.pack(side='left', fill='both', expand=True)
        self.canvas.create_window((4, 4), window=self.table, tags='table')
        self.table.bind("<Configure>", self.onFrameConfigure)

        self.widgets = {}
        rowid = 0
        tuple_att = list_tuples[0]  # recebe a primeira tupla para colocar os nomes de cada tupla
        k=0
        self.widgets[rowid] = {}
        self.var = tkinter.StringVar(master=self.table)
        if self.choose:
            self.widgets[rowid][rowid] = tkinter.Label(self.table, text='Change')
            self.widgets[rowid][rowid].grid(row=rowid, column=k, sticky='nsew')
            k += 1
        for i in tuple_att:
            self.widgets[rowid][i[0]] = tkinter.Label(self.table, text=str(i[0]))
            self.widgets[rowid][i[0]].grid(row=rowid, column=k, sticky='nsew')
            k += 1
        # TODO colocar os nome dos atributos
        for tuple_att in list_tuples:
            rowid += 1
            self.widgets[rowid] = {}
            k=0
            if self.choose:
                self.widgets[rowid][rowid] = tkinter.Radiobutton(self.table, text='', variable=self.var, value=rowid)
                self.widgets[rowid][rowid].grid(row=rowid, column=k, sticky='nsew')
                k += 1
            for i in tuple_att:
                self.widgets[rowid][i[0]] = tkinter.Label(self.table, text=str(tuple_att[i]))
                self.widgets[rowid][i[0]].grid(row=rowid, column=k, sticky='nsew')
                k += 1

        tkinter.Button(self.table, text='Done!', command=self.choosed).grid(row=rowid+1, column=0)

        self.table.grid_columnconfigure(1, weight=1, pad=4)
        self.table.grid_columnconfigure(2, weight=1, pad=4)
        self.table.grid_rowconfigure(rowid+2, weight=1, pad=4)

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def choosed(self):
        if self.choose:
            if self.var.get() is '':
                self.error_window('Nao foi escolhido nenhuma tupla')
                return
            index = int(self.var.get())
            tuple_values = {}
            for i in self.widgets[index]:
                """
                    key: i = nome do atributo da tabela
                    value: valor de cada atributo da linha selecionada
                """
                tuple_values[i] = self.widgets[index][i]['text']
            self.variavel(tuple_values)
        # destroi tudo para sair da pagina
        self.table.destroy()
        self.canvas.destroy()
        self.root.destroy()
        self.root.quit()