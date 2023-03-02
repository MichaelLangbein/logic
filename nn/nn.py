from nodes import Node, Variable, MatMul, Sigmoid, gradient
import numpy as np




"""
For a fully connected net:

yl = a(xl)
xl = Wl yl-1
E = \Sum(yObs - yL)^2

dE/dxL = - 2 \Sum (yObs - yL) da(xL)/dxL
dE/dxl = dE/dxl+1 dxl+1/dxl
                  dxl+1/dxl = Wl+1 da(xl)/dxl
dE/dWl = dE/dxl dxl/dWl 
                dxl/dWl = yl-1
delta Wl = - alpha dE/dWl

"""


