from behave import given, when, then
from necroterio import *

@given("o ambiente esta preparado")
def given_ambiente_preparado(context):
    context.preparado, context.falecidos_registrados = preparar()

    context.causas_da_morte = {}

    context.legista_ocupado = False

    assert context.preparado is True


@when("uma foto {foto} foi escaneada")
def when_foto_escaneada(context,foto):
    context.foto = foto

    assert context.foto is not None


@then('pelo menos um paciente deve ser reconhecido')
def then_pelo_menos_um_paciente_reconhecido(context):
    houve_reconhecidos, reconhecidos = reconhecer_falecidos(context.foto, context.falecidos_registrados)

    registrar_reconhecido(reconhecidos,context.falecidos_registrados,context.causas_da_morte)

    assert houve_reconhecidos > 0


@then('nenhum paciente deve ser reconhecido')
def then_nenhum_paciente_reconhecido(context):
    houve_reconhecidos, _ = reconhecer_falecidos(
        context.foto, context.falecidos_registrados)

    assert houve_reconhecidos == 0
