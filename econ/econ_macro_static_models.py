

#%%
import matplotlib.pyplot as plt
import numpy as np


def radioPlot(labels, stats1, stats2, label1, label2):
    angles = np.linspace(0, 2 * np.pi, len(labels) + 1, endpoint=False).tolist()
    _, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles[:-1], stats1, color='red', alpha=0.25)
    ax.fill(angles[:-1], stats2, color='blue', alpha=0.25)
    ax.plot(angles[:-1], stats1, color='red', linewidth=2, label=label1)
    ax.plot(angles[:-1], stats2, color='blue', linewidth=2, label=label2)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    plt.legend()
    plt.show()

#%%
"""
The neoclassical model is the only macro economic model that still optimizes profit (for firms) and utility (for households)
It assumes households are very rational and know that today's government spending must be financed with tomorrow's taxes.
It implies Ricardo-Barro effect (demand is unchanged when government tries to stimulate the economy by debt-financed spending).
That seems quite unrealistic, but it describes an economy where everyone
is rational and budgets are (in the long term) balanced.
"""

def neoclassical(
        A = 2,       # productivity
        a = 0.3,     # Douglass-Cobb factor
        b1 = 0.4,    # household preference for leisure
        b2 = 0.9,    # discount rate
        b3 = 0.6,    # household preference for money
        G0 = 1,      # Government spending
        Gf = 1,      # future government spending
        Yf = 1,      # expected future productivity
        M0 = 5,      # money supply
        K = 5,       # capital (exogenous)
        pe = 0.02    # expected future profit
):
    
    # Initialise endogenous variables at arbitrary positive value
    w = C = I = Y = r = N = P = 1 
    
    for _ in range(1000):
        
        # Cobb douglass production
        Y = A * K**a * N**(1-a)

        # Labor demand
        w = A * (1-a) * K**a * N**(-a)

        # Labor supply
        N = 1 - b1/w

        # Consumption demand
        C = (1/(1 + b2 + b3)) * (Y - G0 + (Yf - Gf)/(1+r)   - b1*(b2+b3) * np.log(b1/w))

        # Investment demand, solved for r
        r = I**(a-1) * a * A * N**(1-a)

        # Goods market equilibrium, solved for I
        I = Y - C - G0

        # Nominal interest rate
        rn = r + pe

        # Price level
        P = (M0 * rn) / ((1 + rn) * b3 * C)

    return w , C , I , Y , r , N , P 


stats1 = neoclassical()
stats2 = neoclassical(G0=1.5)
radioPlot(["w" , "C" , "I" , "Y" , "r" , "N" , "P"], stats1, stats2, "baseline", "fiscal policy")

# %%

"""
Neo-classical synthesis model
- no longer optimizes for profit (firms) or utility (households)

- monetary policy:
    - fed spending
    - affects mostly investment?
- fiscal policy:
    - government spending
    - affects mostly consumption?
"""


def neoclassicalSynthesis(       
    c0 = 2    ,  # autonomous consumption
    c1 = 0.6  ,  # sensitivity of consumption w.r.t. income
    i0 = 2    ,  # investment demand (aka. animal spirits)
    i1 = 0.1  ,  # sensitivity of investment w.r.t. interest rate
    A = 2     ,  # productivity
    Pe = 1    ,  # expected price level
    m0 = 6    ,  # liquidity preference
    m1 = 0.2  ,  # sensitivity of money demand w.r.t. income
    m2 = 0.4  ,  # sensitivity of money demand w.r.t. interest rate
    M0 = 5    ,  # money demand
    G0 = 1    ,  # government spending
    T0 = 1    ,  # taxes
    K0 = 1    ,  # capital stock (exogenous)
    Nf = 7    ,  # full employment
    a = 0.3   ,  # capital elasticity of output
    b = 0.4   ,  # household preference for leisure
):
    """
    https://macrosimulation.org/a_neoclassical_synthesis_model_is_lm_as_ad
    """

    # Endogenous variables
    Y = C = I = r = P = w = N = W = 1

    for _ in range(100):

        # Goods market equilibrium
        Y = C + I + G0

        # Consumption demand
        C = c0 + c1 * (Y - T0)

        # Investment demand
        I = i0 - i1 * r

        # Money market, solved for interest rate
        r = (m0 - (M0/P)) / m2  +  m1 * Y/m2

        # Unemployment rate
        U = 1 - N/Nf

        # Real wage
        w = A * (1-a) * K0**a * N**(-a)

        # Nominal wage
        W = Pe * b * C / U

        # Price level
        P = W / w

        # Employment
        N = (Y / (A * K0**a))**(1/(1-a))

    return Y, C, I, r, U, w, W, P, N


stats1 = neoclassicalSynthesis()
stats2 = neoclassicalSynthesis(G0=1.125)
radioPlot(["Y", "C", "I", "r", "U", "w", "W", "P", "N"], stats1, stats2, "baseline", "fiscal policy")


#%%


# Post keynesian with endogenous money
def postKeynesianWithMoney(
    b = 0.5,    # propensity to spend out of income
    c = 0.7,    # share of credit-demand that is accommodated
    d0 = 5,     # autonomous demand, debt-financed
    d1 = 0.8,   # sensitivity of demand w.r.t. interest rate
    i0 = 0.01,  # central bank rate, discretionary component
    i1 = 0.5,   # sensitivity of central bank rate w.r.t. price level
    m = 0.15,   # banks' interest rate markup
    k = 0.3,    # desired reserve ratio
    n = 0.15,   # price mark-up
    W0 = 2,     # nominal wage (exogenous)
    h = 0.8,    # sensitivity of nominal wage w.r.t. unemployment
    a = 0.8,    # productivity
    Nf = 12     # full employment
):
    """
    https://macrosimulation.org/a_post_keynesian_macro_model_with_endogenous_money#overview
    """

    for _ in range(1000):
        # Initialize endogenous variables at some arbitrary positive value
        Y = D = ND = r = N = U = P = w = W = i = dL = dR = dM = 1

        # Goods market
        Y = ND + c * D

        # Non-debt financed component of demand
        ND = b * Y

        # Debt financed component of demand
        D = d0 - d1 * r

        # Policy rate
        # Assumes that fed raises interest when prices increase
        i = i0 + i1 * P

        # Lending rate
        # Banks lend at policy rate plus markup
        r = (1 + m) * i

        # Change in loans
        dL = c * D

        # Change in deposits
        dM = dL

        # Change in reserves
        dR = k * dM

        # Price level
        # Firms charge at production cost plus markup
        P =  (1 + n) * a * W

        # Nominal wage
        # base wage, lower if high unemployment
        W = W0 - h * U

        # Real wage
        w = 1 / ((1+n) * a)

        # Employment
        N = a * Y

        # Unemployment
        U = (Nf - N) / Nf

    return Y, D, ND, r, N, U, P, w, W, i, dL, dR, dM


stats1 = postKeynesianWithMoney()
stats2 = postKeynesianWithMoney(c=0.9)


labels = ["Y", "D", "ND", "r", "N", "U", "P", "w", "W", "i", "dL", "dR", "dM" ]
radioPlot(labels, stats1, stats2, "baseline", "more lending")
# %%
