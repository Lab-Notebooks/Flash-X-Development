import yt
import numpy
from scipy.interpolate import griddata
from matplotlib import pyplot
from matplotlib.animation import PillowWriter
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Video writer setup
metadata = dict(title='INS Flow Boiling', artist='Matplotlib', comment='Fluid visualization')
writer = PillowWriter(fps=5, metadata=metadata)

filetags = [*range(37,38)]

delta = 0.039
nx_bins = 5000 #int(2.5/delta)  # Resolution for the interpolation
ny_bins = 5000 #int(60/delta)

# Set up figure and axis once
fig, ax = pyplot.subplots(figsize=(10, 2), dpi=300, constrained_layout=True)
pyplot.rc("font", family="serif", size=15, weight="bold")
pyplot.rc("axes", labelweight="bold", titleweight="bold")
pyplot.rc("text", usetex=True)

# Create a blank image that will be updated
X, Y = None, None
contourf_plot = [None]  # use list to hold reference

dirname = "case-37.44pct-chf"

with writer.saving(fig, f"INS_Flow_Boiling_Video.gif", dpi=300):
    for ftag in filetags:
        filename = f"{dirname}/INS_Flow_Boiling_hdf5_plt_cnt_{str(ftag).zfill(4)}"
        dataset = yt.load(filename)
        region = dataset.all_data()

        x = region["x"]
        y = region["y"]

        if X is None or Y is None:
            x_bins = numpy.linspace(x.min(), x.max(), nx_bins)
            y_bins = numpy.linspace(y.min(), y.max(), ny_bins)
            X, Y = numpy.meshgrid(x_bins, y_bins)

        dfun = griddata((x, y), region["dfun"], (X, Y), method='linear')
        temp = griddata((x, y), region["temp"], (X, Y), method='linear')

        temp_limits = [1e-3, 1.]
        temp_levels = numpy.linspace(temp_limits[0],temp_limits[1],200) 
        temp = numpy.where(temp <= 0, temp_limits[0], temp)
        temp = numpy.where(temp >= temp_limits[1], temp_limits[1], temp)

        ax.clear()

        #contourf = ax.contourf(X, Y, dfun, levels=[-0.001, 0.001], extend='both', cmap='Greens')
        contourf = ax.contourf(X, Y, temp, levels=temp_levels, extend='both', cmap='rainbow', norm = LogNorm())
        contour = ax.contour(X, Y, dfun, levels=[0], colors='k', linewidths=0.5, linestyles='-')

        ax.set_xlim([x.min(), x.max()])
        ax.set_ylim([y.min(), y.max()])
        ax.set_aspect('equal', adjustable='box')
        xticks = [0, 80, 161]
        yticks = [0, 7]
        ax.set_xticks(xticks)
        ax.set_yticks(yticks)
	# Set custom labels scaled by 0.7
        ax.set_xticklabels([f"{x * 0.7:.1f}" for x in xticks])
        ax.set_yticklabels([f"{y * 0.7:.1f}" for y in yticks])
        ax.set_xlabel(r"mm")
        ax.set_ylabel(r"mm")
        #fig.colorbar(contourf, ax=ax)
        #cbar = fig.colorbar(contourf, ax=ax, ticks=[1e-3, 5e-2, 1, 10])
        #ax.set_title(f"time = {ftag*0.1*8.5:5.1f} ms, t_nuc = {0.2*8.5:5.1f} ms")
        writer.grab_frame()
