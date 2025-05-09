# Entrega 2: Armazenamento de Dados em Banco SQL com Python

Este projeto implementa a camada de armazenamento e análise de dados do sistema de irrigação inteligente, focando na captura de dados do ESP32 e seu armazenamento em banco de dados SQL.

## Estrutura do Projeto

```
src/python/
├── config/                    # Configurações do projeto
│   ├── __init__.py
│   └── settings.py           # Configurações gerais e constantes
│
├── database/                 # Camada de acesso a dados
│   ├── __init__.py
│   ├── models.py            # Definição dos modelos SQLAlchemy
│   ├── oracle.py            # Configuração da conexão Oracle
│   ├── setup.py             # Script de inicialização do banco
│   └── repositories/        # Implementação dos repositórios
│       ├── __init__.py
│       ├── produtor_repository.py
│       ├── cultura_repository.py
│       ├── sensor_repository.py
│       ├── leitura_sensor_repository.py
│       └── aplicacao_repository.py
│
├── examples/                 # Exemplos de uso
│   ├── __init__.py
│   └── repository_example.py # Exemplo de uso dos repositórios
│
├── logs/                    # Logs do sistema
│
├── services/               # Camada de serviços
│   ├── __init__.py
│   ├── sensor_service.py   # Serviço de processamento de sensores
│   ├── irrigation_service.py # Serviço de controle de irrigação
│   ├── produtor_service.py # Serviço de gerenciamento de produtores
│   ├── cultura_service.py  # Serviço de gerenciamento de culturas
│   └── aplicacao_service.py # Serviço de gerenciamento de aplicações
│
├── tests/                  # Testes automatizados
│   ├── __init__.py
│   ├── conftest.py        # Configurações dos testes
│   ├── test_models.py     # Testes dos modelos
│   ├── test_repositories.py # Testes dos repositórios
│   └── test_services.py   # Testes dos serviços
│
├── .env                    # Variáveis de ambiente
├── .gitignore             # Arquivos ignorados pelo git
├── Dockerfile             # Configuração do container
├── main.py               # Ponto de entrada da aplicação
├── pytest.ini            # Configuração do pytest
├── README.md             # Documentação do projeto
└── requirements.txt      # Dependências do projeto
```

### Descrição dos Diretórios

#### config/
Contém as configurações do projeto, incluindo:
- Configurações do banco de dados
- Constantes do sistema
- Configurações de logging
- Variáveis de ambiente

#### database/
Implementa a camada de acesso a dados:
- `models.py`: Define as classes que mapeiam as tabelas do banco
- `oracle.py`: Gerencia a conexão com o banco Oracle
- `setup.py`: Script para inicialização do banco
- `repositories/`: Implementa o padrão Repository para cada entidade

#### examples/
Contém exemplos de uso do sistema:
- Exemplos de uso dos repositórios
- Exemplos de consultas complexas
- Exemplos de integração com serviços

#### logs/
Armazena os logs do sistema:
- Logs da aplicação em produção
- Logs dos testes
- Logs de erro e debug

#### services/
Implementa a lógica de negócio:
- Processamento de dados dos sensores
- Lógica de controle de irrigação
- Regras de negócio do sistema

#### tests/
Contém os testes automatizados:
- Testes unitários
- Testes de integração
- Fixtures e configurações de teste

## Metas da Entrega

1. **Captura de Dados**
   - Implementar a leitura dos dados do monitor serial do ESP32
   - Processar e validar os dados recebidos
   - Simular a comunicação serial em ambiente de desenvolvimento

2. **Armazenamento em Banco SQL**
   - Criar script Python para simulação do armazenamento
   - Implementar estrutura de banco de dados relacional
   - Garantir integridade e consistência dos dados

3. **Operações CRUD**
   - Implementar operações de inserção (Create)
   - Implementar operações de consulta (Read)
   - Implementar operações de atualização (Update)
   - Implementar operações de remoção (Delete)

4. **Documentação e Justificativa**
   - Relacionar a estrutura de dados com o MER da Fase 2
   - Justificar as escolhas de implementação
   - Documentar as operações CRUD implementadas

## Entregáveis

### 1. Script Python Funcional

O script principal (`main.py`) implementa:
- Leitura de dados do ESP32
- Processamento e validação
- Armazenamento em banco SQL
- Operações CRUD básicas

