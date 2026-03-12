import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Simulador Ferroviário - Jansen", layout="wide")

st.title("🚂 Simulador de Dinâmica Ferroviária")
st.sidebar.header("Parâmetros de Entrada")

# Sliders na barra lateral
p_kw = st.sidebar.number_input("Potência (kW)", value=3077)
tec_kn = st.sidebar.number_input("TEC (kN)", value=500)
n_loc = st.sidebar.slider("Nº de Locomotivas", 1, 4, 2)
n_vag = st.sidebar.slider("Nº de Vagões", 1, 100, 40)
rampa = st.sidebar.slider("Rampa (%)", 0.0, 3.0, 0.5, 0.1)
raio = st.sidebar.number_input("Raio da Curva (m)", value=1000)

# Cálculos
v = np.linspace(1, 120, 500)
peso_loc, peso_vag = 180, 120
eta = 0.82

# Esforço Trator
f_ad = 0.24 * (peso_loc * 10) * n_loc
f_pot = (n_loc * eta * 3.6 * p_kw) / v
ft = np.minimum(f_ad, np.minimum(tec_kn * n_loc, f_pot))

# Resistências
g_total = (n_loc * peso_loc) + (n_vag * peso_vag)
r_inerente = (1.3 * g_total + 29 * (n_loc*6 + n_vag*4) + 0.01 * g_total * v + 0.0005 * 14.5 * v**2) / 100
r_rampa = g_total * (rampa / 100) * 9.81
r_curva = g_total * (700 / raio) / 100 if raio > 0 else 0
r_total = r_inerente + r_rampa + r_curva

# Gráfico
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(v, ft, 'r-', label='Esforço Trator ($F_t$)', linewidth=2)
ax.plot(v, r_total, 'b--', label='Resistência ($R$)', linewidth=2)

idx = np.argwhere(np.diff(np.sign(ft - r_total))).flatten()
if len(idx) > 0:
    v_eq = v[idx[0]]
    ax.plot(v_eq, ft[idx[0]], 'go', markersize=10)
    st.success(f"Velocidade de Equilíbrio: {v_eq:.1f} km/h")

ax.set_xlabel("Velocidade (km/h)")
ax.set_ylabel("Força (kN)")
ax.legend()
ax.grid(True, alpha=0.3)
st.pyplot(fig)
