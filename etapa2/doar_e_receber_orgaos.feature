Feature: o sistema do necroterio trabalha com doacoes de orgaos

    Scenario: orgaos foram recebidos no necroterio
    Given o ambiente esta preparado
    Given o necroterio esta preparado para lidar com orgaos
    When houver 100 porcento de chance de recebimento de orgaos
    Then orgaos devem ser recebidos

    Scenario: orgaos nao foram recebidos no necroterio
    Given o ambiente esta preparado
    Given o necroterio esta preparado para lidar com orgaos
    When houver 0 porcento de chance de recebimento de orgaos
    Then orgaos nao devem ser recebidos

    Scenario: orgaos foram doados no necroterio
    Given o ambiente esta preparado
    Given o necroterio esta preparado para lidar com orgaos
    When houver 100 porcento de chance de recebimento de orgaos
    Then orgaos devem ser recebidos
    When houver pelo menos um orgao para ser doado
    When houver 100 porcento de chance de doacao de orgaos
    Then orgaos devem ser doados

    Scenario: nao ha orgaos para doar no necroterio
    Given o ambiente esta preparado
    Given o necroterio esta preparado para lidar com orgaos
    When houver 0 porcento de chance de doacao de orgaos
    Then orgaos nao devem ser doados