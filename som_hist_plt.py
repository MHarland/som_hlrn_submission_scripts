import sys, numpy as np, os
from mpltotex import PRLPlotConf
from pytriqs.gf.local import GfReFreq, GfImTime, GfLegendre, GfImFreq
from pytriqs.archive import HDFArchive
from pytriqs.statistics.histograms import Histogram


mplcfg = PRLPlotConf(add_ax = False)
fig = mplcfg.fig
plt = mplcfg.plt
for archive_name in sys.argv[1:]:
    archive = HDFArchive(archive_name, 'r')
    if not archive.is_group('g_w'):
        print 'g_w of '+archive_name+' not found'
        continue
    try:
        histos = archive['histograms']
    except:
        print 'couldn\'t load histos of '+archive_name
        continue
    ax0 = fig.add_axes([.17,.15+.5,.82,.82-.5])
    hist = histos[0]
    dx = (hist.limits[1] - hist.limits[0]) / len(hist)
    x = np.linspace(hist.limits[0], hist.limits[1], len(hist.data))
    y = hist.data
    i_max = 0
    for i, yi in enumerate(y):
        if not np.allclose(yi, 0):
            i_max = i
    ax0.bar(x, y, dx, color = 'gray', linewidth = 0.1)
    #ax0.hist(hist.data, 20)
    ax0.set_xlabel("$D$")
    ax0.set_ylabel("$P(D)$")
    #ax0.set_xlim(x[0], x[min(i_max+1, len(x))])
    ax0.set_ylim(bottom=0)

    ax1 = fig.add_axes([.17,.15,.82,.82-.5])
    grec = archive['g_rec']
    gori = archive['g']
    #s = archive[results_groupname]['s']
    if isinstance(gori, GfLegendre):
        mesh = [x.real for x in grec.mesh]
        ax1.plot(mesh, np.log(abs(gori.data[:,0,0].real)), label = "$\\mathrm{original}$", marker = "+")
        ax1.plot(mesh, np.log(abs(grec.data[:,0,0].real)), ls = '--', label = "$\\mathrm{reconstructed}$", marker = 'x')
        #ax1.plot(mesh, np.log(abs(s.data[:,0,0].real)), ls = ':', label = "s")
        ax1.set_xlabel("$l$")
        ax1.set_ylabel("$\\mathrm{log}\,|G(l)|$")
    elif isinstance(gori, GfImTime):
        mesh = [x.real for x in grec.mesh]
        """
        center = int(len(mesh)*.5)
        halfrange = int(len(mesh)*.1)
        pr = (center - halfrange, center + halfrange)
        ax1.plot(mesh[pr[0]:pr[1]], gori.data[pr[0]:pr[1],0,0].real, label = "original", marker = "+")
        ax1.plot(mesh[pr[0]:pr[1]], grec.data[pr[0]:pr[1],0,0].real, ls = '--', label = "reconstructed", marker = 'x')
        """
        ax1.plot(mesh, gori.data[:,0,0].real, label = "$\\mathrm{original}$")#, marker = "+")
        ax1.plot(mesh, grec.data[:,0,0].real, ls = '--', label = "$\\mathrm{reconstructed}$")#, marker = 'x')
        ax1.set_xlabel("$\\tau$")
        ax1.set_ylabel("$G(\\tau)$")
        #ax1.set_ylim(top = 0)
    elif isinstance(gori, GfImFreq):
        mesh = [x.imag for x in grec.mesh]
        ax1.plot(mesh, gori.data[:,0,0].real, label = "$\\mathrm{original}$")#, marker = "+")
        ax1.plot(mesh, grec.data[:,0,0].real, label = "$\\mathrm{reconstructed}$", lw = .5)#, marker = 'x')
        ax1.set_xlabel("$i\\omega_n$")
        ax1.set_ylabel("$\\Re G(i\\omega_n)$")
        #ax1.set_ylim(top = 0)
        #ax1.set_xlim(0, mesh[-1])
    ax1.legend(**mplcfg.legendkwargs)
    
    outname = archive_name[:-3]+"_som_hist.pdf"
    plt.savefig(outname)
    print outname+" ready"
    ax0.clear()
    ax1.clear()
