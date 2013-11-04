from neuron import h
from matplotlib import pyplot as plt
from numpy import array, interp, arange

model_name = 'Traub'

def load_file(name):
    if name == 'Traub': 
        h.load_file("Traub.hoc")
        Ca_curr.record(h.L5PC.comp[1](0.5)._ref_ica)
        Ca_T_curr.record(h.L5PC.comp[1](0.5)._ref_i_cat) #
        Ca_L_curr.record(h.L5PC.comp[1](0.5)._ref_ica_cal) 

        Na_curr.record(h.L5PC.comp[1](0.5)._ref_ina)
        Na_P_curr.record(h.L5PC.comp[1](0.5)._ref_ina_nap)
        Na_F_curr.record(h.L5PC.comp[1](0.5)._ref_ina_naf)

        K_curr.record(h.L5PC.comp[1](0.5)._ref_ik)
        K_DR_curr.record(h.L5PC.comp[1](0.5)._ref_ik_kdr)
        K_C_curr.record(h.L5PC.comp[1](0.5)._ref_ik_kc)
        K_A_curr.record(h.L5PC.comp[1](0.5)._ref_ik_ka_ib)
        K_M_curr.record(h.L5PC.comp[1](0.5)._ref_ik_km)
        K_2_curr.record(h.L5PC.comp[1](0.5)._ref_ik_k2)
        K_AHP_curr.record(h.L5PC.comp[1](0.5)._ref_ik_kahp_deeppyr)
    else:
        h.load_file("Hay.hoc")
        Ca_curr.record(h.L5PC.soma[0](0.5)._ref_ica)
        Ca_T_curr.record(h.L5PC.soma[0](0.5)._ref_ica_Ca_HVA)
        Ca_L_curr.record(h.L5PC.soma[0](0.5)._ref_ica_Ca_LVAst)

        Na_curr.record(h.L5PC.soma[0](0.5)._ref_ina)
        Na_P_curr.record(h.L5PC.soma[0](0.5)._ref_ina_NaTa_t)
        Na_F_curr.record(h.L5PC.soma[0](0.5)._ref_ina_Nap_Et2)

        K_curr.record(h.L5PC.soma[0](0.5)._ref_ik)
        K_P_curr.record(h.L5PC.soma[0](0.5)._ref_ik_K_Pst)
        K_T_curr.record(h.L5PC.soma[0](0.5)._ref_ik_K_Tst)
        K_SK_curr.record(h.L5PC.soma[0](0.5)._ref_ik_SK_E2)
        K_3_curr.record(h.L5PC.soma[0](0.5)._ref_ik_SKv3_1)
#        K_M_curr.record(h.L5PC.soma[0](0.5)._ref_ik_Im)

Ca_curr = h.Vector()
Ca_T_curr = h.Vector()
Ca_L_curr = h.Vector()

Na_curr = h.Vector()
Na_F_curr = h.Vector()
Na_P_curr = h.Vector()

K_curr = h.Vector()
if model_name == 'Traub': #traub specific
    K_DR_curr = h.Vector() 
    K_C_curr = h.Vector()
    K_A_curr = h.Vector()
    K_M_curr = h.Vector()
    K_2_curr = h.Vector()
    K_AHP_curr = h.Vector()
else: #Hay specific
    K_P_curr = h.Vector() 
    K_T_curr = h.Vector()
    K_SK_curr = h.Vector()
    K_3_curr = h.Vector()
#    K_M_curr = h.Vector()

load_file(model_name)

h.load_file("stdrun.hoc")
h.init()
h.run()
time_vals_orig = array(h.tvec)
time_vals = array(arange(0,600,0.025))

vsoma = interp(time_vals, time_vals_orig, h.vsoma)
vdend = interp(time_vals, time_vals_orig, h.vdend)
vdend2 = interp(time_vals, time_vals_orig, h.vdend2)

isoma = interp(time_vals, time_vals_orig, h.isoma)
isyn = interp(time_vals, time_vals_orig, h.isyn)
    
ica = interp(time_vals, time_vals_orig, Ca_curr)
ica_T = interp(time_vals, time_vals_orig, Ca_T_curr)
ica_L = interp(time_vals, time_vals_orig, Ca_L_curr)

