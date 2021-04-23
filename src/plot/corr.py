import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import sys
from pathlib import Path
home = str(Path.home())
sys.path.append(home+"/climate_causal/utils/")
import algs

def heatmap(data, names, ax=None,annot=True,linewidths=0.0):
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    data = np.where(data!=0, data, np.nan)
    data_pd = pd.DataFrame(data,columns=names,index=names)
    g = sns.heatmap(data_pd.T, cmap=cmap, annot=annot, fmt="0.2f", vmin=-0.8, vmax=0.8, ax=ax, linewidths=linewidths)
    #g.set_xticklabels(g.get_xmajorticklabels(), fontsize = 14)
    #g.set_yticklabels(g.get_ymajorticklabels(), fontsize = 14)
    sns.set(font_scale=1.8)

def corrdot(*args, **kwargs):
    corr_r = args[0].corr(args[1], 'pearson')
    corr_text = round(corr_r, 2)
    ax = plt.gca()
    font_size = abs(corr_r) * 80 + 5
    ax.annotate(corr_text, [.5, .5,],  xycoords="axes fraction",
                ha='center', va='center', fontsize=font_size)

def corrfunc(x, y, **kws):
    r, p = stats.pearsonr(x, y)
    p_stars = ''
    if p <= 0.05:
        p_stars = '*'
    if p <= 0.01:
        p_stars = '**'
    if p <= 0.001:
        p_stars = '***'
    ax = plt.gca()
    ax.annotate(p_stars, xy=(0.50, 0.6), xycoords=ax.transAxes,
                color='red', fontsize=70)

def corr_analysis(data):
    sns.set(style='white', font_scale=1.6)
    iris = sns.load_dataset('iris')
    g = sns.PairGrid(data, aspect=1.5, diag_sharey=False, despine=False)
    g.map_lower(sns.regplot, lowess=True, ci=False,
                line_kws={'color': 'red', 'lw': 1},
                scatter_kws={'color': 'black', 's': 20})
    #g.map_diag(sns.distplot, color='black',
    #           kde_kws={'color': 'red', 'cut': 0.7, 'lw': 1},
    #           hist_kws={'histtype': 'bar', 'lw': 2,
    #                     'edgecolor': 'k', 'facecolor':'grey'})
    #g.map_diag(sns.rugplot, color='black')
    g.map_upper(corrdot)
    g.map_upper(corrfunc)
    g.fig.subplots_adjust(wspace=0, hspace=0)
    
    # Remove axis labels
    for ax in g.axes.flatten():
        ax.set_ylabel('')
        ax.set_xlabel('')
    
    # Add titles to the diagonal axes/subplots
    for ax, col in zip(np.diag(g.axes), data.columns):
        ax.set_title(col, y=0.82, fontsize=18)


def corr_analysis_2p(data, names, ax=None):
    sns.set(style='white', font_scale=1.6)
    
    if len(names) != 2:
        sys.exit("Length of names should be 2")

    sns.regplot(x=data[names[0]], y=data[names[1]],
            line_kws={'color': 'red', 'lw': 1},
            scatter_kws={'color': 'black', 's': 20}, ax = ax)
    
    corr, pval = algs.calc_corr(data[names[0]], data[names[1]])
    if pval <= 0.001:
        sig = '***'
    elif pval <= 0.01:
        sig = '**'
    elif pval <= 0.05:
        sig = '*'
    else:
        sig = 'x'
    
    title = 'corr = {:.2f} ({:s})'.format(corr, sig)
    ax.set_title(title, fontsize=20)
