# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
# from dotenv import find_dotenv, load_dotenv

import pandas as pd
from pathlib import Path
from src.data.tackler_info import (
    simplify_tackles_df, player_dist_to_ball_carrier, tackler_distance
)
from src.data.physics import calculate_angles, physics_calculations


@click.command()
@click.argument('input_directory', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_directory, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    games_df, plays_df, players_df, tackles_df = import_support_files(input_directory)
    tracking_df = import_tracking_files(input_directory)

    # normalize left/right field direction
    standard_tracking_df = standardize_field(tracking_df)

    # merge weight into tracking dataframe
    weight_df = standard_tracking_df.merge(players_df[['nflId', 'weight']], on='nflId')

    # add force, momentum, and angles
    angle_tracking_df = calculate_angles(weight_df)
    force_tracking_df = physics_calculations(angle_tracking_df, "force")
    physics_tracking_df = physics_calculations(force_tracking_df, "momentum")

    physics_tracking_df.to_csv(output_filepath, index=False)

    # # tackler distance conversion
    # tackle_simple_df = simplify_tackles_df(tackles_df)
    # ball_carrier_dist_df = player_dist_to_ball_carrier(plays_df, physics_tracking_df)
    # tackler_dist_df = tackler_distance(tackle_simple_df, ball_carrier_dist_df)

    # tackler_dist_df.to_csv(output_filepath, index=False)

def import_support_files(input_directory):
    games_df = pd.read_csv(f'{input_directory}/games.csv')
    plays_df = pd.read_csv(f'{input_directory}/plays.csv')
    players_df = pd.read_csv(f'{input_directory}/players.csv')
    tackles_df = pd.read_csv(f'{input_directory}/tackles.csv')
    return(games_df, plays_df, players_df, tackles_df)

def import_tracking_files(input_directory):
    path = Path(input_directory)
    tracking_df = pd.concat(
        [pd.read_csv(p) for p in path.rglob('*') if p.match('tracking_week_*.csv')]
        )
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
        
        # Can ignore that values will exceed 360 because they will
        # be converted to sine and cosine values.
        o=(df.o + HALF_ROTATION),
        dir = (df.dir + HALF_ROTATION)
    )

    # Reminder: the where method in pandas goes against intuition and
    # replaces columns for which the condition is False.
    return df.where(df.playDirection == "right", flipped)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    # load_dotenv(find_dotenv())

    main()
