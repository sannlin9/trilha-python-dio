from datetime import datetime

class ContaBancaria:
    LIMITE_SAQUES = 3
    LIMITE_TRANSACOES_DIARIAS = 10
    
    def __init__(self, saldo_inicial=0, limite=500):
        self.saldo = saldo_inicial
        self.limite = limite
        self.extrato = []
        self.numero_saques = 0
        self.total_sacado = 0
        self.transacoes = 0
        self.data_ultima_transacao = datetime.now().date()
    
    def _atualizar_transacoes(self):
        """Verifica e reseta o número de transações diárias."""
        data_atual = datetime.now().date()
        if self.data_ultima_transacao != data_atual:
            self.transacoes = 0
            self.numero_saques = 0
            self.data_ultima_transacao = data_atual
    
    def _registrar_transacao(self, tipo, valor):
        """Registra uma transação no extrato com data e hora."""
        self.extrato.append(f"{tipo}: R$ {valor:.2f} - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        self.transacoes += 1

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self._registrar_transacao("Depósito", valor)
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
        else:
            print("Operação falhou! O valor informado é inválido.")

    def sacar(self, valor):
        self._atualizar_transacoes()
        
        if self.transacoes >= self.LIMITE_TRANSACOES_DIARIAS:
            print("Operação falhou! Limite de transações diárias excedido.")
            return
        
        limite_disponivel = self.saldo + self.limite - self.total_sacado

        if self.numero_saques >= self.LIMITE_SAQUES:
            print("Operação falhou! Número máximo de saques excedido.")
        elif valor > limite_disponivel:
            print(f"Operação falhou! O valor do saque excede o limite disponível de R$ {limite_disponivel:.2f}.")
        elif valor > 0:
            # Calcular quanto será retirado do saldo e quanto do limite
            if valor <= self.saldo:
                self.saldo -= valor
            else:
                diferenca = valor - self.saldo
                self.saldo = 0
                self.total_sacado += diferenca

            self._registrar_transacao("Saque", valor)
            self.numero_saques += 1
            print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
            print(f"Você já utilizou - R$ {self.total_sacado:.2f} do seu limite de R$ {self.limite:.2f}.")
        else:
            print("Operação falhou! O valor informado é inválido.")
    
    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        if not self.extrato:
            print("Não foram realizadas movimentações.")
        else:
            for transacao in self.extrato:
                print(transacao)
        print(f"\nSaldo: R$ {self.saldo:.2f}")
        print(f"Total sacado do limite: R$ {self.total_sacado:.2f} de um limite de R$ {self.limite:.2f}")
        print("==========================================")
    
    def menu(self):
        return """
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [q] Sair

        => """

def main():
    conta = ContaBancaria()

    while True:
        opcao = input(conta.menu()).strip().lower()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            conta.depositar(valor)
        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            conta.sacar(valor)
        elif opcao == "e":
            conta.exibir_extrato()
        elif opcao == "q":
            print("Obrigado por usar o sistema bancário. Até logo!")
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()
