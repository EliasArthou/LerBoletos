from pyzbar.pyzbar import decode
from pdf2image import convert_from_path
import os
import auxiliares as aux


def barcodereader(pdf_path, pdffile, cabecalho):
    try:
        completepath = os.path.join(pdf_path, pdffile)
        pages = convert_from_path(completepath, 300, poppler_path=r'C:\Users\oi234957\PycharmProjects\Ler Boletos\poppler-23.01.0\library\bin')
        for pagina in pages:
            infocodigobarras = decode(pagina)
            if infocodigobarras:
                infocodigobarras = decode(pagina)[0]
                dados = [aux.left(pdffile, 4), infocodigobarras.data.decode('ASCII'), infocodigobarras.type, pdffile, linha_digitavel(infocodigobarras.data.decode('ASCII'))]
                return dict(zip(cabecalho, dados))

        return False

    except Exception as e:
        print(e, pdffile)
        return False


def linha_digitavel(linha):
    def modulo10(num):
        soma = 0
        peso = 2
        for c in reversed(num):
            parcial = int(c) * peso
            if parcial > 9:
                s = str(parcial)
                parcial = int(s[0]) + int(s[1])
            soma += parcial
            if peso == 2:
                peso = 1
            else:
                peso = 2

        resto10 = soma % 10
        if resto10 == 0:
            modulo10 = 0
        else:
            modulo10 = 10 - resto10

        return modulo10

    def monta_campo(campo):
        campo_dv = "%s%s" % (campo, modulo10(campo))
        return "%s.%s" % (campo_dv[0:5], campo_dv[5:])

    return ' '.join([monta_campo(linha[0:4] + linha[19:24]), monta_campo(linha[24:34]), monta_campo(linha[34:44]), linha[4], linha[5:19]])


def listarcodigobarras(visual, caminho):
    import time

    pdfs = [i for i in os.listdir(caminho) if '.pdf' in i]
    dados = []
    cabecalho = ['Cliente', 'Código de Barras', 'Tipo Código de Barras', 'Nome do Arquivo', 'Linha Digitável']

    for indice, boletos in enumerate(pdfs):
        # ===================================== Parte Gráfica =======================================================
        visual.mudartexto('labelcodigocliente', 'Arquivo: ' + boletos.replace('.pdf', ''))
        visual.mudartexto('labelquantidade', 'Item ' + str(indice + 1) + ' de ' + str(len(pdfs)) + '...')
        visual.mudartexto('labelstatus', 'Extraindo Código de Barras...')
        # Atualiza a barra de progresso das transações (Views)
        visual.configurarbarra('barraextracao', len(pdfs), indice + 1)
        time.sleep(0.1)
        # ===================================== Parte Gráfica =======================================================
        teste = barcodereader(caminho, boletos, cabecalho)
        dados.append(teste)
    if len(dados) > 0:
        retorno = dados
    else:
        retorno = None

    return retorno


def importar_boletos(visual):
    import auxiliares as aux
    import messagebox

    salvouarquivo = False
    arquivo_caminho_origem = aux.caminhoselecionado(3, 'Pasta dos Boletos')
    local_destino = aux.caminhoselecionado(3, 'Pasta do Resultado')

    if len(arquivo_caminho_origem) > 0:
        listaexcel = listarcodigobarras(visual, arquivo_caminho_origem)
        if len(listaexcel) > 0:
            visual.mudartexto('labelstatus', 'Salvando Arquivo...')
            if len(local_destino) > 0:
                nomearquivo = os.path.join(local_destino, 'Log_' + aux.acertardataatual() + '.xlsx')
            else:
                nomearquivo = 'Log_' + aux.acertardataatual() + '.xlsx'

            if len(nomearquivo) > 0:
                aux.escreverlistaexcelog(nomearquivo, listaexcel)

            if os.path.isfile(nomearquivo):
                salvouarquivo = True

            if salvouarquivo:
                messagebox.msgbox('Arquivo Salvo com Sucesso!', messagebox.MB_OK, 'Arquivo Salvo')
            else:
                messagebox.msgbox('Problema ao salvar o arquivo!', messagebox.MB_OK, 'Erro Salvamento')
        else:
            messagebox.msgbox('Nenhum Código de Barras encontrado no caminho selecionado!', messagebox.MB_OK, 'Erro Caminho')

    else:
        messagebox.msgbox('Pasta Não Selecionada!', messagebox.MB_OK, 'Erro Caminho')

    visual.configurarbarra('barraextracao', 200, 0)
    visual.mudartexto('labelquantidade', '')
    visual.mudartexto('labelstatus', '')
    visual.mudartexto('labelcodigocliente', 'Arquivo:            ')
