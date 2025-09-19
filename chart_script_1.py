import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Create DataFrame from the data
data = [
    {"city": "Hanoi", "generation": 0, "best_fitness": 25000, "avg_fitness": 35000, "converged": False},
    {"city": "Hanoi", "generation": 10, "best_fitness": 20000, "avg_fitness": 28000, "converged": False},
    {"city": "Hanoi", "generation": 20, "best_fitness": 18000, "avg_fitness": 25000, "converged": False},
    {"city": "Hanoi", "generation": 30, "best_fitness": 16000, "avg_fitness": 22000, "converged": False},
    {"city": "Hanoi", "generation": 38, "best_fitness": 15108.91, "avg_fitness": 20000, "converged": True},
    {"city": "Hanoi", "generation": 50, "best_fitness": 15108.91, "avg_fitness": 19500, "converged": True},
    {"city": "Da Nang", "generation": 0, "best_fitness": 18000, "avg_fitness": 25000, "converged": False},
    {"city": "Da Nang", "generation": 10, "best_fitness": 14000, "avg_fitness": 20000, "converged": False},
    {"city": "Da Nang", "generation": 20, "best_fitness": 12000, "avg_fitness": 17000, "converged": False},
    {"city": "Da Nang", "generation": 23, "best_fitness": 11066.55, "avg_fitness": 16000, "converged": True},
    {"city": "Da Nang", "generation": 40, "best_fitness": 11066.55, "avg_fitness": 15500, "converged": True},
    {"city": "Ho Chi Minh City", "generation": 0, "best_fitness": 30000, "avg_fitness": 40000, "converged": False},
    {"city": "Ho Chi Minh City", "generation": 10, "best_fitness": 25000, "avg_fitness": 32000, "converged": False},
    {"city": "Ho Chi Minh City", "generation": 20, "best_fitness": 22000, "avg_fitness": 28000, "converged": False},
    {"city": "Ho Chi Minh City", "generation": 30, "best_fitness": 20000, "avg_fitness": 25000, "converged": False},
    {"city": "Ho Chi Minh City", "generation": 36, "best_fitness": 19139.71, "avg_fitness": 24000, "converged": True},
    {"city": "Ho Chi Minh City", "generation": 50, "best_fitness": 19139.71, "avg_fitness": 23500, "converged": True}
]

df = pd.DataFrame(data)

# Create figure
fig = go.Figure()

# Define colors in order
colors = ['#1FB8CD', '#DB4545', '#2E8B57', '#5D878F', '#D2BA4C', '#B4413C']

# Add traces for each city
cities = ['Hanoi', 'Da Nang', 'Ho Chi Minh City']
city_short = ['Hanoi', 'Da Nang', 'HCMC']

for i, city in enumerate(cities):
    city_data = df[df['city'] == city]
    
    # Best fitness line
    fig.add_trace(go.Scatter(
        x=city_data['generation'],
        y=city_data['best_fitness'],
        mode='lines+markers',
        name=f'{city_short[i]} Best',
        line=dict(color=colors[i*2], width=2),
        marker=dict(size=4),
        hovertemplate='Gen: %{x}<br>Best: %{y:.0f}<extra></extra>'
    ))
    
    # Average fitness line
    fig.add_trace(go.Scatter(
        x=city_data['generation'],
        y=city_data['avg_fitness'],
        mode='lines+markers',
        name=f'{city_short[i]} Avg',
        line=dict(color=colors[i*2+1], width=2, dash='dash'),
        marker=dict(size=4),
        hovertemplate='Gen: %{x}<br>Avg: %{y:.0f}<extra></extra>'
    ))

# Add convergence markers
for i, city in enumerate(cities):
    city_data = df[df['city'] == city]
    converged_data = city_data[city_data['converged'] == True]
    if not converged_data.empty:
        first_converged = converged_data.iloc[0]
        
        # Marker for best fitness convergence
        fig.add_trace(go.Scatter(
            x=[first_converged['generation']],
            y=[first_converged['best_fitness']],
            mode='markers',
            marker=dict(
                size=10,
                color=colors[i*2],
                symbol='star',
                line=dict(width=2, color='white')
            ),
            showlegend=False,
            hovertemplate=f'{city_short[i]} Conv: Gen %{{x}}<extra></extra>'
        ))

# Update layout
fig.update_layout(
    title='GA Convergence Analysis',
    xaxis_title='Generation',
    yaxis_title='Fitness Score',
    showlegend=True
)

# Update axes with grid
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

# Format y-axis to show values in k format
fig.update_yaxes(
    tickformat=',.0f',
    tickvals=[10000, 15000, 20000, 25000, 30000, 35000, 40000],
    ticktext=['10k', '15k', '20k', '25k', '30k', '35k', '40k']
)

# Update traces
fig.update_traces(cliponaxis=False)

# Center legend under title since we have 6 legend items (more than 5)
# Keep default legend position

# Save the chart
fig.write_image("chart.png")
fig.write_image("chart.svg", format="svg")

print("Chart saved as chart.png and chart.svg")