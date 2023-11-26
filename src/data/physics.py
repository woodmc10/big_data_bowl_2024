import pandas as pd
import numpy as np

def calculate_angles(df):
    df['dir_cos'] = np.cos(np.radians(df['dir']))
    df['dir_sin'] = np.sin(np.radians(df['dir']))
    df['dir_tan'] = np.tan(np.radians(df['dir']))
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
    df['contact_x'] = ((df['y']/(df['dir_tan'] * df['x']) - 
                        df['y_ball_carrier']/(df['dir_tan_ball_carrier'] * 
                                              df['x_ball_carrier'])
                        ) / (df['dir_tan_ball_carrier'] - df['dir_tan'])
                      )
    df['contact_y'] = (df['dir_tan_ball_carrier'] * df['contact_x'] +
                       (df['y_ball_carrier'] / 
                            (df['dir_tan_ball_carrier'] * df['x_ball_carrier'])
                       )
                      )

    df['contact_y_check'] = (df['dir_tan'] * df['contact_x'] +
                                df['y'] / (df['dir_tan'] * df['x'])
                            )
    # pd.testing.assert_series_equal(df['contact_y'], 
    #                                (df['dir_tan'] * df['contact_x'] +
    #                                     df['y'] / (df['dir_tan'] * df['x'])
    #                                 ),
    #                                check_names=False
    #                               )
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