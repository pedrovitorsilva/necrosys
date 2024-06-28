Feature: o sistema monitora as causas de morte contabilizadas naquele turno

  Scenario: ninguem faleceu e as causas de morte nao foram contabilizadas
    Given o ambiente esta preparado
    When uma foto ./rostos/personagens4.jpeg foi escaneada
    Then nenhum paciente deve ser reconhecido
    Then nenhuma causa de morte foi contabilizada

  Scenario: pessoas faleceram e as causas de morte foram contabilizadas
    Given o ambiente esta preparado
    When uma foto ./rostos/personagens1.jpeg foi escaneada
    Then pelo menos um paciente deve ser reconhecido
    Then pelo menos uma causa de morte foi contabilizada



