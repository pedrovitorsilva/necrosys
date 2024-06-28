from behave import then
from necroterio import *

@then("nenhuma causa de morte foi contabilizada")
def then_nenhuma_causa_de_morte_contabilizada(context):
    assert context.causas_da_morte == {}

@then("pelo menos uma causa de morte foi contabilizada")
def then_causa_de_morte_contabilizada(context):
    assert context.causas_da_morte != {}