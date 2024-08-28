<h1 align="center">AI-Powered Data Team</h1>

<h5 align="center">Keywords: Large Language Model | Google Generative AI | Multi-Agents Langchain | CrewAI</h5>

## Project Description:

This project leveraged the power of Generative AI to create an automated database manipulation, allowing for efficient data querying and retrieval. These enhanced database operations are made possible by building intelligent agents that understand natural language, construct accurate SQL queries, analyze results and generate clear and concise executive summaries of the findings. One of the key benefits of this project is reducing the time and effort required to perform repetitive and complex tasks as writing SQL queries can be challenging and requires a deep understanding of its syntax and the underlying database structure.

## Key Technologies:

Combining these technologies, an advanced SQL agent capable of handling intricate databse operations and generating insightful reports can be created.

💡 CrewAI 
- A powerful framework for defining and managing agents that perform specific tasks in a coordinated manner.
- Provides the tools necessary to create complex workflows involving multiple agents.

💡 GoogleGenerativeAI 
- The GoogleGenerativeAI class is the primary interface for interacting with Google’s Gemini LLMs. It allows users to generate text using a specified Gemini model.
- [More info](https://python.langchain.com/v0.2/api_reference/google_genai/index.html)

## Multi-Agents Framework:

🤖 SQL Developer
- Construct and executes SQL queries based on the given input.
- This agent utilizes multiple defined tools to list the available tables, get the table schemas, execute queries and check for query correctness.

🤖 Data Analyst
- Analyze data extracted by the SQL developer.
- Provide detailed insights and in-depth analysis based on the query.

🤖 Report Generator
- This agent will wrap everything up in a well-written and straightforward executive report based on the insights by the Data Analyst.
- The executive summaries should be bullet points of the key findings and would not exceed 100 words.

## Future Enhancements:

1. Include integration with other databases such as MySQL, PostgreSQL or NoSQL databases.
2. Allow data from different sources such as csv and xlsx files.
3. Implement real-time data processing capabilities to handle streaming data and provide instant insights.
4. Graphs/Charts generator as part of the reports generated to provide graphical insights of the data query.
5. Optimize agents for scalability to handle larger datasets and more complex quieries efficiently.
