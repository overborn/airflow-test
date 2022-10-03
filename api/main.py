from fastapi import FastAPI
from sqlalchemy import func, select
from api.db import engine, t_parsed_total
app = FastAPI()


@app.get('/api/status')
def status():
    return {'message': 'ok'}


@app.get('/api/business/{business_id}')
def get_business_stats(
    business_id: int
):
    with engine.connect() as conn:
        data = conn.execute(
            select(
                func.sum(t_parsed_total.c.value).label('sum_value'),
                func.round(func.avg(t_parsed_total.c.score), 2).label('avg_score'),
                func.round(func.avg(t_parsed_total.c.ocr_score), 2).label('avg_ocr_score'),
                func.round(func.avg(t_parsed_total.c.bounding_box[1]), 2).label('avg_bounding_box_1'),
                func.round(func.avg(t_parsed_total.c.bounding_box[2]), 2).label('avg_bounding_box_2'),
                func.round(func.avg(t_parsed_total.c.bounding_box[3]), 2).label('avg_bounding_box_3'),
                func.round(func.avg(t_parsed_total.c.bounding_box[4]), 2).label('avg_bounding_box_4'),
            ).group_by(
                t_parsed_total.c.business_id
            ).having(
                business_id == t_parsed_total.c.business_id
            )
        ).fetchone()

    return data
