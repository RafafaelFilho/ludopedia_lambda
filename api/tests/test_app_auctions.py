from http import HTTPStatus

def testar_leitura_de_leiloes(client, user):
    response=client.get(
        '/leiloes/',
        params={
            'senha':'1613',
            'token':user.token
        }
    )
    assert response.status_code==HTTPStatus.OK
    assert isinstance(response.json(),list), "Não é uma lista"
    assert len(response.json())>0

def testar_atualizar_leilao(client, user):
    response=client.put(
        '/leiloes/1111',
        params={
            'senha':'1613',
            'token':user.token
        },
        json={
            'observacoes':'obs alterado'
        }
    )
    leilao=response.json()
    assert response.status_code==HTTPStatus.OK
    assert leilao['observacoes']=='obs alterado'
    
def testar_ERRO_leitura_de_leiloes(client, user):
    response=client.get(
        '/leiloes/',
        params={
            'senha':'1614',
            'token':user.token
        }
    )
    assert response.status_code==HTTPStatus.FORBIDDEN
    
def testar_ERRO_id_leilao_atualizar_leilao(client, user):
    response=client.put(
        '/leiloes/11112',
        params={
            'senha':'1613',
            'token':user.token
        },
        json={
            'observacoes':'obs alterado'
        }
    )
    leilao=response.json()
    assert response.status_code==HTTPStatus.NOT_FOUND
 
def testar_ERRO_autenticacao_atualizar_leilao(client, user):
    response=client.put(
        '/leiloes/1111',
        params={
            'senha':'1614',
            'token':user.token
        },
        json={
            'observacoes':'obs alterado'
        }
    )
    leilao=response.json()
    assert response.status_code==HTTPStatus.FORBIDDEN

def testar_leitura_de_leiloes_por_nome_ludopedia(client, user, jogo):
    response=client.get(
        f'/leiloes/{jogo.nome_ludopedia}',
        params={
            'senha':'1613',
            'token':user.token
        }
    )
    assert response.status_code==HTTPStatus.OK
    assert isinstance(response.json(),list), "Não é uma lista"
    assert len(response.json())>0

def testar_ERRO_leitura_de_leiloes_por_nome_ludopedia_senha_errada(client, user, jogo):
    response=client.get(
        f'/leiloes/{jogo.nome_ludopedia}',
        params={
            'senha':'1614',
            'token':user.token
        }
    )
    assert response.status_code==HTTPStatus.FORBIDDEN

def testar_ERRO_leitura_de_leiloes_por_nome_ludopedia_sem_jogo_com_o_nome_ludopedia(client, user, jogo):
    response=client.get(
        f'/leiloes/running_nation',
        params={
            'senha':'1613',
            'token':user.token
        }
    )
    assert response.status_code==HTTPStatus.NOT_FOUND


