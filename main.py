from tkinter import Tk, Canvas, PhotoImage, Label, Entry, Button, ttk, StringVar, Frame, messagebox, Menu
from ttkthemes import ThemedStyle
import random
import string
import sqlite3
import os
from cryptography.fernet import Fernet

class Pass(Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager")
        self.config(padx=50, pady=50)
        
        self.style = ThemedStyle(self)
        self.style.set_theme('equilux')
        self.configure(background="#333333")
        
        #Color
        self.bg_color = "#333333"
        self.text_color = "white"
        
        #Configura criptografia
        self.setup_encryption_key()
        
        #Configurar banco de dados
        self.conn = sqlite3.connect("password.db")
        self.cursor = self.conn.cursor()
        self.setup_database()
        
        #Inicializa password_data
        self.password_data = []
            
        #Criar notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        
        #Tab Generate
        self.tab_generate = Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(self.tab_generate, text="Generate")
        
        #Tab Password
        self.tab_password = Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(self.tab_password, text="Password")
        
        # Configurar a abas
        self.setup_generate_tab()
        self.setup_password_tab()
        
        #Criar menu de contexto
        self.create_context_menu()
        
        # Estilizar elementos ttk
        self.setup_styles()
        
        # Carregar dados do banco de dados / Carregar dados na tabela 
        self.load_passwords_from_db()
        self.load_password_data()
        
        
    def setup_encryption_key(self):
        """Configura ou carrega a chave de criptografia."""
        key_file = "encryption.key"
        if os.path.exists(key_file):
            # Carregar chave existente
            with open(key_file, "rb") as file:
                self.key = file.read()
        else:
            # Gerar nova chave
            self.key = Fernet.generate_key()
            # Salvar chave em arquivo
            with open(key_file, "wb") as file:
                file.write(self.key)
        
        # Inicializar o cipher com a chave
        self.cipher = Fernet(self.key)
        
        
    def load_passwords_from_db(self):
        """Carrega as senhas do banco de dados para o atributo password_data"""
        self.password_data = []
        self.cursor.execute("SELECT id, website, email, password FROM passwords")
        rows = self.cursor.fetchall()
        
        for row in rows:
            try:
                decrypted_password = self.decrypt_password(row[3])
                self.password_data.append({
                    "id": row[0],
                    "website": row[1],
                    "email": row[2],
                    "password": decrypted_password,
                    "hidden": True
                })
            except Exception as e:
                print(f"Erro ao descriptografar senha: {e}")
        
    def setup_database(self):
        """Configura o banco de dados."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT,
            email TEXT,
            password TEXT
        )''')
        self.conn.commit()
        
              
    def setup_styles(self):
        """Configura todos os estilos dos elementos ttk"""
        self.style.configure("TButton", background="#333333", foreground="white", font=("Helvetica", 10))
        self.style.configure("TLabel", background="#333333", foreground="white", font=("Helvetica", 10))
        self.style.configure("TEntry", fieldbackground="#555555", background="#333333", foreground="white", font=("Helvetica", 10))
        self.style.configure("TNotebook", background="#333333", tabmargins=[2, 5, 2, 0])
        self.style.configure("TNotebook.Tab", background="#555555", foreground="white", padding=[10, 2])
        self.style.map("TNotebook.Tab", background=[("selected", "#666666")])
        self.style.configure("Treeview", fieldbackground="#444444", background="#444444", foreground="white", font=("Helvetica", 9))
        self.style.map("Treeview", background=[("selected", "#666666")])
        
        
    def setup_generate_tab(self):
            #Canva
            self.canvas = Canvas(self.tab_generate, width =200, height=200, background="#333333", highlightthickness=0)
            self.canvas.grid(row=0, column=1)
            self.image = PhotoImage(file="coden.png")
            self.canvas.create_image(100, 100, image=self.image)
            
            
            #Label
            self.label_website = Label(self.tab_generate, text="Website:", bg=self.bg_color, fg=self.text_color)
            self.label_website.grid(row=1, column=0, sticky="w")
            
            self.label_email = Label(self.tab_generate, text="Email/Username:", bg=self.bg_color, fg=self.text_color)
            self.label_email.grid(row=2, column=0, sticky="w", padx=(0, 15))
            
            self.label_password = Label(self.tab_generate, text="Password:", bg=self.bg_color, fg=self.text_color)
            self.label_password.grid(row=3, column=0, sticky="w")
            
            
            #Inputs
            self.entry_website = Entry(self.tab_generate, width=35)
            self.entry_website.grid(row=1, column=1, columnspan=2, sticky="w")
            self.entry_website.focus()
            
            self.entry_email = Entry(self.tab_generate, width=35)
            self.entry_email.grid(row=2, column=1, columnspan=2, sticky="w")
            
            
            self.entry_password = Entry(self.tab_generate, width=30)
            self.entry_password.grid(row=3, column=1, sticky="w", padx=(0, 15))
            
            
            #Button
            self.button_generate = ttk.Button(self.tab_generate, text="Generate", width=16, command=self.generate_password)
            self.button_generate.grid(row=3, column=2)
            
            self.button_add = ttk.Button(self.tab_generate, text="Add", width=36, command=self.add_password)
            self.button_add.grid(row=4, column=1, columnspan=2, sticky="w")
        
        
    def create_context_menu(self):
        """Criar o menu de contexto para copiar ou excluir senha"""
        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.add_command(label="Copiar Senha", command=self.copy_password)
        self.context_menu.add_command(label="Excluir", command=self.delete_selected_password)
        
        
    def show_context_menu(self, event):
        """Exibe o menu de contexto ao clicar com o botao direito"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
            
            
    def copy_password(self):
        """Copia a senha para a area de transferencia"""
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item, "values")
            website, email = values[0], values[1]
            for data in self.password_data:
                if data["website"] == website and data["email"] == email:
                    self.clipboard_clear()
                    self.clipboard_append(data["password"])
                    self.update()
                    messagebox.showinfo("Copiado", "Senha copiada para a area de transferencia!")
                    break
                
                
    def delete_selected_password(self):
        """Exclui o registro selecionado do banco de dados e da interface"""
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        values = self.tree.item(selected_item, "values")
        website, email = values[0], values[1]
        
        confirm = messagebox.askyesno("Excluir", f"Tem certeza que deseja excluir os dados de {website}?")
        if confirm:
            self.cursor.execute("DELETE FROM passwords WHERE website = ? AND email = ?", (website, email))
            self.conn.commit()
            
            self.load_passwords_from_db()
            self.load_password_data()
        
        
    def setup_password_tab(self):
        """Configura a interface da aba Passwords"""
        #Treeview(table)
        columns = ('website', 'email', 'password')
        self.tree = ttk.Treeview(self.tab_password, columns=columns, show='headings', height=15)
        
        #Set headers
        self.tree.heading('website', text='Website')
        self.tree.heading('email', text='Email/Username')
        self.tree.heading('password', text='Password')
        
        #Set colums
        self.tree.column('website', width=150)
        self.tree.column('email', width=200)
        self.tree.column('password', width=150)
        
        #Vincular evento de clique na tabela
        self.tree.bind('<ButtonRelease-1>', self.handle_click)
        self.tree.bind('<Button-3>', self.show_context_menu)
        
        #add scrollbar
        scrollbar = ttk.Scrollbar(self.tab_password, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        #Posicionar elementos
        self.tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
    
    
    def handle_click(self, event):
        """Gerencia cliques na tabela"""
        #Obter o item selecionado
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return
        
        column = self.tree.identify_column(event.x)
        if column != "#3":
            return
        
        item = self.tree.selection()
        if not item:
            return
        
        #Obter valores
        values = self.tree.item(item, "values")
        if not values:
            return
        
        # Encontrar o item correspondente em password_data
        website, email = values[0], values[1]
        for data in self.password_data:
            if data["website"] == website and data ["email"] == email:
                data["hidden"] = not data["hidden"]
                break
        
        #Recarregar a tabela para mostrar/ocultar senha
        self.load_password_data()
        
        
    def generate_password(self):
        """Gera uma senha aleatória e a insere no campo de senha"""
        length = 16
        chars = string.ascii_letters + string.digits + "!@#$%^&*()"
        password = ''.join(random.choice(chars) for _ in range(length))
        
        #Limpar campo atual e inserir nova senha
        self.entry_password.delete(0, 'end')
        self.entry_password.insert(0, password)
        
        
    def encrypt_password(self, password):
        """Criptografa uma senha"""
        return self.cipher.encrypt(password.encode()).decode()
    
    
    def decrypt_password(self, encrypted_password):
        """Descriptografa uma senha"""
        return self.cipher.decrypt(encrypted_password.encode()).decode()
    
        
    def add_password(self):
        """Adiciona uma nova senha a lista de senhas"""
        #obter dados dos campos
        website = self.entry_website.get().strip()
        email = self.entry_email.get().strip()
        password = self.entry_password.get()
        
        if not website or not email or not password:
            messagebox.showwarning("Dados incompletos", "Preencha todos os campos.")
            return
        
        #Verificar se ja existe
        self.cursor.execute(
            "SELECT id FROM passwords WHERE website = ? AND email = ?",
            (website, email)
        )
        if self.cursor.fetchone():
            messagebox.showinfo(
                "Registro existente",
                f"Ja existe um registro para {website} com este email."
            )
            return
        
        #criptografar e salvar
        encrypted_password = self.encrypt_password(password)
        self.cursor.execute(
            "INSERT INTO passwords (website, email, password) VALUES (?, ?, ?)",
            (website, email, encrypted_password)
        )
        self.conn.commit()
        messagebox.showinfo("Sucesso", "Senha adicionada com sucesso!")
        
        #Atualiza lista de senhas
        self.load_passwords_from_db()
        
        #atualizar tabela
        self.load_password_data()
        
        #Limpas campos
        self.entry_website.delete(0, 'end')
        self.entry_password.delete(0, 'end')
        self.entry_website.focus()
        
        
    def load_password_data(self):
        """Carrega os dados de senha na tabela"""
        #Limpar tabela atual
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        #Verificar se ha dados para carregar
        if not self.password_data:
            return
        
        #Recarregar dados
        for data in self.password_data:
            password_display = data["password"]
            if data["hidden"]:
                password_display = "•" * len(data["password"])
                
            self.tree.insert('', 'end', values=(data["website"], data["email"], password_display))

if __name__ == "__main__":
    app = Pass()
    app.mainloop()