from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates

router = APIRouter(
    prefix='/page',
    tags=['Pages']
)

templates = Jinja2Templates(directory='templates')


@router.get('/reg')
async def reg(request: Request):
    return templates.TemplateResponse('reg.html', {'request': request})


@router.get('/sign-in')
async def sign_in(request: Request):
    return templates.TemplateResponse('sign_in.html', {'request': request})


@router.get('/main')
async def main_page(request: Request):
    # todo Сделать проверку на роль
    return templates.TemplateResponse('main_student.html', {'request': request})
