Feature: a partir de uma foto, pode-se saber se uma pessoa faleceu

    Scenario: um paciente foi reconhecido entre os falecidos
    Given o ambiente esta preparado
    When uma foto ./rostos/personagens1.jpeg foi escaneada
    Then pelo menos um paciente deve ser reconhecido

    Scenario: um paciente nao foi reconhecido entre os falecidos
    Given o ambiente esta preparado
    When uma foto ./rostos/personagens4.jpeg foi escaneada
    Then nenhum paciente deve ser reconhecido