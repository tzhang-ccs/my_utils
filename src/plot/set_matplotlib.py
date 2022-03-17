from cycler import cycler

my_cycler = (cycler(color=['#94c8d8','#FE9A84','#296540','#E63F39','#C3AAD1',
              '#D5AC5A','#F4B6C3','#B4BCCA','#DBD468','#B1D3E1','#8b1821']))
plt.rcParams['figure.figsize'] = (18,12)
plt.rcParams['axes.prop_cycle'] = my_cycler
plt.rcParams['lines.linewidth'] = 3
plt.rcParams['lines.markersize'] = 8
plt.rcParams['legend.fontsize'] = 15
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 16
plt.rcParams['axes.titlesize'] = 18


color_list = ['#08808E','#FE9A84','#296540','#E63F39','#C3AAD1',
              '#D5AC5A','#F4B6C3','#B4BCCA','#DBD468','#B1D3E1','#8B1821']
my_cmap = LinearSegmentedColormap.from_list('excalibur',color_list)
cm.register_cmap(cmap=my_cmap)

#blue: 94c8d8
#orange: FE9A84
#green: 296540
#red: E63F39
#purple: C3AAD1
#brown: D5AC5A
#pink: F4B6C3
#gray: B4BCCA
#yellow: DBD468
#cyan: B1D3E1
#wine: 8b1821
