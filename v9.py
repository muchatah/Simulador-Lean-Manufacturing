import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Simulador Lean - Botellas Térmicas", layout="wide")

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .portada {
        background-color: #f1f3f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 8px solid #1f77b4;
        color: #333 !important;
        margin-bottom: 20px;
    }
    [data-testid="stSidebar"] {
        min-width: 550px;
        max-width: 550px;
    }
    .header-input {
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        border-bottom: 2px solid #1f77b4;
        margin-bottom: 10px;
        font-size: 0.9em;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #1f77b4 !important; 
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# BARRA LATERAL (ENTRADA DE DATOS ORDENADA)
# ==========================================
st.sidebar.header("📥 CONFIGURACIÓN DE DATOS")

def row_input(label, val_a, val_d, unit, key_suffix):
    col1, col2, col3, col4 = st.columns([2.5, 1.5, 1.5, 1])
    with col1: st.write(f"**{label}**")
    with col2: a = st.number_input("A", value=float(val_a), key=f"{key_suffix}_a", label_visibility="collapsed")
    with col3: d = st.number_input("D", value=float(val_d), key=f"{key_suffix}_d", label_visibility="collapsed")
    with col4: st.write(f"*{unit}*")
    return a, d

with st.sidebar.expander("📊 VARIABLES DE OPERACIÓN Y COSTO", expanded=True):
    st.markdown('<p class="header-input">Variable | Antes | Después | Unidad</p>', unsafe_allow_html=True)
    op_a, op_d = row_input("Operarios", 6, 5, "pers", "op")
    hr_a, hr_d = row_input("Horas/Turno", 8, 8, "h", "hr")
    ub_a, ub_d = row_input("Unid. Buenas", 378, 400, "unid", "ub")
    ui_a, ui_d = row_input("Unid. Iniciadas", 420, 410, "unid", "ui")
    pv_a, pv_d = row_input("Precio Venta", 65, 65, "S/", "pv")
    cm_a, cm_d = row_input("Costo Material", 26, 26, "S/", "cm")
    tl_a, tl_d = row_input("Tarifa Laboral", 18, 18, "S/hh", "tl")
    gg_a, gg_d = row_input("Gasto General", 22, 22, "S/h", "gg")
    oav_a, oav_d = row_input("OAV", 5.2, 5.0, "min", "oav")
    onav_a, onav_d = row_input("ONAV", 3.3, 1.0, "min", "onav")

with st.sidebar.expander("🚫 LAS 8 MUDAS (min/turno)", expanded=False):
    st.markdown('<p class="header-input">Tipo | Antes | Después | Unidad</p>', unsafe_allow_html=True)
    m_esp = row_input("Espera", 70, 18, "min", "m1")
    m_tra = row_input("Transporte", 35, 12, "min", "m2")
    m_mov = row_input("Movimiento", 30, 10, "min", "m3")
    m_ins = row_input("Inspección", 25, 5, "min", "m4")
    m_sop = row_input("Sobreproc.", 0, 0, "min", "m5")
    m_spr = row_input("Sobreprod.", 0, 0, "min", "m6")
    m_inv = row_input("Inventario", 0, 0, "min", "m7")
    m_def = row_input("Defectos", 45, 15, "min", "m8")
    m_tal = row_input("Talento", 0, 0, "min", "m9")

# --- LÓGICA DE CÁLCULO ---
def calcular_full(esc):
    if esc == "A":
        o, h, ub, ui, pv, cm, tl, gg, oav, onav = op_a, hr_a, ub_a, ui_a, pv_a, cm_a, tl_a, gg_a, oav_a, onav_a
    else:
        o, h, ub, ui, pv, cm, tl, gg, oav, onav = op_d, hr_d, ub_d, ui_d, pv_d, cm_d, tl_d, gg_d, oav_d, onav_d
    
    hh = o * h
    v_salida = ub * pv
    c_mat = ui * cm
    c_mo = hh * tl
    c_gg = h * gg
    c_total = c_mat + c_mo + c_gg
    
    p_mo = ub / hh if hh > 0 else 0
    p_tot = v_salida / c_total if c_total > 0 else 0
    cd = 1 + (onav / oav) if oav > 0 else 0
    pce = (oav / (oav + onav)) * 100 if (oav + onav) > 0 else 0
    c_unit = c_total / ub if ub > 0 else 0
    t_min = (c_mo + c_gg) / (h * 60) if h > 0 else 0
    
    return [hh, v_salida, c_mat, c_mo, c_gg, c_total, p_mo, p_tot, cd, pce, c_unit, t_min]

res_a = calcular_full("A")
res_d = calcular_full("D")

# ==========================================
# ESTRUCTURA DE PESTAÑAS (OUTPUTS)
# ==========================================
tab1, tab2, tab3 = st.tabs(["📥 1. EQUIPO Y RESUMEN KPI", "📊 2. ANÁLISIS DE COSTOS", "📝 3. ANÁLISIS Y REFLEXIÓN"])

# --- PESTAÑA 1 ---
with tab1:
    st.markdown("""<div class="portada"><h1>LEAN MANUFACTURING</h1><p><b>NRC:</b> 35625</p><p><b>DOCENTE:</b> Nieto Astahuaman, Carlos Alberto</p></div>""", unsafe_allow_html=True)
    st.subheader("👥 Integrantes del Grupo:")
    st.text("- Meza Barreto Breggitt Solansh\n- Mucha Villar Tahirih\n- Quilca Mendoza Jose")
    st.markdown("---")
    st.header("📋 Resumen y Fórmulas")
    with st.expander("Ver Fórmulas Aplicadas"):
        st.markdown("* **Productividad MO** = Unid. buenas / HH\n* **Prod. Total** = Valor salida / Costo Total\n* **Cd** = 1 + ONAV/OAV\n* **PCE** = OAV/(OAV+ONAV)\n* **Costo unitario** = Costo Total / Unid. buenas")

    st.subheader("Comparación de KPIs")
    kpi_df = pd.DataFrame({
        "Indicador": ["Productividad MO", "Productividad Total", "Coef. Desperdicio (Cd)", "PCE (%)", "Costo Unitario"],
        "Antes Lean": [res_a[6], res_a[7], res_a[8], res_a[9], res_a[10]],
        "Después Lean": [res_d[6], res_d[7], res_d[8], res_d[9], res_d[10]],
        "Unidad": ["unid/hh", "Ratio", "Ratio", "%", "S/"]
    })
    def calc_mejora(row):
        a, d, n = row["Antes Lean"], row["Después Lean"], row["Indicador"]
        if a == 0: return "0.00%"
        m = ((a - d)/a*100) if ("Costo" in n or "Cd" in n) else ((d - a)/a*100)
        return f"{m:.2f}%"
    kpi_df["Mejora"] = kpi_df.apply(calc_mejora, axis=1)
    st.table(kpi_df.style.format({"Antes Lean": "{:.2f}", "Después Lean": "{:.2f}"}))

    if st.button("🔄 Actualizar Gráfico de KPIs"):
        plt.clf()
        fig_kpi, ax_kpi = plt.subplots(figsize=(8, 4))
        x = range(len(kpi_df["Indicador"]))
        ax_kpi.bar(x, kpi_df["Antes Lean"], width=0.3, label='Antes Lean', color='#a3c1ad')
        ax_kpi.bar([i + 0.3 for i in x], kpi_df["Después Lean"], width=0.3, label='Después Lean', color='#1f77b4')
        ax_kpi.set_xticks([i + 0.15 for i in x])
        ax_kpi.set_xticklabels(kpi_df["Indicador"], fontsize=7, rotation=35, ha='right')
        ax_kpi.legend(fontsize=8)
        plt.tight_layout()
        st.pyplot(fig_kpi)
        plt.close()

# --- PESTAÑA 2 ---
with tab2:
    st.header("📊 Análisis Económico")
    st.subheader("1. Indicadores Detallados")
    detalles = pd.DataFrame({
        "Indicador": ["Horas Hombre", "Valor de Salida", "Costo de Materiales", "Costo de Mano de Obra", "Gastos Generales", "Costo Total", "Costo Unitario"],
        "Antes": [res_a[0], res_a[1], res_a[2], res_a[3], res_a[4], res_a[5], res_a[10]],
        "Después": [res_d[0], res_d[1], res_d[2], res_d[3], res_d[4], res_d[5], res_d[10]],
        "Unidad": ["hh", "S/", "S/", "S/", "S/", "S/", "S/"]
    })
    st.dataframe(detalles, use_container_width=True)

    st.subheader("2. Costo del Desperdicio")
    df_muda = pd.DataFrame({
        "Tipo": ["Espera", "Transporte", "Movimiento", "Inspección", "Sobreproc.", "Sobreprod.", "Inventario", "Defectos", "Talento"],
        "Antes Min": [m_esp[0], m_tra[0], m_mov[0], m_ins[0], m_sop[0], m_spr[0], m_inv[0], m_def[0], m_tal[0]],
        "Después Min": [m_esp[1], m_tra[1], m_mov[1], m_ins[1], m_sop[1], m_spr[1], m_inv[1], m_def[1], m_tal[1]],
    })
    df_muda["Costo Antes"] = df_muda["Antes Min"] * res_a[11]
    df_muda["Costo Desp"] = df_muda["Después Min"] * res_d[11]
    df_muda["Ahorro"] = df_muda["Costo Antes"] - df_muda["Costo Desp"]
    st.dataframe(df_muda.style.format({"Costo Antes": "{:.2f}", "Costo Desp": "{:.2f}", "Ahorro": "{:.2f}"}), use_container_width=True)

    if st.button("📊 Generar Pareto Actualizado"):
        plt.clf()
        df_p = df_muda[df_muda["Costo Antes"] > 0].sort_values("Costo Antes", ascending=False)
        if not df_p.empty:
            df_p["% Acum"] = (df_p["Costo Antes"].cumsum() / df_p["Costo Antes"].sum() * 100)
            fig_p, ax_p1 = plt.subplots(figsize=(8, 4.5))
            ax_p1.bar(df_p["Tipo"], df_p["Costo Antes"], color="#1f77b4")
            ax_p1.set_ylabel("Costo (S/)")
            plt.xticks(rotation=35, ha='right', fontsize=8)
            ax_p2 = ax_p1.twinx()
            ax_p2.plot(df_p["Tipo"], df_p["% Acum"], color="#d62728", marker="D", linewidth=2, ms=6)
            ax_p2.set_ylim(0, 110)
            ax_p2.set_ylabel("% Acumulado", color="#d62728")
            plt.tight_layout()
            st.pyplot(fig_p)
            plt.close()

# --- PESTAÑA 3 ---
with tab3:
    st.header("📝 Análisis y Reflexión")
    mayor_muda = df_muda.loc[df_muda['Costo Antes'].idxmax()]
    impacto_total = (res_a[10] - res_d[10]) / res_a[10] * 100
    st.write(f"De acuerdo con los datos actuales, el desperdicio que impacta más el costo es **{mayor_muda['Tipo']}**, generando un gasto de **S/ {mayor_muda['Costo Antes']:.2f}** por turno.")
    st.write(f"La implementación Lean ha logrado una reducción del costo unitario del **{impacto_total:.2f}%**.")
    st.subheader("Preguntas de Reflexión")
    with st.expander("¿Puede una línea con menos operarios producir más?"):
        st.write("Sí. Bajo el enfoque Lean, al eliminar actividades que no agregan valor (desperdicios), el personal restante se enfoca exclusivamente en tareas de valor añadido, mejorando el flujo y la capacidad de salida total.")
    with st.expander("Relación desperdicio, productividad y costo?"):
        st.write("Existe una relación crítica: a medida que el desperdicio disminuye, la productividad aumenta, lo que permite diluir los costos fijos en una mayor cantidad de unidades buenas, reduciendo así el costo unitario.")
    with st.expander("Si el precio de venta no cambia, ¿por qué reducir desperdicio mejora la rentabilidad?"):
        st.write("Porque la rentabilidad es la diferencia entre el precio y el costo. Al reducir el desperdicio se baja el costo total de operación, y dado que el precio es fijo, el margen de utilidad crece directamente.")
