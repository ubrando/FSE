# FSE

## Aluno
|Matrícula | Aluno |
| -- | -- |
| 17/0164357  |  Ugor Brandão |

## Descrição
Trabalho de Fundamentos de Sistemas Embarcados de 2022.2 da Universade de Brasília. O sistema desenvolvido baseia-se na contrução de sistemas distribuidos que monitoram salas e que se comunicam com um servidor central o qual por meio de uma interface pode controlar saídas da sala bem como solicitar relatório contendo os estados dos sensores, ocupantes, humidade e temperatura da sala. <br>

## USO
Instale as dependencias do projeto
`pip3 install adafruit-circuitpython-dht`<br>

Execute o servidor central ao entrar no diretório Server: <br>
 'python index-server.py'

Execute o servidor distribuido ao entrar no siretório Client: <br>
 'python index-client.py'

 Interaja com a sala através do servidor distribuído.


