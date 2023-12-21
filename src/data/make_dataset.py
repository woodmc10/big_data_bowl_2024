# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
# from dotenv import find_dotenv, load_dotenv

import pandas as pd
from pathlib import Path
import random
import math
from src.data.tackler_info import (
    simplify_tackles_df, join_ball_carrier_tracking,
    dist_calc, tackler_distance_frame, contact_behind
)
from src.data.physics import (
    calculate_angles, physics_calculations, find_contact_point,
    metric_diffs, time_to_contact, out_of_phase, ball_carrier_plane_of_contact
)


@click.command()
@click.argument('input_directory', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
@click.argument('play_type', type=str)
def main(input_directory, output_filepath, play_type):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    games_df, plays_df, players_df, tackles_df = import_support_files(input_directory)

    tracking_df = import_tracking_files(input_directory)
    print('tracking data file created')

    # reduce tracking data to run plays with frames before the tackle
    reduced_tracking_df = reduce_tracking_data(tracking_df, plays_df, play_type)
    print('tracking data reduced')

    # normalize left/right field direction
    standard_tracking_df = standardize_field(reduced_tracking_df)
    print('tracking data standardized')

    # merge weight into tracking dataframe
    weight_df = standard_tracking_df.merge(players_df[['nflId', 'weight', 'position']], on='nflId')
    print('player data merged')

    # add force, momentum, and angles
    physics_tracking_df = calculate_angles(weight_df)
    physics_calculations(physics_tracking_df, "force")
    physics_calculations(physics_tracking_df, "momentum")
    out_of_phase(physics_tracking_df)
    print('physics columns added')

    # add ball carrier details to every row
    ball_carrier_join_df = join_ball_carrier_tracking(plays_df, physics_tracking_df)
    print('ball carrier joined')

    # reduce data to only defensive players
    defenders_tracking_df = defenders_only(ball_carrier_join_df)
    print('reduced to defenders only')

    # calculate distances and select single frame
    ball_carrier_dist_df = dist_calc(defenders_tracking_df, name='tackler_to_ball_carrier_dist')
    tackle_simple_df = simplify_tackles_df(tackles_df)
    tackler_dist_df = tackler_distance_frame(tackle_simple_df, ball_carrier_dist_df, dist=1)
        # TODO: distance argument should be a command line argument
    print('distance calculations completed')

    # calculate metrics differences
    metrics_df = metric_diffs(tackler_dist_df, 'force')
    metric_diffs(metrics_df, 'momentum')
    print('metrics differences calculated')

    # calculate contact point and player distance/time
    find_contact_point(metrics_df)
    dist_calc(metrics_df, first='', second='_contact', name='tackler_to_contact_dist')
    dist_calc(metrics_df, first='_ball_carrier', second='_contact',
              name='ball_carrier_to_contact_dist')
    contact_behind(metrics_df)
    time_to_contact(metrics_df)
    ball_carrier_plane_of_contact(metrics_df)
    print('contact point metrics calculated')

    metrics_df.to_csv(output_filepath, index=False)

def import_support_files(input_directory):
    games_df = pd.read_csv(f'{input_directory}/games.csv')
    plays_df = pd.read_csv(f'{input_directory}/plays.csv')
    players_df = pd.read_csv(f'{input_directory}/players.csv')
    tackles_df = pd.read_csv(f'{input_directory}/tackles.csv')
    return(games_df, plays_df, players_df, tackles_df)

def import_tracking_files(input_directory):
    path = Path(input_directory)
    parent_path = path.parent
    full_tracking_file = parent_path / 'interim/full_tracking_df.csv'
    if full_tracking_file.exists():
        tracking_df = pd.read_csv(full_tracking_file)
    else:
        pass
        tracking_df = pd.concat(
            [pd.read_csv(p) for p in path.rglob('*') if p.match('tracking_week_*.csv')]
            )
        tracking_df.to_csv(full_tracking_file)
    
    return tracking_df

def standardize_field(df):
    """
    Convert coordinates and orientation such that the offensive team is
    always going to the right.
    
    Direction is not used and, therefore, not updated.
    """
    FIELD_LENGTH = 120
    FIELD_WIDTH = 160 / 3
    HALF_ROTATION = 180

    flipped = df.assign(
        x=FIELD_LENGTH - df.x,
        y=FIELD_WIDTH - df.y,
        
        o=(df.o + HALF_ROTATION),
        dir=(df.dir + HALF_ROTATION)
    )

    flipped['o'] = flipped['o'].apply(lambda x: x if x < 360 else x - 360)
    flipped['dir'] = flipped['dir'].apply(lambda x: x if x < 360 else x - 360)

    # Reminder: the where method in pandas goes against intuition and
    # replaces columns for which the condition is False.
    return df.where(df.playDirection == "right", flipped)

def half_rotation(angle):
    new_angle = angle + 180
    if new_angle > 360:
        return new_angle - 360
    return new_angle


def reduce_tracking_data(df, plays_df, play_type='run'):
    # exclude frames after the tackle
    tackle_frame_df = df[df['event'] == 'tackle'][['gameId', 'playId', 'frameId']].drop_duplicates(keep='first')
    tackle_frame_df.rename(columns={'frameId': 'tackle_frame'}, inplace=True)
    temp_tracking_df = df.merge(tackle_frame_df, on=['gameId', 'playId'])
    tracking_to_tackle_df = temp_tracking_df[temp_tracking_df['tackle_frame'] > temp_tracking_df['frameId']]

    # reduce dataframe to selected play type
    if play_type == 'run':
        run_plays_df = plays_df[plays_df['passResult'].isnull()]
        reduced_tracking_df = run_plays_df[['gameId', 'playId']].merge(tracking_to_tackle_df, on=['gameId', 'playId'])
    elif play_type == 'pass':
        # before evaluating pass plays, reduce the tracking data to only frames after the catch
        pass_caught_df = tracking_to_tackle_df[tracking_to_tackle_df.event == 'pass_outcome_caught'][['gameId', 'playId', 'frameId']].drop_duplicates(keep='first')
        pass_caught_df.rename(columns={'frameId': 'catch_frame'}, inplace=True)
        temp_tracking_df_pass = tracking_to_tackle_df.merge(pass_caught_df, on=['gameId', 'playId'])
        pass_caught_to_tackle_df = temp_tracking_df_pass[temp_tracking_df_pass['catch_frame'] < temp_tracking_df_pass['frameId']]

        pass_plays_df = plays_df[plays_df['passResult'] == "C"]
        reduced_tracking_df = pass_plays_df[['gameId', 'playId']].merge(pass_caught_to_tackle_df, on=['gameId', 'playId'])
    else:
        raise ValueError("Only run plays supported")

    return reduced_tracking_df

def defenders_only(tracking_df):
    df = tracking_df.copy()
    defenders_df = df[df['club'] != df['club_ball_carrier']]
    return defenders_df

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    # load_dotenv(find_dotenv())

    main()
