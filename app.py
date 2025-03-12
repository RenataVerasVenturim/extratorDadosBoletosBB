import os
import pdfquery
import openpyxl
from flask import Flask, request, render_template, send_file, redirect, url_for
import shutil
import threading
import webbrowser

app = Flask(__name__)

def empty_folder(folder_path):
    """Esvazia a pasta especificada."""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    print(f"Pasta '{folder_path}' esvaziada.")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_files = request.files.getlist('pdf_file')

        directory_path = os.path.dirname(os.path.abspath(__file__))
        pdfs_directory = os.path.join(directory_path, 'pdfs')
        drafts_directory = os.path.join(directory_path, 'RascunhosGerados')
        excel_filename = "Modelo.xlsx"
        excel_path = os.path.join(directory_path, excel_filename)
        
        # Definir as coordenadas dos elementos desejados
        coordinates = [
            {'left': 200.0, 'top': 549.52, 'width': 16.68, 'height': 10.0},    # Coordenadas do final do número de empenho
            {'left': 41.0, 'top': 418.52, 'width': 374.62, 'height': 10.0},    # Coordenadas do fornecedor (nome e CNPJ) da nota de empenho
            {'left': 421.0, 'top': 642.52, 'width': 50.02, 'height': 10.0},    # Coordenadas do valor da nota de empenho
            {'left': 200.0, 'top': 464.52, 'width': 139.57, 'height': 10.0},   #Coordenadas do número do processo
            {'left': 200.0, 'top': 503.52, 'width': 56.7, 'height': 10.0},     # Coordenadas da fonte de despesa
            {'left': 43.0, 'top': 627.52, 'width': 387.29, 'height': 10.0},    # Coordenadas da natureza da despesa
            {'left': 125.0, 'top': 306.52, 'width': 122.66, 'height': 10.0} ,   # Modalidade da licitação
            {'left': 122.0, 'top': 503.52, 'width': 33.36, 'height': 10.0} ,   # Coordenadas do PTRES        
            {'left': 296.0, 'top': 503.52, 'width': 33.36, 'height': 10.0} ,   # Coordenadas do nº da natureza da despesa
            {'left': 485.0, 'top': 503.52, 'width': 73.88, 'height': 10.0} ,   # Coordenadas do plano interno
            {'left': 407.0, 'top': 503.52,'width': 33.36, 'height': 10.0} ,   # UGR
 
        ]

        shutil.copy(excel_path, os.path.join(pdfs_directory, "Temp_Consolidado.xlsx"))
        print('Cópia da pasta modelo do excel criada')

        copied_workbook = openpyxl.load_workbook(os.path.join(pdfs_directory, "Temp_Consolidado.xlsx"))
        copied_sheet = copied_workbook.active
        print('Excel aberto para inserção dos dados')

        start_row = 2
        empenho_number = None

        for i, pdf_file in enumerate(uploaded_files):
            pdf_path = os.path.join(pdfs_directory, pdf_file.filename)
            pdf_file.save(pdf_path)
            
            pdf = pdfquery.PDFQuery(pdf_path)
            pdf.load()

            for j, coord in enumerate(coordinates):
                target_left = coord['left']
                target_top = coord['top']
                target_width = coord['width']
                target_height = coord['height']
                
                element = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (target_left, target_top, target_left + target_width, target_top + target_height))
                text = element.text().strip()
                copied_sheet.cell(row=start_row + i, column=j+1).value = text
                
                if j == 0:  # Supondo que o número de empenho está na primeira coordenada
                    empenho_number = text

        if empenho_number:
            new_filename = f"Rascunho inicial-{empenho_number}.xlsx"
        else:
            new_filename = "Consolidado.xlsx"

        final_path = os.path.join(drafts_directory, new_filename)
        copied_workbook.save(final_path)
        copied_workbook.close()
        print(f"Dados inseridos na planilha: {new_filename}")

        return redirect(url_for('download_excel', filename=new_filename))

    return render_template('index.html')

