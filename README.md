# 💇‍♀️ BLUSH - Sistema de Retención de Clientes

Sistema inteligente de análisis de retención de clientes con mensajes personalizados de WhatsApp para salones de belleza.

## 🚀 Características Principales

### 📊 Análisis de Retención
- Tasa de retención por estilista
- Comparativa de desempeño
- Identificación de mejores prácticas
- Clientes activos vs en riesgo

### 👥 Segmentación Inteligente
- **Nuevo**: Clientes con 1 visita reciente
- **Ocasional**: 2-3 visitas
- **Regular**: 4-9 visitas
- **VIP**: 10+ visitas
- **En Riesgo**: Sin visitar 60+ días
- **Perdido**: 1 visita hace más de 60 días

### 📱 Mensajes WhatsApp Automáticos
- Mensajes personalizados según:
  - Días sin visita
  - Número de visitas previas
  - Estilista preferido
  - Segmento del cliente
- Exportación a Excel con números de teléfono
- Links directos a WhatsApp

### 📈 Reportes y Análisis
- KPIs principales del salón
- Top y bottom performers
- Distribución de clientes por segmento
- Estadísticas de gasto
- Top 10 clientes VIP

## 🛠️ Instalación

### Opción 1: Streamlit Cloud (RECOMENDADO)

1. Sube los archivos a GitHub:
   - `app.py` (renombrar de app_retencion.py)
   - `requirements.txt` (renombrar de requirements_retencion.txt)
   - `README.md`

2. Ve a [share.streamlit.io](https://share.streamlit.io)

3. Conecta tu repositorio

4. ¡Listo! Tu app estará en línea en 2-3 minutos

### Opción 2: Local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📋 Cómo Usar

### 1. Subir Archivo
- Formato: Excel (.xlsx)
- Debe contener columnas:
  - FECHA
  - EMPLEADO
  - CLIENTE
  - TELEF
  - PRODUCTO / SERVICIO
  - TOTAL

### 2. Revisar Análisis
- **Tab 1 - Por Estilista**: Compara retención de tu equipo
- **Tab 2 - Segmentación**: Ve distribución de clientes
- **Tab 3 - WhatsApp**: ¡La magia sucede aquí!
- **Tab 4 - Estadísticas**: Números generales

### 3. Generar Mensajes WhatsApp

1. Selecciona filtros:
   - Segmento (Ej: "En Riesgo")
   - Estilista
   - Días mínimos sin visita

2. Revisa preview de mensajes

3. Descarga Excel con lista completa:
   - Nombre del cliente
   - Teléfono
   - Estilista
   - Mensaje personalizado

4. Copia y pega los mensajes en WhatsApp Business

## 💡 Ejemplos de Mensajes Generados

### Cliente en Riesgo (90+ días)
```
¡Hola María! 💇‍♀️ Somos BLUSH Hair & Make-Up y te extrañamos mucho! 

Han pasado 95 días desde tu última visita con Yuri y queremos verte de nuevo ✨

🎁 OFERTA ESPECIAL PARA TI:
- 20% de descuento en tu próximo servicio
- Válido hasta fin de mes

📍 Los Olivos, Lima
📱 Escríbenos para agendar tu cita

¡Yuri te está esperando! 💕
```

### Cliente Ocasional (60 días)
```
Hola Carmen! 😊

Jhon te manda saludos desde BLUSH! ✨

Hace 65 días que no te vemos y ya es hora de consentirte de nuevo 💅

¿Agendamos tu cita esta semana?
🎁 Tenemos promociones especiales para ti

¡Te esperamos! 💕
```

## 📊 Métricas Clave

### Tasa de Retención
```
(Clientes con 2+ visitas / Total clientes) × 100
```

### Clientes Activos
```
Clientes que visitaron en los últimos 60 días
```

### Valor Promedio del Cliente
```
Gasto Total / Número de Visitas
```

## 🎯 Estrategias de Retención

### Para Mejorar del 17% al 40%:

1. **Contacto Inmediato (24-48h después de visita)**
   - Mensaje de agradecimiento
   - Preguntar por satisfacción
   - Agendar próxima cita

2. **Recordatorios Automáticos**
   - A los 30 días: "Te extrañamos"
   - A los 60 días: Oferta especial
   - A los 90 días: Descuento reactivación

3. **Programa de Fidelidad**
   - 5ta visita: 10% descuento
   - 10ma visita: Servicio gratis
   - Cumpleaños: Regalo especial

4. **Seguimiento por Estilista**
   - Cada estilista responsable de sus clientes
   - Meta: Retención 40%+
   - Bonos por cumplimiento

## 📱 Integración WhatsApp Business

### Recomendaciones:
1. Usar WhatsApp Business (no personal)
2. Configurar mensajes de ausencia
3. Etiquetar clientes por segmento
4. Programar envíos (no spam)
5. Personalizar cada mensaje antes de enviar

### Timing Óptimo:
- Martes a Jueves: 10am - 12pm y 3pm - 5pm
- Evitar lunes y viernes
- Nunca después de 8pm

## 🔒 Privacidad

- No se almacenan datos en servidores
- Todo el procesamiento es local
- Los datos solo existen durante la sesión
- Cumple con GDPR y protección de datos

## 📞 Soporte

Para dudas o mejoras:
- Email: contacto@blushsalon.com
- WhatsApp: +51 XXX XXX XXX

## 📈 Roadmap

### Próximas Funcionalidades:
- [ ] Envío automático de mensajes
- [ ] Integración con WhatsApp API
- [ ] Predicción de abandono con ML
- [ ] Dashboard en tiempo real
- [ ] App móvil
- [ ] Notificaciones push

## 🏆 Resultados Esperados

Con uso consistente de este sistema:

- **Mes 1**: +5% retención
- **Mes 2**: +10% retención  
- **Mes 3**: +15-20% retención
- **Mes 6**: 40%+ retención (objetivo)

**ROI**: Cada cliente retenido = S/ 500-1000 anuales adicionales

## ⚖️ Licencia

Uso exclusivo de BLUSH Hair & Make-Up Salon.

---

💇‍♀️ **BLUSH Hair & Make-Up** | Los Olivos, Lima, Perú
Sistema desarrollado con ❤️ para mejorar la experiencia del cliente
