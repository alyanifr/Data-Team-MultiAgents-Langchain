import os
import pandas as pd
import sqlite3

from pyprojroot import here
from textwrap import dedent
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from langchain_google_genai.llms import GoogleGenerativeAI
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)
from crewai_tools import tool
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

print("Environment variables are loaded:", load_dotenv())

## Load data into database
df = pd.read_csv(here("data/ai_job_market_insights.csv"))
db_path = str(here("data")) + "/sqldb.db"
db_path = f"sqlite:///{db_path}"

engine = create_engine(db_path)
df.to_sql("ai_job_market_insights", engine, if_exists='replace', index=False)
db = SQLDatabase(engine=engine)

## Test db connection
# print(db.dialect)
# print(db.get_usable_table_names())
# result = db.run("SELECT DISTINCT Industry FROM ai_job_market_insights WHERE AI_Adoption_Level = 'High'")
# print(result)

## Configure the llm 
llm = GoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

## Implementing tools for SQL operations
@tool("list_tables")
def list_tables() -> str:
    """List the available tables in the database"""
    return ListSQLDatabaseTool(db=db).invoke("")

# list_tables.run()

@tool("table_schemas")
def table_schemas(tables: str) -> str:
    """
    Input is a comma-separated list of tables, output is the schema and sample rows
    for those tables. Be sure that the tables actually exist by calling 'list_tables' first.
    Example Input: table1, table2, table3
    """
    tool = InfoSQLDatabaseTool(db=db)
    return tool.invoke(tables)

@tool("execute_sql")
def execute_sql(sql_query: str) -> str:
    """Execute a SQL query against the database. Returns the result of the query"""
    return QuerySQLDataBaseTool(db=db).invoke(sql_query)

@tool("check_sql")
def check_sql(sql_query: str) -> str:
    """
    Use this tool to double-check if your query is correct before executing it with 'execute_sql' tool.
    Always use this tool before executing a query with 'execute_sql'
    """
    return QuerySQLCheckerTool(db=db, llm=llm).invoke({"query": sql_query})

## Define agents
sql_dev = Agent(
    role="Senior Database Developer",
    goal="Construct and execute SQL queries based on a request",
    backstory=dedent(
        """
        You are an experienced database engineer who is a master a creating efficient and complex SQL queries.
        You have a deep understanding of how different databases work especially the SQLite database and how
        to optimize queries. 
        Use the 'list_tables' to find the available tables.
        Use the 'table_schemas' to understand the metadata for the table.
        Use 'execute_sql' to check your queries for correctness.
        Use the 'check_sql' to execute queries against the database.
    """
    ),
    llm=llm,
    tools=[list_tables, table_schemas, execute_sql, check_sql],
    allow_delegation=False,
)

data_analyst = Agent(
    role="Senior Data Analyst",
    goal="You receive data from the database developer and analyze it",
    backstory=dedent(
        """
        You have more than 10 years of experienced analyzing datasets using Python and are an expert at it.
        Your work is always based on the provided data and is clear, easy-to-understand, and straightforward.
        You have attention to detail and always uncover hidden insights from the data. 
        Your work is very detailed.
    """
    ),
    llm=llm,
    allow_delegation=False,
)

report_editor = Agent(
    role="Senior Report Editor",
    goal="Write an executive summary type of report based on the work of the analyst",
    backstory=dedent(
        """
        Your writing is well known for its clearness and effectiveness in delivering insights.
        You always summarize long texts into bullet points with an introduction of the analysis at the top of your report 
        and include a conclusion of your summary at end of your report.
    """
    ),
    llm=llm,
    allow_delegation=False,
)

## Creating tasks for each agents and crew to manage the whole process
extract_data = Task(
    description="Extract data that is required for the query {query}",
    expected_output="Database result for the query",
    agent=sql_dev,
)

analyze_data = Task(
    description="Analyze the data from the database and write an analysis for {query}",
    expected_output="Detailed analysis text",
    agent=data_analyst,
    context=[extract_data],
)

write_report = Task(
    description=dedent(
        """
        Write an executive summary of the report from the analysis.
        Open your report with a description of the query {query}.
        Write reports in bullet points of the key findings.
        Include the conclusion of the summary at the end of your report.
    """
    ),
    expected_output="Markdown report",
    agent=report_editor,
    context=[analyze_data]
)

crew = Crew(
    agents=[sql_dev, data_analyst, report_editor],
    tasks=[extract_data, analyze_data, write_report],
    process=Process.sequential,
    verbose=2,
    output_log_file="crew.log",
)

### Add dataviz agent
### Add RAQ framework for summarization of the dataset