import numpy as np
import matplotlib.pyplot as plt


plt.ion()

df = np.load("df1.npy",allow_pickle=True)

fig,ax = plt.subplots(figsize=(8,6))

line, = plt.plot(np.arange(1,len(df[0])+1),df[0])

for i in range(len(df)):
    x = np.arange(1,len(df[i])+1)
    y = df[i]
    ax.set_title(f"{i}")
    line.set_ydata(y)
    line.set_xdata(x)
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.001)
    

