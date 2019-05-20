import sys, numpy as np, os
from mpltotex import PRLPlotConf
from pytriqs.gf.local import GfReFreq
from pytriqs.archive import HDFArchive


mplcfg = PRLPlotConf(72, 368)
fig = mplcfg.fig
plt = mplcfg.plt
ax = mplcfg.ax
n_graphs = len(sys.argv[1:])
colors = [plt.cm.viridis(float(i)/max(1,n_graphs-1)) for i in range(n_graphs)]
for archive_name, color in zip(sys.argv[1:], colors):
    archive = HDFArchive(archive_name, 'r')
    if not archive.is_group('g_w'):
        print archive_name+' has no group g_w, skipping...'
        continue
    g_w = archive['g_w']
    mesh = np.array([w for w in g_w.mesh])
    a = -g_w.data[:,0,0].imag/np.pi
    ax.plot(mesh.real, a, label = '$'+archive_name[:-3]+'$', color = color)
ax.legend(**mplcfg.legendkwargs)
ax.set_xlabel("$\\omega$")
ax.set_ylabel("$A(\\omega)$")
#ax.set_ylim(bottom = 0)
#ax.set_ylim(0, 30)
#ax.set_xlim(-1,1)
plt.savefig("som.pdf")
print "som.pdf ready"
plt.close()
