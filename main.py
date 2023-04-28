from fastapi import FastAPI
from api.v1.api import api_router 
from core.configs import settings

app = FastAPI(title='API Cursos Models')
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', port=8080, log_level='info', reload=True)