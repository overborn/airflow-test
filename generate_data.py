import time
import random

from api.db import engine, t_documents


def rand_payload():
    payload = {}
    if random.randint(0, 10) > 5:
        payload = {
            "value": f"{random.randint(0, 1000)}",
            "score": round(random.random(), 2),
            "ocr_score": round(random.random(), 2),
            "bounding_box": [round(random.random(), 2) for i in range(4)],
        }
    return payload


def main():
    while True:
        choices = [
            rand_payload(),
            [rand_payload() for i in range(0, 9)],
        ]
        payload = {"business_id": random.randint(0, 9)}
        fields = ["total", "line_items"]
        for f in fields:
            payload[f] = choices[random.randint(0, 9) % len(fields)]
        print(len(str(payload)), payload)
        with engine.connect() as conn:
            conn.execute(t_documents.insert().values(ml_response=str(payload)))

        time.sleep(3)


if __name__ == '__main__':
    main()

