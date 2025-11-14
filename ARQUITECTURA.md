# 🏗️ Arquitectura del Sistema

## Diagrama de Flujo

```
┌─────────────────────────────────────────────────────────────────┐
│                          USUARIO                                 │
│                     (Telegram App)                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ "Gasté 50 pesos en comida"
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BOT DE TELEGRAM                             │
│                        (bot.py)                                  │
│  - Recibe mensajes                                               │
│  - Maneja comandos (/start, /help, /balance)                   │
│  - Envía respuestas                                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ message_text + user_id
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AGENTE DE FINANZAS                            │
│                        (agent.py)                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │         Google Gemini (gemini-pro)                        │  │
│  │  - Entiende lenguaje natural                              │  │
│  │  - Identifica intención del usuario                       │  │
│  │  - Extrae información (monto, categoría)                  │  │
│  └────────────────────┬──────────────────────────────────────┘  │
│                       │                                          │
│                       │ ReAct Pattern                            │
│                       │ (Thought → Action → Observation)         │
│                       ▼                                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Selección de Herramienta                     │  │
│  │  - add_expense                                            │  │
│  │  - add_income                                             │  │
│  │  - get_balance                                            │  │
│  │  - get_expenses_by_period                                 │  │
│  │  - get_expenses_by_category                               │  │
│  │  - compare_months                                         │  │
│  └────────────────────┬──────────────────────────────────────┘  │
└────────────────────────┼────────────────────────────────────────┘
                         │
                         │ tool_call(params)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   HERRAMIENTAS (TOOLS)                           │
│                        (tools.py)                                │
│  - Ejecutan acciones específicas                                 │
│  - Validan parámetros                                            │
│  - Interactúan con la base de datos                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ database_operation
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  BASE DE DATOS                                   │
│                    (database.py)                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              SQLite (finance.db)                          │  │
│  │                                                           │  │
│  │  Tabla: transactions                                      │  │
│  │  ┌──────────────────────────────────────────────────┐    │  │
│  │  │ id | user_id | type | amount | category | ...    │    │  │
│  │  ├──────────────────────────────────────────────────┤    │  │
│  │  │ 1  | 12345   | exp  | 50.0   | comida   | ...    │    │  │
│  │  │ 2  | 12345   | inc  | 5000   | salario  | ...    │    │  │
│  │  │ 3  | 67890   | exp  | 100    | ropa     | ...    │    │  │
│  │  └──────────────────────────────────────────────────┘    │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Flujo de Datos Detallado

### 1. Agregar un Gasto

```
Usuario escribe: "Gasté 50 pesos en comida"
       │
       ▼
Bot recibe mensaje
       │
       ▼
Agent procesa con Gemini
       │
       ├─► Thought: "El usuario quiere registrar un gasto"
       ├─► Action: add_expense
       ├─► Action Input: {amount: 50, category: "comida"}
       │
       ▼
AddExpenseTool ejecuta
       │
       ▼
Database guarda:
  - user_id: 12345
  - type: "expense"
  - amount: 50.0
  - category: "comida"
  - date: 2024-11-14 16:45:00
       │
       ▼
Observation: "Gasto registrado: $50.0 en comida"
       │
       ▼
Agent genera respuesta final
       │
       ▼
Bot envía: "Gasto registrado: $50.0 en comida. ✅"
```

### 2. Consultar Balance

```
Usuario escribe: "Cuánto dinero tengo?"
       │
       ▼
Bot recibe mensaje
       │
       ▼
Agent procesa con Gemini
       │
       ├─► Thought: "El usuario quiere saber su saldo"
       ├─► Action: get_balance
       ├─► Action Input: {}
       │
       ▼
GetBalanceTool ejecuta
       │
       ▼
Database calcula:
  - Total ingresos (user_id=12345): $5000
  - Total gastos (user_id=12345): $350
  - Balance: $5000 - $350 = $4650
       │
       ▼
Observation: "Tu saldo actual es: $4650.00"
       │
       ▼
Bot envía respuesta
```

### 3. Análisis por Categoría

```
Usuario escribe: "En qué he gastado más?"
       │
       ▼
Bot recibe mensaje
       │
       ▼
Agent procesa con Gemini
       │
       ├─► Thought: "Necesito obtener gastos por categoría"
       ├─► Action: get_expenses_by_category
       ├─► Action Input: {period: "all"}
       │
       ▼
GetExpensesByCategoryTool ejecuta
       │
       ▼
