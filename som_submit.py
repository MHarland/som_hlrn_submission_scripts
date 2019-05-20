#!/usr/bin/env python
import subprocess, sys, os, itertools, numpy as np


pars = [{'prototype_files': ['som_prototype.py','som_prototype_hlrn.sh'],
         'commands': [['chmod +x'], ['chmod +x', 'msub']],
         'target_files': [],
         # target_file scope:
         'cwd': os.getcwd(),
         'accountname': '-',
         'n_nodes': 4,
         'walltime': '4:00:00',
         'n_w': 1000,
         'energy_window': '(0, 4)',
         'adjust_f': False,
         'adjust_l': False,
         't': 50,
         'f': f,
         'l': 2000}
        for f in [150, 1500, 15000]] # use this loop for a parameter sweep if desired

for par in pars:
    par['n_tasks'] = par['n_nodes'] * 24
    par['name'] = 't'+str(par['t'])
    if not par['adjust_f']:
        par['name'] += 'f'+str(par['f'])
    if not par['adjust_l']:
        par['name'] += 'l'+str(par['l'])
    par['pyname'] = 'som_'+par['name']+'.py'
    par['jobname'] = par['name']
    par['target_files'] = ['som_'+par['name']+'.py', 'som_'+par['name']+'.sh']

for par in pars:
    for proto_fname, target_fname, commands in zip(par['prototype_files'], par['target_files'], par['commands']):
        proto = open(proto_fname, 'r')
        target = open(target_fname, 'w')
        for line in proto:
            line = str(line)
            while len(line.split('{%', 1)) > 1:
                split1 = line.split('{%', 1)
                split2 = split1[1].split('%}', 1)
                assert split2[0] in par.keys(), "key "+split2[0]+" not found in par.keys()"
                line = split1[0] + str(par[split2[0]]) + split2[1]
            target.write(line)
        del proto, target
        for command in commands:
            if 'sub' in command:
                jobid_str = subprocess.check_output(command+' '+target_fname, shell = True)
                print par['jobname']+' submitted as '+jobid_str#[9:16]
            else:
                subprocess.call(command+' '+target_fname, shell = True)
