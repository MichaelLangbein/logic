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
import numpy as np
import matplotlib.pyplot as plt

def simulate(
        G: np.ndarray,       # government spending
        beta: np.ndarray,    # fed inflation/unemployment sensitivity,
        PiT: np.ndarray,     # target inflation
        w_a = 2,       # wage bargaining: base demands
        w_L = 0.5,     # wage bargaining: labor sensitive demands
        c_a = 2,     # consumption, autonomous
        c_Y = 0.5,   # consumption, wage sensitive
        i_a = 0.5,   # investment, autonomous
        i_Y = 0.5,   # investment, demand sensitive
        i_r = 0.5,   # investment, interest-rate sensitive
        t_a = 0.5,   # taxes, base interest-rate
        t_y = 0.25,  # taxes, wage sensitive
        p = 1,       # labor productivity
        m = 0.1,     # gains markup
):
    T = len(G)

    Y     = np.ones(T) * 100
    LN    = np.ones(T) * 100
    r     = np.ones(T)
    Pi    = np.ones(T)
    w_nom = np.ones(T)
    L     = np.ones(T) * 100
    P     = np.ones(T)

    # first values
    # r[0] = 1
    # A     = (c_a + c_Y * t_a + i_a + G[0]) / (1 - c_Y + c_Y * t_y - i_Y)
    # alpha = i_r / (1 - c_Y + c_Y * t_y - i_Y)
    # Y[0] = A - alpha * r[0]
    # L[0] = Y[0] / p
    # w_nom[0] = w_a + w_L * L[0]
    # Pi[0] = PiT[0]
    # P[0] = (1+m) * w_nom[0] / p
  
    for t in range(1, T):

        # 1. given the last interest rate, some output is produced
        A     = (c_a + c_Y * t_a + i_a + G[t]) / (1 - c_Y + c_Y * t_y - i_Y)
        alpha = i_r / (1 - c_Y + c_Y * t_y - i_Y)
        Y[t] = A - alpha * r[t-1]
        L[t] = Y[t] / p

        # 2. unions demand a change in nominal wages 
        delta_w_nom_normalized = Pi[t-1] - w_L * (L[t] - LN[t])
        w_nom[t] = w_nom[t-1] + delta_w_nom_normalized * w_nom[t-1]

        # 3. under these new wages, the negotiated labor supply LN would be:
        LN[t] = (1/w_L) * (p/(1+m) - w_a)

        # 4. firms adjust prices to maintain $m$
        P[t] = (1+m) * w_nom[t] / p

        # 5. this increases inflation
        Pi[t] = Pi[t-1] - w_L * (L[t] - LN[t])
        # Pi[t] = (P[t] - P[t-1]) / P[t-1] <-- should be the same value

        # 6. fed adjusts r to minimize unemployment and inflation
        r[t] = (LN[t]/p - A)/alpha - (beta[t] * w_L) / (alpha * (1 - beta[t] * w_L * w_L)) * (Pi[t] - PiT[t])
        r[t] = np.max([0.0, r[t]])

    return Y, L, LN, r, Pi, w_nom, P


T = 20
Ts = np.arange(0, T, 1)
G = np.ones(T) * 5
beta = np.ones(T) * 1
PiT = np.ones(T) * 0.05
Y, L, LN, r, Pi, w_nom, P = simulate(G=G, beta=beta, PiT=PiT)

fig, axes = plt.subplots(4, 1)
axes[0].plot(Ts, L, label="L")
axes[0].plot(Ts, LN, label="LN")
axes[0].legend()
axes[1].plot(Ts, Pi, label="Pi")
axes[1].plot(Ts, PiT, label="PiT")
axes[1].legend()
axes[2].plot(Ts, r, label="r")
axes[2].legend()
axes[3].plot(Ts, P, label="P")
axes[3].plot(Ts, w_nom, label="w_nom")
axes[3].legend()
# %%
