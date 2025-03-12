# Gerador de Rascunhos para liquidação no âmbito da UFF
Extrai dados de pdfs de notas de empenho para rascunhos de liquidação 

<b>Necessário ter instalado:</b>
<ol>1. VS CODE (IDE)</ol>
<ol>2. Python</ol>
<ol>3. Git</ol>

<b>Clonar projeto</b>

    git clone  https://github.com/RenataVerasVenturim/GeradorDeRascunhos.git

<b>Acessar pasta do projeto (verifique o seu)</b>

    cd C:\Users\PROPPI_01\Desktop\Geradorderascunho
    
<b>Comando no terminal - baixar bibliotecas</b>
    
    pip install -r requirements.txt

<b>Executar projeto</b>
    
    python app.py

<b> Gerar um app executável para windows</b>

pyinstaller --onefile --icon=static/IconeApp.ico --add-data "static/style.css;static" --add-data "static/script.js;static" --add-data "static/imgp.jpg;static" --add-data "static/imgg.jpg;static" --add-data "static/logo.png;static" --add-data "static/faviconuff.ico;static" --add-data "static/icon.jpg;static" --add-data "templates/index.html;templates" --add-data "pdfs/2024NE000371.pdf;pdfs" --add-data "Modelo.xlsx;." --add-data "Consolidado.xlsx;." --add-data "README.md;." --add-data "requirements.txt;." --add-data "LICENSE;." --add-data "RascunhosGerados/Rascunho inicial-2024NE00089.xlsx;RascunhosGerados" app.py





