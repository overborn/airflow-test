import ast
import logging
import os
import pendulum
from datetime import timedelta

from airflow.decorators import dag, task
import sys
sys.path.append(os.getcwd())
logger = logging.getLogger(__name__)
logger.info(sys.path)

from api.db import engine, t_parsed_total, t_documents

BATCH_SIZE = 30

logger = logging.getLogger(__name__)


def add_prepared_doc(document_id: int, business_id: int, total: dict, processed: list):
    if total:
        processed.append({
            "document_id": document_id,
            "business_id": business_id,
            "value": int(total["value"]),
            "score": total["score"],
            "ocr_score": total["ocr_score"],
            "bounding_box": total["bounding_box"]
        })


@dag(
    schedule=timedelta(minutes=1),
    start_date=pendulum.today(),
    catchup=False,
    tags=['main'],
    is_paused_upon_creation=False,
)
def process_documents():
    """
    1.  we get latest processed doc_id to know which docs to process.
    this approach doesn't scale well enough, as concurrent workers may get same id
    and start processing same data -> some sort of lock or task params bind to each task is needed
    I assume airflow may have solutions for it, as scheduler may be a good part of handling it.
    2. we get raw docs
    3. we process docs, and create a separate row per non-empty item in 'total' if total is list.
    4. processed data is saved into parsed_total
    """
    @task()
    def get_last_processed_doc_id() -> int:
        # we may speed up this query.
        # if we are sure that insert order is preserved max document_id
        # would match max parsed_total id. this may be huge enhancement as id is indexed
        with engine.connect() as conn:
            max_id = conn.execute("SELECT MAX(document_id) from parsed_total").scalar()
        return max_id or 0

    @task()
    def get_documents(max_id: int) -> list:
        with engine.connect() as conn:
            docs = conn.execute(
                t_documents.select()
                .where(t_documents.c.document_id > max_id)
                .limit(BATCH_SIZE)
            ).fetchall()
        return [dict(d) for d in docs]

    @task()
    def prepare_documents(documents: list):
        processed = []
        for doc in documents:
            document_id = doc['document_id']
            parsed = ast.literal_eval(doc['ml_response'])
            business_id = parsed['business_id']
            total = parsed.get('total')
            if total:
                if isinstance(total, list):
                    for subtotal in total:
                        add_prepared_doc(document_id, business_id, subtotal, processed)
                elif isinstance(total, dict):
                    add_prepared_doc(document_id, business_id, total, processed)
        return processed

    @task()
    def save_documents(docs: list):
        with engine.connect() as conn:
            conn.execute(
                t_parsed_total.insert(),
                docs
            )

    last_doc_id = get_last_processed_doc_id()
    documents = get_documents(last_doc_id)
    if not documents:
        logger.info(f"Nothing to process, last processed: {last_doc_id}")
    prepared_documents = prepare_documents(documents)
    save_documents(prepared_documents)
    logger.info("docs processed")


process_documents()
