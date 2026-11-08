import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app  # Asegúrate de importar tu instancia de FastAPI correctamente

@pytest.fixture
async def client():
    # Usamos ASGITransport para conectar httpx directamente con tu app de FastAPI de forma asíncrona
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:
        yield ac