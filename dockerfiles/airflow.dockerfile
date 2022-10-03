FROM apache/airflow:2.4.0
COPY requirements.txt /
COPY api /api
RUN pip install --no-cache-dir -r /requirements.txt