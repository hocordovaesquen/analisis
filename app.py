import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

st.set_page_config(
    page_title="BLUSH - Sistema de Retención de Clientes",
    page_icon="💇‍♀️",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #E91E63;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #FCE4EC 0%, #F8BBD0 100%);
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background-color: #E91E63;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #E91E63;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .warning-card {
        background: #FFF3CD;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #FFC107;
    }
    .success-card {
        background: #D4EDDA;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28A745;
    }
</style>
""", unsafe_allow_html=True)

def generar_mensaje_whatsapp(nombre, estilista, dias_sin_visita, num_visitas):
    """Genera mensaje personalizado según el perfil del cliente"""
    
    nombre_corto = nombre.split()[0] if nombre else "estimado(a) cliente"
    
    if dias_sin_visita > 90:
        mensaje = f"""¡Hola {nombre_corto}! 💇‍♀️ Somos BLUSH Hair & Make-Up y te extrañamos mucho! 

Han pasado {dias_sin_visita} días desde tu última visita con {estilista} y queremos verte de nuevo ✨

🎁 OFERTA ESPECIAL PARA TI:
- 20% de descuento en tu próximo servicio
- Válido hasta fin de mes

📍 Los Olivos, Lima
📱 Escríbenos para agendar tu cita

¡{estilista} te está esperando! 💕"""
    
    elif dias_sin_visita > 60:
        mensaje = f"""Hola {nombre_corto}! 😊

{estilista} te manda saludos desde BLUSH! ✨

Hace {dias_sin_visita} días que no te vemos y ya es hora de consentirte de nuevo 💅

¿Agendamos tu cita esta semana?
🎁 Tenemos promociones especiales para ti

¡Te esperamos! 💕"""
    
    elif dias_sin_visita > 30:
        mensaje = f"""¡{nombre_corto}! 💖

{estilista} te recuerda que ya pasaron {dias_sin_visita} días desde tu última visita a BLUSH 

Es momento de volver a lucir espectacular! ✨

¿Cuándo te viene bien para tu próxima cita?

Nos vemos pronto! 😊"""
    
    else:
        mensaje = f"""¡Hola {nombre_corto}! 

Gracias por confiar en BLUSH y en {estilista} 💕

Queremos saber si quedaste satisfecha con tu último servicio y recordarte que estamos aquí para consentirte siempre que lo necesites ✨

