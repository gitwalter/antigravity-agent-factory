---
agents:
- none
category: chain
description: SQL generation with LLMs, schema understanding, query optimization, and
  text-to-SQL pipelines
knowledge:
- none
name: managing-database-agents
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Database Agents

SQL generation with LLMs, schema understanding, query optimization, and text-to-SQL pipelines

Build AI agents that interact with databases through natural language, generating and optimizing SQL queries.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Database Connection Setup

```python
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.engine import Engine

def create_db_connection(connection_string: str) -> Engine:
    """Create SQLAlchemy engine."""
    return create_engine(connection_string)

# SQLite example
engine = create_db_connection("sqlite:///example.db")

# PostgreSQL example
# engine = create_db_connection("postgresql://user:pass@localhost/dbname")

# MySQL example
# engine = create_db_connection("mysql+pymysql://user:pass@localhost/dbname")
```

### Step 2: Schema Introspection

```python
from sqlalchemy import inspect
from typing import Dict, List

def get_database_schema(engine: Engine) -> Dict[str, List[Dict]]:
    """Extract database schema information."""
    inspector = inspect(engine)
    schema = {}

    for table_name in inspector.get_table_names():
        columns = []
        for column in inspector.get_columns(table_name):
            columns.append({
                "name": column["name"],
                "type": str(column["type"]),
                "nullable": column["nullable"],
                "default": str(column.get("default", ""))
            })

        # Get foreign keys
        foreign_keys = []
        for fk in inspector.get_foreign_keys(table_name):
            foreign_keys.append({
                "constrained_columns": fk["constrained_columns"],
                "referred_table": fk["referred_table"],
                "referred_columns": fk["referred_columns"]
            })

        # Get indexes
        indexes = []
        for idx in inspector.get_indexes(table_name):
            indexes.append({
                "name": idx["name"],
                "columns": idx["column_names"],
                "unique": idx["unique"]
            })

        schema[table_name] = {
            "columns": columns,
            "foreign_keys": foreign_keys,
            "indexes": indexes
        }

    return schema

def format_schema_for_llm(schema: Dict) -> str:
    """Format schema as text for LLM prompt."""
    lines = []
    for table_name, info in schema.items():
        lines.append(f"\nTable: {table_name}")
        lines.append("Columns:")
        for col in info["columns"]:
            nullable = "NULL" if col["nullable"] else "NOT NULL"
            lines.append(f"  - {col['name']} ({col['type']}) {nullable}")

        if info["foreign_keys"]:
            lines.append("Foreign Keys:")
            for fk in info["foreign_keys"]:
                cols = ", ".join(fk["constrained_columns"])
                ref_cols = ", ".join(fk["referred_columns"])
                lines.append(f"  - {cols} -> {fk['referred_table']}.{ref_cols}")

    return "\n".join(lines)

# Usage
schema = get_database_schema(engine)
schema_text = format_schema_for_llm(schema)
print(schema_text)
```

### Step 3: Basic Text-to-SQL Generation

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

def create_sql_prompt(schema_text: str) -> ChatPromptTemplate:
    """Create prompt template for SQL generation."""
    return ChatPromptTemplate.from_messages([
        ("system", """You are a SQL expert. Generate SQL queries based on the database schema and user questions.

Database Schema:
{schema}

Rules:
- Only generate SELECT queries
- Use proper SQL syntax
- Include JOINs when needed
- Use table aliases for readability
- Return only the SQL query, no explanations"""),
        ("user", "{question}")
    ])

async def generate_sql(question: str, schema_text: str) -> str:
    """Generate SQL query from natural language question."""
    prompt = create_sql_prompt(schema_text)
    chain = prompt | llm | StrOutputParser()

    result = await chain.ainvoke({
        "schema": schema_text,
        "question": question
    })

    # Extract SQL from response (remove markdown code blocks if present)
    sql = result.strip()
    if sql.startswith("```sql"):
        sql = sql[6:]
    if sql.startswith("```"):
        sql = sql[3:]
    if sql.endswith("```"):
        sql = sql[:-3]

    return sql.strip()

# Usage
question = "How many users are in the database?"
sql = await generate_sql(question, schema_text)
print(f"Generated SQL: {sql}")
```

### Step 4: Execute and Validate Queries

```python
from sqlalchemy import text
from typing import Dict, List, Any
import json

