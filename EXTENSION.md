# 🔧 Guía de Extensión

Esta guía te muestra cómo agregar nuevas funcionalidades al bot.

## Ejemplo: Agregar una herramienta de "Establecer Presupuesto"

Vamos a agregar una función que permita a los usuarios establecer un presupuesto mensual y recibir alertas cuando se acerquen al límite.

### Paso 1: Actualizar el modelo de base de datos

Edita `database.py` para agregar una tabla de presupuestos:

```python
class Budget(Base):
    """Model for user budgets."""
    __tablename__ = 'budgets'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    category = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    month = Column(Integer, nullable=False)  # 1-12
    year = Column(Integer, nullable=False)
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category': self.category,
            'amount': self.amount,
            'month': self.month,
            'year': self.year
        }
```

Agregar métodos al DatabaseManager:

```python
def set_budget(self, user_id: int, category: str, amount: float, 
               month: int, year: int) -> Budget:
    """Set a budget for a category."""
    # Verificar si ya existe un presupuesto
    existing = self.session.query(Budget).filter(
        Budget.user_id == user_id,
        Budget.category == category,
        Budget.month == month,
        Budget.year == year
    ).first()
    
    if existing:
        existing.amount = amount
        self.session.commit()
        return existing
    
    budget = Budget(
        user_id=user_id,
        category=category,
        amount=amount,
        month=month,
        year=year
    )
    self.session.add(budget)
    self.session.commit()
    return budget

def get_budget(self, user_id: int, category: str, 
               month: int, year: int) -> Optional[Budget]:
    """Get budget for a category."""
    return self.session.query(Budget).filter(
        Budget.user_id == user_id,
        Budget.category == category,
        Budget.month == month,
        Budget.year == year
    ).first()

def check_budget_status(self, user_id: int, category: str) -> Dict:
    """Check budget status for current month."""
    from datetime import datetime
    now = datetime.now()
    
    budget = self.get_budget(user_id, category, now.month, now.year)
    if not budget:
        return {'has_budget': False}
    
    # Get expenses for this month and category
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    expenses = self.get_transactions(
        user_id=user_id,
        transaction_type='expense',
        start_date=start
    )
    
    spent = sum(t.amount for t in expenses if t.category == category)
    remaining = budget.amount - spent
    percentage = (spent / budget.amount * 100) if budget.amount > 0 else 0
    
    return {
        'has_budget': True,
        'budget': budget.amount,
        'spent': spent,
        'remaining': remaining,
        'percentage': percentage,
        'exceeded': spent > budget.amount
    }
```

### Paso 2: Crear nuevas herramientas

Edita `tools.py` para agregar las nuevas herramientas:

```python
class SetBudgetInput(BaseModel):
    """Input for SetBudget tool."""
    category: str = Field(description="Category to set budget for")
    amount: float = Field(description="Budget amount")

class SetBudgetTool(BaseTool):
    """Tool to set a monthly budget."""
    name = "set_budget"
    description = "Use this tool to set a monthly budget for a category."
    args_schema: Type[BaseModel] = SetBudgetInput
    user_id: int = 0
    db: DatabaseManager = None
    
    def _run(self, category: str, amount: float) -> str:
        """Set a budget."""
        try:
            from datetime import datetime
            now = datetime.now()
            
            budget = self.db.set_budget(
                user_id=self.user_id,
                category=category,
                amount=amount,
                month=now.month,
                year=now.year
            )
            
            return f"Presupuesto establecido: ${amount} para {category} este mes."
        except Exception as e:
            return f"Error al establecer presupuesto: {str(e)}"

class CheckBudgetInput(BaseModel):
    """Input for CheckBudget tool."""
    category: str = Field(description="Category to check budget for")

class CheckBudgetTool(BaseTool):
    """Tool to check budget status."""
    name = "check_budget"
    description = "Use this tool to check budget status for a category."
    args_schema: Type[BaseModel] = CheckBudgetInput
    user_id: int = 0
    db: DatabaseManager = None
    
    def _run(self, category: str) -> str:
        """Check budget status."""
        try:
            status = self.db.check_budget_status(self.user_id, category)
            
            if not status['has_budget']:
                return f"No tienes un presupuesto establecido para {category}."
            
            result = f"Estado del presupuesto para {category}:\n"
            result += f"- Presupuesto: ${status['budget']:.2f}\n"
            result += f"- Gastado: ${status['spent']:.2f} ({status['percentage']:.1f}%)\n"
            result += f"- Restante: ${status['remaining']:.2f}\n"
            
            if status['exceeded']:
                result += "\n⚠️ ¡Has excedido tu presupuesto!"
            elif status['percentage'] > 80:
                result += "\n⚠️ Estás cerca de tu límite."
            elif status['percentage'] > 50:
                result += "\n✓ Vas bien, has gastado la mitad."
            else:
                result += "\n✓ Vas muy bien con tu presupuesto."
            
            return result
        except Exception as e:
            return f"Error al verificar presupuesto: {str(e)}"
```

Actualizar la función `get_tools()`:

```python
def get_tools(user_id: int, db: DatabaseManager) -> list:
    """Get all tools for the agent."""
    tools = [
        AddExpenseTool(user_id=user_id, db=db),
        AddIncomeTool(user_id=user_id, db=db),
        GetBalanceTool(user_id=user_id, db=db),
        GetExpensesByPeriodTool(user_id=user_id, db=db),
        GetExpensesByCategoryTool(user_id=user_id, db=db),
        CompareMonthsTool(user_id=user_id, db=db),
        SetBudgetTool(user_id=user_id, db=db),  # NUEVO
        CheckBudgetTool(user_id=user_id, db=db),  # NUEVO
    ]
    return tools
```

