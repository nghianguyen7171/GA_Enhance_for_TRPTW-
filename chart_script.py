import pandas as pd
import plotly.express as px

# Create dataframe from the provided data
data = [
    {"City": "Hanoi", "Algorithm": "GA", "Fitness_Score": 15108.91, "Execution_Time": 0.194, "Distance_Efficiency": 1.262},
    {"City": "Hanoi", "Algorithm": "Greedy", "Fitness_Score": 17107.36, "Execution_Time": 0.0, "Distance_Efficiency": 0.879},
    {"City": "Hanoi", "Algorithm": "Random", "Fitness_Score": 17133.57, "Execution_Time": 0.067, "Distance_Efficiency": 1.751},
    {"City": "Da Nang", "Algorithm": "GA", "Fitness_Score": 11066.55, "Execution_Time": 0.168, "Distance_Efficiency": 0.947},
    {"City": "Da Nang", "Algorithm": "Greedy", "Fitness_Score": 12068.09, "Execution_Time": 0.0, "Distance_Efficiency": 0.773},
    {"City": "Da Nang", "Algorithm": "Random", "Fitness_Score": 12077.69, "Execution_Time": 0.055, "Distance_Efficiency": 1.219},
    {"City": "HCMC", "Algorithm": "GA", "Fitness_Score": 19139.71, "Execution_Time": 0.336, "Distance_Efficiency": 1.19},
    {"City": "HCMC", "Algorithm": "Greedy", "Fitness_Score": 24151.23, "Execution_Time": 0.0, "Distance_Efficiency": 0.83},
    {"City": "HCMC", "Algorithm": "Random", "Fitness_Score": 23197.36, "Execution_Time": 0.081, "Distance_Efficiency": 2.196}
]

df = pd.DataFrame(data)

# Convert fitness scores to thousands for better readability
df['Fitness_k'] = df['Fitness_Score'] / 1000

# Create grouped bar chart for fitness scores comparison
fig = px.bar(df, 
             x="City", 
             y="Fitness_k", 
             color="Algorithm",
             barmode="group",
             title="Algorithm Fitness Scores by City",
             color_discrete_sequence=["#1FB8CD", "#DB4545", "#2E8B57"],
             hover_data={'Fitness_k': ':.1f', 'Execution_Time': ':.3f', 'Distance_Efficiency': ':.2f'})

# Update axes labels
fig.update_yaxes(title="Fitness (k)")
fig.update_xaxes(title="City")

# Update traces
fig.update_traces(cliponaxis=False)

# Center legend since there are 3 items (≤5)
fig.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5))

# Save as both PNG and SVG
fig.write_image("chart.png")
fig.write_image("chart.svg", format="svg")

fig.show()