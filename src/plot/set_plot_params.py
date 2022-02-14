def fig_size(W=15,H=5) :
    import matplotlib.pylab as pylab
    params = {'legend.fontsize': 'x-large',
              'figure.figsize': (W, H),
             'axes.labelsize': 'xx-large',
             'axes.titlesize':'xx-large',
             'xtick.labelsize':'xx-large',
             'ytick.labelsize':'xx-large'}
    pylab.rcParams.update(params)
