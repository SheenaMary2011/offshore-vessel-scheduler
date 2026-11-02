import pandas as pd
import matplotlib.pyplot as plt


def draw_schedule(ax, schedule, title):
    vessels = sorted(schedule["vessel"].unique())      # ["VESSEL_1", "VESSEL_2"]

    for index, row in schedule.iterrows():
        y = vessels.index(row["vessel"])               # which row: 0 or 1
        length = row["finish_day"] - row["start_day"] + 1

        # one bar: at row y, starting at start_day, "length" days long
        ax.barh(y, length, left=row["start_day"] - 0.5, height=0.5, color="#4C78A8", edgecolor="white")

        # the job name in the middle of the bar
        ax.text(row["start_day"] - 0.5 + length / 2, y, row["job_id"],
                ha="center", va="center", color="white", fontsize=8)
        last_day = schedule["finish_day"].max()                 # the latest finish in this schedule
    ax.axvline(last_day + 0.5, color="#E45756", linestyle="--")        # vertical dashed line
    ax.text(last_day + 0.7, len(vessels) - 0.6, f"finishes day {last_day}", color="#E45756")
    ax.set_yticks(range(len(vessels)))      # put a label on each row...
    ax.set_yticklabels(vessels)             # ...with the vessel names
    ax.set_xlim(0.5, 30.5)                  # show days 1 to 30
    ax.set_title(title)


if __name__ == "__main__":
    baseline = pd.read_csv("data/baseline_schedule.csv")
    optimized = pd.read_csv("data/optimized_schedule.csv")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 5), sharex=True)
    draw_schedule(ax1, baseline, "Greedy baseline")
    draw_schedule(ax2, optimized, "OR-Tools optimizer")
    ax2.set_xlabel("Day of November 2026")
    plt.tight_layout()
    plt.savefig("schedule_comparison.png", dpi=150)
    plt.show()