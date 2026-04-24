import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import subprocess
import os

# --- Configurações do Banco de Dados --- #
DB_CONFIG = {
    'driver': '{ODBC Driver 17 for SQL Server}', # Pode variar dependendo da sua instalação
    'server': 'LBR-96WT9H4,1433', # Substitua pelo seu servidor SQL Server
    'database': 'AutomacaoSwitchesDB',
    'uid': 'sa', # Substitua pelo seu usuário
    'pwd': 'YourStrongPassword!' # Substitua pela sua senha
}

# --- Funções de Conexão e CRUD com o Banco de Dados --- #
def get_db_connection():
    try:
        conn = pyodbc.connect(
            f"DRIVER={DB_CONFIG['driver']};"
            f"SERVER={DB_CONFIG['server']};"
            f"DATABASE={DB_CONFIG['database']};"
            f"UID={DB_CONFIG['uid']};"
            f"PWD={DB_CONFIG['pwd']}"
        )
        return conn
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao banco de dados: {sqlstate}")
        return None

def create_cliente(nome_cliente):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Clientes (Nome_Cliente) VALUES (?) ", nome_cliente)
            conn.commit()
            messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            messagebox.showerror("Erro", f"Erro ao adicionar cliente: {sqlstate}")
        finally:
            conn.close()

def read_clientes():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ID_Cliente, Nome_Cliente FROM Clientes")
        clientes = cursor.fetchall()
        conn.close()
        return clientes
    return []

def update_cliente(id_cliente, novo_nome):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE Clientes SET Nome_Cliente = ? WHERE ID_Cliente = ?", novo_nome, id_cliente)
            conn.commit()
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            messagebox.showerror("Erro", f"Erro ao atualizar cliente: {sqlstate}")
        finally:
            conn.close()

def delete_cliente(id_cliente):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Clientes WHERE ID_Cliente = ?", id_cliente)
            conn.commit()
            messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            messagebox.showerror("Erro", f"Erro ao excluir cliente: {sqlstate}\nCertifique-se de que não há equipamentos associados a este cliente.")
        finally:
            conn.close()

def create_equipamento(nome_equipamento, ip_equipamento, id_cliente, configuracao_inicial):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Equipamentos (Nome_Equipamento, IP_Equipamento, ID_Cliente, Configuracao_Inicial) VALUES (?, ?, ?, ?)",
                           nome_equipamento, ip_equipamento, id_cliente, configuracao_inicial)
            conn.commit()
            messagebox.showinfo("Sucesso", "Equipamento adicionado com sucesso!")
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            messagebox.showerror("Erro", f"Erro ao adicionar equipamento: {sqlstate}")
        finally:
            conn.close()

def read_equipamentos():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT E.ID_Equipamento, E.Nome_Equipamento, E.IP_Equipamento, C.Nome_Cliente, E.Configuracao_Inicial FROM Equipamentos E JOIN Clientes C ON E.ID_Cliente = C.ID_Cliente")
        equipamentos = cursor.fetchall()
        conn.close()
        return equipamentos
    return []

def update_equipamento(id_equipamento, nome_equipamento, ip_equipamento, id_cliente, configuracao_inicial):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE Equipamentos SET Nome_Equipamento = ?, IP_Equipamento = ?, ID_Cliente = ?, Configuracao_Inicial = ? WHERE ID_Equipamento = ?",
                           nome_equipamento, ip_equipamento, id_cliente, configuracao_inicial, id_equipamento)
            conn.commit()
            messagebox.showinfo("Sucesso", "Equipamento atualizado com sucesso!")
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            messagebox.showerror("Erro", f"Erro ao atualizar equipamento: {sqlstate}")
        finally:
            conn.close()

def delete_equipamento(id_equipamento):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Equipamentos WHERE ID_Equipamento = ?", id_equipamento)
            conn.commit()
            messagebox.showinfo("Sucesso", "Equipamento excluído com sucesso!")
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            messagebox.showerror("Erro", f"Erro ao excluir equipamento: {sqlstate}")
        finally:
            conn.close()

