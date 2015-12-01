import cx_Oracle


class DBConnection:
    """
        Classe que interage diretamente com o bando de dados

        metodos:
            __init__:
                cria algumas variaves padrao
                    self.ip:
                        ip que sera usado para acessar o banco de dados
                    self.port:
                        porta que deve ser usada para acessar o banco de dados
                    self.SID:
                        SID que deve ser usado para acessar o banco de dados
                    self.dsn_tns:
                        cria a base para acessar posteriormente o banco de dados

            start_connection(login, senha):
                recebe o login e senha e tenta se conectar com o banco de dados

                    login: string
                        login do usuario
                    senha: string
                        senha do usuario

            stop_connection:
                se a conexao esta estabelecida entao desconecta
                se nao , nao faz nada

            search(string):
                ?

            get_all_table:
                procura e retorna todas as tabelas no banco de dados

            get_attributes_from_table(name_table):
                procura e retorna todos os atributos da tabela escolhida

                    name_table: string
                        nome da tabela

            insert_into_table(insert_tuple, name_table):
                cria a string que sera enviado para o banco de dados
                e insere no banco de dados

                    insert_tuple: dicionario
                        contem
                         nome do atributo : conteudo

                    name_table: string
                        nome da tabela

            get_primary_key(name_table):
                ?

            get_tuple(name_table):
                retorna todas as tuplas da tabela dada

                    name_table: string
                        nome da tabela

            is_connect:
                retorna True se estivar conectado
                False caso contrario

    """
    def __init__(self):
        self.ip = 'grad.icmc.usp.br'
        self.port = 15215
        self.SID = 'orcl'
        self.dsn_tns = cx_Oracle.makedsn(self.ip, self.port, self.SID)
        self.con = None

    def start_connection(self, login, senha):
        self.con = cx_Oracle.connect(login, senha, self.dsn_tns)

    def stop_connection(self):
        '''
            Retorna True se a conexao foi parada
            e False se a conexao ja estava parada
        '''
        if self.con is not None:
            self.con.close()
            self.con = None
            return True
        return False

    def search(self, string):
        cur = self.con.cursor()
        resposta = cur.execute(string)
        a = open('teste1.txt', 'w')
        a.write(resposta)
        a.close()

    def get_all_tables(self):
        all_tables = []
        cur = self.con.cursor()
        cur.execute('SELECT * FROM tab')
        for table in cur:
            if not table[0].startswith('BIN$'):
                table_name = table
                all_tables.append(table_name[0])
        return all_tables

    def get_attributes_from_table(self, name_table):
        cur = self.con.cursor()
        cur.execute('select * from ' + name_table)
        list_attributes = []
        # print(cur)
        # print(cur.description)
        for at in cur.description:
            # at[0] = nome do atributo
            # at[1] = tipo do atributo
            # at[2] = quantidade de caracters
            # at[len(at)-1] = 0 - not null, 1 - nullable
            list_attributes.append((at[0], at[1].__name__, at[2], at[len(at) - 1]))
        return list_attributes

    def insert_into_table(self, insert_tuple, name_table):
        cur = self.con.cursor()
        sql = 'INSERT INTO ' + name_table + ' ('
        for name_att in insert_tuple:
            # print('escrito: ' + str(name_att[0]) + ' tamanho: ' + str(len(name_att[0])))
            if str(insert_tuple[name_att]) != '':
                sql += ''.join(name_att[0])
                sql += ''.join(', ')
        sql = sql[:len(sql) - 2]
        sql += ''.join(') VALUES (')
        for name_att in insert_tuple:
            if str(insert_tuple[name_att]) != '':
                sql += ''.join(str(insert_tuple[name_att]))
                sql += ''.join(', ')
        sql = sql[:len(sql) - 2]
        sql += ''.join(')')
        print(sql)
        cur.execute(sql)
        self.con.commit()

    def get_primary_key(self, name_table):
        # TODO como faz essa coisa??
        pass

    def get_tuples(self, name_table):
        cur = self.con.cursor()
        sql = 'SELECT * FROM ' + name_table
        cur.execute(sql)
        list_tuples = list()
        list_att = self.get_attributes_from_table(name_table)
        for tuple in cur:
            dictionary = {}
            for j in range(len(tuple)):
                dictionary[list_att[j]] = tuple[j]
            list_tuples.append(dictionary)
        print(list_tuples)
        return list_tuples

    def is_connect(self):
        if self.con is not None:
            return True
        return False
