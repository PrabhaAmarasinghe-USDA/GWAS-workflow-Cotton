import pandas as pd
import numpy as np
from scipy import stats

def calculate_stats():
    # Load the data
    try:
        df = pd.read_csv('All_Data.csv')
    except FileNotFoundError:
        print("Error: All_Data.csv not found in the current directory.")
        return
    
    # Check if required columns exist
    required_columns = ['Location']
    trait_columns = [col for col in df.columns if col not in required_columns]
    
    if not trait_columns:
        print("Error: No trait columns found in the dataset.")
        return
    
    # Group data by location
    grouped = df.groupby('Location')
    
    # Create a list to store results
    results = []
    
    # Calculate statistics for each location and trait
    for location, group in grouped:
        location_data = {'Location': location}
        
        for trait in trait_columns:
            # Skip non-numeric columns
            if not np.issubdtype(group[trait].dtype, np.number):
                continue
                
            # Calculate statistics
            stats_dict = {
                f'{trait}_mean': group[trait].mean(),
                f'{trait}_median': group[trait].median(),
                f'{trait}_range': group[trait].max() - group[trait].min(),
                f'{trait}_std': group[trait].std(),
                f'{trait}_cv': (group[trait].std() / group[trait].mean()) * 100,  # Coefficient of variation in %
                f'{trait}_skewness': group[trait].skew(),
                f'{trait}_kurtosis': group[trait].kurtosis(),
                f'{trait}_min': group[trait].min(),
                f'{trait}_max': group[trait].max()
            }
            
            location_data.update(stats_dict)
        
        results.append(location_data)
    
    # Create a DataFrame from results
    stats_df = pd.DataFrame(results)
    
    # Save results to Excel with multiple sheets for better readability
    with pd.ExcelWriter('descriptive_statistics.xlsx') as writer:
        # Save full results
        stats_df.to_excel(writer, sheet_name='All_Statistics', index=False)
        
        # Save a summary sheet with just the means and standard deviations
        mean_cols = [col for col in stats_df.columns if '_mean' in col]
        std_cols = [col for col in stats_df.columns if '_std' in col]
        summary_df = stats_df[['Location'] + mean_cols + std_cols]
        summary_df.to_excel(writer, sheet_name='Summary_Mean_Std', index=False)
    
    print("Analysis complete! Results have been saved to 'descriptive_statistics.xlsx'")
    print("\nSummary of locations analyzed:")
    print(stats_df[['Location'] + [col for col in stats_df.columns if 'mean' in col]])

if __name__ == "__main__":
    calculate_stats()
