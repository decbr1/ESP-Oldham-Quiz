import sys
try:
    from .logger import critical
    from .colours import c
except ImportError:
    from logger import critical
    from colours import c
crashLater = False
try:
    import matplotlib.pyplot as plt
except ImportError:
    critical("matplotlib is not installed in this environment")
    crashLater = True
try:
    import pandas as pd
except ImportError:
    critical("pandas is not installed in this environment")
    crashLater = True
if crashLater:
    sys.exit()

def plot_bar(df: pd.DataFrame, metric_col: str, title: str):
    """Display a bar chart for the chosen metric"""
    names   = df["player_name"]
    values  = df[metric_col]

    plt.figure(figsize=(8,5))
    bars = plt.bar(names, values, color=["#4C78A8", "#F58518", "#54A24B"])
    plt.title(title)
    plt.xlabel("Player")
    plt.ylabel(metric_col)
    plt.grid(axis="y", linestyle="--", alpha=0.4)

    for bar, val in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_width(),
        f"{val}", ha="center", va="bottom", fontsize=10)
    plt.tight_layout()
    plt.show()

def plot_pie(df: pd.DataFrame, metric_col: str, title: str):
    """Display a pie chart for the chosen metric"""
    names   = df["player_name"]
    values  = df[metric_col].astype(float)
    total   = float(values.sum())
    
    if total == 0.0:
        print("\nCannot display a pie chart because the total value is 0.")
        return
    
    plt.figure(figsize=(6,6))
    plt.pie(
        values,
        labels=names,
        autopct=lambda pct: f"{pct:.1f}%\n({round(pct*total/100, 2)})",
        startangle=90,
        colors=["#4C78A8", "#F58518", "#54A24B"]
    )
    plt.title(title)
    plt.tight_layout()
    plt.show()
