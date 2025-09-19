# Create comparison methods - implement different optimization algorithms for comparison

class GreedyTRP:
    """Greedy algorithm for tourist route planning"""
    
    def __init__(self, df, city_name, budget, hotel=(0,0)):
        self.df = df
        self.city_name = city_name
        self.hotel = hotel
        self.budget = budget
        
        self.attraction_ids = list(df['id'])
        self.coord = {row.id: (row.x, row.y) for row in df.itertuples()}
        self.open_min = {row.id: row.open_min for row in df.itertuples()}
        self.close_min = {row.id: row.close_min for row in df.itertuples()}
        self.dur = {row.id: row.duration for row in df.itertuples()}
        self.cost = {row.id: row.cost for row in df.itertuples()}
    
    def run(self):
        """Greedy nearest neighbor algorithm"""
        start_time = time.time()
        
        unvisited = self.attraction_ids.copy()
        route = []
        current_pos = self.hotel
        total_cost = 0
        
        while unvisited:
            # Find feasible attractions (budget and time constraints)
            feasible = []
            for aid in unvisited:
                if total_cost + self.cost[aid] <= self.budget:
                    feasible.append(aid)
            
            if not feasible:
                break
                
            # Choose nearest feasible attraction
            distances = [(aid, euclidean(current_pos, self.coord[aid])) for aid in feasible]
            distances.sort(key=lambda x: x[1])
            
            best_id = distances[0][0]
            route.append(best_id)
            unvisited.remove(best_id)
            current_pos = self.coord[best_id]
            total_cost += self.cost[best_id]
        
        # Evaluate the route
        if route:
            eval_result = self._evaluate_route(route)
        else:
            eval_result = {
                'fitness': float('inf'),
                'total_dist': 0,
                'total_cost': 0,
                'total_time': 0,
                'feasible': False,
                'route_times': []
            }
        
        execution_time = time.time() - start_time
        
        return {
            'best_route': route,
            'best_details': eval_result,
            'execution_time': execution_time,
            'attractions_visited': len(route)
        }
    
    def _evaluate_route(self, perm):
        """Evaluate route quality - same as GA evaluation"""
        t = 0
        total_dist = 0.0
        total_cost = 0
        feasible = True
        route_times = []
        violations = {'time': 0, 'budget': 0}
        
        cur = self.hotel
        
        for aid in perm:
            coord = self.coord[aid]
            travel_time = euclidean(cur, coord) * 30
            total_dist += euclidean(cur, coord)
            t += travel_time
            
            open_time = self.open_min[aid]
            close_time = self.close_min[aid]
            
            if t < open_time:
                t = open_time
                
            if t > close_time:
                feasible = False
                violations['time'] += 1
                t += 300
                
            start_time = t
            t += self.dur[aid]
            leave_time = t
            total_cost += self.cost[aid]
            
            route_times.append((aid, start_time, leave_time))
            cur = coord
        
        travel_time = euclidean(cur, self.hotel) * 30
        t += travel_time
        total_dist += euclidean(cur, self.hotel)
        
        if total_cost > self.budget:
            feasible = False
            violations['budget'] = total_cost - self.budget
            
        fitness_score = total_dist + t/60.0
        if not feasible:
            fitness_score += 5000
            fitness_score += violations['time'] * 1000
            fitness_score += max(0, violations['budget']) * 0.01
            
        return {
            'fitness': fitness_score,
            'total_dist': total_dist,
            'total_cost': total_cost,
            'total_time': t,
            'route_times': route_times,
            'feasible': feasible,
            'violations': violations
        }

