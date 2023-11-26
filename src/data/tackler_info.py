from scipy.spatial.distance import euclidean
import pandas as pd

matching_frame_columns = ['gameId', 'playId', 'frameId']
player_details_columns = ['nflId', 'displayName', 'club']
play_info_columns = ['time', 'event']
tracking_info_columns = ['x', 'y', 's', 'a', 'dis', 'o', 'dir']
drop_columns = ['jerseyNumber', 'playDirection']
angle_columns = ['dir_cos', 'dir_sin', 'dir_tan']
physics_columns = ['force', 'force_x', 'force_y', 'momentum', 'momentum_x',
                   'momentum_y']
ball_carrier_columns = ['nflId_ball_carrier',
                        'displayName_ball_carrier', 'club_ball_carrier', 
                        'x_ball_carrier', 'y_ball_carrier', 's_ball_carrier',
                        'a_ball_carrier', 'dis_ball_carrier', 'o_ball_carrier',
                        'dir_ball_carrier', 'dir_cos_ball_carrier',
                        'dir_sin_ball_carrier', 'dir_tan_ball_carrier',
                        'force_ball_carrier', 'force_x_ball_carrier',
                        'force_y_ball_carrier', 'momentum_ball_carrier',
                        'momentum_x_ball_carrier', 'momentum_y_ball_carrier']

def simplify_tackles_df(tackles_df):
    # assign the tackle Id for each boolean column
    tackle_ids = tackles_df.copy()
    tackle_ids[
        ["tackle", "assist", "forcedFumble", "pff_missedTackle"]
    ] = tackles_df[["tackle", "assist", "forcedFumble", "pff_missedTackle"]].multiply(
        tackles_df["nflId"],
        axis="index"
    )

    # melt (unpivot) to make computing distance to ball carrier easier
    tackle_melt = pd.melt(tackle_ids, id_vars=['gameId', 'playId'],
                         value_vars=["tackle", "assist", "forcedFumble", "pff_missedTackle"])
    tackle_melt.rename(columns={'variable': 'event', 'value': 'nflId'}, inplace=True)

    # remove all extra rows
    tackle_simple = tackle_melt.query('nflId != 0')
    return tackle_simple

def join_ball_carrier_tracking(plays_df, tracking_df):
    # get ball carrier tracking details for each frame
    ball_carrier_tracking_df = plays_df[['gameId', 'playId', 'ballCarrierId']].merge(
                                    tracking_df[matching_frame_columns +
                                                player_details_columns +
                                                tracking_info_columns +
                                                angle_columns +
                                                physics_columns
                                                ],
                                    left_on=['gameId', 'playId', 'ballCarrierId'],
                                    right_on=['gameId', 'playId', 'nflId']
                        )
    # add ball carrier position to every row of tracking data
    ball_carrier_join = ball_carrier_tracking_df.merge(
                                tracking_df[matching_frame_columns +
                                            player_details_columns +
                                            tracking_info_columns +
                                            play_info_columns +
                                            angle_columns +
                                            physics_columns
                                            ],
                                on=['gameId', 'playId', 'frameId'],
                                suffixes=['_ball_carrier', None]
                        )
    return ball_carrier_join

def player_dist_to_ball_carrier(ball_carrier_dist):
    # calculate distance from each player to ball carrier
    ball_carrier_dist['distance'] = ball_carrier_dist.apply(
                    lambda row: euclidean((row['x'], row['y']), 
                                          (row['x_ball_carrier'], row['y_ball_carrier']))
                    , axis=1)
    return ball_carrier_dist

def tackler_distance_frame(tackle_simple_df, ball_carrier_dist_df, dist='min'):
    if dist == 'min':
        ball_carrier_min_dist = ball_carrier_dist_df.loc[
            ball_carrier_dist_df.groupby(["gameId", "playId", "nflId"])["distance"].idxmin()
        ][matching_frame_columns + player_details_columns + tracking_info_columns +
          angle_columns + physics_columns + ball_carrier_columns +['distance']]
    else:
        #TODO: add code for finding the first frame where a defender gets within a 
        # certain distance from the ball carrier
        ball_carrier_dist_limit_df = ball_carrier_min_dist[ball_carrier_dist_df['distance'] < dist]
        ball_carrier_min_dist = ball_carrier_dist_limit_df.loc[
            ball_carrier_dist_limit_df.groupby(["gameId", "playId", "nflId"])["frameId"].idxmin()
        ][matching_frame_columns + player_details_columns + tracking_info_columns +
          angle_columns + physics_columns + ball_carrier_columns +['distance']]
    tackles_dist = tackle_simple_df.merge(
                        ball_carrier_min_dist,
                        on=['gameId', 'playId', 'nflId'],
                        how='right')
    tackles_dist.rename(columns={'distance': 'min_dist'}, inplace=True)
    tackles_dist['event'].fillna('None', inplace=True)
    return tackles_dist

def dist_group(row):
    dist_range = 'unknown'
    if row.min_dist < 0.5:
        dist_range = '0 - 0.5'
    elif row.min_dist < 1:
        dist_range = '0.5 - 1'
    elif row.min_dist < 2:
        dist_range = '1 - 2'
    else:
        dist_range = '>2'
    return dist_range