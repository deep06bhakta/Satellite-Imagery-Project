
import tkinter as tk
from tkinter import *
import numpy as np
import time
import matplotlib
matplotlib.use('TKAgg')

import matplotlib.pyplot as pp
import scipy.integrate as integrate
import matplotlib.animation as animation
from matplotlib.patches import Rectangle

from math import pi
from numpy import sin, cos, sign

# physical constants
g = 9.81
L = 1.0
m = 0.5

# simulation time
dt = 0.05
Tmax = 100
t = np.arange(0.0, Tmax, dt)

# initial conditions
Y = .0 		# pendulum angular velocity
th = pi - 0.1		# pendulum angle
x = .0		# cart position
x0 = 0		# desired cart position
Z = -0.05	# cart velocity
k = 0.08	# control gain coefficient

# Controller coefficients
Kp_th = 50
Kd_th = 15
Kp_x = 3.1
Kd_x = 4.8

state = np.array([th, Y, x, Z])

stabilizing = False


def energy(th, dth):
	return m * dth * L * dth * L / 2 + m * g * L * (cos(th) - 1)

# Check if the pendulum is controllable by using the provided parameters
def isControllable(th, dth):
	return th < pi/9 and abs(energy(th, dth)) < 0.9

# Controller coefficients for the derivatives
def derivatives(state, t):
	global stabilizing
	ds = np.zeros_like(state)

	_th = state[0]
	_Y = state[1]	# th'
	_x = state[2]
	_Z = state[3]	# x'

	if stabilizing or isControllable(_th, _Y):
		stabilizing = True
		u = Kp_th * _th + Kd_th * _Y + Kp_x * (_x - x0) + Kd_x * _Z
	else:
		E = energy(_th, _Y)
		u = k * E * _Y * cos(_th)

	ds[0] = state[1]
	ds[1] = (g * sin(_th) - u * cos(_th)) / L
	ds[2] = state[3]
	ds[3] = u

	return ds

print("Integrating...")
# integrate your ODE using scipy.integrate.
solution = integrate.odeint(derivatives, state, t)
print("Done")

ths = solution[:, 0]
Ys = solution[:, 1]
xs = solution[:, 2]
vs = solution[:, 3]

pxs = L * sin(ths) + xs
pys = L * cos(ths)

# Create the GUI window
root = tk.Tk()
root.wm_title("Catching Pendulum")

# Create the canvas
fig = pp.figure(figsize=(5, 4))
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-1.5, 1.5), ylim=(-1.2, 1.2))
ax.set_aspect('equal')
ax.grid()

patch = ax.add_patch(Rectangle((0, 0), 0, 0, linewidth=1, edgecolor='k', facecolor='g'))

line, = ax.plot([], [], 'o-', lw=2)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

energy_template = 'E = %.3f J'
energy_text = ax.text(0.05, 0.85, '', transform=ax.transAxes)

cart_width = 0.3
cart_height = 0.2


def init():
    line.set_data([], [])
    time_text.set_text('')
    energy_text.set_text('')

    patch.set_xy((-cart_width/2, -cart_height/2))
    patch.set_width(cart_width)
    patch.set_height(cart_height)
    return line, time_text, energy_text, patch


def animate(i):
    thisx = [xs[i], pxs[i]]
    thisy = [0, pys[i]]

    line.set_data(thisx, thisy)
    time_text.set_text(time_template % (i*dt))
	
    E = energy(ths[i], Ys[i])

    energy_text.set_text(energy_template % (E))

    patch.set_x(xs[i] - cart_width/2)

    return line, time_text, energy_text, patch

# Set up the animation
ani = animation.FuncAnimation(fig, animate, np.arange(1, len(solution)),
                            	interval=25, blit=True, init_func=init)

# Add the animation to the GUI window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Start the GUI
root.mainloop()