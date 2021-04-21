FROM python:3.8-slim
RUN useradd --create-home --shell /bin/bash pentest
WORKDIR /home/pentest

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

USER pentest
COPY . .

CMD ["bash"]