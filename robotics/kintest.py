import numpy as np
import matplotlib.pyplot as plt

# ----- Parameters -----
S = 200   # side length of the frame (cm)
d = 30   # side length of the end effector (cm)

# Frame corners
frame_points = np.array([
    [-S/2,  S/2],  # top-left
    [ S/2,  S/2],  # top-right
    [ S/2, -S/2],  # bottom-right
    [-S/2, -S/2],  # bottom-left
])

# End effector corners in local coordinates (relative to center)
local_eff_points = np.array([
    [-d/2,  d/2],  # top-left
    [ d/2,  d/2],  # top-right
    [ d/2, -d/2],  # bottom-right
    [-d/2, -d/2],  # bottom-left
])


def compute_eff_points(x, y):
    """Return world coordinates of the end effector corners."""
    return local_eff_points + np.array([x, y])


def rope_lengths(frame_pts, eff_pts):
    """Compute the length of each rope."""
    diffs = eff_pts - frame_pts
    return np.linalg.norm(diffs, axis=1)


def plot_config(x, y):
    eff_points = compute_eff_points(x, y)
    lengths = rope_lengths(frame_points, eff_points)

    fig, ax = plt.subplots(figsize=(6, 6))

    # Draw frame
    frame_closed = np.vstack([frame_points, frame_points[0]])
    ax.plot(frame_closed[:, 0], frame_closed[:, 1], '-k')

    # Draw end effector
    eff_closed = np.vstack([eff_points, eff_points[0]])
    ax.plot(eff_closed[:, 0], eff_closed[:, 1], '-b')

    # Draw ropes
    for i in range(4):
        ax.plot(
            [frame_points[i, 0], eff_points[i, 0]],
            [frame_points[i, 1], eff_points[i, 1]],
            '--', color='gray'
        )

    # Text block (legend) for rope lengths
    text = "\n".join([
        f"Rope top-left: {lengths[0]:.3f}",
        f"Rope top-right: {lengths[1]:.3f}",
        f"Rope bottom-right: {lengths[2]:.3f}",
        f"Rope bottom-left: {lengths[3]:.3f}",
    ])

    ax.text(
        1.05, 0.5, text,
        transform=ax.transAxes,
        fontsize=10,
        va='center',
        ha='left',
        family='monospace'
    )

    # Axes formatting
    ax.set_aspect('equal', 'box')
    margin = S * 0.1
    ax.set_xlim(-S/2 - margin, S/2 + margin + 0.5)
    ax.set_ylim(-S/2 - margin, S/2 + margin)

    ax.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print("Basic ropebot visualisation. Close plot to enter new values.")
    print("Enter: x y   (press Ctrl+C/Ctrl+D to exit)\n")

    while True:
        try:
            line = input("x y > ").strip()
            if not line:
                continue
            x, y = map(float, line.split())
            plot_config(x, y)
        except KeyboardInterrupt:
            print("\nExiting.")
            break
        except Exception as e:
            print("Error:", e)
