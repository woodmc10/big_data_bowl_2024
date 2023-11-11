# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

import pandas as pd
from pathlib import Path
from src.data.tackler_info import (
    simplify_tackles_df, player_dist_to_ball_carrier, tackler_distance
)


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

    # tackler distance conversion
    tackle_simple_df = simplify_tackles_df(tackles_df)
    ball_carrier_dist_df = player_dist_to_ball_carrier(plays_df, tracking_df)
    tackler_dist_df = tackler_distance(tackle_simple_df, ball_carrier_dist_df)

    tackler_dist_df.to_csv(output_filepath)

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

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
