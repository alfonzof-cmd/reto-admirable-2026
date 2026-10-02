import streamlit as st
import pandas as pd
from datetime import timedelta

st.set_page_config(page_title="Plan Agroalimentario Comunal 2026", layout="wide")

st.title("🌱 Plan Agroalimentario Comunal 'Reto Admirable 2026'")
st.subheader("Protocolo de Manejo Agronómico: Caraota y Frijol Gringo")

# ==========================================
# SIDEBAR: DATOS DEL PRODUCTOR Y PREDIO
# ==========================================
st.sidebar.header("👤 Datos del Productor")
nombre_productor = st.sidebar.text_input("Nombre y Apellido:")
cedula = st.sidebar.text_input("Cédula de Identidad:")
telefono = st.sidebar.text_input("Teléfono de Contacto:")

st.sidebar.header("📍 Ubicación y Predio")
comuna = st.sidebar.text_input("Comuna / Consejo Comunal:")
nombre_fundo = st.sidebar.text_input("Nombre del Fundo / Predio:")
tecnico_responsable = st.sidebar.text_input("Técnico Responsable:")

st.sidebar.header("🌾 Parámetros del Cultivo")
rubro = st.sidebar.radio("Seleccione Rubro:", ["Caraota", "Frijol (Gringo)"])

st.sidebar.subheader("📐 Control de Superficie (Ha)")
ha_financiadas = st.sidebar.number_input("Hectáreas Financiadas (Aprobadas):", min_value=0.1, value=2.0, step=0.5)
ha_sembradas = st.sidebar.number_input("Hectáreas Sembradas (Reales en Campo):", min_value=0.0, value=ha_financiadas, step=0.5)

fecha_siembra = st.sidebar.date_input("Fecha de Siembra:")

if ha_sembradas > ha_financiadas:
    st.sidebar.warning("⚠ Atención: Ha sembradas superan las financiadas.")

# ==========================================
# LÓGICA TÉCNICA Y COSTOS SEGÚN PROTOCOLO
# ==========================================
if rubro == "Caraota":
    sacos_npk_ha = 4
    herbicida_post = "Flex (Fomesafen)"
    costo_herbicida = 35.55
    insecticida_esp = "Abamectina"
    costo_insecticida = 23.28
    costo_npk_ha = 208.00
    total_costo_ha = 412.21
else: # Frijol Gringo
    sacos_npk_ha = 2
    herbicida_post = "Sonic"
    costo_herbicida = 35.55
    insecticida_esp = "Deltametrina (2.5 EC)"
    costo_insecticida = 25.00
    costo_npk_ha = 104.00
    total_costo_ha = 309.93

fecha_germ = fecha_siembra + timedelta(days=4)
cumplimiento = (ha_sembradas / ha_financiadas * 100) if ha_financiadas > 0 else 0

# ==========================================
# VISTA PRINCIPAL - FICHA Y MÉTRICAS
# ==========================================
with st.expander("📌 Ficha Consolidada del Lote y Productor", expanded=True):
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"**Productor:** {nombre_productor if nombre_productor else 'N/A'}\n\n**Cédula:** {cedula if cedula else 'N/A'}\n\n**Teléfono:** {telefono if telefono else 'N/A'}")
    col2.markdown(f"**Comuna:** {comuna if comuna else 'N/A'}\n\n**Fundo:** {nombre_fundo if nombre_fundo else 'N/A'}\n\n**Técnico:** {tecnico_responsable if tecnico_responsable else 'N/A'}")
    col3.markdown(f"**Rubro:** {rubro}\n\n**Fecha Siembra:** {fecha_siembra.strftime('%d/%m/%Y')}\n\n**Ejecución Superficie:** {cumplimiento:.1f}%")

    st.divider()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Ha Financiadas", f"{ha_financiadas:.1f} Ha")
    m2.metric("Ha Sembradas", f"{ha_sembradas:.1f} Ha", delta=f"{ha_sembradas - ha_financiadas:.1f} Ha")
    m3.metric("Monto Financiado Total", f"${total_costo_ha * ha_financiadas:.2f}")
    m4.metric("Monto Real Ejecutado", f"${total_costo_ha * ha_sembradas:.2f}", delta=f"${(ha_sembradas - ha_financiadas) * total_costo_ha:.2f}")

