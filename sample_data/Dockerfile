FROM python:3.10-bullseye

WORKDIR /mock_data

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD python inject_data.py