### Paso 3: Actualizar el prompt del agente (opcional)

Edita `agent.py` para agregar información sobre las nuevas herramientas:

```python
self.prompt = PromptTemplate.from_template("""Eres un asistente personal de finanzas...

[prompt existente]

Nuevas funcionalidades:
- "Establece un presupuesto de 1000 para comida" -> usa set_budget
- "Cómo voy con mi presupuesto de comida?" -> usa check_budget

[resto del prompt]
""")
```

### Paso 4: Actualizar la base de datos existente

Cuando ejecutes el bot con los cambios, SQLAlchemy creará automáticamente la nueva tabla `budgets`. Si ya tienes una base de datos existente, puedes:

1. Simplemente ejecutar el bot - SQLAlchemy agregará la tabla
2. O hacer una migración manual si necesitas más control

### Paso 5: Probar la nueva funcionalidad

```python
# En test.py, agregar:

def test_budget():
    """Test budget operations."""
    print("\n🧪 Testing Budget Operations...")
    
    db = DatabaseManager("test_finance.db")
    test_user_id = 12345
    
    try:
        # Set budget
        budget = db.set_budget(test_user_id, "comida", 1000.0, 11, 2024)
        print(f"✓ Budget set: ${budget.amount} for {budget.category}")
        
        # Add some expenses
        db.add_transaction(test_user_id, 'expense', 500.0, 'comida', 'Supermercado')
        
        # Check status
        status = db.check_budget_status(test_user_id, "comida")
        print(f"✓ Budget status checked: {status['percentage']:.1f}% used")
        
        print("\n✅ Budget tests passed!")
        return True
    except Exception as e:
        print(f"\n❌ Budget test failed: {str(e)}")
        return False
    finally:
        db.close()
```

### Paso 6: Usar la nueva funcionalidad

Ahora los usuarios pueden:

```
"Establece un presupuesto de 1000 pesos para comida"
→ "Presupuesto establecido: $1000 para comida este mes."

"Gasté 300 en comida"
→ "Gasto registrado: $300.0 en comida."

"Cómo voy con mi presupuesto de comida?"
→ "Estado del presupuesto para comida:
   - Presupuesto: $1000.00
   - Gastado: $300.00 (30.0%)
   - Restante: $700.00
   
   ✓ Vas muy bien con tu presupuesto."
```

## Otros Ejemplos de Extensiones

### 1. Exportar datos a CSV

```python
class ExportDataTool(BaseTool):
    """Tool to export data to CSV."""
    name = "export_data"
    description = "Export all transactions to a CSV file."
    
    def _run(self) -> str:
        import csv
        from datetime import datetime
        
        transactions = self.db.get_transactions(self.user_id)
        filename = f"export_{self.user_id}_{datetime.now().strftime('%Y%m%d')}.csv"
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Fecha', 'Tipo', 'Monto', 'Categoría', 'Descripción'])
            for t in transactions:
                writer.writerow([
                    t.date.strftime('%Y-%m-%d'),
                    t.type,
                    t.amount,
                    t.category,
                    t.description
                ])
        
        return f"Datos exportados a {filename}"
```

### 2. Recordatorios de gastos recurrentes

```python
class RecurringExpense(Base):
    """Model for recurring expenses."""
    __tablename__ = 'recurring_expenses'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(String(500))
    frequency = Column(String(20))  # 'daily', 'weekly', 'monthly'
    next_date = Column(DateTime, nullable=False)
```

### 3. Análisis con IA más avanzado

```python
class AnalyzeSpendingTool(BaseTool):
    """Tool to get AI insights about spending patterns."""
    name = "analyze_spending"
    description = "Get AI-powered insights about spending patterns."
    
    def _run(self) -> str:
        # Obtener datos
        transactions = self.db.get_transactions(self.user_id)
        summary = self.db.get_summary_by_category(self.user_id, 'expense')
        
        # Crear prompt para Gemini
        prompt = f"""
        Analiza estos gastos y proporciona insights:
        
        Resumen por categoría: {summary}
        Total de transacciones: {len(transactions)}
        
        Proporciona:
        1. Patrones observados
        2. Sugerencias de ahorro
        3. Categorías donde se podría reducir gastos
        """
        
        # Usar Gemini para análisis
        response = self.llm.invoke(prompt)
        return response.content
```

## Mejores Prácticas

1. **Mantén las herramientas simples**: Cada herramienta debe hacer una cosa bien
2. **Valida inputs**: Usa Pydantic models para validar parámetros
3. **Maneja errores**: Siempre usa try/except y retorna mensajes útiles
4. **Documenta bien**: Los `description` de las herramientas ayudan al agente
5. **Prueba todo**: Agrega tests para cada nueva funcionalidad
6. **Actualiza la documentación**: Mantén README.md y GUIA_DE_USO.md actualizados

## Conclusión

El sistema está diseñado para ser extensible. Solo necesitas:
1. Agregar modelos de datos si es necesario
2. Crear nuevas herramientas
3. Registrarlas en `get_tools()`
4. ¡Listo! El agente aprenderá a usarlas automáticamente

El patrón ReAct y Gemini se encargan de entender cuándo usar cada herramienta.
