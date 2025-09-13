from http import HTTPStatus

def testar_ler_jogos_nivel_admin(client, user):
    response=client.get(
        '/jogos/',
        params={
            'senha':'1613',
            'token':user.token
        }
    )
    assert response.status_code==HTTPStatus.OK
    assert isinstance(response.json(),list), "Não é uma lista"
    assert len(response.json())>0

def testar_ler_jogos_nivel_reader(client, user2):
    response=client.get(
        '/jogos/',
        params={
            'senha':'1234',
            'token':user2.token
        }
    )
    assert isinstance(response.json(),list), "Não é uma lista"
    assert response.status_code==HTTPStatus.OK
    assert len(response.json())>0

def testar_registrar_jogos(client, user):
    response=client.post(
        '/jogos/',
        params={
            'senha':'1613',
            'token':user.token
        },
        json={
            'nome':'teste',
            'nome_ludopedia':'teste_ludopedia'
        }
    )
    assert response.status_code==HTTPStatus.OK

def testar_ERRO_registrar_jogos_sem_permissao(client, user2):
    response=client.post(
        '/jogos/',
        params={
            'senha':'1613',
            'token':user2.token
        },
        json={
            'nome':'teste',
            'nome_ludopedia':'teste_ludopedia'
        }
    )
    assert response.status_code==HTTPStatus.FORBIDDEN

def testar_ERRO_ler_jogos_senha_errada(client, user2):
    response=client.get(
        '/jogos/',
        params={
            'senha':'12345',
            'token':user2.token
        }
    )
    assert response.status_code==HTTPStatus.FORBIDDEN