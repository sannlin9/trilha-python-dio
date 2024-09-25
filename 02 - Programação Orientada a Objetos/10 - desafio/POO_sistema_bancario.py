
from abc import ABC, abstractmethod, classmethod, property
from datetime import datetime
import textwrap

#Classe Cliente  
class Cliente:
    def __init__(self,endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self,conta,transacao) : ##incluir transacao ao historico
        transacao.registrar(conta)
        
    def adicionar_conta(self, conta): #criar conta atrelada ao cliente
        self.contas.append(conta)
     
#cria novo cliente    
class PessoaFisica(Cliente): 
    def __init__(self,nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
    
#criar clase conta
class Conta:
    def __init__(self,numero,cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        
    @classmethod
    def nova_conta(cls, cliente,numero):
        return cls(numero,cliente)
    @property
    def  saldo(self):
        return self._saldo
    @property
    def numero(self):
        return self._numero
    @property
    def agencia(self):
        return self._agencia
    @property
    def cliente(self):
        return self._cliente
    @property
    def historico(self):
        return self._historico
    def sacar(self,valor):  # operação de saque
        saldo = self.saldo
        sem_saldo = valor > saldo

        if sem_saldo:
            print(f"Operação falhou! O valor do saque excede o limite disponível de R$ {saldo:.2f}.")
        elif valor > 0:
            self._saldo -= valor 
            print(f"Saque de R$ {valor:.2f} realizado com sucesso na conta!")
            return True
        
        else:
            print("Operação falhou! O valor informado é inválido.")
        
        return False
    
    def depositar(self, valor): #operação deposito
        if valor > 0:
            self._saldo += valor #conta["saldo"] += valor
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso na conta!")
        else:
            print("Operação falhou! O valor informado é inválido.")
            return False
        
        return True
    
class Conta_corrente(Conta): #cria conta
    def __init__(self, numero, cliente, limite = 500, limite_saque=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque
        
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["Tipo"]== sacar.__name__]
        )
        passa_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saque
        if passa_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número de saques diarias excedeu o limite. @@@")
        else:
            return super().sacar(valor)
        
        return False
def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

#Criar as classes de transação, extrato e historico
class Historico:
    def __init__(self):
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes
    def adicionar_transacoes(self, transacao):
        self._transacoes.append(
            {
                "Tipo": transacao.__class__.__name__,
                "Valor": transacao.valor,
                "Data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )
        
class Transacao(abs):
    @property
    @abstractmethod
    def valor(self):
        pass
    @abstractmethod
    def registrar(self, conta):
        pass
##gravando saque e deposito na transacao e no historico
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao: 
            conta.historico.adicionar_transacao(self)
            
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao: 
            conta.historico.adicionar_transacao(self)
    
def menu():
    menu = """
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nu] Novo Usuário
    [nc] Nova Conta
    [lc] Listar Contas
    [q] Sair
    => """
    
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf,cliente):
    clientes_filtrados = [cliente for cliente in cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not Cliente.conta: 
        print("Cliente não possui conta!")
        return
    
    return Cliente.conta[0]

def depositar(cliente):
    cpf = input("Informe o CPF do titular: ")
    cliente = filtrar_cliente(cpf, cliente)

    if not Cliente:
        print("Cliente não encontrado!")
        return

    valor = float(input("Informe o valor a ser depositado: "))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta,transacao)
    
def sacar(cliente):
    cpf = input("Informe o CPF do titular: ")
    cliente = filtrar_cliente(cpf, cliente)

    if not Cliente:
        print("Cliente não encontrado!")
        return

    valor = float(input("Informe o valor a ser depositado: "))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta,transacao)
    
def exibir_extrato(cliente):
    cpf = input("Informe o CPF do titular: ")
    cliente = filtrar_cliente(cpf, cliente)
    
    if not Cliente:
        print("Cliente não encontrado!")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")
    
def criar_cliente(cliente):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, cliente)
    
    if cliente:
        print("CLiente já cadastrado.")
        return
    
    nome = input("Informe o nome completo do titular: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    cliente = PessoaFisica(nome=nome, data_nascimento= data_nascimento, cpf=cpf, endereco=endereco)
    cliente.append(cliente)
    
    print("Cadastro criado com sucesso!")
    
def criar_conta(numero_conta, cliente, conta):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, cliente)
    
    if not Cliente:
        print("Cliente não encontrado!")
        return
    conta = Conta_corrente.nova_conta(cliente=cliente, numero=numero_conta, cpf=cpf)
    conta.append(conta)
    print("\n=== Conta criada com sucesso! ===")

def listar_contas(conta):
    if not conta:
        print("\n@@@ Não há contas cadastradas! @@@")
    for conta in conta:
        print(f"\nAgência: {conta['agencia']}, Número da Conta: {conta['numero_conta']}, Titular: {conta['usuario']['nome']}")

def main():
    Cliente = []
    conta = []
     

    while True:
        opcao = menu

        if opcao == "d":
            depositar(Cliente)
        elif opcao == "s":
            sacar(Cliente)
        elif opcao == "e":
            exibir_extrato(Cliente)
        elif opcao == "nu":
            criar_cliente(Cliente)
        elif opcao == "nc":
            numero_conta = len(conta) + 1
            conta = criar_conta(numero_conta,Cliente, conta)
           
        elif opcao == "lc":
            listar_contas(conta)
        elif opcao == "q":
            print("Obrigado por usar o sistema bancário. Até logo!")
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