# --- Função de Automação (Simulada) --- #
def simular_automacao_ssh(ip_equipamento, configuracao):
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Iniciando simulação de automação para {ip_equipamento}...\n")
    output_text.insert(tk.END, f"Conectando via SSH a {ip_equipamento}... (Simulado)\n")
    output_text.insert(tk.END, "Enviando configuração:\n")
    output_text.insert(tk.END, "------------------------------------\n")
    output_text.insert(tk.END, configuracao + "\n")
    output_text.insert(tk.END, "------------------------------------\n")
    output_text.insert(tk.END, "Configuração aplicada com sucesso! (Simulado)\n")
    output_text.insert(tk.END, "\n")

    # Exemplo de uso do subprocess (apenas para demonstração, não para SSH real)
    try:
        # Simula um ping para o IP do equipamento
        result = subprocess.run(['ping', '-n', '1', ip_equipamento], capture_output=True, text=True, check=True, encoding='latin-1')
        output_text.insert(tk.END, "Resultado do Ping (Simulado):\n")
        output_text.insert(tk.END, result.stdout)
    except subprocess.CalledProcessError as e:
        output_text.insert(tk.END, f"Erro no Ping (Simulado):\n{e.stderr}")
    except FileNotFoundError:
        output_text.insert(tk.END, "Comando 'ping' não encontrado. Certifique-se de que está no PATH.\n")

    output_text.insert(tk.END, "Simulação de automação concluída para {ip_equipamento}.\n")

