from behave import given, when, then
from necroterio import *


@given("o necroterio esta preparado para lidar com orgaos")
def given_preparar_necroterio_para_orgaos(context):
    context.orgaos = 0
    assert context.orgaos == 0

@when("houver {porcentagem} porcento de chance de recebimento de orgaos")
def when_probalilidade_receber_orgaos(context, porcentagem):
    context.probabilidade_recebimento_orgaos = porcentagem
    assert context.probabilidade_recebimento_orgaos

@then("orgaos devem ser recebidos")
def then_receber_orgaos(context):
    recebeu, orgaos = receber_orgaos(context.orgaos, int(
        context.probabilidade_recebimento_orgaos))
    
    context.orgaos = orgaos

    assert recebeu is True

@then("orgaos nao devem ser recebidos")
def then_nao_receber_orgaos(context):
    recebeu, orgaos = receber_orgaos(context.orgaos, int(
        context.probabilidade_recebimento_orgaos))

    context.orgaos = orgaos

    assert recebeu is False

@when("houver pelo menos um orgao para ser doado")
def when_orgaos_disponiveis_para_doacao(context):
    assert context.orgaos > 0

@when("houver {porcentagem} porcento de chance de doacao de orgaos")
def when_probalilidade_doacao_orgaos(context, porcentagem):
    if context.orgaos == 0:
        context.probabilidade_doacao_orgaos = 0
    else:
        context.probabilidade_doacao_orgaos = porcentagem
    assert context.probabilidade_doacao_orgaos == 0 or context.probabilidade_doacao_orgaos

@then("orgaos devem ser doados")
def then_doar_orgaos(context):
    doou, orgaos_restantes = doar_orgaos(
        context.orgaos, int(context.probabilidade_doacao_orgaos))
    
    context.orgaos = orgaos_restantes

    assert doou is True

@when("nao houver orgaos para serem doados")
def when_nao_ha_orgaos(context):       
    assert context.orgaos <= 0

@then("orgaos nao devem ser doados")
def then_nao_doar_orgaos(context):
    doou, orgaos_restantes = doar_orgaos(
        context.orgaos, int(context.probabilidade_doacao_orgaos))

    context.orgaos = orgaos_restantes

    assert doou is False
