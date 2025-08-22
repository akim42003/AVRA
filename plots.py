import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# ---- Data (copied from LaTeX tables) ----
epochs     = [1, 2, 3, 4, 5, 6]
train_loss = [1.394666, 0.764612, 0.548216, 0.302725, 0.116176, 0.064901]

val_loss = [0.781375, 0.653277, 0.445461, 0.320593, 0.185138, 0.111533]
val_acc  = [68.0, 72.3, 82.4, 88.5, 93.8, 96.2]  # in percent

# ---- Plotting ----
plt.style.use("seaborn-v0_8-whitegrid")
fig, ax1 = plt.subplots(figsize=(8, 5.5))

# Loss curves (left axis)
ax1.plot(epochs, train_loss, marker='o', linewidth=2, color="#1f77b4", label="Training Loss")
ax1.plot(epochs, val_loss,   marker='s', linewidth=2, color="#ff7f0e", label="Validation Loss")
ax1.set_xlabel("Epoch")
ax1.set_ylabel("Loss")
ax1.set_xticks(epochs)
ax1.set_title("Learning Curves")

# Accuracy curve (right axis)
ax2 = ax1.twinx()
ax2.plot(epochs, val_acc, marker='^', linewidth=2, color="#2ca02c", label="Validation Accuracy")
ax2.set_ylabel("Accuracy")
ax2.yaxis.set_major_formatter(PercentFormatter(xmax=100))

# Combine legends from both axes
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="center right")

# Cosmetics
ax1.grid(True, which="both", linestyle="--", alpha=0.4)
fig.tight_layout()

# Save figure
plt.savefig("learning_curves.png", dpi=200, bbox_inches="tight")
plt.show()
