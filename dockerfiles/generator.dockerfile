FROM python:3.7
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./api/db.py /api/
COPY generate_data.py .
CMD ["python", "-m", "generate_data"]