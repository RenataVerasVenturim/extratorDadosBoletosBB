# Gerador de Rascunhos para liquidação no âmbito da UFF
Extrai dados de pdfs de notas de empenho para rascunhos de liquidação 

<b>Necessário ter instalado:</b>
<ol>1. VS CODE (IDE)</ol>
<ol>2. Python</ol>
<ol>3. Git</ol>

<b>Clonar projeto</b>

    git clone  https://github.com/RenataVerasVenturim/extratorDadosBoletosBB.git

<b>Acessar pasta do projeto (verifique o seu)</b>

    cd C:\Users\PROPPI_01\Desktop\Geradorderascunho
    
<b>Comando no terminal - baixar bibliotecas</b>
    
    pip install -r requirements.txt

<b>Executar projeto</b>
    
    python app.py

<b> Gerar um app executável para windows</b>
pyinstaller --onefile --icon=static/IconeApp.ico --add-data "static/style.css;static" --add-data "static/script.js;static" --add-data "static/imgp.jpg;static" --add-data "static/imgg.jpg;static" --add-data "static/logo.png;static" --add-data "static/faviconuff.ico;static" --add-data "static/icon.jpg;static" --add-data "templates/index.html;templates" --add-data "pdfs/Seu boleto 1.pdf;pdfs" --add-data "pdfs/Seu boleto 2.pdf;pdfs" --add-data "pdfs/Sua nota de empenho.pdf;pdfs" --add-data "pdfs/Temp_Consolidado.xlsx;pdfs" --add-data "Modelo.xlsx;." --add-data "ModeloParaAjustesNosCampos.xltm;." --add-data "README.md;." --add-data "requirements.txt;." --add-data "LICENSE;." --add-data "RascunhosGerados/Rascunho-32.xlsx;RascunhosGerados" app.py
