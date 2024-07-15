#%%
import numpy as np
import matplotlib.pyplot as plt

#%%



def simulate(A, pt, ye):
    Q = len(A)

    # Create arrays to store simulated data
    y = np.zeros(Q)  # Income/output
    p = np.zeros(Q)  # Inflation rate
    r = np.zeros(Q)  # Real interest rate
    rs = np.zeros(Q)  # Stabilizing interest rate

    # Set constant parameter values
    a1 = 0.3  # Sensitivity of inflation with respect to output gap
    a2 = 0.7  # Sensitivity of output with respect to interest rate
    b = 1     # Sensitivity of the central bank to inflation gap
    a3 = (a1 * (1 / (b * a2) + a2)) ** (-1)

    # Initialize endogenous variables at equilibrium values
    y[0] = ye[0]
    p[0] = pt[0]
    rs[0] = (A[0] - ye[0]) / a1
    r[0] = rs[0]

    # Simulate the model by looping over Q time periods for S different scenarios
    for t in range(1, Q):
        # (1) IS curve
        y[t] = A[t] - a1 * r[t - 1]
        # (2) Phillips Curve
        p[t] = p[t - 1] + a2 * (y[t] - ye[t])
        # (3) Stabilizing interest rate
        rs[t] = (A[t] - ye[t]) / a1
        # (4) Monetary policy rule, solved for r
        r[t] = rs[t] + a3 * (p[t] - pt[t])

    return y, p, rs, r


#%%

# Set number of periods
Q = 50
# Set parameter values
A = np.full(Q, 10)  # Autonomous spending
pt = np.full(Q, 2)  # Inflation target
ye = np.full(Q, 5)  # Potential output

# A[5:Q] = 12  # Scenario 1: AD boost
# pt[5:Q] = 3  # Scenario 2: Higher inflation target
ye[5:Q] = 7  # Scenario 3: Higher potential output

y, p, rs, r = simulate(A, pt, ye)


#%%

img, axes = plt.subplots(2, 1)
axes[0].plot(y, label="y: production")
axes[0].plot(p, label="p: inflation") 
axes[0].legend()
axes[1].plot(rs, label="rs: stabilizing interest rate")
axes[1].plot(r, label="r: interest rate") 
axes[1].legend()

# plt.plot(y)
# plt.plot(p)
# plt.plot(rs)
# plt.plot(r)
# %%