async def execute_query(engine: Engine, query: str, limit: int = 100) -> Dict[str, Any]:
    """Execute SQL query safely."""
    # Security: Only allow SELECT queries
    query_upper = query.strip().upper()
    if not query_upper.startswith("SELECT"):
        return {
            "error": "Only SELECT queries are allowed",
            "results": None
        }

    try:
        with engine.connect() as conn:
            # Add LIMIT if not present (safety measure)
            if "LIMIT" not in query_upper:
                query = f"{query.rstrip(';')} LIMIT {limit}"

            result = conn.execute(text(query))
            columns = result.keys()
            rows = [dict(row) for row in result.fetchall()]

            return {
                "error": None,
                "columns": list(columns),
                "rows": rows,
                "row_count": len(rows)
            }
    except Exception as e:
        return {
            "error": str(e),
            "results": None
        }

# Usage
result = await execute_query(engine, sql)
if result["error"]:
    print(f"Error: {result['error']}")
else:
    print(f"Found {result['row_count']} rows")
    print(json.dumps(result["rows"][:5], indent=2))
```

### Step 5: Schema-Aware SQL Generation

```python
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class SQLQuery(BaseModel):
    """Structured SQL query output."""
    query: str = Field(description="The SQL query")
    explanation: str = Field(description="Brief explanation of the query")
    confidence: float = Field(ge=0, le=1, description="Confidence score")

def create_advanced_sql_prompt(schema_text: str, sample_data: Dict[str, List[Dict]] = None) -> ChatPromptTemplate:
    """Create advanced prompt with schema and sample data."""

    sample_text = ""
    if sample_data:
        sample_text = "\n\nSample Data:\n"
        for table, rows in sample_data.items():
            sample_text += f"\n{table}:\n"
            for row in rows[:3]:  # Show first 3 rows
                sample_text += f"  {row}\n"

    return ChatPromptTemplate.from_messages([
        ("system", """You are an expert SQL query generator. You understand database schemas and can generate efficient queries.

Database Schema:
{schema}{samples}

Guidelines:
1. Use appropriate JOINs based on foreign key relationships
2. Use WHERE clauses to filter efficiently
3. Consider indexes when writing queries
4. Use aggregate functions (COUNT, SUM, AVG) when appropriate
5. Group related conditions logically
6. Use table aliases for multi-table queries

Generate SQL queries that are:
- Correct and syntactically valid
- Efficient (use indexes, proper JOINs)
- Readable (clear aliases, formatting)
- Safe (only SELECT queries)"""),
        ("user", "{question}")
    ])

async def generate_schema_aware_sql(
    question: str,
    schema_text: str,
    sample_data: Dict[str, List[Dict]] = None
) -> SQLQuery:
    """Generate SQL with schema awareness."""
    from langchain_core.output_parsers import PydanticOutputParser

    prompt = create_advanced_sql_prompt(schema_text, sample_data)
    parser = PydanticOutputParser(pydantic_object=SQLQuery)

    chain = prompt.partial(format_instructions=parser.get_format_instructions()) | llm | parser

    result = await chain.ainvoke({
        "schema": schema_text,
        "samples": sample_text if sample_data else "",
        "question": question
    })

    return result

# Usage
question = "Show me the top 5 customers by total order value"
sql_result = await generate_schema_aware_sql(question, schema_text)
print(f"Query: {sql_result.query}")
print(f"Confidence: {sql_result.confidence}")
```

### Step 6: Query Optimization Patterns

```python
from langchain_core.prompts import ChatPromptTemplate

def create_optimization_prompt(original_query: str, schema_text: str, execution_plan: str = None) -> ChatPromptTemplate:
    """Create prompt for query optimization."""

    plan_text = f"\n\nExecution Plan:\n{execution_plan}" if execution_plan else ""

    return ChatPromptTemplate.from_messages([
        ("system", """You are a SQL query optimizer. Analyze queries and suggest improvements.

Database Schema:
{schema}{plan}

Optimization Goals:
1. Reduce execution time
2. Minimize data scanned
3. Use indexes effectively
4. Avoid unnecessary JOINs
5. Use appropriate WHERE clause order
6. Consider query rewriting opportunities

Provide optimized SQL query with explanation of improvements."""),
        ("user", "Optimize this query:\n{query}")
    ])

