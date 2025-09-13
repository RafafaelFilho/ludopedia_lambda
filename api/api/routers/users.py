from api.database   import getSession
from api.models     import UsuarioPublico, UsuarioRegistro, Usuario, UsuarioPublicoToken
from api.security   import getPasswordHash, createAccessToken, verifyPermission, validationTokenProcess
from datetime       import datetime
from fastapi        import Depends, HTTPException,  APIRouter
from http           import HTTPStatus
from sqlmodel       import Session, select

router = APIRouter(
    prefix='/usuarios',
    tags=['usuarios']
)

@router.post('/', response_model=UsuarioPublicoToken)
def criar_usuario(usuario:UsuarioRegistro, session:Session=Depends(getSession)):
    query=session.exec(select(Usuario).where((Usuario.username==usuario.username)|(Usuario.email==usuario.email))).first()
    if query:
        raise HTTPException(status_code=HTTPStatus.CONFLICT,detail='Username ou Email já existente!')
    data={'username':usuario.username,'email':usuario.email, 'senha': usuario.senha, 'nivel': 1}
    u=Usuario(
        nome=usuario.nome,
        username=usuario.username,
        email=usuario.email,
        senha=getPasswordHash(usuario.senha),
        token=createAccessToken(data),
        nivel=1,
        status=True,
        dt_criacao=datetime.now()
    )
    session.add(u)
    session.commit()
    session.refresh(u)
    return u

@router.post('/token')
def buscar_token(usuario: UsuarioRegistro, session:Session=Depends(getSession)):
    token=validationTokenProcess(usuario, session)
    if not token:
        raise HTTPException(HTTPStatus.FORBIDDEN, 'Sem permissão')
    return token

@router.get('/', response_model=list[UsuarioPublico])
def ler_usuarios(senha: str, token: str, session:Session=Depends(getSession)):
    usuario = verifyPermission(senha, token, session)
    if not usuario:
        raise HTTPException(HTTPStatus.FORBIDDEN, 'Sem permissão')
    usuarios=session.exec(select(Usuario)).all()
    return usuarios