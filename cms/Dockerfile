FROM python

WORKDIR /frontend

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "src/app.py"]
