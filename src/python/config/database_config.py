from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    """Configurações do banco de dados."""
    host: str = "localhost"
    port: int = 5432
    database: str = "farmtech_db"
    user: str = "postgres"
    password: str = "postgres"

    @property
    def connection_string(self) -> str:
        """Retorna a string de conexão com o banco de dados."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}" 