Database agrupa y suma:
  SELECT category, SUM(amount)
  FROM transactions
  WHERE user_id=12345 AND type='expense'
  GROUP BY category
  ORDER BY SUM(amount) DESC
       │
       ▼
Resultado:
  - comida: $850
  - renta: $1000
  - transporte: $300
       │
       ▼
Bot envía:
"Gastos por categoría en total:
- renta: $1000.00
- comida: $850.00
- transporte: $300.00

Total: $2150.00"
```

## Componentes del Sistema

### 1. **bot.py** - Interfaz de Telegram
- **Responsabilidad**: Comunicación con usuarios
- **Funciones principales**:
  - `start()`: Mensaje de bienvenida
  - `help_command()`: Ayuda
  - `balance_command()`: Atajo para balance
  - `handle_message()`: Procesar mensajes de texto
  - `error_handler()`: Manejo de errores

### 2. **agent.py** - Cerebro del Sistema
- **Responsabilidad**: Entender y decidir qué hacer
- **Componentes**:
  - `ChatGoogleGenerativeAI`: Modelo de lenguaje Gemini
  - `create_react_agent`: Patrón ReAct para razonamiento
  - `AgentExecutor`: Ejecutor de agente con herramientas
- **Proceso**:
  1. Recibe mensaje del usuario
  2. Gemini lo interpreta y razona
  3. Selecciona herramienta apropiada
  4. Ejecuta la herramienta
  5. Genera respuesta natural

### 3. **tools.py** - Herramientas Disponibles
- **Responsabilidad**: Acciones específicas
- **Herramientas implementadas**:
  
  | Herramienta | Propósito | Parámetros |
  |------------|-----------|------------|
  | `AddExpenseTool` | Registrar gasto | amount, category, description |
  | `AddIncomeTool` | Registrar ingreso | amount, category, description |
  | `GetBalanceTool` | Obtener balance | ninguno |
  | `GetExpensesByPeriodTool` | Gastos por período | period (week/month/all) |
  | `GetExpensesByCategoryTool` | Gastos por categoría | period (week/month/all) |
  | `CompareMonthsTool` | Comparar meses | ninguno |

### 4. **database.py** - Persistencia de Datos
- **Responsabilidad**: Almacenamiento y consultas
- **Modelo de datos**:
  ```python
  Transaction:
    - id: int (PK)
    - user_id: int (indexed)
    - type: str ('expense' | 'income')
    - amount: float
    - category: str
    - description: str
    - date: datetime
  ```
- **Operaciones**:
  - `add_transaction()`: Agregar transacción
  - `get_transactions()`: Obtener transacciones filtradas
  - `get_balance()`: Calcular balance
  - `get_summary_by_category()`: Resumen por categoría

## Tecnologías Clave

### LangChain
- Framework para aplicaciones con LLM
- Proporciona abstracción para agentes y herramientas
- Facilita la integración de múltiples componentes

### Google Gemini (gemini-pro)
- Modelo de lenguaje de Google
- Entiende español naturalmente
- Gratuito con límites generosos
- Excelente para casos de uso conversacionales

### ReAct Pattern
- **Re**asoning + **Act**ing
- Ciclo: Thought → Action → Observation → Repeat
- Permite al agente razonar antes de actuar
- Más confiable que simplemente llamar funciones

### SQLite + SQLAlchemy
- Base de datos ligera, sin servidor
- Archivo único (finance.db)
- ORM para facilitar operaciones
- Perfecto para aplicaciones pequeñas/medianas

## Escalabilidad

### Para más usuarios:
- Mantener SQLite (soporta miles de usuarios)
- O migrar a PostgreSQL/MySQL si necesario
- Cada user_id tiene datos aislados

### Para más funcionalidades:
- Agregar nuevas herramientas en `tools.py`
- El agente aprenderá a usarlas automáticamente
- Actualizar el prompt del sistema si es necesario

### Para producción:
- Usar supervisor de procesos (systemd, supervisor, pm2)
- Implementar logging apropiado
- Considerar webhook en lugar de polling
- Backups automáticos de la base de datos
- Monitoreo y alertas

## Seguridad

✅ **Implementado:**
- Aislamiento de datos por usuario (user_id)
- Variables de entorno para secretos (.env)
- .gitignore para evitar commits accidentales
- Validación de inputs en herramientas

⚠️ **Considerar para producción:**
- Encriptación de base de datos
- Rate limiting por usuario
- Logs de auditoría
- Backup automático y encriptado
- Manejo de excepciones más robusto
