# Gerenciador de Senhas

Este projeto consiste em um Gerenciador de Senhas desenvolvido em Python utilizando a biblioteca Tkinter para a interface gráfica e SQLite para armazenamento seguro das senhas.

![Demo](assets/images/demo.gif)

## Tecnologias Utilizadas
- Python 3
- Tkinter (Interface Gráfica)
- SQLite (Banco de Dados)
- Cryptography (Fernet para criptografia de senhas)

## Funcionalidades
- **Adicionar uma nova senha**: Salva credenciais de login de maneira segura.
- **Visualizar senhas salvas**: Exibe as senhas armazenadas.
- **Remover senhas**: Permite deletar senhas salvas.
- **Autenticação**: Protege o acesso ao gerenciador de senhas com uma senha mestra.

## Instalação e Execução
1. Clone este repositório:
   ```sh
   git clone https://github.com/seuusuario/gerenciador-de-senhas.git
   cd gerenciador-de-senhas
   ```
2. Instale as dependências:
   ```sh
   pip install cryptography
   ```
3. Execute o programa:
   ```sh
   python main.py
   ```

## Estrutura do Projeto
```
/
|-- main.py          # Arquivo principal que inicia a interface Tkinter
|-- database.db      # Banco de dados SQLite onde as senhas são armazenadas
|-- encrypt.py       # Arquivo responsável pela criptografia e decriptação das senhas
|-- README.md        # Documento explicativo do projeto
```

## Melhorias Futuras
- Adicionar opção de exportação/importação de senhas.
- Melhorar a interface gráfica com um design mais moderno.

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir um Pull Request ou relatar problemas na aba de Issues.

## Licença
Este projeto está sob a licença MIT. Sinta-se livre para usá-lo e modificá-lo conforme necessário.

---
## 📧 Contato

Para dúvidas ou sugestões, entre em contato:
 - Email: (shadowindev@gmail.com)
 - GitHub: (https://github.com/codennomad)

---

Feito com 💖 por Gabriel.

