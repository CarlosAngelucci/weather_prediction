from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
def get_status():
    return {"status": "API is running"}

@router.get("/data")
def get_data():
    # Lógica para retornar dados para o frontend
    return {"data": "Exemplo de dado"}