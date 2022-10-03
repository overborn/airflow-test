import os

from sqlalchemy import (
    create_engine, Column, Integer, text, String, ForeignKey, SmallInteger, Numeric,
    ARRAY, MetaData, Table
)

os.environ['POSTGRES_USER'] = 'airflow'
os.environ['POSTGRES_PASSWORD'] = 'airflow'
os.environ['POSTGRES_DB'] = 'airflow'

conn_string = os.environ.get(
    "AIRFLOW__DATABASE__SQL_ALCHEMY_CONN",
    "postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5433/{POSTGRES_DB}".format(**os.environ)
)
engine = create_engine(conn_string)
metadata = MetaData(bind=engine)

# used sqlacodegen for table generation from sql.
# I am using Sqlalchemy core not ORM to gain processing speed.

t_documents = Table(
    'documents', metadata,
    Column('document_id', Integer, primary_key=True,
           server_default=text("nextval('documents_document_id_seq'::regclass)")),
    Column('ml_response', String(2048)) # may be tuned
)

t_parsed_total = Table(
    'parsed_total', metadata,
    Column('id', Integer, primary_key=True, server_default=text("nextval('parsed_total_id_seq'::regclass)")),
    Column('document_id', ForeignKey('documents.document_id', ondelete='CASCADE')),
    Column('business_id', SmallInteger),
    Column('value', SmallInteger),
    Column('score', Numeric(2, 0)),
    Column('ocr_score', Numeric(2, 0)),
    Column('bounding_box', ARRAY(Numeric(precision=2, scale=0)))
)