ina = interp(time_vals, time_vals_orig, Na_curr)
ina_F = interp(time_vals, time_vals_orig, Na_F_curr)
ina_P = interp(time_vals, time_vals_orig, Na_P_curr)

ik = interp(time_vals, time_vals_orig, K_curr)
if model_name == 'Traub':
    ik_DR = interp(time_vals, time_vals_orig, K_DR_curr)
    ik_C = interp(time_vals, time_vals_orig, K_C_curr)
    ik_A = interp(time_vals, time_vals_orig, K_A_curr)
    ik_M = interp(time_vals, time_vals_orig, K_M_curr)
    ik_2 = interp(time_vals, time_vals_orig, K_2_curr)
    ik_AHP = interp(time_vals, time_vals_orig, K_AHP_curr)
else:
    ik_P = interp(time_vals, time_vals_orig, K_P_curr)
    ik_T = interp(time_vals, time_vals_orig, K_T_curr)
    ik_SK = interp(time_vals, time_vals_orig, K_SK_curr)
    ik_3 = interp(time_vals, time_vals_orig, K_3_curr)
#    ik_M = interp(time_vals, time_vals_orig, K_M_curr)
    
plot_start = 250
plot_end = 350

fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
plt.hold(True)
ax1.plot(time_vals, vsoma, label='soma')
ax1.plot(time_vals, vdend, label='comp_high')
ax1.plot(time_vals, vdend2, label='comp_low')
ax1.set_xlim(plot_start,plot_end)
plt.legend()
plt.hold(False)

# fig2 = plt.figure()
# ax2 = fig2.add_subplot(111)
# ax2.plot(time_vals, isoma)
# plt.hold(True)
# ax2.plot(time_vals, isyn)
# ax2.set_xlim(plot_start,plot_end)

fig3 = plt.figure()
ax3 = fig3.add_subplot(111)
ax3.plot(time_vals, ica, label='ica')
plt.hold(True)
plt.title("Na-Ca-K currents"+model_name)
ax3.plot(time_vals, ina, label='ina')
ax3.plot(time_vals, ik, label='ik')
ax3.set_xlim(plot_start,plot_end)
plt.legend()
plt.hold(False)

fig4 = plt.figure()
ax4 = fig4.add_subplot(111)
ax4.plot(time_vals, ik, label='ik')
plt.hold(True)
plt.title("K currents"+model_name)
if model_name == 'Traub':
    ax4.plot(time_vals, ik_DR, label='ik_DR')
    ax4.plot(time_vals, ik_C, label='ik_C')
    ax4.plot(time_vals, ik_A, label='ik_A')
    ax4.plot(time_vals, ik_M, label='ik_M')
    ax4.plot(time_vals, ik_2, label='ik_2')
    ax4.plot(time_vals, ik_AHP, label='ik_AHP')
else:
    ax4.plot(time_vals, ik_P, label='ik_P')
    ax4.plot(time_vals, ik_T, label='ik_T')
    ax4.plot(time_vals, ik_SK, label='ik_SK')
    ax4.plot(time_vals, ik_3, label='ik_3')
#    ax4.plot(time_vals, ik_M, label='ik_M')
ax4.set_xlim(plot_start,plot_end)
plt.legend()
plt.hold(False)

fig5 = plt.figure()
ax5 = fig5.add_subplot(111)
plt.hold(True)
plt.title("Ca currents"+model_name)
ax5.plot(time_vals, ica_T, label='ica_T')
ax5.plot(time_vals, ica_L, label='ica_L')
ax5.plot(time_vals, ica, label='ica')
ax5.set_xlim(plot_start,plot_end)
plt.legend()
plt.hold(False)

fig6 = plt.figure()
ax6 = fig6.add_subplot(111)
plt.hold(True)
plt.title("Na currents"+model_name)
ax6.plot(time_vals, ina_F, label='ina_F')
ax6.plot(time_vals, ina_P, label='ina_P')
ax6.plot(time_vals, ina, label='ina')
ax6.set_xlim(plot_start,plot_end)
plt.legend()
plt.hold(False)
#plt.savefig('traubs_currs_bap.png', format='png')

plt.show()