class RandomTRP:
    """Random search algorithm for comparison"""
    
    def __init__(self, df, city_name, budget, hotel=(0,0), iterations=1000):
        self.df = df
        self.city_name = city_name
        self.hotel = hotel
        self.budget = budget
        self.iterations = iterations
        
        self.attraction_ids = list(df['id'])
        self.coord = {row.id: (row.x, row.y) for row in df.itertuples()}
        self.open_min = {row.id: row.open_min for row in df.itertuples()}
        self.close_min = {row.id: row.close_min for row in df.itertuples()}
        self.dur = {row.id: row.duration for row in df.itertuples()}
        self.cost = {row.id: row.cost for row in df.itertuples()}
        
    def run(self):
        """Random search with multiple iterations"""
        start_time = time.time()
        
        best_route = None
        best_details = None
        best_score = float('inf')
        
        for _ in range(self.iterations):
            # Generate random route
            route = self.attraction_ids.copy()
            random.shuffle(route)
            
            # Evaluate route
            eval_result = self._evaluate_route(route)
            
            if eval_result['fitness'] < best_score:
                best_score = eval_result['fitness']
                best_route = route.copy()
                best_details = eval_result
        
        execution_time = time.time() - start_time
        
        return {
            'best_route': best_route,
            'best_details': best_details,
            'execution_time': execution_time,
            'iterations': self.iterations
        }
    
    def _evaluate_route(self, perm):
        """Same evaluation as GA"""
        t = 0
        total_dist = 0.0
        total_cost = 0
        feasible = True
        route_times = []
        violations = {'time': 0, 'budget': 0}
        
        cur = self.hotel
        
        for aid in perm:
            coord = self.coord[aid]
            travel_time = euclidean(cur, coord) * 30
            total_dist += euclidean(cur, coord)
            t += travel_time
            
            open_time = self.open_min[aid]
            close_time = self.close_min[aid]
            
            if t < open_time:
                t = open_time
                
            if t > close_time:
                feasible = False
                violations['time'] += 1
                t += 300
                
            start_time = t
            t += self.dur[aid]
            leave_time = t
            total_cost += self.cost[aid]
            
            route_times.append((aid, start_time, leave_time))
            cur = coord
        
        travel_time = euclidean(cur, self.hotel) * 30
        t += travel_time
        total_dist += euclidean(cur, self.hotel)
        
        if total_cost > self.budget:
            feasible = False
            violations['budget'] = total_cost - self.budget
            
        fitness_score = total_dist + t/60.0
        if not feasible:
            fitness_score += 5000
            fitness_score += violations['time'] * 1000
            fitness_score += max(0, violations['budget']) * 0.01
            
        return {
            'fitness': fitness_score,
            'total_dist': total_dist,
            'total_cost': total_cost,
            'total_time': t,
            'route_times': route_times,
            'feasible': feasible,
            'violations': violations
        }

# Run comparative analysis
def run_comparative_analysis():
    """Compare GA with other algorithms"""
    print("\n" + "="*80)
    print("🔬 COMPARATIVE ANALYSIS: GA vs Greedy vs Random Search")
    print("="*80)
    
    datasets = {
        'Hanoi': (hanoi_df, 400000),        # Increased budgets for feasible solutions
        'Da Nang': (danang_df, 350000),
        'Ho Chi Minh City': (hcmc_df, 500000)
    }
    
    comparison_results = {}
    
    for city, (df, budget) in datasets.items():
        print(f"\n🏙️ Analyzing {city} (Budget: {budget:,} VND)")
        print("-" * 50)
        
        city_results = {}
        
        # 1. Genetic Algorithm
        print("🧬 Running Genetic Algorithm...")
        ga = EnhancedTRP_GA(df, city, budget, population_size=60, generations=100)
        ga_result = ga.run()
        city_results['GA'] = ga_result
        
        # 2. Greedy Algorithm
        print("🎯 Running Greedy Algorithm...")
        greedy = GreedyTRP(df, city, budget)
        greedy_result = greedy.run()
        city_results['Greedy'] = greedy_result
        
        # 3. Random Search
        print("🎲 Running Random Search...")
        random_search = RandomTRP(df, city, budget, iterations=2000)
        random_result = random_search.run()
        city_results['Random'] = random_result
        
        # Display comparison
        print("\n📊 Results Summary:")
        algorithms = ['GA', 'Greedy', 'Random']
        
        for alg in algorithms:
            result = city_results[alg]
            details = result['best_details']
            print(f"  {alg:8s}: Fitness={details['fitness']:8.1f} | "
                  f"Distance={details['total_dist']:6.2f} | "
                  f"Cost={details['total_cost']:7.0f} | "
                  f"Time={result['execution_time']:6.3f}s | "
                  f"Feasible={'✅' if details['feasible'] else '❌'}")
        
        comparison_results[city] = city_results
    
    return comparison_results

# Run comparative analysis
comparison_results = run_comparative_analysis()