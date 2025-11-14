# 💰 Agente Personal de Finanzas

Un bot de Telegram inteligente que te ayuda a gestionar tus finanzas personales usando IA (Google Gemini). Registra tus gastos e ingresos con lenguaje natural y obtén análisis detallados de tus finanzas.

## ✨ Características

- 📝 **Registro intuitivo**: Registra gastos e ingresos usando lenguaje natural
- 🤖 **IA integrada**: Usa Google Gemini para entender tus mensajes
- 💵 **Consulta tu saldo**: Conoce cuánto dinero tienes en cualquier momento
- 📊 **Análisis por período**: Consulta gastos semanales, mensuales o totales
- 🏷️ **Categorización automática**: Agrupa y analiza gastos por categoría
- 📈 **Comparaciones**: Compara tus gastos entre diferentes meses
- 🔒 **Privado**: Cada usuario tiene sus propios datos

## 🚀 Instalación

### Requisitos previos

- Python 3.8 o superior
- Una cuenta de Telegram
- Una API key de Google Gemini (gratuita)

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/Erysnell/agente-personal-de-finanzas.git
cd agente-personal-de-finanzas
```

### Paso 2: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 3: Configurar variables de entorno

1. Crea un archivo `.env` en la raíz del proyecto:

```bash
cp .env.example .env
```

2. Edita el archivo `.env` y configura:

**TELEGRAM_BOT_TOKEN**: 
- Ve a Telegram y busca [@BotFather](https://t.me/botfather)
- Envía `/newbot` y sigue las instrucciones
- Copia el token que te proporciona

**GOOGLE_API_KEY**:
- Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
- Crea una API key (es gratuita)
- Copia la API key

Tu archivo `.env` debe verse así:
```
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
GOOGLE_API_KEY=AIzaSyA...
```

### Paso 4: Ejecutar el bot

```bash
python bot.py
```

¡Listo! Tu bot está funcionando. Ahora ve a Telegram y busca tu bot.

## 📱 Uso

### Comandos disponibles

- `/start` - Iniciar el bot y ver mensaje de bienvenida
- `/help` - Ver ayuda y ejemplos
- `/balance` - Consultar tu saldo actual

### Ejemplos de uso

**Registrar gastos:**
```
"Gasté 50 pesos en comida"
"Compré ropa por 200"
"Pagué 1000 de renta"
```

**Registrar ingresos:**
```
"Recibí mi salario de 5000"
"Gané 500 por freelance"
"Vendí algo por 300"
```

**Consultar información:**
```
"Cuánto dinero tengo?"
"Cuánto gasté esta semana?"
"Cuánto gasté este mes?"
"En qué he gastado más?"
"En qué categoría gasto más este mes?"
"Compara mis gastos del mes pasado con este mes"
```

## 🛠️ Tecnologías utilizadas

- **Python**: Lenguaje de programación principal
- **python-telegram-bot**: Framework para crear el bot de Telegram
- **LangChain**: Framework para aplicaciones con LLM
- **Google Gemini (gemini-pro)**: Modelo de lenguaje para entender mensajes
- **SQLAlchemy**: ORM para la base de datos
- **SQLite**: Base de datos ligera para almacenar transacciones

## 📊 Estructura del proyecto

```
agente-personal-de-finanzas/
├── bot.py              # Bot de Telegram (punto de entrada)
├── agent.py            # Agente LangChain con Gemini
├── tools.py            # Herramientas del agente (funciones)
├── database.py         # Gestor de base de datos
├── requirements.txt    # Dependencias Python
├── .env.example        # Ejemplo de variables de entorno
├── .gitignore         # Archivos ignorados por git
└── README.md          # Este archivo
```

## 💡 Cómo funciona

1. **Usuario envía mensaje**: Escribes en lenguaje natural a través de Telegram
2. **Procesamiento con IA**: Google Gemini interpreta tu mensaje y determina la acción
3. **Ejecución de herramienta**: El agente ejecuta la función correspondiente (agregar gasto, consultar saldo, etc.)
4. **Almacenamiento**: Los datos se guardan en una base de datos SQLite
5. **Respuesta**: Recibes una confirmación o la información solicitada

## 🔧 Personalización

Puedes modificar las categorías, añadir nuevas herramientas o cambiar los prompts editando los siguientes archivos:

- `agent.py`: Modifica el prompt del sistema
- `tools.py`: Añade nuevas herramientas o modifica las existentes
- `database.py`: Cambia el esquema de la base de datos

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## ⚠️ Notas importantes

- Los datos se almacenan localmente en un archivo `finance.db`
- Cada usuario de Telegram tiene sus propios datos separados
- La base de datos NO incluye backup automático - haz copias de seguridad regularmente
- El bot debe estar ejecutándose constantemente para responder mensajes

## 📧 Soporte

Si tienes problemas o preguntas, abre un issue en GitHub.

## 🎯 Roadmap

Futuras mejoras planeadas:

- [ ] Exportar datos a Excel/CSV
- [ ] Gráficos y visualizaciones
- [ ] Recordatorios de gastos recurrentes
- [ ] Presupuestos por categoría
- [ ] Múltiples monedas
- [ ] Reportes mensuales automáticos