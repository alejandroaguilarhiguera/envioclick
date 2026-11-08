import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.routes import api_router
from app.utils.exceptions import global_exception_handler
from dotenv import load_dotenv
import os

load_dotenv()

if os.environ.get("ENVIOCLICK_API_KEY") is None:
    raise ValueError("ENVIOCLICK_API_KEY environment variable is not set. Please set it in the .env file.")

if os.environ.get("ENVIOCLICK_USER_AGENT") is None:
    raise ValueError("ENVIOCLICK_USER_AGENT environment variable is not set. Please set it in the .env file.")

if os.environ.get("ENVIOCLICK_URL") is None:
    raise ValueError("ENVIOCLICK_URL environment variable is not set. Please set it in the .env file.")

app = FastAPI(
    title="Envioclick interface",
    version="1.0.0",
)
@app.get("/")
def root():
    return {"message": "Welcome to the Envioclick API"}

# Incluir todas las rutas desde el router centralizado
app.include_router(api_router)

# Exception handlers
app.add_exception_handler(Exception, global_exception_handler)