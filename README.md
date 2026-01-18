# browser
 pip install PyQt5 PyQtWebEngine

# Instalar o módulo de ambientes virtuais, se necessário
python -m pip install --upgrade pip

# Criar um ambiente virtual chamado "venv"
python -m venv venv

# Ativar o ambiente virtual
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate

---
**script COMPLETO**

- ✔ Menu
- ✔ Botões
- ✔ Abrir ficheiro
- ✔ Abrir URL
- ✔ Guardar link (favoritos)
- ✔ Guardar onde (pasta configurável)
- ✔ Histórico
- ✔ Sair
- ✔ Explicações embutidas no código

Compatível com **Windows / Linux / macOS** (PyQt5).

---

## ✅ O que este script já faz

* Navegador com abas
* Menu completo
* Botões
* Favoritos
* Histórico
* Escolha de pasta
* Abrir ficheiros HTML locais
* Abrir URLs
* Código limpo e extensível

---

Próximo passo:

* 🔹 Converter favoritos/histórico para **XML**
* 🔹 Adicionar **atalhos de teclado**
* 🔹 Criar versão **Qt6**
* 🔹 Tema escuro
* 🔹 Empacotar em **EXE**



---

**SCRIPT COMPLETO convertido para XML**, onde:

- ✔ Favoritos → `favorites.xml`
- ✔ Histórico → `history.xml`
- ✔ Criação automática dos ficheiros XML
- ✔ Leitura / escrita estruturada
- ✔ Mantém menus, botões e abas
- ✔ Código comentado (PT-PT)

---


## 📂 Estrutura dos ficheiros XML

### `favorites.xml`

```xml
<favorites>
    <url>https://www.python.org</url>
    <url>https://qt.io</url>
</favorites>
```

### `history.xml`

```xml
<history>
    <url>https://google.com</url>
    <url>https://openai.com</url>
</history>
```

---

## ✅ Benefícios do XML

✔ Estruturado
✔ Fácil de expandir (data, título, ícone)
✔ Compatível com HTML, Qt, web, Arduino, etc.
✔ Ideal para logs e favoritos

---

## Próximos upgrades possíveis

* 📅 Data/hora no XML
* ⭐ Nome personalizado do favorito
* 🔍 Pesquisa nos favoritos
* 📤 Exportar/importar XML
* 🌓 Tema escuro
* 🔑 Autenticação

Se quiseres, digo já o **próximo passo recomendado** 😉
