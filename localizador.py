#seletor para indicar localização dos elementos a serem extraidos do PDF

import pdfquery

pdf = pdfquery.PDFQuery(r'C:\Users\RENATA-PROPPI\Downloads\0062___gru_3017___complem._29409192339800062.pdf')
pdf.load()

# Exemplo de seletor para localizar um elemento com base em seu texto
elementos = pdf.pq('LTTextLineHorizontal:contains("Serviço: 800 - Complementação de retribuição")')

# Loop para iterar sobre os elementos encontrados
for elemento in elementos:
    # Acessar propriedades do elemento
    left = float(elemento.attrib['x0'])
    top = float(elemento.attrib['y0'])
    width = float(elemento.attrib['width'])
    height = float(elemento.attrib['height'])
    texto = elemento.text

    # Imprimir informações do elemento
    print(f'Posição: left={left}, top={top}')
    print(f'Tamanho: width={width}, height={height}')
    print(f'Texto: {texto}')