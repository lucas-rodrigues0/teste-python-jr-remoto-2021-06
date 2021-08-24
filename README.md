# API REST MagPy

---

### sumário
  - [Instruções](#instruções)
  - [Instalação](#instalação)
  - [Testes existentes](#testes-existentes)
  - [Considerações finais](#considerações-finais)

---

## Instruções

MagPy é uma API REST que gerencia uma coleção de projetos. <br >
Cada projeto tem um nome e uma lista de pacotes. <br >
Cada pacote tem um nome e uma versão.

A API valida o projeto cadastrado: todos os pacotes informados devem
estar cadastrados na Api públca [PyPI](https://pypi.org/). 

Quando o pacote vem apenas com o nome, a API vai acrescentar 
a última versão publicada no [PyPI](https://pypi.org/).

Abaixo, alguns exemplos de chamadas que podem ser feitas nessa API:

```
POST /api/projects
{
    "name": "titan",
    "packages": [
        {"name": "Django"},
        {"name": "graphene", "version": "2.0"}
    ]
}
```
O código HTTP de retorno: 201 <br >
O corpo na resposta é:
```
{
    "name": "titan",
    "packages": [
        {"name": "Django", "version": "3.2.5"},  // Usou a versão mais recente
        {"name": "graphene", "version": "2.0"}   // Manteve a versão especificada
    ]
}
```

Caso não seja informado os campos "name" ou "packages" um erro será retornado com o código HTTP 400 e a seguinte menssagem:
```
{
    "<field>":["This field is required."]
}
```

Se um dos pacotes informados não existir, ou uma das versões especificadas for
inválida, um erro será retornado com o código HTTP 400 e a seguinte menssagem:
```
{
    "error":"One or more packages doesn't exist"
}
```

Para visitar projetos previamente cadastrados, usar o
nome na URL:
```
GET /api/projects/titan
{
    "name": "titan",
    "packages": [
        {"name": "Django", "version": "3.2.5"},
        {"name": "graphene", "version": "2.0"}
    ]
}
```

E deletar projetos pelo nome:
```
DELETE /api/projects/titan
```

## Instalação

clone o repositório e em seu ambiente virtual instale as dependencias necessárias pelo arquivo `requirement.txt`.

No ambiente virtual rode o seguinte comando:
``` 
  $ python pip install -r requirement.txt
```
Depois da instalação crie seu super usuario para a sessão de admin do Django com o comando:
``` 
  $ python manage.py createsuperuser
```
Faça a migration e suba a aplicação para o servidor com o comando:
``` 
  $ python manage.py migrate
  $ python manage.py runserver
```
e acesse pelo browser a interface pela url, substituindo o `<port>` pela porta em que estiver servindo.
- para acessar a sessão admin: `http://127.0.0.1:<port>/admin`
- para acessar a Api: `http://127.0.0.1:<port>/api/projects/`

## Testes existentes

Existem dois tipos de testes na aplicação. Os testes de unidade feitos em python unittest, que pode ser rodado sem 
a nessecidade de subir a aplicação para o servidor.

Execute o comando:
``` 
  $ python manage.py test
```

E o teste de carga feito com o [K6](https://k6.io/) que precisa subir a aplicação para rodar o teste.

Execute o comando substituindo o `<port>` pela porta em que estiver servindo:
``` 
  $ python manage.py runserver
  $ k6 run -e API_BASE='http://localhost:<port>/' tests-open.js
```

____________________________________________________________________
## Considerações finais

Esse projeto fez parte de um desafio técnico em que tive que implementar apenas parte das funcionalidades, já tendo uma estrutura pronta e o teste de carga implementados.

E apesar de ser o meu primeiro contato com o Django consegui aprender bastante.

Algumas sugestões para escalabilidade seriam a implementação de uma função para atualizar o projeto registrado e outra para ver os detalhes de cada pacote, que poderiam de forma simples acrescentar mais valor a Api.

Qualquer dúvida pode entrar em contato.

### Tecnologias

- Python 3.9.5
- Django 3.2
- Django Rest Framework 3.12.0


Deploy no Heroku. Link de acesso: <br >
[magpy_heroku](https://magpy-api-rest-0705.herokuapp.com/api/projects/)
