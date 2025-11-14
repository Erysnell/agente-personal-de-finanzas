# 📘 Guía de Uso - Agente Personal de Finanzas

Esta guía te ayudará a sacar el máximo provecho de tu asistente de finanzas en Telegram.

## 🎯 Índice

1. [Inicio Rápido](#inicio-rápido)
2. [Registrar Gastos](#registrar-gastos)
3. [Registrar Ingresos](#registrar-ingresos)
4. [Consultar Información](#consultar-información)
5. [Análisis Avanzado](#análisis-avanzado)
6. [Consejos y Trucos](#consejos-y-trucos)

## 🚀 Inicio Rápido

1. **Busca tu bot en Telegram**
   - Abre Telegram
   - Busca el nombre de tu bot (el que configuraste con @BotFather)
   - Inicia una conversación

2. **Envía el comando `/start`**
   - Verás un mensaje de bienvenida
   - El bot te explicará qué puede hacer

3. **Empieza a usar el bot con lenguaje natural**
   - No necesitas comandos especiales
   - Escribe como le hablarías a un amigo

## 💸 Registrar Gastos

### Formato básico

El bot entiende diferentes formas de expresar un gasto:

```
"Gasté 50 en comida"
"Pagué 1000 de renta"
"Compré ropa por 200 pesos"
"Me costó 30 el taxi"
"Almorcé y gasté 80"
```

### Categorías comunes

El bot categoriza automáticamente tus gastos. Algunas categorías comunes:

- **Comida**: restaurantes, supermercado, almuerzo, cena
- **Transporte**: taxi, uber, gasolina, transporte público
- **Renta**: alquiler, renta
- **Servicios**: luz, agua, internet, teléfono
- **Entretenimiento**: cine, conciertos, salidas
- **Salud**: medicinas, doctor, hospital
- **Ropa**: ropa, zapatos, accesorios
- **Educación**: cursos, libros, matrícula

### Con descripción detallada

Puedes agregar más contexto:

```
"Gasté 150 en comida, compré despensa en el supermercado"
"Pagué 50 de transporte en uber para ir al trabajo"
```

## 💰 Registrar Ingresos

### Formato básico

```
"Recibí mi salario de 5000"
"Gané 500 por freelance"
"Vendí algo por 300"
"Me pagaron 1000"
"Ingreso de 200 por un trabajo extra"
```

### Categorías de ingresos

- **Salario**: sueldo mensual
- **Freelance**: trabajos independientes
- **Ventas**: venta de artículos
- **Bonos**: bonificaciones, premios
- **Otros**: otros ingresos

## 📊 Consultar Información

### Saldo actual

```
"Cuánto dinero tengo?"
"Cuál es mi saldo?"
"Muéstrame mi balance"
```

### Gastos por período

**Esta semana:**
```
"Cuánto gasté esta semana?"
"Gastos de la semana"
```

**Este mes:**
```
"Cuánto gasté este mes?"
"Gastos del mes"
```

**Todos los gastos:**
```
"Cuánto he gastado en total?"
"Todos mis gastos"
```

## 📈 Análisis Avanzado

### Gastos por categoría

Ver en qué gastas más dinero:

```
"En qué he gastado más?"
"Muéstrame mis gastos por categoría"
"En qué categoría gasto más este mes?"
```

**Respuesta ejemplo:**
```
Gastos por categoría este mes:
- Renta: $1000.00
- Comida: $850.00
- Transporte: $300.00
- Entretenimiento: $200.00

Total: $2350.00
```

### Comparar meses

```
"Compara mis gastos del mes pasado con este mes"
"Diferencia entre este mes y el anterior"
```

**Respuesta ejemplo:**
```
Comparación de gastos:
- Mes anterior: $2500.00
- Mes actual: $2350.00
- Diferencia: $150.00 (-6.0% menos que el mes anterior)
```

## 💡 Consejos y Trucos

### 1. Sé consistente con las categorías

Trata de usar los mismos términos para las mismas categorías:
- ✅ Siempre usa "comida" en lugar de mezclar "comida", "alimentos", "food"
- ✅ Usa "transporte" en lugar de mezclar "transporte", "uber", "taxi"

### 2. Registra gastos de inmediato

- Registra tus gastos cuando ocurren para no olvidarlos
- Puedes usar Telegram desde cualquier lugar

### 3. Usa descripciones para gastos importantes

```
"Gasté 1500 en ropa, compré un abrigo de invierno"
```

Esto te ayudará a recordar por qué gastaste ese dinero.

### 4. Revisa tus gastos regularmente

Cada semana o mes, pregunta:
```
"Cuánto gasté esta semana?"
"En qué categoría gasto más?"
```

### 5. Usa el comando /balance

Es la forma más rápida de ver tu saldo actual:
```
/balance
```

### 6. Compara meses para detectar patrones

Al final de cada mes:
```
"Compara mis gastos del mes pasado con este mes"
```

Esto te ayudará a identificar si estás gastando más o menos.

## 🎯 Casos de Uso Completos

### Ejemplo 1: Día normal

```
Usuario: "Gasté 45 en comida, desayuné fuera"
Bot: Gasto registrado: $45.0 en comida. Desayuné fuera

Usuario: "Pagué 25 de uber"
Bot: Gasto registrado: $25.0 en transporte.

Usuario: "Cuánto he gastado hoy?"
Bot: Has gastado $70.00 hoy (2 transacciones).
```

### Ejemplo 2: Día de cobro

```
Usuario: "Recibí mi salario de 5000"
Bot: Ingreso registrado: $5000.0 en salario.

Usuario: "Cuál es mi saldo?"
Bot: Tu saldo actual es: $5070.00
```

### Ejemplo 3: Análisis de fin de semana

```
Usuario: "Cuánto gasté esta semana?"
Bot: Has gastado $450.00 esta semana (12 transacciones).

Usuario: "En qué he gastado más?"
Bot: Gastos por categoría esta semana:
- Comida: $220.00
- Transporte: $130.00
- Entretenimiento: $100.00

Total: $450.00
```

## 🔧 Solución de Problemas

### El bot no responde

1. Verifica que el bot esté corriendo en el servidor
2. Revisa que las API keys estén configuradas correctamente
3. Intenta reiniciar la conversación con `/start`

### El bot no entiende mi mensaje

1. Intenta ser más específico con el monto y la categoría
2. Usa números claros: "50" en lugar de "cincuenta"
3. Menciona explícitamente si es un gasto o ingreso

Ejemplos:
- ❌ "Compré cosas"
- ✅ "Gasté 100 en compras"

### Categoría incorrecta

Si el bot asigna una categoría que no esperabas, intenta ser más específico:
- ❌ "Gasté 50"
- ✅ "Gasté 50 en comida"

## 📞 Soporte

Si tienes problemas o sugerencias:
1. Revisa este documento
2. Consulta el README.md principal
3. Abre un issue en GitHub

## 🎉 ¡Disfruta tu asistente financiero!

Recuerda: el objetivo es hacer un seguimiento de tus finanzas de manera simple y natural. No te preocupes por la sintaxis perfecta, ¡el bot está diseñado para entenderte!
