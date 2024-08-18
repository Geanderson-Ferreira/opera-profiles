from fastapi import FastAPI, Header, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from routine import get_data
from src.check_token import check_token

app = FastAPI()

class Reserva(BaseModel):
    id: int
    nome: str
    data_checkin: str
    data_checkout: str

# Exemplo de tokens e hotéis válidos
valid_tokens = {"your_super_long_token_here"}
valid_hotels = {123, 456, 789}

@app.get("/reservas/")
async def get_reservations_by_rules(
    hotel_id: str = Query(..., description="ID do hotel"),
    authorization: Optional[str] = Header(None, alias="Authorization")
):
    
    # Verificar o token
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token ausente ou inválido")
    

    token = authorization[len("Bearer "):]

    checker = check_token(hotel_id, token)

    if not checker['token_is_valid']:
        raise HTTPException(status_code=401, detail=checker['info'])
        

    return get_data(hotel_id, token)

# Para testes e execução local, use o seguinte código:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
