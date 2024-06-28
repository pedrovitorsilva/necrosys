Feature: o sistema monitora se o legista esta disponivel para atendimento

    Scenario: o legista esta disponivel
    Given o ambiente esta preparado
    When o legista nao esta ocupado
    When houver 100 porcento de chance de atendimento do legista
    Then o legista ira atender

    Scenario: o legista ja esta em atendimento
    Given o ambiente esta preparado
    Given o legista esta de plantao mas esta ocupado
    Then o legista nao ira atender