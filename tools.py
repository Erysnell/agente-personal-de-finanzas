"""
LangChain tools for the finance agent.
"""
from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from database import DatabaseManager
import json


class AddExpenseInput(BaseModel):
    """Input for AddExpense tool."""
    amount: float = Field(description="The amount of money spent")
    category: str = Field(description="The category of the expense (e.g., food, transport, entertainment)")
    description: str = Field(default="", description="Optional description of the expense")


class AddExpenseTool(BaseTool):
    """Tool to add an expense."""
    name = "add_expense"
    description = "Use this tool to register a new expense. You need the amount and category."
    args_schema: Type[BaseModel] = AddExpenseInput
    user_id: int = 0
    db: DatabaseManager = None
    
    def _run(self, amount: float, category: str, description: str = "") -> str:
        """Add an expense to the database."""
        try:
            transaction = self.db.add_transaction(
                user_id=self.user_id,
                transaction_type='expense',
                amount=amount,
                category=category,
                description=description
            )
            return f"Gasto registrado: ${amount} en {category}. {description if description else ''}"
        except Exception as e:
            return f"Error al registrar el gasto: {str(e)}"


class AddIncomeInput(BaseModel):
    """Input for AddIncome tool."""
    amount: float = Field(description="The amount of money received")
    category: str = Field(description="The category of the income (e.g., salary, freelance, investment)")
    description: str = Field(default="", description="Optional description of the income")


class AddIncomeTool(BaseTool):
    """Tool to add an income."""
    name = "add_income"
    description = "Use this tool to register a new income. You need the amount and category."
    args_schema: Type[BaseModel] = AddIncomeInput
    user_id: int = 0
    db: DatabaseManager = None
    
    def _run(self, amount: float, category: str, description: str = "") -> str:
        """Add an income to the database."""
        try:
            transaction = self.db.add_transaction(
                user_id=self.user_id,
                transaction_type='income',
                amount=amount,
                category=category,
                description=description
            )
            return f"Ingreso registrado: ${amount} en {category}. {description if description else ''}"
        except Exception as e:
            return f"Error al registrar el ingreso: {str(e)}"


class GetBalanceInput(BaseModel):
    """Input for GetBalance tool."""
    pass


class GetBalanceTool(BaseTool):
    """Tool to get current balance."""
    name = "get_balance"
    description = "Use this tool to get the current balance (total income - total expenses)."
    args_schema: Type[BaseModel] = GetBalanceInput
    user_id: int = 0
    db: DatabaseManager = None
    
    def _run(self) -> str:
        """Get current balance."""
        try:
            balance = self.db.get_balance(self.user_id)
            return f"Tu saldo actual es: ${balance:.2f}"
        except Exception as e:
            return f"Error al obtener el saldo: {str(e)}"


class GetExpensesByPeriodInput(BaseModel):
    """Input for GetExpensesByPeriod tool."""
    period: str = Field(description="Period to analyze: 'week', 'month', or 'all'")


class GetExpensesByPeriodTool(BaseTool):
    """Tool to get expenses by period."""
    name = "get_expenses_by_period"
    description = "Use this tool to get total expenses for a specific period (week, month, or all)."
    args_schema: Type[BaseModel] = GetExpensesByPeriodInput
    user_id: int = 0
    db: DatabaseManager = None
    
    def _run(self, period: str = "all") -> str:
        """Get expenses for a specific period."""
        try:
            end_date = datetime.now()
            start_date = None
            
            if period == "week":
                start_date = end_date - timedelta(days=7)
                period_text = "esta semana"
            elif period == "month":
                start_date = end_date - timedelta(days=30)
                period_text = "este mes"
            else:
                period_text = "en total"
            
            transactions = self.db.get_transactions(
                user_id=self.user_id,
                transaction_type='expense',
                start_date=start_date,
                end_date=end_date
            )
            
            total = sum(t.amount for t in transactions)
            return f"Has gastado ${total:.2f} {period_text} ({len(transactions)} transacciones)."
        except Exception as e:
            return f"Error al obtener gastos: {str(e)}"


