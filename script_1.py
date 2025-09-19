# Enhanced Genetic Algorithm with multiple comparison methods
class EnhancedTRP_GA:
    def __init__(self, df, city_name, budget, hotel=(0,0), 
                 population_size=100, generations=150, 
                 crossover_p=0.85, mutation_p=0.15, seed=42):
        self.df = df
        self.city_name = city_name
        self.hotel = hotel
        self.budget = budget
        self.pop_size = population_size
        self.generations = generations
        self.cx_p = crossover_p
        self.mut_p = mutation_p
        self.rng = random.Random(seed)
        
        # Attraction data structures
        self.attraction_ids = list(df['id'])
        self.coord = {row.id: (row.x, row.y) for row in df.itertuples()}
        self.open_min = {row.id: row.open_min for row in df.itertuples()}
        self.close_min = {row.id: row.close_min for row in df.itertuples()}
        self.dur = {row.id: row.duration for row in df.itertuples()}
        self.cost = {row.id: row.cost for row in df.itertuples()}
        
        # Performance tracking
        self.fitness_history = []
        self.convergence_gen = 0
        self.execution_time = 0
        
    def eval_route(self, perm):
        """Enhanced route evaluation with detailed metrics"""
        t = 0  # Current time in minutes from 9:00 AM
        total_dist = 0.0
        total_cost = 0
        feasible = True
        route_times = []
        violations = {'time': 0, 'budget': 0}
        
        cur = self.hotel
        
        for aid in perm:
            coord = self.coord[aid]
            travel_time = euclidean(cur, coord) * 30  # minutes per unit distance
            total_dist += euclidean(cur, coord)
            t += travel_time
            
            # Time window constraints
            open_time = self.open_min[aid]
            close_time = self.close_min[aid]
            
            # Wait if arrive before opening
            if t < open_time:
                t = open_time
                
            # Check if arrive after closing
            if t > close_time:
                feasible = False
                violations['time'] += 1
                t += 300  # 5-hour penalty
                
            start_time = t
            t += self.dur[aid]
            leave_time = t
            total_cost += self.cost[aid]
            
            route_times.append((aid, start_time, leave_time))
            cur = coord
        
        # Return to hotel
        travel_time = euclidean(cur, self.hotel) * 30
        t += travel_time
        total_dist += euclidean(cur, self.hotel)
        
        # Budget constraint
        if total_cost > self.budget:
            feasible = False
            violations['budget'] = total_cost - self.budget
            
        # Multi-objective fitness calculation
        fitness_score = total_dist + t/60.0  # Base score: distance + time
        
        # Heavy penalties for constraint violations
        if not feasible:
            fitness_score += 5000  # Base penalty
            fitness_score += violations['time'] * 1000  # Time violation penalty
            fitness_score += max(0, violations['budget']) * 0.01  # Budget violation penalty
            
        return {
            'fitness': fitness_score,
            'total_dist': total_dist,
            'total_cost': total_cost,
            'total_time': t,
            'route_times': route_times,
            'feasible': feasible,
            'violations': violations
        }
    
    def initial_pop(self):
        """Generate initial population with diversity"""
        pop = []
        
        # 50% random permutations
        for _ in range(self.pop_size // 2):
            perm = self.attraction_ids.copy()
            self.rng.shuffle(perm)
            pop.append(perm)
            
        # 25% nearest neighbor heuristic variations
        for _ in range(self.pop_size // 4):
            perm = self.nearest_neighbor_heuristic()
            pop.append(perm)
            
        # 25% cost-based heuristic
        for _ in range(self.pop_size // 4):
            perm = self.cost_based_heuristic()
            pop.append(perm)
            
        return pop
    
    def nearest_neighbor_heuristic(self):
        """Generate route using nearest neighbor with random start"""
        unvisited = self.attraction_ids.copy()
        route = []
        
        # Random starting point
        current = self.rng.choice(unvisited)
        route.append(current)
        unvisited.remove(current)
        current_coord = self.coord[current]
        
        while unvisited:
            # Find nearest unvisited attraction
            distances = [(aid, euclidean(current_coord, self.coord[aid])) for aid in unvisited]
            distances.sort(key=lambda x: x[1])
            
            # Select from top 3 nearest with randomness
            top_candidates = min(3, len(distances))
            next_id = distances[self.rng.randint(0, top_candidates-1)][0]
            
            route.append(next_id)
            unvisited.remove(next_id)
            current_coord = self.coord[next_id]
            
        return route
    
    def cost_based_heuristic(self):
        """Generate route prioritizing low-cost attractions first"""
        attractions_by_cost = sorted(self.attraction_ids, key=lambda x: self.cost[x])
        
        # Add some randomness
        route = []
        remaining = attractions_by_cost.copy()
        
        while remaining:
            # Select from cheapest 30% with randomness
            candidates = remaining[:max(1, len(remaining)//3)]
            selected = self.rng.choice(candidates)
            route.append(selected)
            remaining.remove(selected)
            
        return route
    
    def pmx_crossover(self, p1, p2):
        """Partially Mapped Crossover for permutation encoding"""
        size = len(p1)
        cx1 = self.rng.randint(0, size - 2)
        cx2 = self.rng.randint(cx1 + 1, size - 1)
        
        child = [None] * size
        child[cx1:cx2+1] = p1[cx1:cx2+1]
        
        for i in range(size):
            if not (cx1 <= i <= cx2):
                v = p2[i]
                while v in child:
                    idx = p2.index(v)
                    v = p1[idx]
                child[i] = v
        
        return child
    
    def swap_mutation(self, individual):
        """Swap mutation operator"""
        if len(individual) > 1:
            a, b = self.rng.sample(range(len(individual)), 2)
            individual[a], individual[b] = individual[b], individual[a]
    
    def tournament_selection(self, pop, scores, k=3):
        """Tournament selection"""
        chosen = self.rng.sample(range(len(pop)), k)
        best = min(chosen, key=lambda i: scores[i])
        return pop[best]
    
    def run(self):
        """Enhanced GA execution with performance tracking"""
        start_time = time.time()
        
        pop = self.initial_pop()
        best = None
        best_score = float('inf')
        best_details = None
        generations_without_improvement = 0
        
        for g in range(self.generations):
            # Evaluate population
            eval_results = [self.eval_route(indiv) for indiv in pop]
            scores = [result['fitness'] for result in eval_results]
            
            # Track best solution
            min_idx = np.argmin(scores)
            if scores[min_idx] < best_score:
                best_score = scores[min_idx]
                best = pop[min_idx].copy()
                best_details = eval_results[min_idx]
                self.convergence_gen = g
                generations_without_improvement = 0
            else:
                generations_without_improvement += 1
            
            # Track fitness progress
            self.fitness_history.append({
                'generation': g,
                'best_fitness': best_score,
                'avg_fitness': np.mean(scores),
                'worst_fitness': np.max(scores)
            })
            
            # Early stopping if no improvement for too long
            if generations_without_improvement > 30:
                break
                
            # Create new population
            new_pop = []
            
            # Elitism - keep best 2
            sorted_indices = np.argsort(scores)
            new_pop.append(pop[sorted_indices[0]].copy())
            new_pop.append(pop[sorted_indices[1]].copy())
            
            # Generate offspring
            while len(new_pop) < self.pop_size:
                p1 = self.tournament_selection(pop, scores)
                p2 = self.tournament_selection(pop, scores)
                
                # Crossover
                if self.rng.random() < self.cx_p:
                    c1 = self.pmx_crossover(p1, p2)
                    c2 = self.pmx_crossover(p2, p1)
                else:
                    c1 = p1.copy()
                    c2 = p2.copy()
                
                # Mutation
                if self.rng.random() < self.mut_p:
                    self.swap_mutation(c1)
                if self.rng.random() < self.mut_p:
                    self.swap_mutation(c2)
                    
                new_pop.append(c1)
                if len(new_pop) < self.pop_size:
                    new_pop.append(c2)
            
            pop = new_pop
        
        self.execution_time = time.time() - start_time
        
        return {
            'best_route': best,
            'best_details': best_details,
            'fitness_history': self.fitness_history,
            'convergence_generation': self.convergence_gen,
            'execution_time': self.execution_time
        }

# Test the enhanced GA on all datasets
def run_comprehensive_experiment():
    """Run comprehensive experiments on all datasets"""
    datasets = {
        'Hanoi': (hanoi_df, 120000),      # Budget in VND
        'Da Nang': (danang_df, 180000),   # Increased budgets
        'Ho Chi Minh City': (hcmc_df, 250000)
    }
    
    results = {}
    
    print("Running comprehensive experiments...")
    print("="*60)
    
    for city, (df, budget) in datasets.items():
        print(f"\n🏙️ Running experiment for {city}...")
        print(f"   Attractions: {len(df)}")
        print(f"   Budget: {budget:,} VND")
        
        # Run GA
        ga = EnhancedTRP_GA(
            df=df, 
            city_name=city, 
            budget=budget,
            population_size=80,  # Increased population
            generations=120,     # Increased generations
            seed=42
        )
        
        result = ga.run()
        results[city] = {
            'ga_instance': ga,
            'result': result,
            'dataset_size': len(df),
            'budget': budget
        }
        
        # Print results
        details = result['best_details']
        print(f"   ✅ Best fitness: {details['fitness']:.2f}")
        print(f"   📏 Total distance: {details['total_dist']:.2f} units")
        print(f"   💰 Total cost: {details['total_cost']:,} VND") 
        print(f"   ⏱️  Total time: {details['total_time']:.0f} minutes")
        print(f"   🎯 Feasible: {'Yes' if details['feasible'] else 'No'}")
        print(f"   🔄 Converged at generation: {result['convergence_generation']}")
        print(f"   ⚡ Execution time: {result['execution_time']:.2f} seconds")
    
    return results

# Run the comprehensive experiment
experiment_results = run_comprehensive_experiment()