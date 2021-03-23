import numpy as np
import seaborn as sns
import pandas as pd

def heatmap(ax, data, names, annot=True,linewidths=0.0):
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    data = np.where(data!=0, data, np.nan)
    data_pd = pd.DataFrame(data,columns=names,index=names)
    g = sns.heatmap(data_pd.T, cmap=cmap, annot=annot, fmt="0.2f", vmin=-0.8, vmax=0.8, ax=ax, linewidths=linewidths)
    #g.set_xticklabels(g.get_xmajorticklabels(), fontsize = 14)
    #g.set_yticklabels(g.get_ymajorticklabels(), fontsize = 14)
    sns.set(font_scale=1.8)
