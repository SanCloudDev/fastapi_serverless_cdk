FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /code

COPY ./preferred_item_service/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./preferred_item_service /code/ 

CMD ["uvicorn", "preferred_item_service.api.main:app", "--host", "0.0.0.0", "--port", "80"]