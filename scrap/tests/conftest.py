from pytest import fixture
from unittest.mock import patch
from scrap.models.entities import Jogo, Usuario, Leilao
from datetime import datetime
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.pool import StaticPool

@fixture(autouse=True)
def disable_logger_setup():
    with patch('scrap.utils.logger.logger_setup'):
        yield

@fixture
def session():
    engine=create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool
        )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        registrar_usuarios(session)
        registrar_jogos(session)
        registrar_leiloes(session)
        yield session
    SQLModel.metadata.drop_all(engine)


@fixture
def game(session):
    j=session.get(Jogo, 1)
    return j






def registrar_usuarios(session):
    usuarios=0
    infos=[
        {'nome':'rafael','data':{'username':'rafafael','email':'rafael@gmail.com', 'senha': '1613', 'nivel': 2}},
        {'nome':'brenno','data':{'username':'brendol','email':'brenno@gmail.com', 'senha': '1234', 'nivel': 1}}
    ]
    for info in infos:
        u=Usuario(
            nome=info['nome'],
            username=info['data']['username'],
            email=info['data']['email'],
            senha=info['data']['senha'],
            nivel=info['data']['nivel'],
            token='test',
            dt_criacao=datetime.now(),
            status=True
        )
        session.add(u)
        session.commit()
        session.refresh(u)
        usuarios+=1
    return usuarios

def registrar_jogos(session):
    jogos=0
    lista_de_jogos=['Carson City Big Box', 'Wonderlans War', 'Root', 'Arcs', 'Barrage', 'Hues and Cues', 
        'Kingsburg 2 dition', 'Hansa Teutonica Big Box', 'The King is Dead 2 edition'
    ]
    lista_de_nomes_ludopedia=['carson-city-big-box', 'wonderland-s-war', 'root', 'arcs', 'barrage', 'hues-and-cues', 
        'kingsburg-second-edition', 'hansa-teutonica-big-box', 'the-king-is-dead-second-edition'
    ]
    if len(lista_de_jogos)==len(lista_de_nomes_ludopedia):
        registros=list(zip(lista_de_jogos, lista_de_nomes_ludopedia))
        for registro in registros:
            j=Jogo(
                nome=registro[0],
                nome_ludopedia=registro[1],
                criado_por=1,
                data_criacao=datetime.now(),
                data_alteracao=datetime.now()
            )
            session.add(j)
            jogos+=1
        session.commit()
    return jogos

def registrar_leiloes(session):
    leiloes=[
        {'id_leilao':1111, 'id_jogo':1, 'link_leilao':'www.ludopedia.com.br', 'valor_pago':50, 
         'data_fim_leilao':datetime(2025,3,25), 'status':'finalizado', 'observacoes':'nada', 
         'data_alteracao':datetime(2025,3,25),'local':'Niteroi/Rio de Janeiro', 'estado_item':True, 
         'tipo':True, 'data_registro':datetime(2025,3,25)}
    ]
    for leilao in leiloes:
        l=Leilao(
            id_leilao=leilao['id_leilao'],
            id_jogo=leilao['id_jogo'],
            link_leilao=leilao['link_leilao'],
            valor_pago=leilao['valor_pago'],
            data_fim_leilao=leilao['data_fim_leilao'],
            status=leilao['status'],
            observacoes=leilao['observacoes'],
            data_alteracao=leilao['data_alteracao'],
            local=leilao['local'],
            estado_item=leilao['estado_item'],
            tipo=leilao['tipo'],
            data_registro=leilao['data_registro']
        )
        session.add(l)
    session.commit()
    return len(leiloes)