@app.route('/download_excel/<filename>', methods=['GET'])
def download_excel(filename):
    drafts_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'RascunhosGerados')
    copied_path = os.path.join(drafts_directory, filename)
    return send_file(copied_path, as_attachment=True)

if __name__ == '__main__':
    directory_path = os.path.dirname(os.path.abspath(__file__))
    pdfs_directory = os.path.join(directory_path, 'pdfs')
    drafts_directory = os.path.join(directory_path, 'RascunhosGerados')

    # Esvaziar a pasta pdfs e a pasta RascunhosGerados antes de iniciar o servidor
    empty_folder(pdfs_directory)
    empty_folder(drafts_directory)
    
    webbrowser.open('http://localhost:5000') 
    print('Servidor iniciado na porta http://localhost:5000 !') 
    print('App desenvolvido por: RENATA VERAS VENTURIM') 

    flask_thread = threading.Thread(target=app.run)
    flask_thread.start()
    flask_thread.join()

    #------------------------notas fiscais------------------------

import os
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import cv2
import pytesseract
import re
import time
import shutil
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import fitz  # PyMuPDF
from PIL import Image
import pandas as pd
from io import BytesIO


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'Notas'  # Pasta onde as imagens de notas fiscais serão armazenadas
app.config['UPLOAD_FOLDER_PDF'] = 'Notas_pdf'  # Pasta onde os PDFs temporários serão armazenados

# Configurar o caminho do Tesseract OCR
caminho_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe" #No pc do trabalho: r"D:\\Tesseract-OCR\\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = caminho_tesseract

# Registrar o tempo inicial
inicio = time.time()

# Função para limpar o diretório 'Notas'
def limpar_diretorio_notas():
    start_time = time.time()
    diretorio_notas = app.config['UPLOAD_FOLDER']
    if os.path.exists(diretorio_notas):
        shutil.rmtree(diretorio_notas)
    os.makedirs(diretorio_notas)
    end_time = time.time()
    print(f"Tempo para limpar o diretório 'Notas': {end_time - start_time:.2f} segundos")

# Função para limpar o diretório 'Notas_pdf'
def limpar_diretorio_notas_pdf():
    start_time = time.time()
    diretorio_notas_pdf = app.config['UPLOAD_FOLDER_PDF']
    if os.path.exists(diretorio_notas_pdf):
        shutil.rmtree(diretorio_notas_pdf)
    os.makedirs(diretorio_notas_pdf)
    end_time = time.time()
    print(f"Tempo para limpar o diretório 'Notas_pdf': {end_time - start_time:.2f} segundos")

# Função para converter PDF em imagem PNG usando PyMuPDF
def converter_pdf_para_png(pdf_file):
    
    try:
        document = fitz.open(pdf_file)
        imagens = []

        dpi = 300
        largura_total = 0
        altura_total = 0

        # Calcular as dimensões totais
        for page_number in range(len(document)):
            page = document.load_page(page_number)
            pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
            imagens.append(pix)
            largura_total = max(largura_total, pix.width)
            altura_total += pix.height

        # Criar uma imagem grande para combinar todas as páginas
        img_combined = Image.new("RGB", (largura_total, altura_total))
        y_offset = 0

        # Adicionar cada imagem de página à imagem combinada
        for pix in imagens:
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img_combined.paste(img, (0, y_offset))
            y_offset += pix.height
        
        nome_base_arquivo = os.path.splitext(os.path.basename(pdf_file))[0]
        nome_arquivo_png = os.path.join(app.config['UPLOAD_FOLDER'], f"{secure_filename(nome_base_arquivo)}_combined.png")
        img_combined.save(nome_arquivo_png)

        document.close()
        return [nome_arquivo_png]

    except PermissionError as e:
        print(f"Erro de permissão ao acessar o arquivo '{pdf_file}': {e}")
        return []

    except Exception as e:
        print(f"Erro ao converter o arquivo '{pdf_file}': {e}")
        return []
