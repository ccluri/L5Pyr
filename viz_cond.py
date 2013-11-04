import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from mpl_toolkits.mplot3d import Axes3D
from neuron import h
import numpy as np
import sys

def retrieve_coordinate(sec):
    sec.push()
    x, y, z = [],[],[]
    connect_next = False
    for i in range(int(h.n3d())):
        present = False
        x_i = h.x3d(i)
        y_i = h.y3d(i)
        z_i = h.z3d(i)
        if x_i in x:
            ind = len(x) - 1 - x[::-1].index(x_i)
            if y_i == y[ind]:
                if z_i == z[ind]:
                    present = True
        if not present:
            x.append(x_i)
            y.append(y_i)
            z.append(z_i)
    h.pop_section()
    return (np.array(x),np.array(y),np.array(z))

def get_values(cell0, var_name='g_pas'):
    value_dict = {}
    for sec in cell0.allsec():
        try:
            value_dict[sec.name()] = eval("sec."+var_name)
        except(NameError,AttributeError):
            print 'No attribute called %s for %s' %(var_name, sec.name())
    return value_dict

def main(cell_model='Hay', var_name='g_pas'):
    h.load_file(cell_model+".hoc")
    cell0 = h.L5PC
    value_dict = get_values(cell0, var_name)
    var_vals = value_dict.values()
    cNorm  = colors.LogNorm(vmin=min(var_vals), vmax=max(var_vals))
    jet = cm = plt.get_cmap('jet') 
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.hold(True)
    def onpick3(event):
        ind = event.artist
        print 'picking:', ind

    for sec in cell0.allsec():
        x, y, z = retrieve_coordinate(sec)
        try:
            colorVal = scalarMap.to_rgba(value_dict[sec.name()])
        except(NameError,AttributeError):
            colorVal = (0.0,0.0,0.0,0.0)
        if len(x):
            hi = ax.plot([x[0],x[-1]],[y[0],y[-1]],[z[0],z[-1]],color=colorVal, picker=True, label=sec.name())
    fig.canvas.mpl_connect('pick_event', onpick3)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    ax.set_zticklabels([])
    ax.auto_scale_xyz([-230,1200],[-230,1200],[-230,1200])
    #fig.colorbar(ax) #fix colorbar!
    plt.show()

if __name__ == '__main__':
    if len(sys.argv) > 2:
        main(sys.argv[-2], sys.argv[-1])
    else:
        main(sys.argv[-1], 'g_pas')
