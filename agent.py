"""
Finance agent using LangChain and Gemini.
"""
from langchain.agents import AgentExecutor, create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from tools import get_tools
from database import DatabaseManager


class FinanceAgent:
    """Finance agent that can understand and respond to financial queries."""
    
    def __init__(self, google_api_key: str, db: DatabaseManager):
        """Initialize the finance agent."""
        self.db = db
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=google_api_key,
            temperature=0.1
        )
        
        # Create the prompt template for ReAct agent
        self.prompt = PromptTemplate.from_template("""Eres un asistente personal de finanzas. Tu trabajo es ayudar al usuario a:
1. Registrar gastos e ingresos
2. Consultar su saldo actual
3. Analizar sus gastos por período (semana, mes)
4. Ver en qué categorías gasta más dinero
5. Comparar gastos entre meses

Debes ser amable, claro y usar español. Cuando el usuario te diga algo como:
- "Gasté 50 pesos en comida" -> usa add_expense
- "Recibí mi salario de 5000" -> usa add_income  
- "Cuánto dinero tengo" -> usa get_balance
- "Cuánto gasté esta semana" -> usa get_expenses_by_period con period='week'
- "En qué he gastado más" -> usa get_expenses_by_category
- "Compara mis gastos del mes" -> usa compare_months

Siempre confirma las acciones realizadas de forma clara y amigable.

Tienes acceso a las siguientes herramientas:

{tools}

Usa el siguiente formato:

Question: la pregunta o solicitud del usuario
Thought: siempre debes pensar qué hacer
Action: la acción a tomar, debe ser una de [{tool_names}]
Action Input: el input para la acción
Observation: el resultado de la acción
... (este Thought/Action/Action Input/Observation puede repetirse N veces)
Thought: Ahora sé la respuesta final
Final Answer: la respuesta final para el usuario en español

Comienza!

Question: {input}
Thought: {agent_scratchpad}""")
        
    def create_agent_for_user(self, user_id: int) -> AgentExecutor:
        """Create an agent executor for a specific user."""
        tools = get_tools(user_id, self.db)
        agent = create_react_agent(self.llm, tools, self.prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5
        )
        return agent_executor
    
    def process_message(self, user_id: int, message: str) -> str:
        """Process a user message and return a response."""
        try:
            agent_executor = self.create_agent_for_user(user_id)
            response = agent_executor.invoke({"input": message})
            return response.get("output", "Lo siento, no pude procesar tu mensaje.")
        except Exception as e:
            return f"Ocurrió un error: {str(e)}"
