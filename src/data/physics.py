import pandas as pd
import numpy as np

def calculate_angles(df):
    df['dir_cos'] = np.cos(np.radians(df['dir']))
    df['dir_sin'] = np.sin(np.radians(df['dir']))
    df['dir_tan'] = np.tan(np.radians(df['dir']))
    df['slope'] = np.tan(np.radians(90 - df['dir']))
    df['o_sin'] = np.sin(np.radians(df['o']))
    return df

def physics_calculations(df, metric_type):
    assert metric_type in ['force', 'momentum']

    if metric_type == 'force':
        move_type = 'a'
    else:
        move_type = 's'
    
    df[f'{metric_type}'] = df[move_type] * df['weight']
    df[f'{metric_type}_y'] = df[f'{metric_type}'] * df['dir_cos']
    df[f'{metric_type}_x'] = df[f'{metric_type}'] * df['dir_sin']
    return df

def find_contact_point(df):
    df['x_contact'] = ((df['y'] - (df['slope'] * df['x']) -
                        (df['y_ball_carrier'] - (df['slope_ball_carrier'] *
                                              df['x_ball_carrier']))
                        ) / (df['slope_ball_carrier'] - df['slope'])
                      )
    df['x_contact'] = np.where(np.isnan(df['x_contact']), df['x'], df['x_contact'])
    df['x_contact'] = np.where(np.isinf(df['x_contact']), df['x'], df['x_contact'])
    df['y_contact'] = (df['slope_ball_carrier'] * df['x_contact'] +
                       (df['y_ball_carrier'] -
                            (df['slope_ball_carrier'] * df['x_ball_carrier'])
                       )
                      )
    df['y_contact'] = np.where(np.isnan(df['y_contact']), df['y'], df['y_contact'])
    df['y_contact'] = np.where(np.isinf(df['y_contact']), df['y'], df['y_contact'])
    df['contact_y_check'] = (df['slope'] * df['x_contact'] +
                             (df['y'] - (df['slope'] * df['x'])
                             )
                            )
    df['contact_y_check'] = np.where(np.isnan(df['contact_y_check']), df['y'], df['contact_y_check'])
    df['contact_y_check'] = np.where(np.isinf(df['contact_y_check']), df['y'], df['contact_y_check'])
    # pd.testing.assert_series_equal(df['y_contact'], df['contact_y_check'])

    return df

def metric_diffs(df, metric_type):
    # metric diff 
        # will not have any directonal sign
        # moving in same direction or opposite direction will not be captured
        # negative means tackler is moving with more momentum/force than ball carrier
    df[f'{metric_type}_diff'] = df[f'{metric_type}_ball_carrier'] - df[f'{metric_type}']
    # x diff and y diff
        # force will be larger than ball carrier force if tackler is moving in opposite direction
    df[f'{metric_type}_x_diff'] = df[f'{metric_type}_x_ball_carrier'] - df[f'{metric_type}_x']
    df[f'{metric_type}_y_diff'] = df[f'{metric_type}_y_ball_carrier'] - df[f'{metric_type}_y']
    return df

def time_to_contact(df):
    df['tackler_time_to_contact'] = df['tackler_to_contact_dist'] / df['s']
    df['ball_carrier_time_to_contact'] = df['ball_carrier_to_contact_dist'] / df['s_ball_carrier']
    df['diff_time_to_contact'] = df['tackler_time_to_contact'] - df['ball_carrier_time_to_contact']
    return df

def out_of_phase(df):
    df['in_phase'] = abs(df['dir_sin'] - df['o_sin'])
    return df