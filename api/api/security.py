from api.models     import Usuario
from api.settings   import settings
from jwt            import encode, decode
from pwdlib         import PasswordHash
from sqlmodel       import select

pwd_context=PasswordHash.recommended()

def getPasswordHash(password:str):
    return pwd_context.hash(password)

def verifyPassword(pwd_to_verify:str , hashed_pwd:str):
    return pwd_context.verify(pwd_to_verify, hashed_pwd)

def createAccessToken(data: dict):
    data_to_encode=data.copy()
    encoded_jwt=encode(data_to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verifyPermission(senha, token, session, level: int = 1):
    data=decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    usuario=session.exec(select(Usuario).where((Usuario.username==data['username']))).first()
    if usuario.nivel<level or data['nivel']<level:
        return None
    if not verifyPassword(data['senha'],usuario.senha) or data['senha']!=senha:
        return
    return usuario

def validationTokenProcess(user_form, session):
    usuario=session.exec(select(Usuario).where((Usuario.username==user_form.username))).first()
    if not usuario:
        return None
    if not verifyPassword(user_form.senha, usuario.senha):
        return None
    if usuario.email!=user_form.email:
        return None
    if usuario.nome.upper()!=user_form.nome.upper():
        return None 
    return usuario.token