tab1, tab2, tab3 = st.tabs(["📅 Cronograma Técnico", "🧮 Balance de Insumos", "⚠️ Normas Fitosanitarias"])

# TAB 1: CRONOGRAMA DE APLICACIÓN
with tab1:
    st.header(f"📅 Cronograma de Campo para {ha_sembradas:.1f} Ha Sembradas")
    cronograma = [
        {"Labor / Aplicación": "Inoculación de Semilla", "Fecha Estimada": f"Siembra ({fecha_siembra.strftime('%d/%m/%Y')})", "Dosis Total Lote": f"{500*ha_sembradas:.0f} cc El Guerrero", "Especificaciones": "Asperjar 30 min antes de la siembra en superficie limpia."},
        {"Labor / Aplicación": "Fertilización NPK (10-26-26)", "Fecha Estimada": f"5 D.G. ({(fecha_germ + timedelta(days=5)).strftime('%d/%m/%Y')})", "Dosis Total Lote": f"{sacos_npk_ha * ha_sembradas:.0f} Sacos NPK", "Especificaciones": "Aplicación edáfica incorporada o en banda."},
        {"Labor / Aplicación": f"Post-emergente ({herbicida_post})", "Fecha Estimada": f"10 D.G. / 15 D.S. ({(fecha_siembra + timedelta(days=15)).strftime('%d/%m/%Y')})", "Dosis Total Lote": f"{1.0 * ha_sembradas:.1f} Litros", "Especificaciones": "Aplicar con maleza de 2 a 4 hojas verdaderas."},
        {"Labor / Aplicación": "Paso 4: 1ra Aplicación Foliar", "Fecha Estimada": f"10-12 D.G. ({(fecha_germ + timedelta(days=11)).strftime('%d/%m/%Y')})", "Dosis Total Lote": f"{2*ha_sembradas:.1f}L Guerrero + {125*ha_sembradas:.0f}g Metomilo + {400*ha_sembradas:.0f}cc Micro.", "Especificaciones": "Mezcla en 200 L agua/ha."},
        {"Labor / Aplicación": "Paso 5: 2da Aplicación Foliar", "Fecha Estimada": f"22-25 D.G. ({(fecha_germ + timedelta(days=23)).strftime('%d/%m/%Y')})", "Dosis Total Lote": f"{2*ha_sembradas:.1f}L Guerrero + {400*ha_sembradas:.0f}cc Micro. + {insecticida_esp}", "Especificaciones": "Mezcla en 200 L agua/ha."},
        {"Labor / Aplicación": "Paso 6: 3ra Aplicación Foliar", "Fecha Estimada": f"Antes 35 D.G. ({(fecha_germ + timedelta(days=32)).strftime('%d/%m/%Y')})", "Dosis Total Lote": f"{2*ha_sembradas:.1f}L Guerrero + {400*ha_sembradas:.0f}cc Micro. + {insecticida_esp}", "Especificaciones": "Refuerzo en 200 L agua/ha."},
        {"Labor / Aplicación": "Monitoreo Técnico", "Fecha Estimada": f"Hasta 60 D.G. ({(fecha_germ + timedelta(days=60)).strftime('%d/%m/%Y')})", "Dosis Total Lote": "Inspección semanal", "Especificaciones": "Visitas obligatorias de la brigada técnica."},
        {"Labor / Aplicación": "Cosecha Manual", "Fecha Estimada": f"90 D.S. ({(fecha_siembra + timedelta(days=90)).strftime('%d/%m/%Y')})", "Dosis Total Lote": "N/A", "Especificaciones": "Cosecha manual y transporte asignado."}
    ]
    st.table(pd.DataFrame(cronograma))

