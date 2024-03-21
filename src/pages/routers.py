from pprint import pprint

from fastapi import APIRouter, Request, Form
from pydantic import EmailStr
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

import requests

from typing import Annotated

from config import SERVER_HOST, SERVER_PORT, SERVER_PROTOCOL
from src.pages.schemas import UserRegistrationSchema

router = APIRouter(
    prefix='/page',
    tags=['Pages']
)

templates = Jinja2Templates(directory='templates')


@router.get('/reg')
async def reg(request: Request):
    return templates.TemplateResponse('reg.html', {'request': request})


@router.post('/reg')
async def reg_post(data: UserRegistrationSchema):
    body = data.dict()

    pprint({'body': body})

    role = body.pop('role')
    body.update({'role_id': 1 if role else 0})

    pprint({'body': body})

    headers = {'Content-Type': 'application/json'}

    res = requests.post(f'{SERVER_PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}/api/auth/register', data=body, headers=headers)
    pprint({"res": res.status_code})
    return {}


@router.get('/sign-in')
async def sign_in(request: Request):
    return templates.TemplateResponse('sign_in.html', {'request': request})


@router.get('/main')
async def main_page(request: Request):
    # todo Сделать проверку на роль
    return templates.TemplateResponse('main_student.html', {'request': request})