### 2. Tabelas de Exemplo

#### produtor
```sql
CREATE TABLE produtor (
    id_produtor NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR2(200) NOT NULL,
    email VARCHAR2(200) NOT NULL,
    telefone VARCHAR2(30) NOT NULL
);
```

#### cultura
```sql
CREATE TABLE cultura (
    id_cultura NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR2(100) NOT NULL,
    tipo VARCHAR2(50) NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE,
    id_produtor NUMBER NOT NULL,
    CONSTRAINT fk_cultura_produtor FOREIGN KEY (id_produtor) 
        REFERENCES produtor(id_produtor)
);
```

#### sensor
```sql
CREATE TABLE sensor (
    id_sensor NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tipo VARCHAR2(50) NOT NULL,
    modelo VARCHAR2(50) NOT NULL,
    localizacao VARCHAR2(100) NOT NULL,
    id_cultura NUMBER NOT NULL,
    CONSTRAINT fk_sensor_cultura FOREIGN KEY (id_cultura) 
        REFERENCES cultura(id_cultura)
);
```

#### leitura_sensor
```sql
CREATE TABLE leitura_sensor (
    id_leitura NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_sensor NUMBER NOT NULL,
    data_hora TIMESTAMP NOT NULL,
    valor_umidade NUMBER,
    valor_ph NUMBER,
    valor_npk_fosforo NUMBER,
    valor_npk_potassio NUMBER,
    CONSTRAINT fk_leitura_sensor FOREIGN KEY (id_sensor) 
        REFERENCES sensor(id_sensor)
);
```

#### aplicacao
```sql
CREATE TABLE aplicacao (
    id_aplicacao NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_cultura NUMBER NOT NULL,
    data_hora TIMESTAMP NOT NULL,
    tipo VARCHAR2(50) NOT NULL,
    quantidade NUMBER NOT NULL,
    CONSTRAINT fk_aplicacao_cultura FOREIGN KEY (id_cultura) 
        REFERENCES cultura(id_cultura)
);
```

### 3. Relação com MER da Fase 2

A estrutura do banco de dados foi projetada seguindo o MER desenvolvido na Fase 2, com as seguintes considerações:

- **Entidades Principais**:
  - Produtor: Responsável pela plantação
  - Cultura: Plantação gerenciada
  - Sensor: Equipamento de coleta de dados
  - Leitura_Sensor: Dados coletados
  - Aplicacao: Ações realizadas na lavoura

- **Relacionamentos**:
  - 1 Produtor → N Culturas
  - 1 Cultura → N Sensores
  - 1 Sensor → N Leituras
  - 1 Cultura → N Aplicações

- **Adaptações Práticas**:
  - Uso de NUMBER em vez de INT/DOUBLE para compatibilidade Oracle
  - Adição de constraints para garantir integridade referencial
  - Timestamps para rastreamento temporal
  - Campos opcionais em leitura_sensor para diferentes tipos de sensores

## Como Executar

1. **Configuração do Ambiente**
   ```bash
   cd src/python
   pip install -r requirements.txt
   ```

2. **Configuração do Banco**

   Você pode escolher entre usar um banco Oracle local ou usar a versão dockerizada:

   ### Opção 1: Usando Docker (Recomendado)
   
   ```bash
   # Na raiz do projeto
   docker-compose up -d
   ```
   
   Aguarde alguns minutos até o banco estar pronto (você pode verificar o status com `docker-compose ps`).
   
   Configure o arquivo `.env` na pasta `src/python` com as seguintes variáveis:
   ```bash
   ORACLE_USER=system
   ORACLE_PASSWORD=oracle
   ORACLE_HOST=localhost
   ORACLE_PORT=1521
   ORACLE_SERVICE=XE
   ```

   ### Opção 2: Usando Oracle Local
   
   Se você preferir usar uma instalação local do Oracle, configure o arquivo `.env` com suas credenciais:
   ```bash
   ORACLE_USER=seu_usuario
   ORACLE_PASSWORD=sua_senha
   ORACLE_HOST=localhost
   ORACLE_PORT=1521
   ORACLE_SERVICE=XE
   ```

   ### Inicialização do Banco
   
   Após configurar o banco (seja via Docker ou local), execute:
   ```bash
   cd src/python
   # Adiciona o diretório atual ao PYTHONPATH
   export PYTHONPATH=$PYTHONPATH:$(pwd)
   python database/setup.py
   ```
   
   Este script irá:
   - Criar todas as tabelas necessárias
   - Inicializar o banco com dados de exemplo
   - Configurar as conexões necessárias

   Uma mensagem como essa deve aparecer:

   ![Banco populado com sucesso](../../assets/banco-populado-com-sucesso.png)
   

   ### Comandos Docker Úteis
   
   ```bash
   # Verificar status do container
   docker-compose ps
   
   # Ver logs do banco
   docker-compose logs -f oracle
   
   # Parar o banco
   docker-compose down
   
   # Parar e remover os volumes (apaga todos os dados)
   docker-compose down -v
   ```

