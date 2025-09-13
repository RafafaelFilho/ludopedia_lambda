from datetime   import datetime
from pydantic   import EmailStr
from sqlmodel   import SQLModel, Field
from typing     import Optional

# Tables
class Leilao(SQLModel, table=True):
    __tablename__ = "leiloes"
    id: Optional[int] = Field(default=None, primary_key=True)
    id_leilao: int = Field(unique=True)
    id_jogo: int = Field(foreign_key="jogos.id")
    link_leilao: str
    valor_pago: int
    data_fim_leilao: datetime = Field(nullable=True)
    status: str = Field(default='em andamento')
    observacoes: str = Field(nullable=True)
    data_alteracao: datetime
    local: str = Field(nullable=True)
    estado_item: bool = Field(nullable=True) # true-novo | false-usado
    tipo: bool = Field(nullable=True) # true-jogo | false-extras
    data_registro: datetime 

class Jogo(SQLModel, table=True):
    __tablename__ = "jogos"
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    nome_ludopedia: str
    criado_por: int = Field(foreign_key='usuarios.id')
    data_criacao: datetime
    data_alteracao: datetime

class Usuario(SQLModel, table=True):
    __tablename__='usuarios'
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    username: str
    email: EmailStr
    senha: str
    token: str
    ultimo_request: datetime = Field(nullable=True)
    dt_criacao: datetime
    nivel: int # 1 = leitor | 2 = admin
    status: bool

class Registro(SQLModel, table=True):
    __tablename__='registros'
    id: Optional[int] = Field(primary_key=True)
    id_usuario: int = Field(foreign_key='usuarios.id')
    endpoint: str
    data_registro: datetime