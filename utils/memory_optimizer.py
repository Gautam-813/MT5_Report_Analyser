"""
Memory optimization utilities for large MT5 reports
Handles memory-efficient processing of large datasets
"""

import pandas as pd
import numpy as np
import gc

def optimize_dataframe_memory(df):
    """
    Optimize DataFrame memory usage by downcasting numeric types
    """
    if df.empty:
        return df
    
    # Create a copy to avoid modifying original
    df_optimized = df.copy()
    
    # Optimize numeric columns
    for col in df_optimized.select_dtypes(include=[np.number]).columns:
        col_type = df_optimized[col].dtype
        
        if col_type != object:
            c_min = df_optimized[col].min()
            c_max = df_optimized[col].max()
            
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df_optimized[col] = df_optimized[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df_optimized[col] = df_optimized[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df_optimized[col] = df_optimized[col].astype(np.int32)
            else:
                if c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df_optimized[col] = df_optimized[col].astype(np.float32)
    
    return df_optimized

def sample_large_dataset(df, max_size=5000, method='systematic'):
    """
    Sample large datasets while preserving temporal patterns
    """
    if len(df) <= max_size:
        return df
    
    if method == 'systematic':
        # Systematic sampling - take every nth row
        step = len(df) // max_size
        return df.iloc[::step].copy()
    
    elif method == 'stratified':
        # Stratified sampling by time periods
        if 'time' in df.columns:
            df['time_group'] = pd.cut(df.index, bins=20, labels=False)
            sampled = df.groupby('time_group').apply(
                lambda x: x.sample(min(len(x), max_size // 20))
            ).reset_index(drop=True)
            return sampled.drop('time_group', axis=1)
    
    # Fallback to random sampling
    return df.sample(n=max_size).sort_index()

def chunk_process_dataframe(df, chunk_size=1000, process_func=None):
    """
    Process large DataFrames in chunks to avoid memory issues
    """
    results = []
    
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        
        if process_func:
            result = process_func(chunk)
            results.append(result)
        else:
            results.append(chunk)
        
        # Force garbage collection after each chunk
        gc.collect()
    
    return results

def memory_efficient_groupby(df, group_cols, agg_dict, chunk_size=2000):
    """
    Memory-efficient groupby operations for large datasets
    """
    if len(df) <= chunk_size:
        return df.groupby(group_cols).agg(agg_dict)
    
    # Process in chunks and combine results
    chunks = []
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        chunk_result = chunk.groupby(group_cols).agg(agg_dict)
        chunks.append(chunk_result)
    
    # Combine chunk results
    combined = pd.concat(chunks)
    
    # Re-aggregate the combined results
    final_result = combined.groupby(level=0).agg({
        col: 'sum' if agg_dict[col.split('_')[0]] in ['sum', 'count'] else 'mean'
        for col in combined.columns
    })
    
    return final_result

def clear_memory():
    """
    Force garbage collection to free memory
    """
    gc.collect()

def get_memory_usage(df):
    """
    Get memory usage information for a DataFrame
    """
    memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
    return {
        'rows': len(df),
        'columns': len(df.columns),
        'memory_mb': round(memory_mb, 2)
    }