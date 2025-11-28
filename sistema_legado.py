from fastapi import FastAPI, Request, Response
import xml.etree.ElementTree as ET

app = FastAPI()

BANCO = {}

@app.post("/legado")
async def legado(request: Request):
    body_bytes = await request.body()
    
    root = ET.fromstring(body_bytes.decode())
    acao = root.tag
    
    if acao == 'cadastro':
        id_c = root.find('id').text
        nome = root.find('nome').text
        cpf_secret = root.find('cpf').text
        
        BANCO[id_c] = {'nome': nome, 'cpf': cpf_secret}
        
        xml_resposta = f"<resp><status>OK</status><msg>Cliente {id_c} salvo</msg></resp>"
        return Response(content=xml_resposta, media_type="application/xml")

    elif acao == 'consulta':
        id_c = root.find('id').text
        cliente = BANCO.get(id_c)
        
        if cliente:
            xml_resposta = f"<cliente><id>{id_c}</id><nome>{cliente['nome']}</nome><cpf>{cliente['cpf']}</cpf></cliente>"
        else:
            xml_resposta = "<erro>Cliente nao existe</erro>"
            
        return Response(content=xml_resposta, media_type="application/xml")

if __name__ == "__main__":
    import uvicorn
    print("Sistema Legado (XML) rodando na porta 5001")
    uvicorn.run(app, host="127.0.0.1", port=5001)