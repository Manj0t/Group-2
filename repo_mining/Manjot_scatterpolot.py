import matplotlib.pyplot as plt
import json

with open("data/author_touches.json") as f:
    data = json.load(f)

plt.figure()

i = 0
for author in data:
    file_x = []
    week_y = []
    for week, file_id in data[author]:
        file_x.append(file_id)
        week_y.append(week)

    if i < 10:
        marker = 'o'
    else:
        marker = 's'
    plt.scatter(file_x, week_y, label=author, marker=marker)
    i += 1
plt.title("Scatter plot of touches")
plt.xlabel("files")
plt.ylabel("weeks")
plt.grid(True)
plt.legend(
    title="Author",
    bbox_to_anchor=(1.05, 1),
    loc="upper left"
)
plt.tight_layout()
plt.savefig("data/scatter_plot_of_touches", dpi=200)
plt.show()
