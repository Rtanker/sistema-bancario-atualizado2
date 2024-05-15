import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

class Cliente:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

class ContaBancaria:
    numero_conta = 1

    def __init__(self, cliente, saldo_inicial=0):
        self.agencia = "0001"
        self.numero_conta = ContaBancaria.numero_conta
        ContaBancaria.numero_conta += 1
        self.cliente = cliente
        self.saldo = saldo_inicial
        self.transacoes = []

    def depositar(self, valor):
        if valor > 0:
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.transacoes.append((data_hora, f"Depósito de R${valor:.2f}"))
            self.saldo += valor
            return True
        else:
            return False

    def sacar(self, valor):
        if valor > 0 and valor <= self.saldo:
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.transacoes.append((data_hora, f"Saque de R${valor:.2f}"))
            self.saldo -= valor
            return True
        else:
            return False

    def obter_extrato(self):
        extrato = "Extrato:\n"
        for transacao in sorted(self.transacoes, key=lambda x: datetime.strptime(x[0], "%d/%m/%Y %H:%M:%S")):
            extrato += f"{transacao[1]} - Data: {transacao[0]}\n"
        extrato += f"Saldo atual: R${self.saldo:.2f}"
        return extrato

class SistemaBancario:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Bancário")

        # Variáveis
        self.clientes = []
        self.contas = []

        # Labels
        self.label_saldo = tk.Label(root, text="Saldo: R$0.00", font=("Arial", 12))
        self.label_saldo.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Botões
        self.button_depositar = tk.Button(root, text="Depositar", command=self.depositar)
        self.button_depositar.grid(row=1, column=0, padx=10, pady=5, sticky="we")

        self.button_sacar = tk.Button(root, text="Sacar", command=self.sacar)
        self.button_sacar.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        self.button_extrato = tk.Button(root, text="Visualizar Extrato", command=self.visualizar_extrato)
        self.button_extrato.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.button_listar_usuarios = tk.Button(root, text="Listar Usuários Cadastrados", command=self.listar_usuarios_cadastrados)
        self.button_listar_usuarios.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

    def cadastrar_cliente(self, cliente):
        self.clientes.append(cliente)

    def cadastrar_conta(self, cliente):
        valor_deposito = float(simpledialog.askstring("Cadastrar Conta Bancária", "Valor do Depósito Inicial:"))
        nova_conta = ContaBancaria(cliente, valor_deposito)
        self.contas.append(nova_conta)
        messagebox.showinfo("Sucesso", f"Conta cadastrada com sucesso para {cliente.nome}!")

    def depositar(self):
        cliente = self.selecionar_cliente()
        if cliente:
            valor = float(simpledialog.askstring("Depositar", "Digite o valor a ser depositado:"))
            conta = self.obter_conta(cliente)
            if conta:
                if conta.depositar(valor):
                    messagebox.showinfo("Sucesso", f"Depósito de R${valor:.2f} realizado com sucesso!")
                else:
                    messagebox.showerror("Erro", "Valor de depósito inválido!")
            else:
                messagebox.showerror("Erro", "Conta não encontrada!")

    def sacar(self):
        cliente = self.selecionar_cliente()
        if cliente:
            valor = float(simpledialog.askstring("Sacar", "Digite o valor a ser sacado:"))
            conta = self.obter_conta(cliente)
            if conta:
                if conta.sacar(valor):
                    messagebox.showinfo("Sucesso", f"Saque de R${valor:.2f} realizado com sucesso!")
                else:
                    messagebox.showerror("Erro", "Valor de saque inválido!")
            else:
                messagebox.showerror("Erro", "Conta não encontrada!")

    def visualizar_extrato(self):
        cliente = self.selecionar_cliente()
        if cliente:
            conta = self.obter_conta(cliente)
            if conta:
                extrato = conta.obter_extrato()
                messagebox.showinfo("Extrato", extrato)
            else:
                messagebox.showerror("Erro", "Conta não encontrada!")

    def listar_usuarios_cadastrados(self):
        lista_usuarios = ""
        for cliente in self.clientes:
            lista_usuarios += f"Nome: {cliente.nome}\nCPF: {cliente.cpf}\n"
            for conta in self.contas:
                if conta.cliente == cliente:
                    lista_usuarios += f"Número da Conta: {conta.numero_conta}\n"
            lista_usuarios += "\n"
        messagebox.showinfo("Usuários Cadastrados", lista_usuarios)

    def selecionar_cliente(self):
        nome_cliente = simpledialog.askstring("Selecionar Cliente", "Nome do Cliente:")
        for cliente in self.clientes:
            if cliente.nome == nome_cliente:
                return cliente
        messagebox.showerror("Erro", "Cliente não encontrado!")
        return None

    def obter_conta(self, cliente):
        for conta in self.contas:
            if conta.cliente == cliente:
                return conta
        return None

if __name__ == "__main__":
    root = tk.Tk()
    sistema_bancario = SistemaBancario(root)

    # Botões de cadastro
    button_cadastrar_usuario = tk.Button(root, text="Cadastrar Usuário", command=lambda: sistema_bancario.cadastrar_cliente(Cliente(
        simpledialog.askstring("Cadastrar Usuário", "Nome:"),
        simpledialog.askstring("Cadastrar Usuário", "Data de Nascimento (dd/mm/aaaa):"),
        simpledialog.askstring("Cadastrar Usuário", "CPF:"),
        simpledialog.askstring("Cadastrar Usuário", "Endereço (logradouro, numero, bairro, cidade/sigla estado):")
    )))
    button_cadastrar_usuario.grid(row=4, column=0, padx=10, pady=5, sticky="we")

    button_cadastrar_conta = tk.Button(root, text="Cadastrar Conta Bancária", command=lambda: sistema_bancario.cadastrar_conta(sistema_bancario.selecionar_cliente()))
    button_cadastrar_conta.grid(row=4, column=1, padx=10, pady=5, sticky="we")

    root.mainloop()
