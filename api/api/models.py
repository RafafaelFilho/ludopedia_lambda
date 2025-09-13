from datetime   import datetime
from pydantic   import EmailStr
from sqlmodel   import SQLModel, Field
from typing     import Optional

# Tables
class Leilao(SQLModel, table=True):
    __tablename__ = "leilao"
    id: Optional[int] = Field(default=None, primary_key=True)
    id_leilao: int = Field(unique=True)
    id_jogo: int = Field(foreign_key="jogo.id")
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
    __tablename__ = "jogo"
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

# Schemas
class UsuarioRegistro(SQLModel):
    nome: str
    username: str
    email: EmailStr
    senha: str
    
class UsuarioPublico(SQLModel):
    id: int
    nome: str
    username: str
    email: EmailStr
    ultimo_request: Optional[datetime]
    dt_criacao: datetime
    nivel: int
    status: bool

class UsuarioPublicoToken(UsuarioPublico):
    token: str
    
class JogoRegistro(SQLModel):
    nome: str
    nome_ludopedia: str

class LeilaoUpdate(SQLModel):
    valor_pago: Optional[int] = None
    data_fim_leilao: Optional[datetime] = None
    status: Optional[str] = None
    observacoes: Optional[str] = None
    local: Optional[str] = None
    estado_item: Optional[bool] = None
    tipo: Optional[bool] = None