# Função para executar OCR e buscar os padrões no texto extraído
def extrair_dados_da_nf(image):
    start_time = time.time()
    # Executar OCR na imagem
    texto = pytesseract.image_to_string(image)

    # Definir os padrões regex
    padrao_numero_nf = r'N[°º]\s?[.]?\s?\d{1,10}(?:\.\d{3})*|[0-9]{3}\.[0-9]{3}\.[0-9]{3}'
    padrao_data_emissao = r'(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[0-2])\/[0-9]{4}'
    padrao_cnpj_empresa = r'[0-9]{2}\.[0-9]{3}\.[0-9]{3}\/[0-9]{4}-[0-9]{2}'
    padrao_empenho = r'\b(?:[2][0][0-9]{2}\s*[NEne]{2}\s*[0-9]{1,6}|[0-9]{3}\/[2][0][0-9]{2}|\d{4}[NEne]\d{2})\b'
    padrao_processo = r'[2][3][0][6][9][., ][0-9]{6}\/[0-9]{4}[-, ][0-9]{2}'

    # Buscar os padrões no texto extraído
    match_numero = re.search(padrao_numero_nf, texto)
    match_data = re.search(padrao_data_emissao, texto)
    match_cnpj = re.search(padrao_cnpj_empresa, texto)
    match_empenho = re.search(padrao_empenho, texto)
    match_processo = re.search(padrao_processo, texto)

    # Retornar os resultados encontrados
    numero = match_numero.group(0) if match_numero else None
    data = match_data.group(0) if match_data else None
    cnpj = match_cnpj.group(0) if match_cnpj else None
    empenho = match_empenho.group(0) if match_empenho else None
    processo = match_processo.group(0) if match_processo else None

    end_time = time.time()
    print(f"Tempo para extrair dados da nota fiscal: {end_time - start_time:.2f} segundos")

    return numero, data, cnpj, empenho, processo

# Função para ajustar o brilho e extrair os dados
def ajustar_brilho_e_extrair_dados(image, brightness):
    start_time = time.time()
    # Ajustar o brilho
    adjusted_image = cv2.add(image, brightness)

    # Extrair dados da imagem ajustada
    resultado = extrair_dados_da_nf(adjusted_image)
    end_time = time.time()
    print(f"Tempo para ajustar brilho e extrair dados: {end_time - start_time:.2f} segundos")
    
    return resultado

# Função para processar uma imagem
@lru_cache(maxsize=32)  # Cache com capacidade para 32 resultados
def processar_imagem(nome_arquivo):
    start_time = time.time()
    
    # Carregar a imagem usando OpenCV
    caminho_imagem = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
    image = cv2.imread(caminho_imagem)

    # Verificar se a imagem foi carregada corretamente
    if image is None:
        print(f"Erro ao carregar a imagem em '{caminho_imagem}'.")
        return None

    # Ajustar o contraste (aumentar o valor para aumentar o contraste)
    contrast = 1.5
    adjusted_image = cv2.convertScaleAbs(image, alpha=contrast, beta=0)

    # Tentar ajustar o brilho em níveis otimizados
    ajustes_de_brilho = [0, 50, 80]  # Exemplo de ajustes de brilho
    numero, data, cnpj, empenho, processo = None, None, None, None, None
    
    for brilho in ajustes_de_brilho:
        resultado = ajustar_brilho_e_extrair_dados(adjusted_image, brilho)
        if resultado[0]:  # Se o número foi encontrado
            numero = resultado[0]
        if resultado[1]:  # Se a data foi encontrada
            data = resultado[1]
        if resultado[2]:  # Se o CNPJ foi encontrado
            cnpj = resultado[2]
        if resultado[3]:  # Se o empenho foi encontrado
            empenho = resultado[3]
        if resultado[4]:  # Se o processo foi encontrado
            processo = resultado[4]
        
        # Se todos os dados foram encontrados, parar a iteração
        if all([numero, data, cnpj]):
            break

    # Retornar os resultados incluindo o nome do arquivo
    end_time = time.time()
    print(f"Tempo para processar a imagem '{nome_arquivo}': {end_time - start_time:.2f} segundos")
    
    return {
        'nome_arquivo': nome_arquivo,
        'numero_nf': numero,
        'data_emissao': data,
        'cnpj_empresa': cnpj,
        'empenho': empenho,
        'processo': processo
    }