class GetExpensesByCategoryInput(BaseModel):
    """Input for GetExpensesByCategory tool."""
    period: str = Field(default="all", description="Period to analyze: 'week', 'month', or 'all'")


class GetExpensesByCategoryTool(BaseTool):
    """Tool to get expenses grouped by category."""
    name = "get_expenses_by_category"
    description = "Use this tool to see how much was spent in each category for a specific period."
    args_schema: Type[BaseModel] = GetExpensesByCategoryInput
    user_id: int = 0
    db: DatabaseManager = None
    
    def _run(self, period: str = "all") -> str:
        """Get expenses grouped by category."""
        try:
            end_date = datetime.now()
            start_date = None
            
            if period == "week":
                start_date = end_date - timedelta(days=7)
                period_text = "esta semana"
            elif period == "month":
                start_date = end_date - timedelta(days=30)
                period_text = "este mes"
            else:
                period_text = "en total"
            
            summary = self.db.get_summary_by_category(
                user_id=self.user_id,
                transaction_type='expense',
                start_date=start_date,
                end_date=end_date
            )
            
            if not summary:
                return f"No hay gastos registrados {period_text}."
            
            # Sort by amount descending
            sorted_summary = sorted(summary.items(), key=lambda x: x[1], reverse=True)
            
            result = f"Gastos por categoría {period_text}:\n"
            for category, amount in sorted_summary:
                result += f"- {category}: ${amount:.2f}\n"
            
            total = sum(summary.values())
            result += f"\nTotal: ${total:.2f}"
            
            return result
        except Exception as e:
            return f"Error al obtener gastos por categoría: {str(e)}"


class CompareMonthsInput(BaseModel):
    """Input for CompareMonths tool."""
    pass


class CompareMonthsTool(BaseTool):
    """Tool to compare expenses between months."""
    name = "compare_months"
    description = "Use this tool to compare expenses between the current month and the previous month."
    args_schema: Type[BaseModel] = CompareMonthsInput
    user_id: int = 0
    db: DatabaseManager = None
    
    def _run(self) -> str:
        """Compare expenses between current and previous month."""
        try:
            now = datetime.now()
            
            # Current month
            current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            current_transactions = self.db.get_transactions(
                user_id=self.user_id,
                transaction_type='expense',
                start_date=current_month_start,
                end_date=now
            )
            current_total = sum(t.amount for t in current_transactions)
            
            # Previous month
            if current_month_start.month == 1:
                prev_month_start = current_month_start.replace(year=current_month_start.year - 1, month=12)
            else:
                prev_month_start = current_month_start.replace(month=current_month_start.month - 1)
            
            prev_transactions = self.db.get_transactions(
                user_id=self.user_id,
                transaction_type='expense',
                start_date=prev_month_start,
                end_date=current_month_start
            )
            prev_total = sum(t.amount for t in prev_transactions)
            
            difference = current_total - prev_total
            percentage = (difference / prev_total * 100) if prev_total > 0 else 0
            
            result = f"Comparación de gastos:\n"
            result += f"- Mes anterior: ${prev_total:.2f}\n"
            result += f"- Mes actual: ${current_total:.2f}\n"
            result += f"- Diferencia: ${abs(difference):.2f} "
            
            if difference > 0:
                result += f"(+{percentage:.1f}% más que el mes anterior)"
            elif difference < 0:
                result += f"(-{abs(percentage):.1f}% menos que el mes anterior)"
            else:
                result += "(igual que el mes anterior)"
            
            return result
        except Exception as e:
            return f"Error al comparar meses: {str(e)}"


def get_tools(user_id: int, db: DatabaseManager) -> list:
    """Get all tools for the agent."""
    tools = [
        AddExpenseTool(user_id=user_id, db=db),
        AddIncomeTool(user_id=user_id, db=db),
        GetBalanceTool(user_id=user_id, db=db),
        GetExpensesByPeriodTool(user_id=user_id, db=db),
        GetExpensesByCategoryTool(user_id=user_id, db=db),
        CompareMonthsTool(user_id=user_id, db=db),
    ]
    return tools
