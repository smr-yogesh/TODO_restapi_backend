FROM python:3.9.13

WORKDIR /usr/src/app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
COPY . .

# defining env vars
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=true
ENV FLASK_ENV=development

CMD ["sh", "-c", "sleep 10 \ 
    && python -m flask run --host=0.0.0.0"]