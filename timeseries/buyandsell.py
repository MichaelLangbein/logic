#%% Getting some example data
import pandas as p

apple = p.read_csv('apple_history.csv')

# Example plot
apple[10000:].plot(x='Date', y=['Open', 'Close'])

# %%
