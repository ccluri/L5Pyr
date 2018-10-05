from neuron import h
import numpy as np
import matplotlib.pyplot as plt


def fetch_soma_sec(section_name):
    cell_model = 'Hayton.hoc'
    h.load_file(cell_model)
    cell = h.L5PC
    soma = cell.soma[0]
    exec('sec = cell.' + section_name)
    return soma, sec


def find_vrest(h, section_name):
    h.load_file("stdrun.hoc")
    tstop = 100
    h.dt = dt = 0.1
    soma, sec = fetch_soma_sec(section_name)
    h.init()
    h.cvode.re_init()
    t_vec, soma_vm, sec_vm = record(soma, sec)
    h.execute('tstop = 100')
    h.run()
    vrest = np.array(sec_vm)[-1]
    return vrest


def exp2(tt, tau_raise, tau_fall, onset):
    vv = []
    for ii,t in enumerate(tt):
        if t < onset:
            vv.append(0)
        else:
            val = np.exp(-t/tau_fall)*(1.-np.exp(-t/tau_raise))
            vv.append(val)
    return np.array(vv)


def square(tt, start, end, v_peak):
    print('Square impuse')
    vv = []
    for ii, t in enumerate(tt):
        if t<start or t>end:
            vv.append(0.)
        else:
            vv.append(v_peak)
    return np.array(vv)


def voltage_clamp(tstop, dt, v_rest, v_peak, tau_raise, tau_fall, onset=100.):
    assert(tau_fall > tau_raise)
    tt = np.arange(0, tstop, dt)
    #vv = v_rest + (v_peak*exp2(tt, tau_raise, tau_fall, onset))
    vv = v_rest + square(tt, 100, 200, v_peak) 
    return vv

def fetch_soma_apic_pots():
    s_v = h.Vector()
    a_v = h.Vector()
    s_v.record(h.L5PC.soma[0](0.5)._ref_v)
    a_v.record(h.L5PC.apic[0](1e-3)._ref_v)
    return s_v, a_v


def record(soma, sec):
    sec_vm = h.Vector()
    sec_vm.record(sec(0.5)._ref_v)
    soma_vm = h.Vector()
    soma_vm.record(soma(0.5)._ref_v)
    t_vec = h.Vector()
    t_vec.record(h._ref_t)
    return t_vec, soma_vm, sec_vm

def run_sim(h, section_name, v_peak, tau_raise, tau_fall, onset=100):
    tstop = 500
    h.dt = dt = 0.1
    h.load_file("stdrun.hoc")
    soma, sec = fetch_soma_sec(section_name)
    v_rest = -75.711 # find_vrest(h, section_name)
    h.init()
    h.cvode.re_init()
    s_v, a_v = fetch_soma_apic_pots()
    vv = voltage_clamp(tstop, dt, v_rest, v_peak, tau_raise, tau_fall, onset)
    vc = h.SEClamp(sec(0.5))
    vc.rs = 0.001
    vc.dur1 = tstop
    vamp = h.Vector(vv)
    vamp.play(vc._ref_amp1, h.dt)
    t_vec, soma_vm, sec_vm = record(soma, sec)
    h.execute('tstop = ' + str(tstop))
    h.run()
    diff_v = np.array(a_v) - np.array(s_v)
    return t_vec, soma_vm, sec_vm, diff_v, vv


dendrite_name = 'apic[26]'
t_vec, soma_vm, sec_vm, diff_v, vv = run_sim(h, dendrite_name, 100, 10, 15)
plt.figure(figsize=(10,5))
plt.subplot(121)
plt.plot(t_vec, soma_vm, 'k', label='V_soma')
plt.plot(t_vec, sec_vm, 'r', label='V_'+dendrite_name)
# tt = np.arange(0, 500, 0.01)
# plt.plot(np.arange(0, tstop, dt), vv, c='g')
plt.xlabel('Time (ms)')
plt.ylabel('Membrane potential (mV)')
plt.legend()
plt.subplot(122)
# h.ri(1e-3) # after access of apic[0] to get the  0.13930698946266598 - neuron blues
plt.plot(t_vec, diff_v / 0.13930698946266598, 'g', label='apical 2 soma')
plt.xlabel('Time (ms)')
plt.ylabel('Axial current (nA)')
plt.legend()
plt.show()
