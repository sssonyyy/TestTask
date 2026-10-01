
import re

from fastapi import FastAPI, Query, HTTPException
from sqlalchemy import text

from database import engine


app = FastAPI()


def normalize_filter(filter_expression: str) -> str:
    columns = {
        "age": '"Age"',
        "sex": '"Sex"',
        "weight": '"Weight"',
        "respondent": "respondent",
    }
    pattern = r"(?<![\"'\w])(age|sex|weight|respondent)(?![\"'\w])"
    return re.sub(
        pattern,
        lambda match: columns[match.group(1).lower()],
        filter_expression,
        flags=re.IGNORECASE,
    )


@app.get("/getPercent")
def get_percent(
    audience1: str = Query(...),
    audience2: str = Query(...)
):
    audience1 = normalize_filter(audience1)
    audience2 = normalize_filter(audience2)

    query = text(f"""
        with audience_1 as (
            select
                respondent,
                avg("Weight") as avg_weight
            from respondents
            where {audience1}
            group by respondent
        ),

        audience_2 as (
            select distinct
                respondent
            from respondents
            where {audience2}
        )

        select
            coalesce(
                sum(a1.avg_weight)
                / nullif(
                    (select sum(avg_weight) from audience_1),
                    0
                ),
                0
            ) as percent
        from audience_1 a1
        inner join audience_2 a2
            on a1.respondent = a2.respondent
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
