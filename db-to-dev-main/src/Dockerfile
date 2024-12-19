FROM python:3.12.3
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
WORKDIR /app
COPY . /app
ENTRYPOINT [ "python3", "postgre_index.py" ]