from typing import Annotated
from infra.postgres import PostgresManager
from dotenv import load_dotenv
import os
import openai
from pydantic import BaseModel

load_dotenv(override=True)

db_connection = PostgresManager()
db_connection.connect_with_url(os.getenv("DB_URI"))


class RunQueryParams(BaseModel):
    query: str

run_query_params = openai.pydantic_function_tool(RunQueryParams, name="run_query", description="Run sql query")
def run_query(query):
    print("🔍 running query ...")
    return db_connection.run_sql(query)

def get_schema() -> Annotated[str, "The where schema of the database"]:
    """
    Get the schema of the database
    """
    print("🔍 getting schema ...")
    return db_connection.get_table_definitions_for_prompt()