import streamlit as st
import pandas as pd

# --- 1. CONFIGURACIÓN VISUAL CORPORATIVA ---
st.set_page_config(page_title="Herramienta cálculo PC - Seguros Bolívar", layout="wide")

st.markdown("""
<style>
    .stApp, .stButton>button, .stNumberInput input, .stSelectbox, .stMetric, [data-testid="stHeader"] {
        --st-color-primary: #0A6A34; 
    }
    .stButton>button {
        background-color: #0A6A34;
        color: white;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #004B23; 
    }
    [data-testid="stMetricValue"] {
        color: #0A6A34;
    }
    .mensaje-error {
        background-color: #FFEBEE; 
        padding: 20px; 
        border-radius: 8px; 
        border-left: 6px solid #D32F2F;
    }
    .mensaje-exito {
        background-color: #E8F5E9; 
        padding: 15px; 
        border-radius: 8px; 
        border-left: 6px solid #0A6A34; 
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. DEFINICIÓN DE LA MATRIZ DE DATOS (TABLA GRANDE) ---
datos_matriz = {
    'CODIGO TIPO': [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 30, 32, 33, 99, 'NA'],
    '251': [0, 0.7, 0.7, 1, 1, 0, 0.7, 0.7, 0.7, 1, 1, 1, 0, 0, 0, 0.6, 0.6, 0.6, 0.6, 0.7, 0.7, 1, 1, 0, 1, 1, 0, 0.7, 0.7, 0, 0],
    '263': [0, 0.6, 0.6, 0, 1, 0, 0.6, 0.6, 0.6, 0, 0, 1, 0, 0, 0, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0, 0, 0, 1, 1, 0, 0.6, 0.6, 0, 0],
    '274': [0, 0.7, 0.7, 0, 1, 0, 0.7, 0.6, 0.7, 0, 0, 1, 0, 0, 0, 0.6, 0.6, 0.6, 0.6, 0.7, 0.7, 0, 0, 0, 1, 1, 0, 0.7, 0.7, 0, 0],
    '369': [0, 0.63, 0.63, 1, 1, 1, 0.63, 1, 0.63, 1, 1, 1, 1, 0, 0, 0.6, 0.6, 0.6, 0.6, 0.63, 0.63, 1, 1, 0, 1, 1, 1, 0.63, 0.63, 0, 0],
    '376': [0, 0.7, 0.7, 1, 1, 0, 0.7, 0.7, 0.7, 1, 1, 1, 0, 0, 0, 0.6, 0.6, 0.6, 0.6, 0.7, 0.7, 1, 1, 0, 1, 1, 1, 0.7, 0.7, 0, 0],
    '360': [0, 0.63, 0.63, 1, 1, 0, 0.63, 1, 0.63, 1, 1, 1, 0, 0, 0, 0.6, 0.6, 0.6, 0.6, 0.63, 0.63, 1, 1, 0, 1, 1, 0, 0.63, 0.63, 0, 0],
    '367': [0, 0.63, 0.63, 1, 1, 1, 0.63, 1, 0.63, 1, 1, 1, 1, 0, 0, 0.2, 0.2, 0.2, 0.2, 0.63, 0.63, 1, 1, 0, 1, 1, 1, 0.63, 0.63, 0, 0],
    '321': [0, 0.7, 0.7, 1, 1, 0, 0.7, 0.7, 0.7, 1, 1, 1, 0, 0, 0, 0.6, 0.6, 0.6, 0.6, 0.7, 0.7, 1, 1, 0, 1, 1, 0, 0.7, 0.7, 0, 0]
}
df_matriz = pd.DataFrame(datos_matriz)

# --- 3. LÓGICA DE TASAS (Fórmula Excel traducida) ---
def obtener_tasa(valor, tarifa):
    t = tarifa.capitalize()
    if t == "Tradicional": t = "Otros" # Tradicional usa la tasa de 'Otros'
    
    if valor <= 30000000:
        tasas = {"Premium": 0.025, "Estandar": 0.023, "Clasico": 0.022, "Otros": 0.034, "Basico": 0.02, "Ligero": 0.019}
    elif valor <= 50000000:
        tasas = {"Premium": 0.018, "Estandar": 0.0175, "Clasico": 0.017, "Otros": 0.021, "Basico": 0.016, "Ligero": 0.015}
    elif valor <= 100000000:
        tasas = {"Premium": 0.0135, "Estandar": 0.0132, "Clasico": 0.013, "Otros": 0.014, "Basico": 0.0127, "Ligero": 0.0125}
    else:
        tasas = {"Premium": 0.012, "Estandar": 0.0117, "Clasico": 0.0115, "Otros": 0.012, "Basico": 0.0112, "Ligero": 0.011}
    
    return tasas.get(t, 0.0)

# --- 4. CABECERA ---
col_t, col_l = st.columns([4, 1])
with col_t:
    st.title("📊 Herramienta cálculo PC - Actuaria")
    st.subheader("Seguros Bolívar - Herramienta de Validación")
with col_l:
    try:
        st.image("image_0.png", use_column_width=True)
    except:
        st.write("Logo")

st.markdown("---")

# --- 5. ENTRADA DE DATOS: CONFIGURACIÓN PRODUCTO ---
st.subheader("1. Parámetros del Producto")
c1, c2, c3 = st.columns(3)
with c1:
    tarifa_sel = st.selectbox("Opción Tarifa", ["PREMIUM", "ESTANDAR", "BASICO", "CLASICO", "LIGERO", "TRADICIONAL"])
with c2:
    subprod_sel = st.selectbox("Subproducto", ["251", "263", "274", "369", "376", "360", "367", "321"])
with c3:
    cod_tipo_sel = st.selectbox("Código Tipo", df_matriz['CODIGO TIPO'].unique())

c4, c5 = st.columns(2)
with c4:
    smmlv_sel = st.selectbox("Salario Mínimo", [1423500, 1750905])
with c5:
    val_asegurado = st.number_input("Valor Asegurado Vehículo", min_value=0.0, value=50000000.0, step=1000000.0)

# --- 6. CÁLCULOS INTERNOS DE PRIMA MÍNIMA ---
# Regla Tradicional: Solo subproducto 367
if tarifa_sel == "TRADICIONAL":
    val_tabla = df_matriz.loc[df_matriz['CODIGO TIPO'] == cod_tipo_sel, "367"].values[0] if subprod_sel == "367" else 0.0
else:
    val_tabla = df_matriz.loc[df_matriz['CODIGO TIPO'] == cod_tipo_sel, subprod_sel].values[0]

tasa_base = obtener_tasa(val_asegurado, tarifa_sel)
prima_min_smmlv = val_tabla * smmlv_sel
prima_min_tasa = tasa_base * val_asegurado

# RESULTADO PRIMA MÍNIMA
prima_minima = max(prima_min_smmlv, prima_min_tasa)

st.success(f"📌 **Prima Mínima Requerida (S/I): ${prima_minima:,.0f}**")
st.markdown("---")

# --- 7. ENTRADA DE DATOS: VALORES DE COTIZACIÓN ---
st.subheader("2. Datos de la Oferta")
v1, v2, v3 = st.columns(3)
with v1:
    p_final_sin_iva = st.number_input("Prima Final SIN IVA (Base)", min_value=0.0, value=2000000.0)
with v2:
    p_total_sin_iva = st.number_input("Prima Final TOTAL SIN IVA", min_value=0.0, value=2200000.0)
with v3:
    target_iva = st.number_input("TARGET: Prima Final CON IVA Deseado", min_value=0.0, value=2500000.0)

# --- 8. LÓGICA DE CALCULO Y VALIDACIÓN FINAL ---
if st.button("Ejecutar Análisis Actuarial"):
    target_sin_iva = target_iva / 1.19
    st.subheader("3. Resultados del Análisis")
    
    # COMPARACIÓN CRÍTICA: Target vs Prima Mínima
    if target_sin_iva < prima_minima:
        st.markdown(f"""
        <div class="mensaje-error">
            <h4 style="margin:0; color:#D32F2F;">❌ OPERACIÓN NO POSIBLE</h4>
            <p style="color:#333; margin:10px 0;">
                El Target sin IVA deseado (<b>${target_sin_iva:,.0f}</b>) es inferior a la 
                Prima Mínima Requerida (<b>${prima_minima:,.0f}</b>).
            </p>
            <p style="font-weight:bold; color:#D32F2F;">% Entregable: No disponible por debajo del mínimo.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # CÁLCULOS SI PASA EL FILTRO
        coberturas_adi = p_total_sin_iva - p_final_sin_iva
        target_base_final = target_sin_iva - coberturas_adi
        
        # % Entregable
        diferencia = (target_base_final / p_final_sin_iva) - 1 if p_final_sin_iva != 0 else 0.0
        pc_entregable = diferencia * 100
        
        # Verificaciones
        nueva_p_sin_iva = p_final_sin_iva * (1 + diferencia)
        nueva_p_total_con_iva = (nueva_p_sin_iva + coberturas_adi) * 1.19
        dto_real = ((nueva_p_total_con_iva / (p_total_sin_iva * 1.19)) - 1) * 100

        # Mostrar % Entregable Resaltado
        st.markdown(f"""
        <div class="mensaje-exito">
            <h3 style="margin: 0; color: #0A6A34;">🎯 % Entregable: {pc_entregable:,.2f}%</h3>
            <p style="margin: 5px 0 0 0; color: #333;">La oferta cumple con el requisito de Prima Mínima.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Métricas de apoyo
        r1, r2, r3 = st.columns(3)
        r1.metric("Nueva Prima Total (C/I)", f"${nueva_p_total_con_iva:,.2f}")
        r2.metric("Descuento Comercial", f"{dto_real:,.2f}%")
        r3.metric("Valor Tabla Usado", f"{val_tabla}")
