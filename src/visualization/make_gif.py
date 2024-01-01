import plotly.graph_objects as go
import pandas as pd
import numpy as np

from PIL import Image
from plotly_gif import GIF, capture

from visualize import animate_frame

gif = GIF()

# @capture(gif)
def get_gif_frame(tracking_df, play_df, players, gameId, playId, frameId, defender, animation_image):
    fig =  animate_frame(tracking_df, play_df, players, gameId, playId, frameId, defender, animation_image)
    gif.create_image(fig, scale=4)
    return fig


# Clean data
def clean_data(metrics_df):
    metrics_df['event'].replace('assist', 'tackle', inplace=True)
    metrics_df.drop(metrics_df[metrics_df['event'] == 'forcedFumble'].index, inplace=True)
    
    metrics_df['tackler_time_to_contact'].replace([np.inf, -np.inf], 1000, inplace=True)
    metrics_df['ball_carrier_time_to_contact'].replace([np.inf, -np.inf], 1000, inplace=True)
    metrics_df['diff_time_to_contact'].replace([np.inf, -np.inf], 1000, inplace=True)
    
    # must be within field of play, and less than 5 seconds from contact point at current speed
    metrics_df['make_contact'] = ((metrics_df['x_contact'] < 110) & 
                                  (metrics_df['x_contact'] > 0) &
                                  (abs(metrics_df['diff_time_to_contact']) < 5)
                                 )
    
    metrics_df['in_field'] = ((metrics_df['x_contact'] < 110) & 
                          (metrics_df['x_contact'] > 0) &
                          (metrics_df['y_contact'] < 53.3) & 
                          (metrics_df['y_contact'] > 0)
                         )
    # reduce data to only contact in field of play
    metrics_df_in_field = metrics_df[metrics_df['in_field'] & (metrics_df['behind_player'] == False)]
    return metrics_df_in_field

# Clean data
def clean_data(metrics_df):
    metrics_df['event'].replace('assist', 'tackle', inplace=True)
    metrics_df.drop(metrics_df[metrics_df['event'] == 'forcedFumble'].index, inplace=True)
    
    metrics_df['tackler_time_to_contact'].replace([np.inf, -np.inf], 1000, inplace=True)
    metrics_df['ball_carrier_time_to_contact'].replace([np.inf, -np.inf], 1000, inplace=True)
    metrics_df['diff_time_to_contact'].replace([np.inf, -np.inf], 1000, inplace=True)
    
    # must be within field of play, and less than 5 seconds from contact point at current speed
    metrics_df['make_contact'] = ((metrics_df['x_contact'] < 110) & 
                                  (metrics_df['x_contact'] > 0) &
                                  (abs(metrics_df['diff_time_to_contact']) < 5)
                                 )
    
    metrics_df['in_field'] = ((metrics_df['x_contact'] < 110) & 
                          (metrics_df['x_contact'] > 0) &
                          (metrics_df['y_contact'] < 53.3) & 
                          (metrics_df['y_contact'] > 0)
                         )
    # reduce data to only contact in field of play
    metrics_df_in_field = metrics_df[metrics_df['in_field'] & (metrics_df['behind_player'] == False)]
    return metrics_df_in_field

if __name__ == "__main__":

    # # Replicate Notebook Setup
    # tracking_df = pd.read_csv('../data/interim/full_tracking_df.csv')
    plays_df = pd.read_csv('../data/raw/plays.csv')
    players_df = pd.read_csv('../data/raw/players.csv')
    # tackler_df = pd.read_csv('../data/raw/tackles.csv')

    # run_metrics_df = pd.read_csv('../data/processed/run_plays_12-22_about2yards.csv')
    # run_metrics_df = clean_data(run_metrics_df)
    # sampled_df_2 = run_metrics_df.groupby('event').apply(lambda x: x.sample(n=629, random_state=12))
    # sampled_df_2 = sampled_df_2[sampled_df_2['event'] != 'None']

    # # pick play
    # sampled_row_2 = sampled_df_2.sample(1, random_state=2)
    # playId_2 = sampled_row_2.playId[0] # 3806
    # gameId_2 = sampled_row_2.gameId[0] # 2022102700
    # frameId_2 = sampled_row_2.frameId[0] # 26
    # ballCarrierId_2 = sampled_row_2.nflId_ball_carrier[0] # 47896.0
    # defenderId_2 = sampled_row_2.nflId[0] # 45063.0

    # play_df_2 = tracking_df[(tracking_df['gameId'] == gameId_2) &
    #                         (tracking_df['playId'] == playId_2)]
    
    # play_df_2.to_csv('gif_df.csv')

    play_df_2 = pd.read_csv('gif_df.csv')

    playId_2 = 3806
    gameId_2 = 2022102700
    frameId_2 = 26
    ballCarrierId_2 = 47896.0
    defenderId_2 = 45063.0

    two_player_play_df_2 = play_df_2[play_df_2['nflId'].isin([ballCarrierId_2, defenderId_2])]

    # breakpoint()

    for i in range(14):
        get_gif_frame(play_df_2, plays_df, players_df, gameId_2, playId_2, frameId_2, defenderId_2, i)

    gif.create_gif(30000) # generate gif (length in milliseconds)

