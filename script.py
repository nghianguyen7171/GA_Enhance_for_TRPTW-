# Extended Tourist Route Planning using Genetic Algorithm
# Based on user's requirements for enhanced experimentation

import math
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import time
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Utility functions
def euclidean(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def minutes_to_time_str(minutes):
    base_hour = 9
    h = base_hour + minutes // 60
    m = minutes % 60
    return f"{int(h):02d}:{int(m):02d}"

def time_str_to_minutes(time_str):
    """Convert time string to minutes from 9:00 AM base"""
    h, m = map(int, time_str.split(':'))
    return (h - 9) * 60 + m

# Enhanced dataset generator for larger scale testing
def generate_attractions_dataset(city_name, num_attractions, grid_size=3.0):
    """Generate a larger dataset of attractions for testing"""
    attractions = []
    
    # Predefined attraction types and their characteristics
    attraction_types = {
        'Museum': {'base_duration': 75, 'base_cost': 35000, 'open_early': True},
        'Temple': {'base_duration': 40, 'base_cost': 10000, 'open_early': True},
        'Park': {'base_duration': 60, 'base_cost': 0, 'open_early': False},
        'Market': {'base_duration': 45, 'base_cost': 5000, 'open_early': True},
        'Monument': {'base_duration': 30, 'base_cost': 15000, 'open_early': True},
        'Beach': {'base_duration': 90, 'base_cost': 0, 'open_early': False},
        'Shopping': {'base_duration': 80, 'base_cost': 20000, 'open_early': True},
        'Cultural Site': {'base_duration': 55, 'base_cost': 25000, 'open_early': True},
    }
    
    type_names = list(attraction_types.keys())
    
    for i in range(1, num_attractions + 1):
        # Random coordinates within grid
        x = random.uniform(-grid_size/2, grid_size/2)
        y = random.uniform(-grid_size/2, grid_size/2)
        
        # Select attraction type
        attr_type = random.choice(type_names)
        type_data = attraction_types[attr_type]
        
        # Generate opening/closing times based on type
        if type_data['open_early']:
            open_hour = random.choice([6, 7, 8])
            close_hour = random.choice([17, 18, 19])
        else:
            open_hour = random.choice([8, 9, 10])
            close_hour = random.choice([19, 20, 21, 22])
            
        # Some attractions are 24/7 (parks, beaches)
        if attr_type in ['Park', 'Beach'] and random.random() < 0.3:
            open_time = "00:00"
            close_time = "23:59"
        else:
            open_time = f"{open_hour:02d}:{random.choice([0, 30]):02d}"
            close_time = f"{close_hour:02d}:{random.choice([0, 30]):02d}"
        
        # Duration and cost with some variation
        duration = type_data['base_duration'] + random.randint(-15, 20)
        cost = type_data['base_cost'] + random.randint(-5000, 10000)
        cost = max(0, cost)  # Ensure non-negative cost
        
        attraction = {
            'id': i,
            'name': f"{city_name} {attr_type} {i}",
            'coord': (x, y),
            'open': open_time,
            'close': close_time,
            'duration': duration,
            'cost': cost
        }
        attractions.append(attraction)
    
    return attractions

# Create enhanced datasets
def create_enhanced_datasets():
    """Create larger datasets for comprehensive testing"""
    
    # Hanoi - 20 attractions
    hanoi_attractions = generate_attractions_dataset("Hanoi", 20, grid_size=4.0)
    
    # Da Nang - 15 attractions  
    danang_attractions = generate_attractions_dataset("Da Nang", 15, grid_size=3.5)
    
    # Ho Chi Minh City - 25 attractions (new dataset)
    hcmc_attractions = generate_attractions_dataset("HCMC", 25, grid_size=5.0)
    
    return hanoi_attractions, danang_attractions, hcmc_attractions

# Convert to DataFrame
def make_df(attractions):
    rows = []
    for a in attractions:
        oh, om = map(int, a['open'].split(':'))
        ch, cm = map(int, a['close'].split(':'))
        open_min = (oh - 9) * 60 + om
        close_min = (ch - 9) * 60 + cm
        
        rows.append({
            'id': a['id'], 
            'name': a['name'], 
            'x': a['coord'][0], 
            'y': a['coord'][1],
            'open_min': open_min, 
            'close_min': close_min, 
            'duration': a['duration'], 
            'cost': a['cost']
        })
    return pd.DataFrame(rows)

# Generate enhanced datasets
print("Generating enhanced datasets...")
hanoi_attractions, danang_attractions, hcmc_attractions = create_enhanced_datasets()

# Convert to DataFrames
hanoi_df = make_df(hanoi_attractions)
danang_df = make_df(danang_attractions)
hcmc_df = make_df(hcmc_attractions)

# Display dataset summaries
print("Dataset Summary:")
print(f"Hanoi: {len(hanoi_df)} attractions")
print(f"Da Nang: {len(danang_df)} attractions") 
print(f"Ho Chi Minh City: {len(hcmc_df)} attractions")

# Display first few rows of each dataset
print("\nHanoi Dataset (first 5 rows):")
print(hanoi_df.head())

print("\nDa Nang Dataset (first 5 rows):")
print(danang_df.head())

print("\nHo Chi Minh City Dataset (first 5 rows):")
print(hcmc_df.head())