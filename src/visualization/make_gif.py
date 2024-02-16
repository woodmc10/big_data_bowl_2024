import plotly.graph_objects as go
import pandas as pd
import numpy as np

from PIL import Image
from plotly_gif import GIF, capture

from visualize import animate_frame

gif = GIF()

def get_gif_frame(tracking_df, play_df, players, gameId, playId, frameId, defender, animation_image):
    """ Create a single frame for the explanation of ball carrier plane gif

    Args:
        tracking_df (pandas dataframe): dataframe containing augmented tracking data
        play_df (pandas dataframe): dataframe containing details about the play
        players (pandas dataframe): dataframe containing players details
        gameId (int): game ID from tracking data
        playId (int): play ID of the selected game
        frameId (int): frame ID for the selected play
        defender (int): defender's NFL ID
        animation_image (int): frame number for the animation GIF

    Returns:
        figure: A single frame of the explanation GIF
    """
    fig =  animate_frame(tracking_df, play_df, players, gameId, playId, frameId, defender, animation_image)
    gif.create_image(fig, scale=4)
    return fig


# Clean data
def clean_data(metrics_df):
    """ Reduce tackle types, adjust calculated fields to avoid unplottable infinite numbers, and
        remove examples where tackles would not be possible based on players' current state.

    Args:
        metrics_df (pandas dataframe): dataframe containing augmented tracking data

    Returns:
        pandas dataframe: updated dataframe
    """
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
    
    plays_df = pd.read_csv('../data/raw/plays.csv')
    players_df = pd.read_csv('../data/raw/players.csv')

    play_df_2 = pd.read_csv('gif_df.csv')

    playId_2 = 3806
    gameId_2 = 2022102700
    frameId_2 = 26
    ballCarrierId_2 = 47896.0
    defenderId_2 = 45063.0

    two_player_play_df_2 = play_df_2[play_df_2['nflId'].isin([ballCarrierId_2, defenderId_2])]

    # breakpoint()
    frames = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13]
    for i in frames:
        get_gif_frame(play_df_2, plays_df, players_df, gameId_2, playId_2, frameId_2, defenderId_2, i)

    gif.create_gif(30000) # generate gif (length in milliseconds)

