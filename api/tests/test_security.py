from api.security import getPasswordHash, verifyPassword, createAccessToken, verifyPermission, validationTokenProcess
from api.settings import settings
from jwt import decode
from api.models import UsuarioRegistro

def testar_gerar_e_verificar_senha_hash():
    pwd_hashed=getPasswordHash('rafael')
    assert verifyPassword('rafael', pwd_hashed)

def testar_criar_token():
    data={'username':'rafafael','email':'rafafaelfilho@gmail.com', 'senha': '1613', 'nivel': 'reader'}
    token=createAccessToken(data)
    decoded=decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert decoded['username']==data['username']
    assert decoded['email']==data['email']
    assert decoded['senha']==data['senha']
    assert decoded['nivel']==data['nivel']

def testar_verificar_permissao(user, session):
    usuario = verifyPermission('1613',user.token, session, 2)
    assert usuario!=None
    
def testar_ERRO_verificar_permissao_sem_permissao_de_nivel(user2, session):
    usuario = verifyPermission('1234',user2.token, session, 2)
    assert usuario==None

def testar_ERRO_verificar_permissao_sem_permissao_de_senha(user, session):
    usuario = verifyPermission('1614',user.token, session, 2)
    assert usuario==None

def testar_recuperar_token(user, session):
    data=UsuarioRegistro(
        nome=user.nome,
        username=user.username,
        email=user.email,
        senha='1613'
    )
    token=validationTokenProcess(data, session)
    assert token==user.token