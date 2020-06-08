# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 16:00:31 2020

@author: wegia
"""
import numpy as np

points = np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2],
                    [2, 0], [2, 1], [2, 2]])
from scipy.spatial import Voronoi, voronoi_plot_2d
vor = Voronoi(points)

import matplotlib.pyplot as plt
fig = voronoi_plot_2d(vor)
plt.show()

import numpy as np 
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay, delaunay_plot_2d, tsearch

pts = np.random.rand(20, 2)
tri = Delaunay(pts)
_ = delaunay_plot_2d(tri)

loc = np.random.uniform(0.2, 0.8, (5, 2))
s = tsearch(tri, loc)
plt.triplot(pts[:, 0], pts[:, 1], tri.simplices[s], 'b-', mask=s==-1)
plt.scatter(loc[:, 0], loc[:, 1], c='r', marker='x')
plt.show()


