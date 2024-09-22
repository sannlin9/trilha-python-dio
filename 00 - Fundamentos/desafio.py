def menu():
    return """
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

    => """

def depositar(saldo, extrato):
    valor = float(input("Informe o valor do depósito: "))
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def sacar(saldo, extrato, limite, numero_saques, LIMITE_SAQUES, total_sacado):
    valor = float(input("Informe o valor do saque: "))
    excedeu_saques = numero_saques >= LIMITE_SAQUES
    limite_disponivel = saldo + limite - total_sacado  # Saldo disponível incluindo o limite

    if excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > limite_disponivel:
        print(f"Operação falhou! O valor do saque excede o limite disponível de R$ {limite_disponivel:.2f}.")
    elif valor > 0:
        # Calcular quanto será retirado do saldo e quanto do limite
        if valor <= saldo:
            saldo -= valor
        else:
            diferenca = valor - saldo
            saldo = 0
            total_sacado += diferenca

        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
        print(f"Você já utilizou - R$ {total_sacado:.2f} do seu limite de R$ {limite:.2f}.")
    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato, numero_saques, total_sacado

def exibir_extrato(saldo, extrato, total_sacado, limite):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"Saldo: R$ {saldo:.2f}")
    print(f"Total sacado do limite: R$ {total_sacado:.2f} de um limite de R$ {limite:.2f}")
    print("==========================================")

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    total_sacado = 0

    while True:
        opcao = input(menu()).strip().lower()

        if opcao == "d":
            saldo, extrato = depositar(saldo, extrato)
        elif opcao == "s":
            saldo, extrato, numero_saques, total_sacado = sacar(
                saldo, extrato, limite, numero_saques, LIMITE_SAQUES, total_sacado
            )
        elif opcao == "e":
            exibir_extrato(saldo, extrato, total_sacado, limite)
        elif opcao == "q":
            print("Obrigado por usar o sistema bancário. Até logo!")
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()
