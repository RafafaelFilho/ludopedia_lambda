from api.database   import getSession
from api.models     import Jogo
from api.security   import verifyPermission
from datetime       import datetime
from fastapi        import APIRouter, Depends, HTTPException
from http           import HTTPStatus
from sqlmodel       import Session, select

router=APIRouter(
    prefix='/jogos',
    tags=['jogos']
)

@router.get('/', response_model=list[Jogo])
def buscar_jogos(senha: str, token: str, session:Session=Depends(getSession)):
    usuario = verifyPermission(senha, token, session)
    if not usuario:
        raise HTTPException(HTTPStatus.FORBIDDEN, 'Sem permissão')
    jogos=session.exec(select(Jogo)).all()
    return jogos

@router.post('/', response_model=Jogo)
def registrar_jogos(senha:str, token:str, jogo: Jogo, session:Session=Depends(getSession)):
    usuario = verifyPermission(senha, token, session, 2)
    if not usuario:
        raise HTTPException(HTTPStatus.FORBIDDEN, 'Sem permissão')
    j=Jogo(
        nome=jogo.nome,
        nome_ludopedia=jogo.nome_ludopedia,
        criado_por=usuario.id,
        data_criacao=datetime.now(),
        data_alteracao=datetime.now()
    )
    session.add(j)
    session.commit()
    session.refresh(j)
    return j

