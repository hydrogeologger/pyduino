#http://stackoverflow.com/questions/2682745/how-to-create-a-constant-in-python
import numpy as np
import matplotlib.pyplot as plt
# belwow are all the constants
def single_fig_initialise():
    import matplotlib.pylab as pylab
    params = {'legend.fontsize': 13,
              'figure.figsize': (10, 5),
             'axes.labelsize': 12,
             'axes.titlesize':'x-large',
             'xtick.labelsize':'20',
             'ytick.labelsize':'20',
    #         'ytick.labelweight':'bold',
              'axes.labelsize': 16,
               'axes.labelweight':'bold'}
    #         'axes.grid':'linewidth=grid_width,color = '0.5''}
    #         'linewidth':lw,'markers.size':ms,'markers.edgewidth':mew}
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    pylab.rcParams.update(params)

    fig = plt.figure(figsize=(8.2,8.2))
    lw=6
    ms=8
    mew=3
    grid_width=2
    y_fontsize=20
    ax = fig.add_subplot(111)
    fig.subplots_adjust(left=0.17, right=0.98, top=0.99, bottom=0.17)
    for axis in ['top','bottom','left','right']:
      ax.spines[axis].set_linewidth(2) 
    return fig



