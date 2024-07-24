from typing import Tuple
import face_recognition as fr
import colored
import random
import simpy
import json

# Inicializando variáveis

falecidos_identificados = "falecidos_identificados.json"

POSSIVEIS_FALECIDOS = [
    "rostos/personagens1.jpeg",
    "rostos/personagens2.jpeg",
    "rostos/personagens3.jpeg",
    "rostos/personagens4.jpeg"
]

fotos_dos_falecidos = [] 

# Definindo ciclos e definindo probabilidades dos acontecimentos

# Estes valores simulam um simulacao real, onde as ações acontecem em ordens aleatórias

CICLO_VERIFICACAO_FALECIDOS = 20
CICLO_VERIFICACAO_CAUSAS_DE_MORTE = 50
CICLO_DISPONIBILIDADE_LEGISTA = 20
CICLO_RECEBIMENTO_ORGAOS = 30
CICLO_DOACAO_ORGAOS = 30

PROBABILIDADE_DISPONIBILIDADE_LEGISTA = 50
PROBABILIDADE_DOACAO_ORGAOS = 50
PROBABILIDADE_RECEBIMENTO_ORGAOS = 40

# Funções Auxilliares --------------------------------------------------------


def imprimir(mensagem: str, cor: str):
    ''' Imprimir a mensagem na cor selecionada '''
    print(colored.fg('black'), colored.bg(
        cor), mensagem, colored.attr('reset'))


def preparar() -> Tuple[bool, simpy.Environment, dict]:
    '''
    Inicializa as variáveis necessárias.

    Retorna: Tuple[bool, simpy.Environment, Dict]: 

    Preparação bem ou mal sucedida;
    Ambiente de simulação;
    Falecidos registrados.
    '''

    simulacao = simpy.Environment()

    try:
        with open(falecidos_identificados, "r") as arquivo:
            falecidos_registrados = json.load(arquivo)
        return True, simulacao, falecidos_registrados

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return False, None, None


def scanner_foto() -> str:
    ''' Escolhe uma foto aleatória e a retorna. Simula um scanner.'''
    foto = random.choice(POSSIVEIS_FALECIDOS)
    print(f"Foto passou pelo scanner: {foto}")
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
        if novo_reconhecido['codigo'] not in [pessoa['codigo'] for pessoa in pessoas_reconhecidas]:
            pessoas_reconhecidas.append(novo_reconhecido)

        # Registrar causa da morte
        causa = novo_reconhecido['causa_morte']
        if causa in causas_da_morte:
            causas_da_morte[causa] += 1
        else:
            causas_da_morte[causa] = 1


def verificar_rostos(simulacao: simpy.Environment, falecidos_registrados: dict, pessoas_reconhecidas: list[str], causas_da_morte: dict):
    '''
    Verifica os novos rostos apresentados.

    Reconhece falecidos e registra as pessoas que foram reconhecidas.
    '''

    while True:
        imprimir(
            f"Atendimento feito. Rosto sendo visto em {simulacao.now}...", "light_blue")

        rostos = scanner_foto()
        ocorreu_reconhecimento, novos_reconhecidos = reconhecer_falecidos(
            rostos, falecidos_registrados)

        if ocorreu_reconhecimento:
            print("Pessoa(s) reconhecida(s):")
            print([pessoa['nome'] for pessoa in novos_reconhecidos])
            print("\n")
            registrar_reconhecido(novos_reconhecidos,
                                  pessoas_reconhecidas, causas_da_morte)

        yield simulacao.timeout(CICLO_VERIFICACAO_FALECIDOS)


def relatorio_causas_morte(simulacao: simpy.Environment, causas_morte: dict):
    '''
    Gera um relatório com as causas de óbito, baseado na quantidade das pessoas pesquisadas no turno.
    '''
    while True:
        relatorio_ordenado = dict(
            sorted(causas_morte.items(), key=lambda item: item[1], reverse=True))

        imprimir(f"Imprimindo Relatório em {simulacao.now} ", "steel_blue")
        print("Causas do óbito mais pesquisadas no turno:")
        for key, value in relatorio_ordenado.items():
            print(f"{key.capitalize()} : {value}")
        print("\n")

        yield simulacao.timeout(CICLO_VERIFICACAO_CAUSAS_DE_MORTE)


def verificar_disponibilidade_legista(simulacao: simpy.Environment, legista_ocupado: bool):
    '''
        Verifica e retorna se o legista está ocupado ou não.
    '''
    while True:
        if random.randint(1, 100) <= PROBABILIDADE_DISPONIBILIDADE_LEGISTA and legista_ocupado:
            legista_ocupado = False
            imprimir(
                f"Verificando status do legista em {simulacao.now}:", "spring_green_4")
            print("Legista terminou o procedimento e está disponível!!")
        else:
            legista_ocupado = True
            imprimir(
                f"Verificando status do legista em {simulacao.now}:", "red_3a")
            print("Legista iniciou um procedimento e está indisponível...")
        print("\n")

        yield simulacao.timeout(CICLO_DISPONIBILIDADE_LEGISTA)


def receber_orgaos(simulacao: simpy.Environment, orgaos: list[int]):
    '''
    Simula o recebimento dos órgãos.
    '''
    while True:
        if random.randint(1, 100) <= PROBABILIDADE_RECEBIMENTO_ORGAOS:
            novos_orgaos = random.randint(1, 5)
            orgaos[0] += novos_orgaos
            imprimir(
                f"{novos_orgaos} órgão(s) recebido(s) com sucesso em {simulacao.now}!", "blue_violet")

        yield simulacao.timeout(CICLO_RECEBIMENTO_ORGAOS)


def doar_orgaos(simulacao: simpy.Environment, orgaos: list[int]):
    '''
    Simulaa doação dos órgãos.
    '''
    while True:
        if orgaos[0] <= 0:
            imprimir(
                f"Não há mais órgaos para doar em {simulacao.now}...", "red_3a")
        else:
            if random.randint(1, 100) <= PROBABILIDADE_DOACAO_ORGAOS:
                novos_orgaos = random.randint(1, orgaos[0])
                orgaos[0] -= novos_orgaos

                if orgaos[0] <= 0:
                    orgaos[0] = 0

                imprimir(
                    f"{novos_orgaos} órgão(s) doado(s) com sucesso em {simulacao.now}!", "medium_spring_green")

        yield simulacao.timeout(CICLO_DOACAO_ORGAOS)

# Main


if __name__ == "__main__":
    houve_inicializacao, simulacao, falecidos_registrados = preparar()

    if houve_inicializacao:

        # Incializando Variáveis

        pessoas_reconhecidas = []
        causas_da_morte = {}
        legista_ocupado = False

        # Lista é um objeto mutável, e pode ser alterado pelas funções,
        # diferentemente de números

        orgaos_disponiveis = [0]  # // orgaos_disponiveis = 0

        # Inicializando processos

        # # Dentro da verificação dos rostos, há o registro dos reconhecidos e das causas da morte
        simulacao.process(verificar_rostos(
            simulacao, falecidos_registrados, pessoas_reconhecidas, causas_da_morte))

        simulacao.process(relatorio_causas_morte(simulacao, causas_da_morte))

        simulacao.process(verificar_disponibilidade_legista(
            simulacao, legista_ocupado))

        simulacao.process(receber_orgaos(simulacao, orgaos_disponiveis))
        simulacao.process(doar_orgaos(simulacao, orgaos_disponiveis))

        simulacao.run(until=100)
