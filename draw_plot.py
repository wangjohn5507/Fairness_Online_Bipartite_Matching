import matplotlib.pyplot as plt

def draw_plot(data1, data2, title, name):

    # Extracting keys and values for the plot
    groups = list(data1.keys())
    weights1 = list(data1.values())
    weights2 = list(data2.values())

    # Correcting the relative positions of the bars in the combined bar chart for clarity and accuracy

    fig, ax = plt.subplots(figsize=(12, 8))
    bar_width = 0.35

    # Total weights calculation
    total_weight1 = sum(weights1)
    total_weight2 = sum(weights2)

    # Min-max difference calculation
    min_max_diff1 = max(weights1) - min(weights1)
    min_max_diff2 = max(weights2) - min(weights2)

    # Generating group labels and their corresponding indices
    group_labels = ['Group 1 Weight', 'Group 2 Weight', 'Group 3 Weight', 'Group 4 Weight', 'Total Weight', 'Min-Max Difference']
    index = range(len(group_labels))  # 0 to 5

    # Plotting weights for groups
    for i in range(4):  # First 4 groups
        ax.bar(i - 0.2, weights1[i], width=0.4, color='cornflowerblue', label='Our Alg' if i == 0 else "")
        ax.text(i - 0.2, weights1[i] + 10, f'{weights1[i]}', ha='center', va='bottom')
        ax.bar(i + 0.2, weights2[i], width=0.4, color='orange', label='Greedy Alg' if i == 0 else "")
        ax.text(i + 0.2, weights2[i] + 10, f'{weights2[i]}', ha='center', va='bottom')

    # Plotting total weight and min-max differences as additional bars
    ax.bar(4 - 0.2, total_weight1, width=0.4, color='cornflowerblue')
    ax.text(4 - 0.2, total_weight1 + 10, f'{total_weight1}', ha='center', va='bottom')
    ax.bar(4 + 0.2, total_weight2, width=0.4, color='orange')
    ax.text(4 + 0.2, total_weight2 + 10, f'{total_weight2}', ha='center', va='bottom')
    ax.bar(5 - 0.2, min_max_diff1, width=0.4, color='cornflowerblue')
    ax.text(5 - 0.2, min_max_diff1 + 10, f'{min_max_diff1}', ha='center', va='bottom')
    ax.bar(5 + 0.2, min_max_diff2, width=0.4, color='orange')
    ax.text(5 + 0.2, min_max_diff2 + 10, f'{min_max_diff2}', ha='center', va='bottom')

    # Setting chart details
    ax.set_xlabel('Metric')
    ax.set_ylabel('Value')
    ax.set_title(title)
    ax.set_xticks(index)
    ax.set_xticklabels(group_labels)
    ax.legend()

    plt.tight_layout()
    plt.show()
    fig.savefig(name)