¡Hasta pronto! 💇‍♀️"""
    
    return mensaje

def analizar_retencion(df):
    """Analiza patrones de retención de clientes"""
    
    df['FECHA'] = pd.to_datetime(df['FECHA'], errors='coerce').ffill()
    df['MES'] = df['FECHA'].dt.to_period('M')
    df['EMPLEADO'] = df['EMPLEADO'].str.strip()
    
    hoy = datetime.now()
    
    # Análisis por cliente
    clientes = df.groupby('CLIENTE').agg({
        'FECHA': ['min', 'max', 'count'],
        'TOTAL': 'sum',
        'EMPLEADO': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
        'TELEF': 'first'
    }).reset_index()
    
    clientes.columns = ['CLIENTE', 'PRIMERA_VISITA', 'ULTIMA_VISITA', 'NUM_VISITAS', 'GASTO_TOTAL', 'ESTILISTA', 'TELEFONO']
    
    clientes['DIAS_SIN_VISITA'] = (hoy - pd.to_datetime(clientes['ULTIMA_VISITA'])).dt.days
    clientes['GASTO_PROMEDIO'] = clientes['GASTO_TOTAL'] / clientes['NUM_VISITAS']
    
    # Segmentación
    def segmentar_cliente(row):
        if row['NUM_VISITAS'] == 1:
            if row['DIAS_SIN_VISITA'] > 60:
                return 'Perdido'
            else:
                return 'Nuevo'
        elif row['NUM_VISITAS'] <= 3:
            if row['DIAS_SIN_VISITA'] > 90:
                return 'En Riesgo'
            else:
                return 'Ocasional'
        elif row['NUM_VISITAS'] <= 9:
            if row['DIAS_SIN_VISITA'] > 60:
                return 'En Riesgo'
            else:
                return 'Regular'
        else:
            return 'VIP'
    
    clientes['SEGMENTO'] = clientes.apply(segmentar_cliente, axis=1)
    
    # Generar mensajes
    clientes['MENSAJE_WHATSAPP'] = clientes.apply(
        lambda row: generar_mensaje_whatsapp(
            row['CLIENTE'], 
            row['ESTILISTA'], 
            row['DIAS_SIN_VISITA'],
            row['NUM_VISITAS']
        ),
        axis=1
    )
    
    return clientes, df

def calcular_metricas_estilista(df, clientes):
    """Calcula métricas de retención por estilista"""
    
    metricas = []
    
    for emp in df['EMPLEADO'].unique():
        clientes_emp = clientes[clientes['ESTILISTA'] == emp]
        
        if len(clientes_emp) == 0:
            continue
        
        # Tasa de retención (clientes con 2+ visitas)
        retencion = (clientes_emp['NUM_VISITAS'] > 1).sum() / len(clientes_emp) * 100
        
        # Clientes activos (visitaron últimos 60 días)
        activos = (clientes_emp['DIAS_SIN_VISITA'] <= 60).sum()
        
        # Clientes en riesgo
        en_riesgo = (clientes_emp['SEGMENTO'] == 'En Riesgo').sum()
        
        metricas.append({
            'ESTILISTA': emp,
            'TOTAL_CLIENTES': len(clientes_emp),
            'CLIENTES_ACTIVOS': activos,
            'TASA_RETENCION': retencion,
            'CLIENTES_EN_RIESGO': en_riesgo,
            'VISITAS_PROMEDIO': clientes_emp['NUM_VISITAS'].mean(),
            'GASTO_PROMEDIO': clientes_emp['GASTO_PROMEDIO'].mean()
        })
    
    return pd.DataFrame(metricas).sort_values('TASA_RETENCION', ascending=False)

def crear_excel_whatsapp(clientes_filtrados):
    """Crea Excel con lista de WhatsApp"""
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Lista WhatsApp"
    
    # Estilos
    header_fill = PatternFill(start_color="E91E63", end_color="E91E63", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=11)
    border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )
    
    # Título
    ws.merge_cells('A1:F1')
    ws['A1'] = f'LISTA WHATSAPP - BLUSH SALON - {datetime.now().strftime("%d/%m/%Y")}'
    ws['A1'].font = Font(bold=True, size=14)
    ws['A1'].alignment = Alignment(horizontal='center')
    
    # Headers
    headers = ['CLIENTE', 'TELEFONO', 'ESTILISTA', 'DIAS SIN VISITA', 'SEGMENTO', 'MENSAJE']
    
    for col, h in enumerate(headers, 1):
        c = ws.cell(3, col)
        c.value = h
        c.fill = header_fill
        c.font = header_font
        c.alignment = Alignment(horizontal='center', wrap_text=True)
        c.border = border
    
    # Datos
    fila = 4
    for _, row in clientes_filtrados.iterrows():
        ws.cell(fila, 1, row['CLIENTE'])
        ws.cell(fila, 2, str(row['TELEFONO']))
        ws.cell(fila, 3, row['ESTILISTA'])
        ws.cell(fila, 4, row['DIAS_SIN_VISITA'])
        ws.cell(fila, 5, row['SEGMENTO'])
        ws.cell(fila, 6, row['MENSAJE_WHATSAPP'])
        
        for col in range(1, 7):
            c = ws.cell(fila, col)
            c.border = border
            if col == 6:
                c.alignment = Alignment(wrap_text=True, vertical='top')
        
        fila += 1
    
    # Anchos
    ws.column_dimensions['A'].width = 35
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 12
    ws.column_dimensions['E'].width = 15
    ws.column_dimensions['F'].width = 80
    
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output

# HEADER
st.markdown('<div class="main-header">💇‍♀️ BLUSH - Sistema de Retención de Clientes</div>', unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #E91E63 0%, #9C27B0 100%); border-radius: 10px;'>
        <h1 style='color: white; margin: 0;'>💇‍♀️</h1>
        <h2 style='color: white; margin: 10px 0;'>BLUSH</h2>
        <p style='color: white; margin: 0;'>Sistema de Retención</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📋 Funcionalidades")
    st.markdown("""
    ✅ Análisis de retención por estilista
    ✅ Segmentación de clientes
    ✅ Identificación de clientes en riesgo
    ✅ **Mensajes WhatsApp personalizados**
    ✅ Exportación de lista de contactos
    """)
    
    st.markdown("---")
    st.markdown("### 📊 Segmentos")
    st.markdown("""
    **Nuevo**: 1 visita reciente
    **Ocasional**: 2-3 visitas
    **Regular**: 4-9 visitas
    **VIP**: 10+ visitas
    **En Riesgo**: Sin visitar 60+ días
    **Perdido**: 1 visita hace 60+ días
    """)

# UPLOAD
uploaded_file = st.file_uploader(
    "📤 Sube tu archivo histórico de ventas",
    type=['xlsx', 'xls'],
    help="El archivo debe tener el formato del sistema de registro de ventas"
)

if uploaded_file:
    try:
        with st.spinner('⏳ Analizando datos...'):
            df = pd.read_excel(uploaded_file, sheet_name='Hoja1', skiprows=9)
            df = df[df['EMPLEADO'].notna()].copy()
            clientes, df_procesado = analizar_retencion(df)
            metricas_estilistas = calcular_metricas_estilista(df_procesado, clientes)
        
        st.success('✅ Análisis completado!')
        
        # KPIs PRINCIPALES
        col1, col2, col3, col4 = st.columns(4)
        
        total_clientes = len(clientes)
        tasa_retencion_global = (clientes['NUM_VISITAS'] > 1).sum() / total_clientes * 100
        clientes_riesgo = (clientes['SEGMENTO'] == 'En Riesgo').sum()
        clientes_activos = (clientes['DIAS_SIN_VISITA'] <= 60).sum()
        
        with col1:
            st.metric("👥 Total Clientes", f"{total_clientes}")
        with col2:
            st.metric("📊 Tasa Retención", f"{tasa_retencion_global:.1f}%")
        with col3:
            st.metric("⚠️ En Riesgo", f"{clientes_riesgo}")
        with col4:
            st.metric("✅ Activos", f"{clientes_activos}")
        
        st.markdown("---")
        
        # TABS
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Análisis por Estilista", 
            "👥 Segmentación", 
            "📱 Mensajes WhatsApp",
            "📈 Estadísticas Generales"
        ])
        
        with tab1:
            st.markdown("### 📊 Desempeño por Estilista")
            
            st.dataframe(
                metricas_estilistas.style.format({
                    'TASA_RETENCION': '{:.1f}%',
                    'VISITAS_PROMEDIO': '{:.2f}',
                    'GASTO_PROMEDIO': 'S/ {:.2f}'
                }).background_gradient(cmap='RdYlGn', subset=['TASA_RETENCION']),
                use_container_width=True,
                height=400
            )
            
            st.markdown("---")
            
            # Top y bottom performers
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🏆 Top 3 en Retención")
                top3 = metricas_estilistas.head(3)
                for _, row in top3.iterrows():
                    st.markdown(f"""
                    <div class='success-card'>
                        <strong>{row['ESTILISTA']}</strong><br>
                        Retención: {row['TASA_RETENCION']:.1f}% | 
                        Clientes: {row['TOTAL_CLIENTES']} |
                        Activos: {row['CLIENTES_ACTIVOS']}
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("")
            
            with col2:
                st.markdown("#### ⚠️ Necesitan Mejorar")
                bottom3 = metricas_estilistas.tail(3)
                for _, row in bottom3.iterrows():
                    st.markdown(f"""
                    <div class='warning-card'>
                        <strong>{row['ESTILISTA']}</strong><br>
                        Retención: {row['TASA_RETENCION']:.1f}% | 
                        En Riesgo: {row['CLIENTES_EN_RIESGO']}
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("")
        
        with tab2:
            st.markdown("### 👥 Segmentación de Clientes")
            
            # Distribución por segmento
            segmentos = clientes['SEGMENTO'].value_counts()
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("#### Distribución")
                for seg, count in segmentos.items():
                    pct = count / len(clientes) * 100
                    st.metric(seg, f"{count} ({pct:.1f}%)")
            
            with col2:
                st.markdown("#### Por Estilista")
                seg_estilista = pd.crosstab(clientes['ESTILISTA'], clientes['SEGMENTO'])
                st.dataframe(seg_estilista, use_container_width=True, height=300)
        
        with tab3:
            st.markdown("### 📱 Mensajes Personalizados para WhatsApp")
            
            st.info("💡 Filtra los clientes que quieres contactar y descarga la lista con mensajes personalizados")
            
            # Filtros
            col1, col2, col3 = st.columns(3)
            
            with col1:
                segmento_filtro = st.multiselect(
                    'Segmento',
                    options=clientes['SEGMENTO'].unique(),
                    default=['En Riesgo', 'Perdido']
                )
            
            with col2:
                estilista_filtro = st.multiselect(
                    'Estilista',
                    options=clientes['ESTILISTA'].unique(),
                    default=list(clientes['ESTILISTA'].unique())
                )
            
            with col3:
                dias_min = st.number_input('Días mínimos sin visita', min_value=0, value=30)
            
            # Filtrar
            clientes_filtrados = clientes[
                (clientes['SEGMENTO'].isin(segmento_filtro)) &
                (clientes['ESTILISTA'].isin(estilista_filtro)) &
                (clientes['DIAS_SIN_VISITA'] >= dias_min)
            ].sort_values('DIAS_SIN_VISITA', ascending=False)
            
            st.markdown(f"#### 📋 Clientes a contactar: **{len(clientes_filtrados)}**")
            
            if len(clientes_filtrados) > 0:
                # Mostrar preview
                for idx, row in clientes_filtrados.head(5).iterrows():
                    with st.expander(f"📱 {row['CLIENTE']} - {row['ESTILISTA']}"):
                        col1, col2 = st.columns([1, 3])
                        
                        with col1:
                            st.markdown(f"""
                            **Teléfono:** {row['TELEFONO']}  
                            **Días sin visita:** {row['DIAS_SIN_VISITA']}  
                            **Visitas totales:** {row['NUM_VISITAS']}  
                            **Segmento:** {row['SEGMENTO']}
                            """)
                        
                        with col2:
                            st.markdown("**Mensaje sugerido:**")
                            st.text_area("", value=row['MENSAJE_WHATSAPP'], height=200, key=f"msg_{idx}")
                            st.markdown(f"[📱 Abrir WhatsApp](https://wa.me/51{row['TELEFONO']})")
                
                if len(clientes_filtrados) > 5:
                    st.info(f"Mostrando 5 de {len(clientes_filtrados)} clientes. Descarga el Excel para ver todos.")
                
                # Botón descarga
                st.markdown("---")
                
                excel_data = crear_excel_whatsapp(clientes_filtrados)
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.download_button(
                        label=f"📥 DESCARGAR LISTA COMPLETA ({len(clientes_filtrados)} clientes)",
                        data=excel_data,
                        file_name=f"WhatsApp_BLUSH_{datetime.now().strftime('%d%m%Y')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
            else:
                st.warning("No hay clientes que cumplan con los filtros seleccionados")
        
        with tab4:
            st.markdown("### 📈 Estadísticas Generales")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📊 Resumen de Visitas")
                st.markdown(f"""
                - **Promedio de visitas por cliente:** {clientes['NUM_VISITAS'].mean():.2f}
                - **Mediana de visitas:** {clientes['NUM_VISITAS'].median():.0f}
                - **Cliente más frecuente:** {clientes['NUM_VISITAS'].max():.0f} visitas
                - **Clientes con 1 sola visita:** {(clientes['NUM_VISITAS'] == 1).sum()} ({(clientes['NUM_VISITAS'] == 1).sum()/len(clientes)*100:.1f}%)
                """)
            
            with col2:
                st.markdown("#### 💰 Análisis de Gasto")
                st.markdown(f"""
                - **Gasto promedio por visita:** S/ {clientes['GASTO_PROMEDIO'].mean():.2f}
                - **Gasto total promedio por cliente:** S/ {clientes['GASTO_TOTAL'].mean():.2f}
                - **Cliente con mayor gasto:** S/ {clientes['GASTO_TOTAL'].max():.2f}
                """)
            
            st.markdown("---")
            st.markdown("#### 🎯 Top 10 Clientes VIP")
            
            top_vip = clientes.nlargest(10, 'NUM_VISITAS')[[
                'CLIENTE', 'NUM_VISITAS', 'GASTO_TOTAL', 'ESTILISTA', 'DIAS_SIN_VISITA'
            ]]
            
            st.dataframe(
                top_vip.style.format({
                    'GASTO_TOTAL': 'S/ {:.2f}'
                }),
                use_container_width=True
            )
    
    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {str(e)}")
        st.info("Verifica que el archivo tenga el formato correcto")

else:
    st.info("👆 Sube tu archivo histórico de ventas para comenzar el análisis")
    
    st.markdown("---")
    st.markdown("### 🎯 ¿Qué hace esta herramienta?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 📊 Analiza
        - Tasa de retención por estilista
        - Segmentación de clientes
        - Patrones de visitas
        - Valor del cliente
        """)
    
    with col2:
        st.markdown("""
        #### 🎯 Identifica
        - Clientes en riesgo
        - Clientes perdidos
        - Oportunidades de reactivación
        - Mejores prácticas
        """)
    
    with col3:
        st.markdown("""
        #### 📱 Genera
        - Mensajes WhatsApp personalizados
        - Listas de contactos
        - Reportes descargables
        - Acciones concretas
        """)

# FOOTER
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>💇‍♀️ <b>BLUSH Hair & Make-Up Salon</b> | Los Olivos, Lima</p>
    <p style='font-size: 0.8rem;'>Sistema de Retención de Clientes v2.0</p>
</div>
""", unsafe_allow_html=True)
