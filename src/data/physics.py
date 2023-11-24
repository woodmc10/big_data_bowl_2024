import pandas as pd
import numpy as np

def calculate_angles(df):
    df['dir_cos'] = np.cos(np.radians(df['dir']))
    df['dir_sin'] = np.sin(np.radians(df['dir']))
    return df

def physics_calculations(df, type):
    assert type in ['force', 'momentum']

    if type == 'force':
        move_type = 'a'
    else:
        move_type = 's'
    
    df[f'{type}'] = df[move_type] * df['weight']
    df[f'{type}_y'] = df[f'{type}'] * df['dir_cos']
    df[f'{type}_x'] = df[f'{type}'] * df['dir_sin']
    return df