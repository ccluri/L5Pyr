import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from neuron import h
import numpy as np
import sys

n3dpoints = {} #has sec name and the first and last coordinates of its location
def retrieve_coordinate(sec):
    sec.push()
    x, y, z, d = [],[],[],[]
    area = 0
    tot_points = 0
    connect_next = False
    for i in range(int(h.n3d())):
        present = False
	x_i = h.x3d(i)
	y_i = h.y3d(i)
	z_i = h.z3d(i)
	d_i = h.diam3d(i)
	a_i = h.area(0.5)
	if x_i in x:
            ind = len(x) - 1 - x[::-1].index(x_i) # Getting the index of last value
	    if y_i == y[ind]:
                if z_i == z[ind]:
                    present = True
                    
	if not present:
            k =(x_i, y_i, z_i)
	    x.append(x_i)
	    y.append(y_i)
	    z.append(z_i)
	    d.append(d_i)                
	    area += np.sum(a_i)
    h.pop_section()
        #adding num 3d points per section
    n3dpoints[sec.name()] = [np.array(x),np.array(y),np.array(z),np.array(d)]
    return (np.array(x),np.array(y),np.array(z),np.array(d),area)

def main(cell_model='Hay', show_morphology=True):
    h.load_file(cell_model+".hoc")
    if show_morphology:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

    total_segments = 0
    total_sections = 0
    total_area = 0
    total_length = 0

    for ii in h.L5PC.allsec():
        total_sections += 1
        x,y,z,d,area= retrieve_coordinate(ii)
        total_area += area
        try:
            for idx,jj in enumerate(x):
                if idx != len(x) -1:
                    if show_morphology:
                        ax.plot([x[idx],x[idx+1]],[y[idx],y[idx+1]],[z[idx],z[idx+1]], 'b')
                    a = np.array((x[idx],y[idx],z[idx]))
                    b = np.array((x[idx+1],y[idx+1],z[idx+1]))
                    length = np.linalg.norm(a-b)
                    total_length += length
                    total_segments += 1
        except IndexError:
            print 'Did not process: ', ii.name()
            pass

    total_segments = max(total_sections, total_segments)
    print 'Cell model name', cell_model
    print 'Total sections', total_sections
    print 'Total segments (atleast)', total_segments
    print 'Total length', total_length
    print 'Total area', total_area/(np.pi*4.0)

    if show_morphology:
        ax.auto_scale_xyz([-230,1200],[-230,1200],[-230,1200])
        plt.show()

if __name__ == '__main__':
    if len(sys.argv)>2:
        print 'Not showing morphology'
        main(sys.argv[-2], eval(sys.argv[-1]))
    else:
        main(sys.argv[-1], True)
