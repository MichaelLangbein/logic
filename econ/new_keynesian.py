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

def simulate2(
        # IS curve
        A: np.ndarray, 
        alpha: float,
        # Phillips curve
        Yeq: np.ndarray,
        k: float,
        # Stabilizing interest
        # Fed policy
        gamma: float,
        piTarget: np.ndarray
):
    """
        IS curve: derived from firm's demands
        $Y_t = A - \alpha r_{t-1}$

        Phillips curve: derived from wage setting in factor market
        $\pi = \pi_{-1} - k(L - L^{eq})$

        Stabilizing interest rate (IS curve at Y^{eq})
        $r^{eq} = (A - Y^{eq}) / \alpha$

        Fed policy: loss function d/dL, substitute IS curve
        $r_t = r^{eq} + \gamma (\pi - \pi^T)$
    """

    T = 50
    Y = np.zeros((T))
    r = np.zeros((T))
    pi = np.zeros((T))
    Y[0] = 1
    r[0] = 1.01
    pi[0] = 0.01

    for t in range(1, T):
        # Productivity from IS curve
        Y[t] = A[t] - alpha * r[t-1]
        # Inflation from Phillips curve
        pi[t] = pi[t-1] - k * (Y[t] - Yeq[t])
        # Equilibrium-interest r_eq from IS curve
        req = (A[t] - Yeq[t]) / alpha
        # Fed sets real interest according to fed-policy
        r[t] = req + gamma * (pi[t] - piTarget[t])

    return Y, r, pi

T = 50
A = np.ones(T) * 10
Yeq = np.ones(T) * 5
YeqShock = np.ones(T) * 5
YeqShock[20:] = 10
piTarget = np.ones(T) * 0.05
Y1, r1, pi1 = simulate2(A=A, alpha=0.1, Yeq=Yeq,      k=0.01, gamma=1, piTarget=piTarget)
Y2, r2, pi2 = simulate2(A=A, alpha=0.1, Yeq=YeqShock, k=0.01, gamma=1, piTarget=piTarget)


ts = np.linspace(0, T)

plt.plot(ts, r1)
plt.plot(ts, r2)
# %%
