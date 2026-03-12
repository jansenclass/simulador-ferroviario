import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output

def simular_ferrovia_percentual(p_kw, tec_kn, n_loc, n_vag, rampa_percent, raio_curva):
    clear_output(wait=True)
    
    v = np.linspace(1, 120, 500)
    peso_loc, peso_vag = 180, 120 # t
    v_min, eta_padrao = 15, 0.82
    
    # 1. ESFORÇO TRATOR (Ft)
    f_ad = 0.24 * (peso_loc * 10) * n_loc
    f_el = tec_kn * n_loc
    f_pot = (n_loc * eta_padrao * 3.6 * p_kw) / v
    ft = np.minimum(f_ad, np.minimum(f_el, f_pot))
    
    # 2. RESISTÊNCIAS (R)
    g_total = (n_loc * peso_loc) + (n_vag * peso_vag)
    
    # Davis Inerente
    r_inerente = (1.3 * g_total + 29 * (n_loc*6 + n_vag*4) + 0.01 * g_total * v + 0.0005 * 14.5 * v**2) / 100
    
    # Resistência de Rampa (Rg) - Convertendo % para força
    # Rg = G * (i/100) * g (aceleração gravidade)
    r_rampa = g_total * (rampa_percent / 100) * 9.81
    
    # Resistência de Curva (Rc)
    if raio_curva > 0:
        r_curva = g_total * (700 / raio_curva) / 100
    else:
        r_curva = 0

    r_total = r_inerente + r_rampa + r_curva

    # 3. PLOTAGEM
    plt.figure(figsize=(12, 6))
    plt.plot(v, ft, 'r-', label='Esforço Trator ($F_t$)', linewidth=3)
    plt.plot(v, r_total, 'b--', label='Resistência Total ($R$)', linewidth=2)
    
    # Ponto de Equilíbrio
    idx = np.argwhere(np.diff(np.sign(ft - r_total))).flatten()
    if len(idx) > 0:
        v_eq = v[idx[0]]
        plt.plot(v_eq, ft[idx[0]], 'go', markersize=12)
        plt.annotate(f'V_eq: {v_eq:.1f} km/h', (v_eq+2, ft[idx[0]]+30), weight='bold', fontsize=12)

    plt.title(f'Simulador USP: Rampa de {rampa_percent}% e Curva de {raio_curva}m', fontsize=14)
    plt.xlabel('Velocidade (km/h)')
    plt.ylabel('Força (kN)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()

# INTERFACE COM RAMPA EM %
style = {'description_width': 'initial'}
ui_percent = widgets.VBox([
    widgets.HBox([
        widgets.IntSlider(value=3952, min=2000, max=5000, description='Potência (kW):', style=style),
        widgets.IntSlider(value=500, min=300, max=800, description='TEC (kN):', style=style)
    ]),
    widgets.HBox([
        widgets.IntSlider(value=2, min=1, max=4, description='Locomotivas:', style=style),
        widgets.IntSlider(value=40, min=1, max=100, description='Vagões:', style=style)
    ]),
    widgets.HBox([
        widgets.FloatSlider(value=0.5, min=0, max=3.0, step=0.1, description='Rampa (%):', style=style),
        widgets.IntSlider(value=1000, min=200, max=5000, step=50, description='Raio Curva (m):', style=style)
    ])
])

out_percent = widgets.interactive_output(simular_ferrovia_percentual, {
    'p_kw': ui_percent.children[0].children[0], 'tec_kn': ui_percent.children[0].children[1],
    'n_loc': ui_percent.children[1].children[0], 'n_vag': ui_percent.children[1].children[1],
    'rampa_percent': ui_percent.children[2].children[0], 'raio_curva': ui_percent.children[2].children[1]
})

display(ui_percent, out_percent)
