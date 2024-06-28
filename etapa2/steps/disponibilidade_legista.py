from behave import given, when, then
from necroterio import *



@when("o legista nao esta ocupado")
def when_legista_desocupado(context):
    assert context.legista_ocupado is False


@when("houver {porcentagem} porcento de chance de atendimento do legista")
def when_porcentagem_atendimento_legista(context, porcentagem):
    context.probabilidade_atendimento_legista = porcentagem
    assert context.probabilidade_atendimento_legista == 0 or context.probabilidade_atendimento_legista


@then("o legista ira atender")
def then_legista_realiza_atendimento(context):
    assert atendimento_legista(
        context.legista_ocupado, int(context.probabilidade_atendimento_legista)) is True


@given("o legista esta de plantao mas esta ocupado")
def given_legista_ocupado(context):
    context.legista_ocupado = True
    context.probabilidade_atendimento_legista = 0
    assert context.legista_ocupado is True


@then("o legista nao ira atender")
def then_legista_nao_realiza_atendimento(context):
    assert atendimento_legista(
        context.legista_ocupado, int(context.probabilidade_atendimento_legista)) is False
