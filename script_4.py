# Create route visualization for the best solutions
def create_route_visualizations():
    """Create visual maps of the best routes found by each algorithm"""
    
    fig, axes = plt.subplots(3, 3, figsize=(18, 15))
    fig.suptitle('Tourist Route Visualizations: Best Solutions by Algorithm and City', 
                 fontsize=16, fontweight='bold')
    
    datasets = {
        'Hanoi': hanoi_df,
        'Da Nang': danang_df, 
        'Ho Chi Minh City': hcmc_df
    }
    
    cities = ['Hanoi', 'Da Nang', 'Ho Chi Minh City']
    algorithms = ['GA', 'Greedy', 'Random']
    colors = {'GA': 'red', 'Greedy': 'blue', 'Random': 'green'}
    
    for i, city in enumerate(cities):
        df = datasets[city]
        
        for j, algorithm in enumerate(algorithms):
            ax = axes[i, j]
            
            # Plot hotel at origin
            ax.scatter(0, 0, c='black', s=200, marker='s', label='Hotel', zorder=5)
            ax.annotate('Hotel', (0, 0), xytext=(0.1, 0.1), fontsize=8, fontweight='bold')
            
            # Plot all attractions
            ax.scatter(df['x'], df['y'], c='lightgray', s=50, alpha=0.6, zorder=1)
            
            # Get the best route for this city/algorithm
            route = comparison_results[city][algorithm]['best_route']
            if route:
                # Plot route connections
                coords = [(0, 0)]  # Start from hotel
                for aid in route:
                    attraction_row = df[df['id'] == aid].iloc[0]
                    coords.append((attraction_row['x'], attraction_row['y']))
                coords.append((0, 0))  # Return to hotel
                
                # Draw route lines
                for k in range(len(coords)-1):
                    ax.plot([coords[k][0], coords[k+1][0]], 
                           [coords[k][1], coords[k+1][1]], 
                           c=colors[algorithm], linewidth=2, alpha=0.7, zorder=2)
                
                # Highlight route attractions
                for idx, aid in enumerate(route):
                    attraction_row = df[df['id'] == aid].iloc[0]
                    ax.scatter(attraction_row['x'], attraction_row['y'], 
                              c=colors[algorithm], s=100, zorder=3)
                    ax.annotate(f'{idx+1}', (attraction_row['x'], attraction_row['y']), 
                               xytext=(2, 2), textcoords='offset points', 
                               fontsize=6, fontweight='bold', zorder=4)
            
            # Formatting
            details = comparison_results[city][algorithm]['best_details']
            ax.set_title(f'{city} - {algorithm}\n'
                        f'Fitness: {details["fitness"]:.0f} | '
                        f'Distance: {details["total_dist"]:.1f}', 
                        fontsize=10, fontweight='bold')
            ax.set_xlabel('X Coordinate')
            ax.set_ylabel('Y Coordinate')
            ax.grid(True, alpha=0.3)
            ax.set_aspect('equal')
            
            # Set consistent axis limits for each city
            margin = 0.2
            x_min, x_max = df['x'].min() - margin, df['x'].max() + margin
            y_min, y_max = df['y'].min() - margin, df['y'].max() + margin
            ax.set_xlim(x_min, x_max)
            ax.set_ylim(y_min, y_max)
    
    plt.tight_layout()
    plt.savefig('tourist_route_visualizations.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("📍 Route visualizations saved as 'tourist_route_visualizations.png'")

# Create route visualizations
create_route_visualizations()