# --- Interface Gráfica (Tkinter) --- #
class AutomacaoSwitchesApp:
    def __init__(self, root):
        self.root = root
        root.title("Sistema de Automação de Switches")
        root.geometry("1000x700")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True, fill="both")

        self.create_clientes_tab()
        self.create_equipamentos_tab()
        self.create_automacao_tab()

    def create_clientes_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Clientes")

        # Formulário de Cliente
        form_frame = ttk.LabelFrame(tab, text="Gerenciar Clientes")
        form_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(form_frame, text="Nome do Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.cliente_nome_entry = ttk.Entry(form_frame, width=40)
        self.cliente_nome_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.add_cliente_btn = ttk.Button(form_frame, text="Adicionar Cliente", command=self.add_cliente)
        self.add_cliente_btn.grid(row=0, column=2, padx=5, pady=5)

        self.update_cliente_btn = ttk.Button(form_frame, text="Atualizar Cliente", command=self.update_cliente)
        self.update_cliente_btn.grid(row=1, column=2, padx=5, pady=5)

        self.delete_cliente_btn = ttk.Button(form_frame, text="Excluir Cliente", command=self.delete_cliente)
        self.delete_cliente_btn.grid(row=2, column=2, padx=5, pady=5)

        # Tabela de Clientes
        self.clientes_tree = ttk.Treeview(tab, columns=("ID", "Nome"), show="headings")
        self.clientes_tree.heading("ID", text="ID")
        self.clientes_tree.heading("Nome", text="Nome do Cliente")
        self.clientes_tree.column("ID", width=50, anchor="center")
        self.clientes_tree.column("Nome", width=300)
        self.clientes_tree.pack(pady=10, padx=10, expand=True, fill="both")
        self.clientes_tree.bind("<<TreeviewSelect>>", self.load_cliente_to_form)

        self.refresh_clientes_list()

    def refresh_clientes_list(self):
        for i in self.clientes_tree.get_children():
            self.clientes_tree.delete(i)
        clientes = read_clientes()
        for cliente in clientes:
            self.clientes_tree.insert('', tk.END, values=cliente)

    def add_cliente(self):
        nome = self.cliente_nome_entry.get()
        if nome:
            create_cliente(nome)
            self.cliente_nome_entry.delete(0, tk.END)
            self.refresh_clientes_list()
        else:
            messagebox.showwarning("Aviso", "O nome do cliente não pode ser vazio.")

    def load_cliente_to_form(self, event):
        selected_item = self.clientes_tree.focus()
        if selected_item:
            values = self.clientes_tree.item(selected_item, 'values')
            self.cliente_id_selected = values[0]
            self.cliente_nome_entry.delete(0, tk.END)
            self.cliente_nome_entry.insert(0, values[1])

    def update_cliente(self):
        if hasattr(self, 'cliente_id_selected'):
            novo_nome = self.cliente_nome_entry.get()
            if novo_nome:
                update_cliente(self.cliente_id_selected, novo_nome)
                self.cliente_nome_entry.delete(0, tk.END)
                del self.cliente_id_selected
                self.refresh_clientes_list()
            else:
                messagebox.showwarning("Aviso", "O nome do cliente não pode ser vazio.")
        else:
            messagebox.showwarning("Aviso", "Selecione um cliente para atualizar.")

    def delete_cliente(self):
        if hasattr(self, 'cliente_id_selected'):
            if messagebox.askyesno("Confirmar Exclusão", f"Deseja realmente excluir o cliente ID {self.cliente_id_selected}?"):
                delete_cliente(self.cliente_id_selected)
                self.cliente_nome_entry.delete(0, tk.END)
                del self.cliente_id_selected
                self.refresh_clientes_list()
                self.refresh_equipamentos_list() # Atualiza equipamentos caso um cliente com equipamentos seja excluído
        else:
            messagebox.showwarning("Aviso", "Selecione um cliente para excluir.")

    def create_equipamentos_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Equipamentos")

        # Formulário de Equipamento
        form_frame = ttk.LabelFrame(tab, text="Gerenciar Equipamentos")
        form_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(form_frame, text="Nome do Equipamento:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.equipamento_nome_entry = ttk.Entry(form_frame, width=40)
        self.equipamento_nome_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="IP do Equipamento:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.equipamento_ip_entry = ttk.Entry(form_frame, width=40)
        self.equipamento_ip_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Cliente:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.cliente_combobox = ttk.Combobox(form_frame, state="readonly", width=37)
        self.cliente_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.populate_clientes_combobox()

        ttk.Label(form_frame, text="Configuração Inicial:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.equipamento_config_text = tk.Text(form_frame, width=40, height=5)
        self.equipamento_config_text.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        self.add_equipamento_btn = ttk.Button(form_frame, text="Adicionar Equipamento", command=self.add_equipamento)
        self.add_equipamento_btn.grid(row=0, column=2, padx=5, pady=5)

        self.update_equipamento_btn = ttk.Button(form_frame, text="Atualizar Equipamento", command=self.update_equipamento)
        self.update_equipamento_btn.grid(row=1, column=2, padx=5, pady=5)

        self.delete_equipamento_btn = ttk.Button(form_frame, text="Excluir Equipamento", command=self.delete_equipamento)
        self.delete_equipamento_btn.grid(row=2, column=2, padx=5, pady=5)

        # Tabela de Equipamentos
        self.equipamentos_tree = ttk.Treeview(tab, columns=("ID", "Nome", "IP", "Cliente", "Config"), show="headings")
        self.equipamentos_tree.heading("ID", text="ID")
        self.equipamentos_tree.heading("Nome", text="Nome")
        self.equipamentos_tree.heading("IP", text="IP")
        self.equipamentos_tree.heading("Cliente", text="Cliente")
        self.equipamentos_tree.heading("Config", text="Configuração Inicial")
        self.equipamentos_tree.column("ID", width=50, anchor="center")
        self.equipamentos_tree.column("Nome", width=150)
        self.equipamentos_tree.column("IP", width=100)
        self.equipamentos_tree.column("Cliente", width=100)
        self.equipamentos_tree.column("Config", width=300)
        self.equipamentos_tree.pack(pady=10, padx=10, expand=True, fill="both")
        self.equipamentos_tree.bind("<<TreeviewSelect>>", self.load_equipamento_to_form)

        self.refresh_equipamentos_list()

    def populate_clientes_combobox(self):
        clientes = read_clientes()
        self.cliente_map = {cliente[1]: cliente[0] for cliente in clientes} # {Nome: ID}
        self.cliente_combobox['values'] = list(self.cliente_map.keys())

    def refresh_equipamentos_list(self):
        for i in self.equipamentos_tree.get_children():
            self.equipamentos_tree.delete(i)
        equipamentos = read_equipamentos()
        for equipamento in equipamentos:
            # Limita a exibição da configuração para não sobrecarregar a coluna
            config_display = equipamento[4][:50] + "..." if equipamento[4] and len(equipamento[4]) > 50 else equipamento[4]
            self.equipamentos_tree.insert('', tk.END, values=(equipamento[0], equipamento[1], equipamento[2], equipamento[3], config_display))

    def add_equipamento(self):
        nome = self.equipamento_nome_entry.get()
        ip = self.equipamento_ip_entry.get()
        cliente_nome = self.cliente_combobox.get()
        config = self.equipamento_config_text.get(1.0, tk.END).strip()

        if nome and ip and cliente_nome and config:
            id_cliente = self.cliente_map.get(cliente_nome)
            if id_cliente:
                create_equipamento(nome, ip, id_cliente, config)
                self.clear_equipamento_form()
                self.refresh_equipamentos_list()
            else:
                messagebox.showwarning("Aviso", "Cliente selecionado inválido.")
        else:
            messagebox.showwarning("Aviso", "Todos os campos do equipamento são obrigatórios.")

    def load_equipamento_to_form(self, event):
        selected_item = self.equipamentos_tree.focus()
        if selected_item:
            values = self.equipamentos_tree.item(selected_item, 'values')
            # Para carregar a configuração completa, precisamos buscar do DB novamente
            # pois a treeview mostra uma versão truncada
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Configuracao_Inicial FROM Equipamentos WHERE ID_Equipamento = ?", values[0])
                full_config = cursor.fetchone()[0]
                conn.close()

                self.equipamento_id_selected = values[0]
                self.equipamento_nome_entry.delete(0, tk.END)
                self.equipamento_nome_entry.insert(0, values[1])
                self.equipamento_ip_entry.delete(0, tk.END)
                self.equipamento_ip_entry.insert(0, values[2])
                self.cliente_combobox.set(values[3]) # Define o nome do cliente na combobox
                self.equipamento_config_text.delete(1.0, tk.END)
                self.equipamento_config_text.insert(1.0, full_config)

    def update_equipamento(self):
        if hasattr(self, 'equipamento_id_selected'):
            nome = self.equipamento_nome_entry.get()
            ip = self.equipamento_ip_entry.get()
            cliente_nome = self.cliente_combobox.get()
            config = self.equipamento_config_text.get(1.0, tk.END).strip()

            if nome and ip and cliente_nome and config:
                id_cliente = self.cliente_map.get(cliente_nome)
                if id_cliente:
                    update_equipamento(self.equipamento_id_selected, nome, ip, id_cliente, config)
                    self.clear_equipamento_form()
                    del self.equipamento_id_selected
                    self.refresh_equipamentos_list()
                else:
                    messagebox.showwarning("Aviso", "Cliente selecionado inválido.")
            else:
                messagebox.showwarning("Aviso", "Todos os campos do equipamento são obrigatórios.")
        else:
            messagebox.showwarning("Aviso", "Selecione um equipamento para atualizar.")

    def delete_equipamento(self):
        if hasattr(self, 'equipamento_id_selected'):
            if messagebox.askyesno("Confirmar Exclusão", f"Deseja realmente excluir o equipamento ID {self.equipamento_id_selected}?"):
                delete_equipamento(self.equipamento_id_selected)
                self.clear_equipamento_form()
                del self.equipamento_id_selected
                self.refresh_equipamentos_list()
        else:
            messagebox.showwarning("Aviso", "Selecione um equipamento para excluir.")

    def clear_equipamento_form(self):
        self.equipamento_nome_entry.delete(0, tk.END)
        self.equipamento_ip_entry.delete(0, tk.END)
        self.cliente_combobox.set('')
        self.equipamento_config_text.delete(1.0, tk.END)

    def create_automacao_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Automação")

        # Seleção de Equipamento para Automação
        selection_frame = ttk.LabelFrame(tab, text="Selecionar Equipamento para Automação")
        selection_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(selection_frame, text="Equipamento:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.automacao_equipamento_combobox = ttk.Combobox(selection_frame, state="readonly", width=50)
        self.automacao_equipamento_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.populate_automacao_equipamentos_combobox()

        self.run_automacao_btn = ttk.Button(selection_frame, text="Executar Automação (Simulada)", command=self.run_automacao)
        self.run_automacao_btn.grid(row=0, column=2, padx=5, pady=5)

        # Área de Saída da Automação
        output_frame = ttk.LabelFrame(tab, text="Saída da Automação")
        output_frame.pack(pady=10, padx=10, expand=True, fill="both")

        global output_text # Torna a variável global para ser acessível pela função simular_automacao_ssh
        output_text = tk.Text(output_frame, wrap="word", height=20)
        output_text.pack(expand=True, fill="both")

        output_scrollbar = ttk.Scrollbar(output_frame, command=output_text.yview)
        output_scrollbar.pack(side="right", fill="y")
        output_text.config(yscrollcommand=output_scrollbar.set)

    def populate_automacao_equipamentos_combobox(self):
        equipamentos = read_equipamentos()
        self.automacao_equipamento_map = {f"{eq[1]} ({eq[2]}) - {eq[3]}": {'id': eq[0], 'ip': eq[2], 'config': eq[4]} for eq in equipamentos}
        self.automacao_equipamento_combobox['values'] = list(self.automacao_equipamento_map.keys())

    def run_automacao(self):
        selected_equipamento_str = self.automacao_equipamento_combobox.get()
        if selected_equipamento_str:
            equipamento_data = self.automacao_equipamento_map.get(selected_equipamento_str)
            if equipamento_data:
                ip = equipamento_data['ip']
                config = equipamento_data['config']
                simular_automacao_ssh(ip, config)
            else:
                messagebox.showwarning("Aviso", "Equipamento selecionado inválido.")
        else:
            messagebox.showwarning("Aviso", "Selecione um equipamento para executar a automação.")


if __name__ == "__main__":
    root = tk.Tk()
    app = AutomacaoSwitchesApp(root)
    root.mainloop()
