from database import (
    get_session,
    close_session,
    Produtor,
    Cultura,
    Sensor,
    LeituraSensor,
    Aplicacao
)
from database.repositories import (
    ProdutorRepository,
    CulturaRepository,
    SensorRepository,
    LeituraSensorRepository,
    AplicacaoRepository
)
from datetime import datetime, date

def main():
    # Obtém uma sessão do banco de dados
    session = get_session()
    
    try:
        # Inicializa os repositórios
        produtor_repo = ProdutorRepository(session)
        cultura_repo = CulturaRepository(session)
        sensor_repo = SensorRepository(session)
        leitura_repo = LeituraSensorRepository(session)
        aplicacao_repo = AplicacaoRepository(session)
        
        # Exemplo: Criar um produtor
        produtor = produtor_repo.create(
            nome="João Silva",
            email="joao.silva@email.com",
            telefone="(11) 99999-9999"
        )
        print(f"Produtor criado: {produtor}")
        
        # Exemplo: Criar uma cultura
        cultura = cultura_repo.create(
            nome="Milho",
            tipo="Grão",
            data_inicio=date(2024, 3, 1),
            id_produtor=produtor.id
        )
        print(f"Cultura criada: {cultura}")
        
        # Exemplo: Criar um sensor
        sensor = sensor_repo.create(
            tipo="Umidade",
            modelo="SHT30",
            localizacao="Setor A",
            id_cultura=cultura.id
        )
        print(f"Sensor criado: {sensor}")
        
        # Exemplo: Registrar uma leitura
        leitura = leitura_repo.create(
            id_sensor=sensor.id,
            valor_umidade=65.5,
            valor_ph=6.8,
            valor_npk_fosforo=15.0,
            valor_npk_potassio=20.0
        )
        print(f"Leitura registrada: {leitura}")
        
        # Exemplo: Registrar uma aplicação
        aplicacao = aplicacao_repo.create(
            id_cultura=cultura.id,
            tipo="Fertilizante",
            quantidade=50.0
        )
        print(f"Aplicação registrada: {aplicacao}")
        
        # Exemplo: Buscar todas as culturas do produtor
        culturas = cultura_repo.get_by_produtor(produtor.id)
        print("\nCulturas do produtor:")
        for c in culturas:
            print(f"- {c}")
        
        # Exemplo: Buscar todas as leituras de um sensor
        leituras = leitura_repo.get_by_sensor(sensor.id)
        print("\nLeituras do sensor:")
        for l in leituras:
            print(f"- {l}")
        
        # Exemplo: Calcular média de valores do sensor
        media = leitura_repo.get_average_values_by_sensor(sensor.id)
        print("\nMédia de valores do sensor:")
        print(f"Umidade: {media['umidade']:.2f}%")
        print(f"pH: {media['ph']:.2f}")
        print(f"Fósforo: {media['fosforo']:.2f}")
        print(f"Potássio: {media['potassio']:.2f}")
        
        # Exemplo: Resumo de aplicações da cultura
        resumo = aplicacao_repo.get_culture_application_summary(cultura.id)
        print("\nResumo de aplicações da cultura:")
        print(f"Total de aplicações: {resumo['total_aplicacoes']}")
        print(f"Tipos aplicados: {', '.join(resumo['tipos_aplicados'])}")
        print(f"Quantidade total: {resumo['quantidade_total']:.2f}")
        
    finally:
        # Fecha a sessão
        close_session()

if __name__ == "__main__":
    main() 