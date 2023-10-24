import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import numpy as np

# define constants for inverted pendulum system
m = 1.0 # mass of pendulum
M = 5.0 # mass of cart
g = 9.81 # gravitational constant
l = 2.0 # length of pendulum


# define functions for the ODEs
def f(t, y):
    theta, omega, x, v = y
    dydt = [omega,
            -(m*g*l*np.sin(theta))/(M+m*(np.sin(theta)**2)),
            v,
            (m*g*l*np.sin(theta)*np.cos(theta) + m*l*omega**2*np.sin(theta)*np.cos(theta) - (M+m)*v)/(l*(M+m*(np.sin(theta)**2)))]
    return dydt

# set up initial conditions and time array
y0 = [np.pi/2, 0, 0, 0]
t = np.linspace(0, 10, 1000)

# solve ODE
soln = solve_ivp(f, [t[0], t[-1]], y0, t_eval=t)

# plot results
plt.plot(soln.y[2], soln.y[3])
plt.xlabel('x')
plt.ylabel('v')
plt.title('Stabilization of Inverted Pendulum on a Cart')
plt.show()