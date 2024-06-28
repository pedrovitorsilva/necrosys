from typing import Tuple
import face_recognition as fr
import random
import json

# Inicializando variáveis

falecidos_identificados = "falecidos_identificados.json"

# Funções Auxilliares --------------------------------------------------------


def preparar():
    '''
    Inicializa as variáveis necessárias.

    Retorna: Tuple[bool, Dict]: 

    Preparação bem ou mal sucedida;
    Falecidos registrados.
    '''

    try:
        with open(falecidos_identificados, "r") as arquivo:
            falecidos_registrados = json.load(arquivo)
        return True, falecidos_registrados

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return False, None


def scanner_foto() -> str:
    ''' Escolhe uma foto aleatória e a retorna. Simula um scanner.'''

    POSSIVEIS_FALECIDOS = [
        "rostos/personagens1.jpeg",
        "rostos/personagens2.jpeg",
        "rostos/personagens3.jpeg",
        "rostos/personagens4.jpeg"
    ]

    foto = random.choice(POSSIVEIS_FALECIDOS)
    return foto


def esta_na_foto(caracteristicas, fotos_ja_registradas: list[str]):
    '''
    Recebe as caracteristicas de pessoas em uma foto. 

    Compara com a lista de fotos de uma pessoa específica e retorna se a pessoa está na foto.
    '''

    total_de_reconhecimentos = 0

    # O reconhecimento das fotos deve ser >= 70%
    MINIMO_APROVACAO = 0.7

    for foto in fotos_ja_registradas:
        foto = fr.load_image_file(foto)
        caracteristicas_foto_atual = fr.face_encodings(foto)[0]
        reconhecimentos = fr.compare_faces(
            caracteristicas, caracteristicas_foto_atual)

        if True in reconhecimentos:
            total_de_reconhecimentos += 1

    if total_de_reconhecimentos/len(fotos_ja_registradas) >= MINIMO_APROVACAO:
        return True
    else:
        return False


# type: ignore
def reconhecer_falecidos(foto_escaneada: str, falecidos_registrados: dict) -> Tuple[bool, list]:
    '''
    Reconhece se na foto escaneada há algum falecido já registrado no sistema.

    Retorna se houve reconhecimento, e uma lista com os reconhecidos.
    '''

    reconhecidos = []

    foto = fr.load_image_file(foto_escaneada)
    caracteristicas = fr.face_encodings(foto)

    # Para cada pessoa falecida registrada
    # Se as caracteristicas de alguém visto na foto atual condizerem com as fotos de alguém que faleceu
    # Considera-se reconhecido
    for pessoa in falecidos_registrados['pessoas']:
        lista_fotos_registradas = pessoa['fotos']

        if esta_na_foto(caracteristicas, lista_fotos_registradas):
            reconhecidos.append(pessoa)

    return len(reconhecidos) > 0, reconhecidos

# Funções principais ---------------------------------------------------------


def registrar_reconhecido(novos_reconhecidos: list[str], pessoas_reconhecidas: list[str], causas_da_morte: dict):
    ''' 
    Adiciona os novos reconhecidos às pessoas reconhecidas naquele turno.     

    Contabiliza também a causa da morte.
    '''

    for novo_reconhecido in novos_reconhecidos:
        # Registrar pessoa
        if novo_reconhecido['codigo'] not in [pessoa['codigo'] for pessoa in pessoas_reconhecidas['pessoas']]:
            pessoas_reconhecidas.append(novo_reconhecido)

        # Registrar causa da morte
        causa = novo_reconhecido['causa_morte']
        if causa in causas_da_morte:
            causas_da_morte[causa] += 1
        else:
            causas_da_morte[causa] = 1


def verificar_rostos(falecidos_registrados: dict, pessoas_reconhecidas: list[str], causas_da_morte: dict):
    '''
    Verifica os novos rostos apresentados.

    Reconhece falecidos e registra as pessoas que foram reconhecidas.
    '''

    rostos = scanner_foto()
    ocorreu_reconhecimento, novos_reconhecidos = reconhecer_falecidos(
        rostos, falecidos_registrados)

    if ocorreu_reconhecimento:
        registrar_reconhecido(novos_reconhecidos,
                              pessoas_reconhecidas, causas_da_morte)

    return ocorreu_reconhecimento, novos_reconhecidos


def relatorio_causas_morte(causas_morte: dict):
    '''
    Gera um relatório com as causas de óbito, baseado na quantidade das pessoas pesquisadas no turno.
    '''
    relatorio_ordenado = dict(
        sorted(causas_morte.items(), key=lambda item: item[1], reverse=True))

    return relatorio_ordenado


def atendimento_legista(legista_ocupado: bool, PROBABILIDADE_DISPONIBILIDADE_LEGISTA: int):
    '''
        Verifica e retorna se o legista pode atender.
        Atualiza o estado do legista
    '''

    if random.randint(1, 100) <= PROBABILIDADE_DISPONIBILIDADE_LEGISTA and not legista_ocupado:
        houve_atendimento = True
    else:
        houve_atendimento = False

    return houve_atendimento


def receber_orgaos(orgaos: int, PROBABILIDADE_RECEBIMENTO_ORGAOS):
    '''
    Simula o recebimento dos órgãos.

    Retorna se houve o recebimento, e os orgaos
    '''

    if random.randint(1, 100) <= PROBABILIDADE_RECEBIMENTO_ORGAOS:
        novos_orgaos = random.randint(1, 5)
        orgaos += novos_orgaos
        return True, orgaos
    else:
        return False, orgaos


def doar_orgaos(orgaos: int, PROBABILIDADE_DOACAO_ORGAOS):
    '''
    Simula doação dos órgãos.
    Retorna se houve a doação, e os orgaos
    '''
    if orgaos <= 0:
        return False, orgaos
    else:
        if random.randint(1, 100) <= PROBABILIDADE_DOACAO_ORGAOS:
            novos_orgaos = random.randint(1, orgaos)
            orgaos -= novos_orgaos
            if orgaos <= 0:
                orgaos = 0
            return True, orgaos

    return False, orgaos
