from api.app            import app
from api.database       import getSession
from api.models         import Leilao, Jogo, Usuario
from api.security       import getPasswordHash, createAccessToken
from datetime           import datetime
from fastapi.testclient import TestClient
from pytest             import fixture
from sqlalchemy.pool    import StaticPool
from sqlmodel           import SQLModel, create_engine, Session

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
def client(session):
    def getSessionOverride():
        return session
    app.dependency_overrides[getSession]=getSessionOverride
    with TestClient(app) as client:
        yield client

@fixture
def user(session):
    u=session.get(Usuario,1)
    return u

@fixture
def user2(session):
    u=session.get(Usuario,2)
    return u

@fixture
def jogo(session):
    j=session.get(Jogo,1)
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
            senha=getPasswordHash(info['data']['senha']),
            nivel=info['data']['nivel'],
            token=createAccessToken(info['data']),
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










#@fixture
#def token(client, user):    
#    response=client.post(
#        '/auth/token/',
#        data={'username': user.username, 'password': '1613986478'}
#        )
#    return response.json()['access_token']