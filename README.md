# Middleware REST + Sistema Legado XML

## Visão Geral

Este projeto demonstra uma arquitetura onde um **Middleware REST
(JSON)** se comunica com um **Sistema Legado baseado em XML**,
criptografando dados sensíveis (CPF) antes de enviá-los ao legado.

    CLIENTE (Postman/Frontend)
            ⇅ JSON + Bearer Token
    MIDDLEWARE (porta 5000)
            ⇅ XML + Dados criptografados
    SISTEMA LEGADO (porta 5001)

------------------------------------------------------------------------

## 1. Como Executar o Projeto

### Requisitos

-   Python 3.10+
-   Instalar dependências:

``` bash
pip install fastapi uvicorn cryptography requests
```

------------------------------------------------------------------------

### Iniciar o Sistema Legado

``` bash
python sistema_legado.py
```

O servidor rodará em:

    http://127.0.0.1:5001/legado

------------------------------------------------------------------------

### Iniciar o Middleware

``` bash
python middleware.py
```

O servidor rodará em:

    http://127.0.0.1:5000/api/clientes

------------------------------------------------------------------------

## 2. Usando no Postman

Todas as requisições ao Middleware exigem:

    Authorization: Bearer 12345

Configure no Postman em **Headers**:

  Key             Value
  --------------- --------------
  Authorization   Bearer 12345

------------------------------------------------------------------------

## 3. Criar Cliente

### POST

    http://127.0.0.1:5000/api/clientes

#### JSON enviado:

``` json
{
  "id": "1",
  "nome": "João da Silva",
  "cpf": "12345678900"
}
```

#### Resposta:

``` json
{
  "status": "OK",
  "msg": "Cliente 1 salvo"
}
```

------------------------------------------------------------------------

## 4. Consultar Cliente

### GET

    http://127.0.0.1:5000/api/clientes/1

#### Resposta:

``` json
{
  "id": "1",
  "nome": "João da Silva",
  "cpf": "12345678900"
}
```

------------------------------------------------------------------------

## 5. Conversão JSON → XML → JSON

### XML enviado ao legado:

``` xml
<cadastro>
    <id>1</id>
    <nome>João da Silva</nome>
    <cpf>gAAAAABl...</cpf>
</cadastro>
```

------------------------------------------------------------------------

## 6. Resposta XML do Legado

``` xml
<cliente>
    <id>1</id>
    <nome>João da Silva</nome>
    <cpf>gAAAAABl...</cpf>
</cliente>
```

------------------------------------------------------------------------

## 7. Segurança

-   Criptografia simétrica **Fernet/AES**\
-   Middleware exige **Bearer Token**\
-   Legado nunca recebe CPF real

------------------------------------------------------------------------

## 8. Estrutura do Projeto

    .
    │── middleware.py
    │── sistema_legado.py
    │── README.md
