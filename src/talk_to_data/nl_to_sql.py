from groq import Groq
from src.utils.config import GROQ_API_KEY
from src.talk_to_data.prompt_templates import NL_TO_SQL_PROMPT, ANSWER_SUMMARY_PROMPT, SCHEMA_DESCRIPTION
from src.utils.logger import get_logger

logger = get_logger(__name__)

client = Groq(api_key=GROQ_API_KEY)

GROQ_MODEL = "llama-3.3-70b-versatile"


def question_to_sql(question: str) -> str:
    """
    Takes a plain English question and returns a SQL query.
    Uses Groq/Llama to do the conversion.
    """
    prompt = NL_TO_SQL_PROMPT.format(
        schema=SCHEMA_DESCRIPTION,
        question=question
    )

    logger.info(f"Converting question to SQL: {question}")

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a SQL expert. Return only raw SQL queries, nothing else."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=300
    )

    sql = response.choices[0].message.content.strip()

    # Clean up any accidental markdown the model might add
    sql = sql.replace("```sql", "").replace("```", "").strip()

    logger.info(f"Generated SQL: {sql}")
    return sql


def results_to_answer(question: str, sql: str, results: str) -> str:
    """
    Takes raw SQL results and converts them to a human-readable answer.
    Uses Groq/Llama to write the business summary.
    """
    prompt = ANSWER_SUMMARY_PROMPT.format(
        question=question,
        sql=sql,
        results=results
    )

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful bank analyst. Give clear, concise business insights."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=200
    )

    answer = response.choices[0].message.content.strip()
    logger.info(f"Generated answer: {answer}")
    return answer