# TAB 2: BALANCE DE INSUMOS FINANCIADOS VS REALES
with tab2:
    st.header("🧮 Balance de Insumos: Financiados vs. Realmente Requeridos")
    datos_insumos = [
        {"Insumo": "Semilla (Sacos 40 Kg)", "Cant. Financiada": f"{1 * ha_financiadas:.0f} Sacos", "Cant. Real Requerida": f"{1 * ha_sembradas:.0f} Sacos", "Diferencia / Sobrante": f"{(ha_financiadas - ha_sembradas) * 1:.0f} Sacos", "Costo Real ($)": 0.00},
        {"Insumo": "Paraquat (Paramax 200 SL)", "Cant. Financiada": f"{2 * ha_financiadas:.1f} L", "Cant. Real Requerida": f"{2 * ha_sembradas:.1f} L", "Diferencia / Sobrante": f"{(ha_financiadas - ha_sembradas) * 2:.1f} L", "Costo Real ($)": 26.00 * ha_sembradas},
        {"Insumo": f"Herbicida ({herbicida_post})", "Cant. Financiada": f"{1 * ha_financiadas:.1f} L", "Cant. Real Requerida": f"{1 * ha_sembradas:.1f} L", "Diferencia / Sobrante": f"{(ha_financiadas - ha_sembradas) * 1:.1f} L", "Costo Real ($)": costo_herbicida * ha_sembradas},
        {"Insumo": "El Guerrero (Bioestimulante)", "Cant. Financiada": f"{7 * ha_financiadas:.1f} L", "Cant. Real Requerida": f"{7 * ha_sembradas:.1f} L", "Diferencia / Sobrante": f"{(ha_financiadas - ha_sembradas) * 7:.1f} L", "Costo Real ($)": 70.00 * ha_sembradas},
        {"Insumo": "Metomilo (Sobre 250g)", "Cant. Financiada": f"{1 * ha_financiadas:.0f} Sobres", "Cant. Real Requerida": f"{1 * ha_sembradas:.0f} Sobres", "Diferencia / Sobrante": f"{(ha_financiadas - ha_sembradas) * 1:.0f} Sobres", "Costo Real ($)": 19.38 * ha_sembradas},
        {"Insumo": f"Insecticida ({insecticida_esp})", "Cant. Financiada": f"{1 * ha_financiadas:.1f} Unid", "Cant. Real Requerida": f"{1 * ha_sembradas:.1f} Unid", "Diferencia / Sobrante": f"{(ha_financiadas - ha_sembradas) * 1:.1f} Unid", "Costo Real ($)": costo_insecticida * ha_sembradas},
        {"Insumo": "NPK (10-26-26)", "Cant. Financiada": f"{sacos_npk_ha * ha_financiadas:.0f} Sacos", "Cant. Real Requerida": f"{sacos_npk_ha * ha_sembradas:.0f} Sacos", "Diferencia / Sobrante": f"{(ha_financiadas - ha_sembradas) * sacos_npk_ha:.0f} Sacos", "Costo Real ($)": costo_npk_ha * ha_sembradas},
        {"Insumo": "Microelementos (Ecoactiva 13)", "Cant. Financiada": f"{2 * ha_financiadas:.0f} Unid", "Cant. Real Requerida": f"{2 * ha_sembradas:.0f} Unid", "Diferencia / Sobrante": f"{(ha_financiadas - ha_sembradas) * 2:.0f} Unid", "Costo Real ($)": 30.00 * ha_sembradas},
    ]
    df_insumos = pd.DataFrame(datos_insumos)
    st.dataframe(df_insumos, use_container_width=True)

    csv = df_insumos.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Balance de Insumos (CSV)",
        data=csv,
        file_name=f"balance_{nombre_productor if nombre_productor else 'productor'}_{rubro}.csv",
        mime='text/csv'
    )

# TAB 3: NORMAS FITOSANITARIAS
with tab3:
    st.header("⚠️ Especificaciones Técnicas Fitosanitarias")
    st.error("🚨 **PROHIBICIÓN MEZCLA FUNGICIDA:** Si se requiere aplicar fungicida, debe hacerse SOLO. NUNCA mezclado con el bioestimulante El Guerrero.")
    st.warning("💧 **VOLUMEN DE AGUA:** Dosis foliares calculadas para 200 Litros de agua por hectárea.")
    st.info("🚜 **INOCULACIÓN:** Inocular 30 minutos antes de sembrar directamente sobre la semilla en superficie limpia.")
