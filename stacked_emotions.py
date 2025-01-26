import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("emotion_log.csv")

# Make srue 'time_seconds' and 'dominant_emotion' are integers
df["time_seconds"] = df["time_seconds"].astype(int)
df["dominant_emotion"] = df["dominant_emotion"].astype(int)

# Sort values to make sure they are ordered properly
df = df.sort_values(by="time_seconds")

df['time_index'] = range(1, len(df) + 1)

# Properly plot and format the graph
pivoted = df.pivot_table(
    index="time_index",  
    columns="dominant_emotion",
    aggfunc="size",
    fill_value=0
)

# Plot the data
plt.figure(figsize=(10, 5))
pivoted.plot(
    kind="area",
    stacked=True,
    colormap="viridis",
    ax=plt.gca()
)

# Fix Y-axis scaling: Set max to 1, since each second should have one emotion
plt.ylim(0, 1)

# Set fonts for labels
plt.title("Emotion Distribution Over Time", fontsize=14, fontweight="bold")
plt.xlabel("Seconds from Start", fontsize=12)
plt.ylabel("Emotion Count (1 per second)", fontsize=12)

# Increase space between x-axis integers
plt.xticks(range(1, len(pivoted) + 1, 4), labels=range(1, len(pivoted) + 1, 4))  # Adjust step size here

# Add gridlines
plt.grid(axis="both", linestyle="-")

# Move the key to the right side
plt.legend(title="Emotion", bbox_to_anchor=(1.05, 0.5), loc="center left")

plt.tight_layout()

save_path = '/Users/nicolestott/Desktop/Desktop - Nicole’s MacBook Pro/UAL/year 3/emotion_distribution.png'

# Save the graph as a PNG image at the specified location
plt.savefig(save_path, dpi=300)

# Show the updated chart
plt.show()