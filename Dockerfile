FROM pytorch/pytorch:latest

WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install -r requirements.txt -v

COPY */ /app/
CMD bash
#CMD "/opt/conda/bin/streamlit run /app/main.py --server.port 8080"
