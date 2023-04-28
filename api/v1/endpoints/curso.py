from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlmodel.sql.expression import Select, SelectOfScalar
from models.curso_model import CursoModel
from core.deps import get_session

# Bypass warning sqlmodel select
SelectOfScalar.inherit_cache = True
Select.inherit_cache = True


router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CursoModel)
async def post_curso(curso: CursoModel, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(titulo=curso.titulo, aulas=curso.aulas, horas = curso.horas)
    db.add(novo_curso)
    await db.commit()
    return novo_curso

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[CursoModel])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos: List[CursoModel] = result.scalars().all()
        return cursos 
    
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=List[CursoModel])
async def get_curso(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).where(CursoModel.id == id)
        result = await session.execute(query)
        curso: List[CursoModel] = result.scalars().all()
        if curso:
            return curso 
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não existe')
    
@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=CursoModel)
async def put_cursos(id: int, body: CursoModel,db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).where(CursoModel.id == id)
        result = await session.execute(query)
        curso: CursoModel = result.scalars().all()        
        if curso:
            curso[0].horas = body.horas
            curso[0].aulas = body.aulas
            curso[0].titulo = body.titulo
            await session.commit()
            return curso[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não existe')
        

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_cursos(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).where(CursoModel.id == id)
        result = await session.execute(query)
        curso: CursoModel = result.scalar_one_or_none()
        if curso:
            print(curso)
            await session.delete(curso)
            await session.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não existe')
        
        
        
