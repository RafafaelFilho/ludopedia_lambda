from http import HTTPStatus

def testar_add_usuario_novo(client):
    response=client.post(
        '/usuarios/',
        json={
            'nome': 'Karine',
            'username': 'kazinha',
            'email': 'karine@gmail.com',
            'senha': 'test123'
        }
    )
    assert response.status_code==HTTPStatus.OK
    data=response.json()
    assert data['id']==3
    assert data['nome']=='Karine'
    assert data['email']=='karine@gmail.com'
    assert data['nivel']==1
    assert data['status']==True
    assert len(data['token'])>10
    
def testar_ERRO_username_add_usuario_novo(client):
    response=client.post(
        '/usuarios/',
        json={
            'nome':'Rafael',
            'username':'rafafael',
            'email':'teste@gmail.com',
            'senha':'1613986478'
        }
    )
    assert response.status_code==HTTPStatus.CONFLICT
    assert response.json()=={'detail': 'Username ou Email já existente!'}

def testar_ERRO_username_add_usuario_novo(client):
    response=client.post(
        '/usuarios/',
        json={
            'nome':'Rafael',
            'username':'rafafael3',
            'email':'rafael@gmail.com',
            'senha':'1613986478'
        }
    )
    assert response.status_code==HTTPStatus.CONFLICT
    assert response.json()=={'detail': 'Username ou Email já existente!'}

def testar_get_users(client, user):
    response=client.get(
        '/usuarios/',
        params={
            'senha':'1613',
            'token':user.token
        }
    )
    assert response.status_code==HTTPStatus.OK
    assert len(response.json())>0

def testar_ERRO_get_users(client, user): # testando somente com a senha errada pois todos os testes na função de verifyPermission ja foram realizados
    response=client.get(
        '/usuarios/',
        params={
            'senha':'1614',
            'token':user.token
        }
    )
    assert response.status_code==HTTPStatus.FORBIDDEN

def test_token(client, user):
    response=client.post(
        '/usuarios/token',
        json={
            'nome':user.nome,
            'username':user.username,
            'email':user.email,
            'senha':'1613'
        }
    )
    assert response.status_code==HTTPStatus.OK
    assert response.json()==user.token

def test_ERRO_token_nome_errado(client, user):
    response=client.post(
        '/usuarios/token',
        json={
            'nome':'karine',
            'username':user.username,
            'email':user.email,
            'senha':'1613'
        }
    )
    assert response.status_code==HTTPStatus.FORBIDDEN

def test_ERRO_token_username_errado(client, user):
    response=client.post(
        '/usuarios/token',
        json={
            'nome':user.nome,
            'username':'outro',
            'email':user.email,
            'senha':'1613'
        }
    )
    assert response.status_code==HTTPStatus.FORBIDDEN

def test_ERRO_token_email_errado(client, user):
    response=client.post(
        '/usuarios/token',
        json={
            'nome':user.nome,
            'username':user.username,
            'email':'teste@gmail.com',
            'senha':'1613'
        }
    )
    assert response.status_code==HTTPStatus.FORBIDDEN

def test_ERRO_token_senha_errada(client, user):
    response=client.post(
        '/usuarios/token',
        json={
            'nome':user.nome,
            'username':user.username,
            'email':user.email,
            'senha':'1614'
        }
    )
    assert response.status_code==HTTPStatus.FORBIDDEN
