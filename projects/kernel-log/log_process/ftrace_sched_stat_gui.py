'''
Make a colorbar as a separate figure.
'''

from matplotlib import pyplot
import matplotlib as mpl

def plot(stat,cost):
    stat_timeline = stat
    cost_timeline = cost
    # 根据状态设置颜色
    cmap_raw = []
    for stat in stat_timeline:
        if 'sched_stat_runtime:' == stat:
            cmap_raw.append('g')
        elif 'sched_stat_sleep:' == stat:
            cmap_raw.append('b')
        elif 'sched_stat_wait:' == stat:
            cmap_raw.append('y')
        else:
            print("Unknown stat")
            cmap_raw.append('k')
    # 根据耗时确定每个颜色长度
    bounds = [1]
    for cost in cost_timeline:
        # bounds[-1] == bounds[len(bounds)-1]
         bounds.append(bounds[-1] + cost)
    print(bounds)

    # Make a figure and axes with dimensions as desired.
    fig = pyplot.figure(figsize=(10, 3))

    ax = fig.add_axes([0.05, 0.475, 0.9, 0.15])

    # The second example illustrates the use of a ListedColormap, a
    # BoundaryNorm, and extended ends to show the "over" and "under"
    # value colors.
    # cmap = mpl.colors.ListedColormap(['r', 'g', 'b', 'c','r', 'g', 'b', 'c'])
    cmap = mpl.colors.ListedColormap(cmap_raw)
    cmap.set_over('0.25')
    cmap.set_under('0.75')
    # If a ListedColormap is used, the length of the bounds array must be
    # one greater than the length of the color list.  The bounds must be
    # monotonically increasing.
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cb = mpl.colorbar.ColorbarBase(ax,
                                   cmap=cmap,
                                   norm=norm,
                                   # to use 'extend', you must
                                   # specify two extra boundaries:
                                   boundaries= bounds ,
                                   # extend='both',
                                   # ticks=[1,bounds[-1]],  # optional
                                   spacing='proportional',
                                   orientation='horizontal'
                                   )
    cb.set_label('Sched_stat cost')

    pyplot.show()
