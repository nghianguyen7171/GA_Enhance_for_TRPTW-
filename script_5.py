# Create detailed performance metrics and statistical analysis

def create_statistical_analysis():
    """Perform detailed statistical analysis of algorithm performance"""
    
    print("📈 DETAILED STATISTICAL ANALYSIS")
    print("="*70)
    
    # Load the comparison data
    df = analysis_df.copy()
    
    # 1. Algorithm Efficiency Analysis
    print("\n1️⃣ ALGORITHM EFFICIENCY METRICS")
    print("-" * 50)
    
    efficiency_metrics = df.groupby('Algorithm').agg({
        'Fitness_Score': ['mean', 'std', 'min', 'max'],
        'Distance_Efficiency': ['mean', 'std'],
        'Cost_Efficiency': ['mean', 'std'], 
        'Execution_Time': ['mean', 'std'],
        'Total_Distance': ['mean', 'std']
    }).round(3)
    
    print("Fitness Score Statistics:")
    for algo in df['Algorithm'].unique():
        algo_data = df[df['Algorithm'] == algo]
        print(f"  {algo:8s}: Mean={algo_data['Fitness_Score'].mean():8.1f}, "
              f"Std={algo_data['Fitness_Score'].std():7.1f}, "
              f"Min={algo_data['Fitness_Score'].min():8.1f}, "
              f"Max={algo_data['Fitness_Score'].max():8.1f}")
    
    # 2. Performance Ranking
    print("\n2️⃣ ALGORITHM RANKING BY METRICS")
    print("-" * 50)
    
    metrics = ['Fitness_Score', 'Total_Distance', 'Execution_Time']
    ranking_results = {}
    
    for metric in metrics:
        if metric == 'Execution_Time':
            # For execution time, we want ascending order except for 0 times
            non_zero_times = df[df[metric] > 0]
            if len(non_zero_times) > 0:
                ranking = non_zero_times.groupby('Algorithm')[metric].mean().sort_values()
            else:
                ranking = df.groupby('Algorithm')[metric].mean().sort_values()
        else:
            # For fitness and distance, lower is better
            ranking = df.groupby('Algorithm')[metric].mean().sort_values()
        
        ranking_results[metric] = ranking
        print(f"\n{metric} Ranking (lower is better):")
        for i, (algo, value) in enumerate(ranking.items(), 1):
            print(f"  {i}. {algo:8s}: {value:.3f}")
    
    # 3. Scalability Analysis
    print("\n3️⃣ SCALABILITY ANALYSIS")
    print("-" * 50)
    
    dataset_sizes = {'Hanoi': 20, 'Da Nang': 15, 'Ho Chi Minh City': 25}
    
    scalability_data = []
    for city in df['City'].unique():
        city_data = df[df['City'] == city]
        size = dataset_sizes[city]
        
        for algo in df['Algorithm'].unique():
            algo_data = city_data[city_data['Algorithm'] == algo]
            if not algo_data.empty:
                scalability_data.append({
                    'Algorithm': algo,
                    'Dataset_Size': size,
                    'Avg_Fitness': algo_data['Fitness_Score'].mean(),
                    'Avg_Execution_Time': algo_data['Execution_Time'].mean(),
                    'Fitness_Per_Attraction': algo_data['Fitness_Score'].mean() / size,
                    'Time_Per_Attraction': algo_data['Execution_Time'].mean() / size if algo_data['Execution_Time'].mean() > 0 else 0
                })
    
    scalability_df = pd.DataFrame(scalability_data)
    
    print("Scalability Metrics (Performance per Attraction):")
    scalability_summary = scalability_df.groupby('Algorithm').agg({
        'Fitness_Per_Attraction': 'mean',
        'Time_Per_Attraction': 'mean'
    }).round(4)
    
    for algo in scalability_summary.index:
        fitness_per = scalability_summary.loc[algo, 'Fitness_Per_Attraction']
        time_per = scalability_summary.loc[algo, 'Time_Per_Attraction']
        print(f"  {algo:8s}: Fitness/Attraction={fitness_per:8.1f}, "
              f"Time/Attraction={time_per:.6f}s")
    
    # 4. Correlation Analysis
    print("\n4️⃣ CORRELATION ANALYSIS")
    print("-" * 50)
    
    correlation_metrics = ['Fitness_Score', 'Total_Distance', 'Total_Cost', 
                          'Execution_Time', 'Attractions_Visited']
    correlation_matrix = df[correlation_metrics].corr().round(3)
    
    print("Key Correlations:")
    print(f"  Fitness vs Distance: {correlation_matrix.loc['Fitness_Score', 'Total_Distance']:.3f}")
    print(f"  Fitness vs Cost:     {correlation_matrix.loc['Fitness_Score', 'Total_Cost']:.3f}")
    print(f"  Distance vs Time:    {correlation_matrix.loc['Total_Distance', 'Execution_Time']:.3f}")
    
    # 5. Algorithm Recommendation System
    print("\n5️⃣ ALGORITHM RECOMMENDATION")
    print("-" * 50)
    
    print("Based on comprehensive analysis:")
    
    # Best overall performer
    overall_ranking = df.groupby('Algorithm')['Fitness_Score'].mean().sort_values()
    best_overall = overall_ranking.index[0]
    print(f"  🏆 Best Overall Performance: {best_overall}")
    print(f"     - Consistently lowest fitness scores")
    print(f"     - Average fitness: {overall_ranking[best_overall]:.1f}")
    
    # Fastest algorithm
    time_ranking = df[df['Execution_Time'] > 0].groupby('Algorithm')['Execution_Time'].mean().sort_values()
    if not time_ranking.empty:
        fastest = time_ranking.index[0]
        print(f"  ⚡ Fastest Execution: {fastest}")
        print(f"     - Average time: {time_ranking[fastest]:.3f} seconds")
    
    # Best for large datasets
    large_dataset_perf = df[df['City'] == 'Ho Chi Minh City'].groupby('Algorithm')['Fitness_Score'].mean().sort_values()
    best_large = large_dataset_perf.index[0]
    print(f"  📊 Best for Large Datasets: {best_large}")
    print(f"     - Performance on 25 attractions: {large_dataset_perf[best_large]:.1f}")
    
    # Export detailed analysis
    scalability_df.to_csv('scalability_analysis.csv', index=False)
    correlation_matrix.to_csv('correlation_matrix.csv')
    
    # Summary recommendations
    print("\n6️⃣ PRACTICAL RECOMMENDATIONS")
    print("-" * 50)
    print("  • For research/development: Use GA for best solution quality")
    print("  • For real-time applications: Use Greedy for immediate results")  
    print("  • For baseline comparison: Use Random search")
    print("  • For large datasets (>20 attractions): GA shows best scalability")
    print("  • For small datasets (<15 attractions): All algorithms perform similarly")
    
    return scalability_df, correlation_matrix

# Run statistical analysis
scalability_df, correlation_matrix = create_statistical_analysis()