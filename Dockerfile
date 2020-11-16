FROM python:3.7-slim

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./markdown_embed_code /app/markdown_embed_code

ENV PYTHONPATH=/app

WORKDIR /app

CMD ["python", "-m", "markdown_embed_code"]