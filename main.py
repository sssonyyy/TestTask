from fastapi import FastAPI, Query, HTTPException
from sqlalchemy import text

from database import engine


app = FastAPI()


@app.get("/getPercent")
def get_percent(
    audience1: str = Query(...),
    audience2: str = Query(...)
):
    query = text(f"""
        WITH audience_1 AS (
            SELECT
                respondent,
                AVG("Weight") AS avg_weight
            FROM respondents
            WHERE {audience1}
            GROUP BY respondent
        ),

        audience_2 AS (
            SELECT DISTINCT
                respondent
            FROM respondents
            WHERE {audience2}
        )

        SELECT
            COALESCE(
                SUM(a1.avg_weight)
                / NULLIF(
                    (SELECT SUM(avg_weight) FROM audience_1),
                    0
                ),
                0
            ) AS percent
        FROM audience_1 a1
        INNER JOIN audience_2 a2
            ON a1.respondent = a2.respondent
    """)

    try:
        with engine.connect() as connection:
            result = connection.execute(query).scalar()

        return {
            "percent": float(result)
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )