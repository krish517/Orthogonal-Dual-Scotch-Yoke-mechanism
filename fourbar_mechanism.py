import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter

# ------------------------------------------------------
# Mechanism: Orthogonal dual Scotch-yoke (two-DOF)
# ------------------------------------------------------
# Idea: Two independent cranks drive perpendicular sliders.
#       The tracing point is the intersection of the sliders:
#           x(t) = Rx * cos(ωx t + φx)
#           y(t) = Ry * sin(ωy t + φy)
# If the frequency ratio ωy/ωx is irrational (≈ golden ratio),
# the path is quasi-periodic and never exactly repeats.

# Parameters
Rx = 3.0          # crank radius for X-slider
Ry = 2.0          # crank radius for Y-slider
omega_x = 1.0     # rad/s (unitless time in animation)
phi_x = 0.0       # phase offset for x

# Use golden ratio for incommensurate frequency ratio
phi = (1 + np.sqrt(5)) / 2
omega_y = phi * omega_x
phi_y = 0.0

# Animation timing
T = 60                    # total "time" units to simulate
fps = 20                    # frames per second (animation granularity)
N = int(T * fps)            # total frames

# Storage for the traced path (cap to avoid memory blow-up)
trail_max = 8000            # number of trail points to keep on screen
trail_x, trail_y = [], []

# Kinematics helpers

def crank_pin_x(t):
    # crank 1 pin (driving horizontal slider) about origin
    return Rx * np.cos(omega_x * t + phi_x), Rx * np.sin(omega_x * t + phi_x)

def crank_pin_y(t):
    # crank 2 pin (driving vertical slider) about origin
    return Ry * np.cos(omega_y * t + phi_y), Ry * np.sin(omega_y * t + phi_y)

def sliders_intersection(t):
    # Intersection of sliders equals the slider setpoints
    x = Rx * np.cos(omega_x * t + phi_x)
    y = Ry * np.sin(omega_y * t + phi_y)
    return x, y

# ------------------------------------------------------
# Plot/animation setup
# ------------------------------------------------------
fig, ax = plt.subplots()
ax.set_aspect('equal', 'box')
margin = 0.8
xlim = (-Rx - 1.5, Rx + 1.5)
ylim = (-Ry - 1.5, Ry + 1.5)
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Orthogonal Dual Scotch-Yoke: Quasi-Periodic (Non-Repeating) Path')

# Static slider rails
ax.axhline(0, lw=1, alpha=0.6)
ax.axvline(0, lw=1, alpha=0.6)

# Artists
link1, = ax.plot([], [], 'o-', lw=2)   # crank 1 (to horizontal slider)
link2, = ax.plot([], [], 'o-', lw=2)   # crank 2 (to vertical slider)
slider_x_marker, = ax.plot([], [], 's', ms=6)  # horizontal slider position at (x, 0)
slider_y_marker, = ax.plot([], [], 's', ms=6)  # vertical slider position at (0, y)
trace_point, = ax.plot([], [], 'o', ms=6)      # intersection point (x, y)
trail_line, = ax.plot([], [], '-', lw=1, alpha=0.8)  # path trail

# Time array for frames
# Note: we step by dt = 1/fps to keep animation smooth
t_values = np.linspace(0, T, N)

# Init function

def init():
    link1.set_data([], [])
    link2.set_data([], [])
    slider_x_marker.set_data([], [])
    slider_y_marker.set_data([], [])
    trace_point.set_data([], [])
    trail_line.set_data([], [])
    return link1, link2, slider_x_marker, slider_y_marker, trace_point, trail_line

# Update function per frame

def update(frame):
    t = t_values[frame]

    # Crank pins
    cx1, cy1 = crank_pin_x(t)
    cx2, cy2 = crank_pin_y(t)

    # Slider intersection (tracing point)
    x, y = sliders_intersection(t)

    # Update crank link drawings (origin -> pin)
    link1.set_data([0, cx1], [0, cy1])
    link2.set_data([0, cx2], [0, cy2])

    # Update slider markers
    slider_x_marker.set_data([x], [0])
    slider_y_marker.set_data([0], [y])

    # Update trace point
    trace_point.set_data([x], [y])

    # Update trail (keep last trail_max points)
    trail_x.append(x)
    trail_y.append(y)
    if len(trail_x) > trail_max:
        del trail_x[:len(trail_x)-trail_max]
        del trail_y[:len(trail_y)-trail_max]
    trail_line.set_data(trail_x, trail_y)

    return link1, link2, slider_x_marker, slider_y_marker, trace_point, trail_line

ani = FuncAnimation(fig, update, frames=N, init_func=init,
                    blit=True, interval=1000/fps, repeat=True)

plt.show()