async def optimize_query(
    query: str,
    schema_text: str,
    execution_plan: str = None
) -> Dict[str, str]:
    """Optimize a SQL query."""
    prompt = create_optimization_prompt(query, schema_text, execution_plan)
    chain = prompt | llm | StrOutputParser()

    result = await chain.ainvoke({
        "schema": schema_text,
        "plan": execution_plan or "",
        "query": query
    })

    # Parse optimized query and explanation
    lines = result.split("\n")
    optimized_query = ""
    explanation = ""
    in_query = False

    for line in lines:
        if "```sql" in line or "```" in line:
            in_query = not in_query
            continue
        if in_query:
            optimized_query += line + "\n"
        else:
            explanation += line + "\n"

    return {
        "original": query,
        "optimized": optimized_query.strip(),
        "explanation": explanation.strip()
    }

# Usage
original_sql = "SELECT * FROM users WHERE age > 25 AND name LIKE '%John%'"
optimized = await optimize_query(original_sql, schema_text)
print(f"Optimized: {optimized['optimized']}")
```

### Step 7: Complete Text-to-SQL Pipeline

```python
from langchain_core.runnables import RunnablePassthrough
from typing import Dict, Any

class DatabaseAgent:
    """Complete database agent with text-to-SQL pipeline."""

    def __init__(self, engine: Engine, llm):
        self.engine = engine
        self.llm = llm
        self.schema = get_database_schema(engine)
        self.schema_text = format_schema_for_llm(self.schema)

    async def query(self, question: str) -> Dict[str, Any]:
        """Complete pipeline: question -> SQL -> results."""

        # Step 1: Generate SQL
        sql_result = await generate_schema_aware_sql(
            question,
            self.schema_text
        )

        # Step 2: Execute query
        query_result = await execute_query(self.engine, sql_result.query)

        # Step 3: Format response
        if query_result["error"]:
            return {
                "success": False,
                "error": query_result["error"],
                "generated_sql": sql_result.query,
                "confidence": sql_result.confidence
            }

        # Step 4: Generate natural language summary
        summary = await self._generate_summary(
            question,
            sql_result.query,
            query_result
        )

        return {
            "success": True,
            "question": question,
            "sql": sql_result.query,
            "explanation": sql_result.explanation,
            "confidence": sql_result.confidence,
            "results": query_result["rows"],
            "row_count": query_result["row_count"],
            "summary": summary
        }

    async def _generate_summary(
        self,
        question: str,
        sql: str,
        results: Dict[str, Any]
    ) -> str:
        """Generate natural language summary of results."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Summarize database query results in natural language."),
            ("user", """Question: {question}
SQL: {sql}
Results: {results}
Row count: {count}

Provide a concise summary answering the original question.""")
        ])

        chain = prompt | self.llm | StrOutputParser()
        summary = await chain.ainvoke({
            "question": question,
            "sql": sql,
            "results": json.dumps(results["rows"][:10], indent=2),
            "count": results["row_count"]
        })

        return summary

# Usage
agent = DatabaseAgent(engine, llm)
result = await agent.query("What are the top 10 products by sales?")
print(result["summary"])
```

## Query Patterns

| Pattern | Example |
|---------|---------|
| Simple SELECT | "Get all users" |
| Filtered SELECT | "Users older than 30" |
| Aggregation | "Total sales by month" |
| JOINs | "Orders with customer names" |
| Subqueries | "Customers who placed orders" |
| Grouping | "Average order value by category" |

## Best Practices

- Always validate and sanitize generated SQL
- Restrict to SELECT queries only
- Use schema introspection for accurate queries
- Add LIMIT clauses to prevent large result sets
- Implement query result caching
- Log all generated queries for auditing
- Provide confidence scores for generated queries
- Handle SQL errors gracefully
- Use parameterized queries when possible
- Consider query optimization suggestions

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| No SQL validation | Validate syntax before execution |
| Allowing DML/DDL | Restrict to SELECT only |
| No LIMIT clauses | Always add LIMIT for safety |
| Ignoring schema | Use schema introspection |
| No error handling | Wrap execution in try/except |
| Hardcoded queries | Generate dynamically from schema |
| No query logging | Log all queries for debugging |
| Ignoring indexes | Consider indexes in optimization |

## Related

- Knowledge: `{directories.knowledge}/data-pipeline-patterns.json`
- Skill: `mcp-integration`
- Skill: `using-langchain`
- Skill: `tool-usage`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