# Função para processar todas as imagens na pasta 'Notas' usando ThreadPoolExecutor
def processar_imagens_notas():
    start_time = time.time()
    resultados = []

    # Diretório onde estão as imagens de notas fiscais
    diretorio_notas = app.config['UPLOAD_FOLDER']

    # Diretório onde estão os PDFs temporários
    diretorio_notas_pdf = app.config['UPLOAD_FOLDER_PDF']

    # Verificar se o diretório de PDFs existe
    if not os.path.exists(diretorio_notas_pdf):
        print(f"O diretório '{diretorio_notas_pdf}' não existe.")
        return []

    # Lista de arquivos PDF no diretório
    arquivos_pdf = [f for f in os.listdir(diretorio_notas_pdf) if f.endswith('.pdf')]

    # Converter PDFs para imagens usando ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=4) as executor:
        resultados_futuros = list(executor.map(lambda f: converter_pdf_para_png(os.path.join(diretorio_notas_pdf, f)), arquivos_pdf))

    # Lista de imagens convertidas
    imagens = [item for sublist in resultados_futuros for item in sublist]

    # Verificar se o diretório de notas existe
    if not os.path.exists(diretorio_notas):
        print(f"O diretório '{diretorio_notas}' não existe.")
        return []

    # Lista de arquivos de imagem no diretório
    arquivos_imagem = [f for f in os.listdir(diretorio_notas) if f.endswith('.png')]

    # Processar cada imagem e coletar resultados
    with ThreadPoolExecutor(max_workers=4) as executor:
        resultados_futuros = list(executor.map(processar_imagem, arquivos_imagem))

    resultados = [resultado for resultado in resultados_futuros if resultado is not None]

    end_time = time.time()
    print(f"Tempo total para processar imagens: {end_time - start_time:.2f} segundos")

    end_time = time.time()
    tempo_total = end_time - start_time
    print(f"Tempo total para processar imagens: {tempo_total:.2f} segundos")

    return resultados, tempo_total

# Rota inicial
@app.route('/')
def index():
    return render_template('index2.html')

# Rota para processar PDFs e extrair dados
@app.route('/processar', methods=['POST'])
def processar():
    # Verificar se o diretório 'Notas' existe
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Verificar se o diretório 'Notas_pdf' existe
    if not os.path.exists(app.config['UPLOAD_FOLDER_PDF']):
        os.makedirs(app.config['UPLOAD_FOLDER_PDF'])

    # Limpar diretórios de PDFs e imagens
    limpar_diretorio_notas()
    limpar_diretorio_notas_pdf()

    # Verificar se há arquivos enviados
    if 'file' not in request.files:
        return "Nenhum arquivo foi enviado.", 400

    files = request.files.getlist('file')

    for file in files:
        if file.filename == '':
            return 'Nenhum arquivo selecionado', 400
        if file:
            # Salvar o arquivo PDF temporariamente
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER_PDF'], filename)
            file.save(file_path)

    # Processar as imagens das notas e extrair os dados
    resultados, tempo_total = processar_imagens_notas()

    # Criar um DataFrame com os resultados
    df = pd.DataFrame(resultados)

    # Criar um arquivo Excel em memória
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Dados nf-es')
        writer.close()
    output.seek(0)


    # Enviar o arquivo Excel para download
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='resultados.xlsx')


if __name__ == '__main__':
    app.run(debug=True)

