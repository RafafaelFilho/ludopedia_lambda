from api.models     import Leilao, LeilaoUpdate, Jogo
from api.security   import verifyPermission
from api.database   import getSession
from datetime       import datetime
from fastapi        import APIRouter, Depends, HTTPException
from http           import HTTPStatus
from sqlmodel       import Session, select

router=APIRouter(
    prefix='/leiloes',
    tags=['leiloes']
)

@router.get('/', response_model=list[Leilao])
def buscar_leiloes(senha: str, token: str, session:Session=Depends(getSession)):
    usuario = verifyPermission(senha, token, session)
    if not usuario:
        raise HTTPException(HTTPStatus.FORBIDDEN, 'Sem permissão')
    leiloes=session.exec(select(Leilao)).all()
    return leiloes

@router.get('/{nome_ludopedia}', response_model=list[Leilao])
def buscar_leiloes_de_um_jogo(nome_ludopedia:str, senha:str, token:str, session:Session=Depends(getSession)):
    usuario = verifyPermission(senha, token, session, 2)
    if not usuario:
        raise HTTPException(HTTPStatus.FORBIDDEN, 'Sem permissão')
    leiloes=session.exec(select(Leilao).join(Jogo, Jogo.id==Leilao.id_jogo).where(Jogo.nome_ludopedia==nome_ludopedia)).all()
    if not leiloes:
        raise HTTPException(HTTPStatus.NOT_FOUND, f'nome_ludopedia: "{nome_ludopedia}" não existe')
    return leiloes

@router.put('/{id_leilao}', response_model=Leilao)
def registrar_jogo(id_leilao:int, dados:LeilaoUpdate, senha:str, token:str, session:Session=Depends(getSession)):
    usuario = verifyPermission(senha, token, session, 2)
    if not usuario:
        raise HTTPException(HTTPStatus.FORBIDDEN, 'Sem permissão')
    leilao = session.exec(select(Leilao).where(Leilao.id_leilao==id_leilao)).first()
    if not leilao:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Leilão não encontrado")
    for key, value in dados.model_dump(exclude_unset=True).items():
        setattr(leilao, key, value)
        leilao.data_alteracao=datetime.now()
    session.add(leilao)
    session.commit()
    session.refresh(leilao)
    return leilao
