import matplotlib.pylab as plt
import numpy as np
from cmocean import cm as cmo
import pandas as pd

def plot_radar(data, sheet_name, save_name=None):
    fig = plt.figure(figsize=(16,9))
    ax = fig.add_subplot(111, polar=True)
    labels = data.columns
    index  = data.index
    shape  = data.shape
    y_max  = np.max(data.values)
    y_min  = np.min(data.values)
    

    for i in range(shape[0]):
        stats = data.values[i,:]
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)

        stats = np.concatenate((stats, [stats[0]]))
        angles = np.concatenate((angles, [angles[0]]))

        ax.plot(angles, stats, 'o-', label=index[i])
        ax.fill(angles, stats, alpha=0.25)
        ax.set_thetagrids(angles * 180/np.pi, labels)
        ax.set_ylim(y_min,y_max)
    
    ax.set_title(sheet_name)
    plt.legend(loc='upper right')
    #plt.legend(loc='upper right', bbox_to_anchor=(1.12,1.12))

    plt.show()

    if save_name is not None:
        plt.savefig(save_name)
    return fig, ax

if __name__ == '__main__':
    x = pd.read_excel("/gscr2/tzhang/E3SM/MOO/post_data/MOO_tuned_metrics.xlsx", sheet_name="MCPI", index_col='step')
    plot_radar(x, "MCPI")
    print(x.head())
