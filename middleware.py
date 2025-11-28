import requests
import xml.etree.ElementTree as ET
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from cryptography.fernet import Fernet

app = FastAPI(title="Middleware Web Service", description="API REST para o Cliente")

CHAVE = b'gQjWMxR1yO4Y4q3GZ7jK8L9mN0pQ5sT2uV3wX6zA8Bc=' 
cipher = Fernet(CHAVE)

def encriptar(texto):
    return cipher.encrypt(texto.encode()).decode()

def decriptar(texto_cifrado):
    return cipher.decrypt(texto_cifrado.encode()).decode()

def verificar_auth(authorization: str = Header(None)):
    if authorization != "Bearer 12345":
        raise HTTPException(status_code=401, detail="Token invalido ou ausente")
    return authorization

class ClienteInput(BaseModel):
    id: str
    nome: str
    cpf: str

@app.post("/api/clientes", dependencies=[Depends(verificar_auth)])
def criar_cliente(cliente: ClienteInput):
    cpf_encriptado = encriptar(cliente.cpf)
    
    xml_envio = f"""
    <cadastro>
        <id>{cliente.id}</id>
        <nome>{cliente.nome}</nome>
        <cpf>{cpf_encriptado}</cpf>
    </cadastro>
    """
    
    try:
        resp = requests.post("http://127.0.0.1:5001/legado", data=xml_envio)
    except:
        raise HTTPException(status_code=502, detail="Erro ao conectar no Sistema Legado")
        
    root = ET.fromstring(resp.content)
    return {"status": root.find('status').text, "msg": root.find('msg').text}

@app.get("/api/clientes/{id_cliente}", dependencies=[Depends(verificar_auth)])
def consultar_cliente(id_cliente: str):
    xml_envio = f"""
    <consulta>
        <id>{id_cliente}</id>
    </consulta>
    """
    try:
        resposta = requests.post("http://127.0.0.1:5001/legado", data=xml_envio)
    except:
        raise HTTPException(status_code=502, detail="Erro ao conectar no Sistema Legado")

    root = ET.fromstring(resposta.content)
    
    if root.tag == 'erro':
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")
    
    cpf_real = decriptar(root.find('cpf').text)
    
    return {
        "id": root.find('id').text,
        "nome": root.find('nome').text,
        "cpf": cpf_real
    }

if __name__ == "__main__":
    import uvicorn
    print("Middleware rodando na porta 5000")
    uvicorn.run(app, host="127.0.0.1", port=5000)