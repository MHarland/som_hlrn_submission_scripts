#!/usr/bin/env pytriqs
import numpy as np
import time
from pytriqs.gf.local import *
from pytriqs.archive import HDFArchive
import pytriqs.utility.mpi as mpi
from pytriqs.applications.analytical_continuation.som import Som
from pytriqs.version import git_hash as pytriqs_hash
from pytriqs.applications.impurity_solvers.cthyb.version import cthyb_hash
from pytriqs.applications.analytical_continuation.som.version import som_hash


name = '{%name%}'
indices = [0]
n_w = {%n_w%}
run_params = {'energy_window' : {%energy_window%}}
run_params['verbosity'] = 1
run_params['adjust_f'] = {%adjust_f%}
run_params['adjust_l'] = {%adjust_l%}
run_params['t'] = {%t%}
run_params['f'] = {%f%}
run_params['l'] = {%l%}
run_params['make_histograms'] = True
run_params['hist_max'] = 5.
run_params['hist_n_bins'] = 1000

# load your data here and pass it to the green function data array!
beta = 10
n_iw = 50
g = GfImFreq(indices = [0], beta = beta, n_points = n_iw, statistic = 'Boson')
g.data[iw_, 0, 0] = ... # TRIQS uses twice n_iw: the first n_iw frequencies are negative!

g_w = GfReFreq(window = run_params['energy_window'], n_points = n_w, indices = indices)
s = g.copy()
g_rec = g.copy()
s.data[:] = 1.0 # either s = const. or s = g

if mpi.is_master_node():
    arch = HDFArchive(name+'.h5','w')
    arch['pytriqs_hash'] = pytriqs_hash
    arch['cthyb_hash'] = cthyb_hash
    arch['som_hash'] = som_hash
    arch.create_group('run_params')
    archpar = arch['run_params']
    for key, val in run_params.items():
        archpar[key] = val
    arch['beta'] = beta
    arch['n_iw'] = n_iw

start = time.clock()
cont = Som(g, s, kind = 'BosonAutoCorr', norms = np.array([ --- ])) # enter norm!
cont.run(**run_params)
exec_time = time.clock() - start
g_rec << cont
g_w << cont
if mpi.is_master_node():
    arch['exec_time'] = exec_time
    arch['g'] = g
    arch['g_w'] = g_w
    arch['g_rec'] = g_rec
    if run_params['make_histograms']:
        arch['histograms'] = cont.histograms

