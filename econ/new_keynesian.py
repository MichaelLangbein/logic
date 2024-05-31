#%%
import numpy as np
import matplotlib.pyplot as plt



def radioPlot(labels, plotData, ax = None):
    isSubplot = ax is not None
    if not isSubplot:
        _, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    angles = np.linspace(0, 2 * np.pi, len(labels) + 1, endpoint=False).tolist()
    for (stats, label, color) in plotData:
        ax.fill(angles[:-1], stats, color=color, alpha=0.25)
        ax.plot(angles[:-1], stats, color=color, linewidth=1, label=label)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    if not isSubplot:
        plt.legend()
        plt.show()

def radioPlotRow(labels, titleLeft, plotDataLeft, titleRight, plotDataRight):
    _, axes = plt.subplots(1, 2, subplot_kw=dict(polar=True))
    radioPlot(labels, plotDataLeft, axes[0])
    axes[0].set_title(titleLeft)
    radioPlot(labels, plotDataRight, axes[1])
    axes[1].set_title(titleRight)
    plt.show()



#%%
def simulate(
        i_a, 
        i_Y, 
        i_r,
        r, # real interest rate
        t_a,
        t_w,
        c_a,
        c_w,
        a, # Cobb-Douglass factor
        G0, # government spending
        balancedBudget = False
):
    # setting initial values
    I = T = C = Y = L = 1
    
    for _ in range(100):
        I = i_a + i_Y * Y - i_r * r
        T = t_a + t_w * Y
        C = c_a + c_w * (Y - T)
        G = T if balancedBudget else G0
        Y = C + G + I
        L = Y
    
    return I, T, C, Y, L


stats1 = simulate(i_a=1, i_Y=0.2, i_r=0.2, r=10, t_a=1, t_w=0.3, c_a=2, c_w=0.5, G0=10, a=0.5, balancedBudget=False)
stats2 = simulate(i_a=1, i_Y=0.2, i_r=0.2, r=1,t_a=1, t_w=0.3, c_a=2, c_w=0.5, G0=10, a=0.5, balancedBudget=False)
stats3 = simulate(i_a=1, i_Y=0.2, i_r=0.2, r=10, t_a=1, t_w=0.3, c_a=2, c_w=0.5, G0=10, a=0.5, balancedBudget=False)
stats4 = simulate(i_a=1, i_Y=0.2, i_r=0.2, r=10,t_a=1, t_w=0.3, c_a=2, c_w=0.5, G0=15, a=0.5, balancedBudget=False)


radioPlotRow(
    ["I", "T", "C", "Y", "L"], 
    "decreased interest",
    [
        (stats1, "baseline", "red"),
        (stats2, "low interest", "blue")
    ],
    "increased govt",
    [
        (stats3, "baseline", "red"),
        (stats4, "high govt", "blue")
    ],
)
"""
monetary policy -> decreased interest -> more investment, gdp
fiscal policy -> more govt. spending -> more gdp

Fiscal policy seems to have a stronger effect on employment than monetary policy does.
"""


# %%

def simulate(
        T = 50,      # time steps
        b = 2,       # wage bargaining: base demands
        k = 0.5,     # wage bargaining: labor sensitive demands
        c_a = 2,     # consumption, autonomous
        c_y = 0.5,   # consumption, wage sensitive
        a_a = 0.5,   # investment, autonomous
        a_y = 0.5,   # investment, demand sensitive
        a_r = 0.5,   # investment, interest-rate sensitive
        t_a = 0.5,   # taxes, base interest-rate
        t_y = 0.25,  # taxes, wage sensitive
        p = 1,       # labor productivity
        m = 0.1,     # gains markup
        beta = 1,    # fed inflation/unemployment sensitivity,
        PiT = 0.05,  # target inflation
        G = 5,       # government spending
        Yeq = 5,     # equilibrium production=goods-demand=employment*productivity && wage-demand=wage-supply, as determined by both goods- and factor-markets
):

    A = (c_a + c_y * t_a + a_a + G) / (1 - c_y + c_y * t_y - a_y)
    alpha = a_r / (1 - c_y + c_y * t_y - a_y)
    rEq = (A - Yeq) / alpha
    Leq = Yeq / p

    # core variables
    Y = np.ones(T)
    r = np.ones(T)
    Pi = np.ones(T)

    # derived
    w_nom = np.ones(T)
    L = np.ones(T)
    P = np.ones(T)

    # initial values: everything normal except goods-market requires more labor than the current wage-equilibrium
    Y[0] = Yeq + 0.5   # shock: had to produce more because high demand on goods-market
    L[0] = Y[0]/p      # Thus had to hire more people
    r[0] = rEq         # r, Pi, w_nom have not yet adjusted
    Pi[0] = PiT
    w_nom[0] = b + k*(Yeq/p)
    P[0] = (1 + m) * (w_nom[0] / p)

    for t in range(1, T):

        # core variables
        # IS curve: productivity(interest-rate)
        Y[t] = A - alpha * r[t-1]
        # Phillips curve: inflation(Labor)
        Pi[t] = Pi[t-1] - k*(L[t-1] - Leq)
        ## Central bank: rate(inflation)
        cte = k / (alpha * (1 + (beta*k*k)/p))
        r[t] = rEq - beta * cte * (Pi[t-1] - PiT)

        # derived
        L[t] = Y[t] / p
        delta_w_nom = (Pi[t-1] - k*(L[t] - Leq)) * w_nom[t-1]
        w_nom[t] = w_nom[t-1] + delta_w_nom
        P[t] = (1 + m) * (w_nom[t] / p)

    return Y, L, r, Pi, w_nom, P


T = 50
Ts = np.arange(0, T, 1)
Y, L, r, Pi, w_nom, P = simulate(T=T)

plt.plot(Ts, r)
# %%
