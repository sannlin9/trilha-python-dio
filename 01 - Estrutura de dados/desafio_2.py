def menu():
    return """
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nu] Novo Usuário
    [nc] Nova Conta
    [lc] Listar Contas
    [q] Sair

    => """

def depositar(conta_corrente):  # Agora passa a lista de contas como argumento
    agencia = input("Informe a agência: ")
    numero_conta = int(input("Informe o número da conta: "))
    conta = filtrar_conta(agencia, numero_conta, conta_corrente)
    
    if conta:
        valor = float(input("Informe o valor do depósito: "))
        if valor > 0:
            conta["saldo"] += valor
            conta["extrato"] += f"Depósito: R$ {valor:.2f}\n"
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso na conta {numero_conta}!")
        else:
            print("Operação falhou! O valor informado é inválido.")
    else:
        print("Conta não encontrada!")

def sacar(conta_corrente):  # Agora passa a lista de contas como argumento
    agencia = input("Informe a agência: ")
    numero_conta = int(input("Informe o número da conta: "))
    conta = filtrar_conta(agencia, numero_conta, conta_corrente)

    if conta:
        valor = float(input("Informe o valor do saque: "))
        excedeu_saques = conta["numero_saques"] >= conta["LIMITE_SAQUES"]
        limite_disponivel = conta["saldo"] + conta["limite"] - conta["total_sacado"]

        if excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")
        elif valor > limite_disponivel:
            print(f"Operação falhou! O valor do saque excede o limite disponível de R$ {limite_disponivel:.2f}.")
        elif valor > 0:
            if valor <= conta["saldo"]:
                conta["saldo"] -= valor
            else:
                diferenca = valor - conta["saldo"]
                conta["saldo"] = 0
                conta["total_sacado"] += diferenca

            conta["extrato"] += f"Saque: R$ {valor:.2f}\n"
            conta["numero_saques"] += 1
            print(f"Saque de R$ {valor:.2f} realizado com sucesso na conta {numero_conta}!")
            print(f"Você já utilizou - R$ {conta['total_sacado']:.2f} do seu limite de R$ {conta['limite']:.2f}.")
        else:
            print("Operação falhou! O valor informado é inválido.")
    else:
        print("Conta não encontrada!")

def exibir_extrato(conta_corrente):  # Agora passa a lista de contas como argumento
    agencia = input("Informe a agência: ")
    numero_conta = int(input("Informe o número da conta: "))
    conta = filtrar_conta(agencia, numero_conta, conta_corrente)

    if conta:
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not conta["extrato"] else conta["extrato"])
        print(f"Saldo: R$ {conta['saldo']:.2f}")
        print(f"Total sacado do limite: R$ {conta['total_sacado']:.2f} de um limite de R$ {conta['limite']:.2f}")
        print("==========================================")
    else:
        print("Conta não encontrada!")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario_existente = filtrar_usuario(cpf, usuarios)
    if usuario_existente:
        print("\n@@@ Já existe um usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("\n=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def filtrar_conta(agencia, numero_conta, conta_corrente):
    contas_filtradas = [conta for conta in conta_corrente if conta["agencia"] == agencia and conta["numero_conta"] == numero_conta]
    return contas_filtradas[0] if contas_filtradas else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do titular: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario,
            "saldo": 0,
            "limite": 500,
            "extrato": "",
            "numero_saques": 0,
            "LIMITE_SAQUES": 3,
            "total_sacado": 0
        }
    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
    return None

def listar_contas(conta_corrente):
    if not conta_corrente:
        print("\n@@@ Não há contas cadastradas! @@@")
    for conta in conta_corrente:
        print(f"\nAgência: {conta['agencia']}, Número da Conta: {conta['numero_conta']}, Titular: {conta['usuario']['nome']}")

def main():
    usuarios = []
    conta_corrente = []
    agencia = "0001"
    numero_conta = 1  # Número inicial para as contas

    while True:
        opcao = input(menu()).strip().lower()

        if opcao == "d":
            depositar(conta_corrente)
        elif opcao == "s":
            sacar(conta_corrente)
        elif opcao == "e":
            exibir_extrato(conta_corrente)
        elif opcao == "nu":
            criar_usuario(usuarios)
        elif opcao == "nc":
            conta = criar_conta(agencia, numero_conta, usuarios)
            if conta:
                conta_corrente.append(conta)
                numero_conta += 1  # Incrementa o número da conta após criação
        elif opcao == "lc":
            listar_contas(conta_corrente)
        elif opcao == "q":
            print("Obrigado por usar o sistema bancário. Até logo!")
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()