## Executando os Testes

O projeto inclui testes automatizados para garantir a qualidade do código. Para executar os testes:

### Opção 1: Usando Docker (Recomendado)

```bash
# Na raiz do projeto
docker-compose up --build tests
```

### Opção 2: Executando Localmente

1. **Configurar o ambiente de testes**:
   ```bash
   cd src/python
   # Adiciona o diretório atual ao PYTHONPATH
   export PYTHONPATH=$PYTHONPATH:$(pwd)
   ```

2. **Executar todos os testes**:
   ```bash
   python -m pytest
   ```

3. **Executar testes específicos**:
   ```bash
   # Testes do banco de dados
   python -m pytest tests/database/
   
   # Testes dos serviços
   python -m pytest tests/services/
   
   # Teste específico
   python -m pytest tests/database/test_models.py
   ```

4. **Executar testes com cobertura**:
   ```bash
   python -m pytest --cov=.
   ```

5. **Verificar logs dos testes**:
   ```bash
   python -m pytest -v
   ```

### Estrutura dos Testes

```
tests/
├── __init__.py         # Marca o diretório como pacote Python
├── conftest.py         # Configurações dos testes
├── test_models.py      # Testes dos modelos
├── test_repositories.py # Testes dos repositórios
└── test_services.py    # Testes dos serviços
```

### Observações sobre os Testes

- Os testes são executados em um banco de dados de teste
- Cada teste é executado em uma transação isolada
- Os dados de teste são limpos após cada execução
- Os logs de erro são salvos em `logs/test.log`
- Certifique-se de que o PYTHONPATH está configurado corretamente

## Operações CRUD Implementadas

### Create (Inserção)
```python
# Exemplo de inserção de registro de sensor
def insert_sensor_record(soil_moisture, ph_level, phosphorus, potassium, irrigation):
    record = SensorRecord.query.add(
        soil_moisture=soil_moisture,
        ph_level=ph_level,
        phosphorus_level=phosphorus,
        potassium_level=potassium,
        irrigation_active=irrigation
    )
    db.session.commit()
```

### Read (Consulta)
```python
# Exemplo de consulta de registros
def get_sensor_records(start_date, end_date):
    return SensorRecord.query.filter(
        SensorRecord.timestamp.between(start_date, end_date)
    ).all()
```

### Update (Atualização)
```python
# Exemplo de atualização de registro
def update_sensor_record(record_id, new_values):
    record = SensorRecord.query.get(record_id)
    for key, value in new_values.items():
        setattr(record, key, value)
    db.session.commit()
```

### Delete (Remoção)
```python
# Exemplo de remoção de registro
def delete_sensor_record(record_id):
    record = SensorRecord.query.get(record_id)
    db.session.delete(record)
    db.session.commit()
```
## Justificativa das Escolhas

1. **SQLAlchemy como ORM**
   - Facilita o mapeamento objeto-relacional
   - Fornece abstração do banco de dados
   - Suporta múltiplos bancos de dados

2. **Estrutura de Tabelas**
   - Normalização para evitar redundância
   - Índices para otimização de consultas
   - Timestamps para rastreamento

3. **Validações**
   - Verificação de tipos de dados
   - Restrições de integridade
   - Tratamento de erros

4. **Docker para Desenvolvimento**
   - Ambiente consistente entre desenvolvedores
   - Fácil configuração do banco Oracle
   - Isolamento de dependências

## Observações

- O sistema foi projetado para ser facilmente extensível
- As operações CRUD são documentadas e testadas
- O código segue as melhores práticas de Python
- A estrutura do banco permite futuras expansões
- O ambiente Docker facilita o desenvolvimento e testes

