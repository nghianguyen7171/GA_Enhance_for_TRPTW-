# Create comprehensive visualization and analysis

def create_comprehensive_analysis_report():
    """Generate comprehensive analysis and export data"""
    
    # Create comparison DataFrame for easier analysis
    comparison_data = []
    
    for city, results in comparison_results.items():
        for algorithm, result in results.items():
            details = result['best_details']
            
            # Calculate additional metrics
            attractions_visited = len(result['best_route']) if result['best_route'] else 0
            efficiency_ratio = details['total_dist'] / max(attractions_visited, 1)
            cost_efficiency = details['total_cost'] / max(attractions_visited, 1)
            
            comparison_data.append({
                'City': city,
                'Algorithm': algorithm,
                'Fitness_Score': details['fitness'],
                'Total_Distance': details['total_dist'],
                'Total_Cost': details['total_cost'],
                'Total_Time_Hours': details['total_time'] / 60,
                'Execution_Time': result['execution_time'],
                'Attractions_Visited': attractions_visited,
                'Feasible': details['feasible'],
                'Distance_Efficiency': efficiency_ratio,
                'Cost_Efficiency': cost_efficiency,
                'Time_Violations': details['violations']['time'] if 'violations' in details else 0,
                'Budget_Violation': details['violations']['budget'] if 'violations' in details else 0
            })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    # Save detailed results to CSV
    comparison_df.to_csv('tourist_route_comparison_results.csv', index=False)
    
    print("📊 COMPREHENSIVE ANALYSIS REPORT")
    print("="*70)
    
    # Performance by Algorithm
    print("\n1️⃣ ALGORITHM PERFORMANCE SUMMARY")
    print("-" * 50)
    
    algo_summary = comparison_df.groupby('Algorithm').agg({
        'Fitness_Score': ['mean', 'std', 'min'],
        'Total_Distance': ['mean', 'std'],
        'Execution_Time': ['mean', 'std'],
        'Attractions_Visited': 'mean'
    }).round(3)
    
    print(algo_summary)
    
    # Performance by City
    print("\n2️⃣ PERFORMANCE BY CITY")
    print("-" * 50)
    
    city_summary = comparison_df.groupby('City').agg({
        'Fitness_Score': ['mean', 'min'],
        'Total_Distance': 'mean',
        'Total_Cost': 'mean',
        'Attractions_Visited': 'mean'
    }).round(2)
    
    print(city_summary)
    
    # Best performing algorithm per city
    print("\n3️⃣ BEST ALGORITHM PER CITY")
    print("-" * 50)
    
    for city in comparison_df['City'].unique():
        city_data = comparison_df[comparison_df['City'] == city]
        best_algo = city_data.loc[city_data['Fitness_Score'].idxmin()]
        print(f"{city:15s}: {best_algo['Algorithm']:8s} "
              f"(Fitness: {best_algo['Fitness_Score']:.1f}, "
              f"Distance: {best_algo['Total_Distance']:.2f}, "
              f"Time: {best_algo['Execution_Time']:.3f}s)")
    
    # Feasibility Analysis
    print("\n4️⃣ FEASIBILITY ANALYSIS")
    print("-" * 50)
    
    feasible_count = comparison_df.groupby('Algorithm')['Feasible'].sum()
    total_count = comparison_df.groupby('Algorithm').size()
    feasibility_rate = (feasible_count / total_count * 100).round(1)
    
    print("Feasibility Rate by Algorithm:")
    for algo in feasibility_rate.index:
        print(f"  {algo:8s}: {feasibility_rate[algo]:5.1f}% "
              f"({feasible_count[algo]}/{total_count[algo]} cases)")
    
    # Dataset complexity analysis
    print("\n5️⃣ DATASET COMPLEXITY IMPACT")
    print("-" * 50)
    
    dataset_info = {
        'Hanoi': len(hanoi_df),
        'Da Nang': len(danang_df),
        'Ho Chi Minh City': len(hcmc_df)
    }
    
    complexity_analysis = comparison_df.groupby('City').agg({
        'Fitness_Score': 'mean',
        'Execution_Time': 'mean',
        'Total_Distance': 'mean'
    }).round(3)
    
    for city in complexity_analysis.index:
        size = dataset_info[city]
        avg_fitness = complexity_analysis.loc[city, 'Fitness_Score']
        avg_time = complexity_analysis.loc[city, 'Execution_Time']
        print(f"{city:15s}: {size:2d} attractions | "
              f"Avg Fitness: {avg_fitness:8.1f} | "
              f"Avg Time: {avg_time:.3f}s")
    
    # Export detailed route information
    detailed_routes = []
    
    for city, results in comparison_results.items():
        for algorithm, result in results.items():
            if result['best_route']:
                route_info = {
                    'city': city,
                    'algorithm': algorithm,
                    'route': result['best_route'],
                    'fitness': result['best_details']['fitness'],
                    'distance': result['best_details']['total_dist'],
                    'cost': result['best_details']['total_cost'],
                    'feasible': result['best_details']['feasible']
                }
                detailed_routes.append(route_info)
    
    # Save detailed route information
    import json
    with open('detailed_routes.json', 'w') as f:
        json.dump(detailed_routes, f, indent=2)
    
    print(f"\n📁 Files Generated:")
    print(f"   • tourist_route_comparison_results.csv")
    print(f"   • detailed_routes.json")
    
    return comparison_df

# Generate comprehensive analysis
analysis_df = create_comprehensive_analysis_report()