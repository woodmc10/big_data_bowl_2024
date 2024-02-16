import pandas as pd
import numpy as np


def calculate_angles(df):
    """Add trigonometry calculations for angles in tracking data

    Args:
        df (pandas dataframe): player tracking dataframe

    Returns:
        pandas dataframe: same datafame with new columns
            ('dir_cos', 'dir_sin', 'dir_tan', 'slope', 'o_sin')
    """
    df["dir_cos"] = np.cos(np.radians(df["dir"]))
    df["dir_sin"] = np.sin(np.radians(df["dir"]))
    df["dir_tan"] = np.tan(np.radians(df["dir"]))
    df["slope"] = np.tan(np.radians(90 - df["dir"]))
    df["o_sin"] = np.sin(np.radians(df["o"]))
    return df


def physics_calculations(df, metric_type):
    """Calculate force or momentum and decompose into x and y directional components

    Args:
        df (pandas dataframe): player tracking dataframe
        metric_type (str): type of metric for calculations, either 'force' or 'momentum'

    Returns:
        pandas dataframe: same dataframe with new columns
            ('{metric}', '{metric}_y', '{metric}_y_abs', '{metric}_x')
    """
    assert metric_type in ["force", "momentum"]

    if metric_type == "force":
        move_type = "a"
    else:
        move_type = "s"

    df[f"{metric_type}"] = df[move_type] * df["weight"]
    df[f"{metric_type}_y"] = df[f"{metric_type}"] * df["dir_cos"]
    df[f"{metric_type}_y_abs"] = abs(df[f"{metric_type}_y"])
    df[f"{metric_type}_x"] = df[f"{metric_type}"] * df["dir_sin"]
    return df


def find_contact_point(df):
    """ Calculate the projected point of contact for the ball carrier and defender and add
        point information to the dataframe

    Args:
        df (pandas dataframe): player tracking dataframe with ball carrier details merged
            for each frame

    Returns:
        pandas dataframe: same dataframe with new columns
            ('x_contact', 'y_contact', 'contact_y_check')
    """
    df["x_contact"] = (
        df["y"]
        - (df["slope"] * df["x"])
        - (df["y_ball_carrier"] - (df["slope_ball_carrier"] * df["x_ball_carrier"]))
    ) / (df["slope_ball_carrier"] - df["slope"])
    df["x_contact"] = np.where(np.isnan(df["x_contact"]), df["x"], df["x_contact"])
    df["x_contact"] = np.where(np.isinf(df["x_contact"]), df["x"], df["x_contact"])
    df["y_contact"] = df["slope_ball_carrier"] * df["x_contact"] + (
        df["y_ball_carrier"] - (df["slope_ball_carrier"] * df["x_ball_carrier"])
    )
    df["y_contact"] = np.where(np.isnan(df["y_contact"]), df["y"], df["y_contact"])
    df["y_contact"] = np.where(np.isinf(df["y_contact"]), df["y"], df["y_contact"])
    df["contact_y_check"] = df["slope"] * df["x_contact"] + (
        df["y"] - (df["slope"] * df["x"])
    )
    df["contact_y_check"] = np.where(
        np.isnan(df["contact_y_check"]), df["y"], df["contact_y_check"]
    )
    df["contact_y_check"] = np.where(
        np.isinf(df["contact_y_check"]), df["y"], df["contact_y_check"]
    )

    # TODO: compare ['y_contact'] and ['contact_y_check'] to ensure calculations match
    # (sanity check)
    # pd.testing.assert_series_equal(df['y_contact'], df['contact_y_check'])

    return df


def metric_diffs(df, metric_type):
    """ Calculate the differences and sums between the defender and ball carrier for the listed
        metric type, including x and y directional components.

    Args:
        df (pandas dataframe): player tracking dataframe with ball carrier details merged
            for each frame and force/momentum metrics

        metric_type (str): type of metric for calculations, either 'force' or 'momentum'

    Returns:
        pandas dataframe: same dataframe with new columns
            ('{metric_type}_diff', '{metric_type}_x_diff', '{metric_type}_y_diff',
             '{metric_type}_sum', '{metric_type}_x_sum', '{metric_type}_y_sum')
    """
    # metric diff
    # will not have any directonal sign
    # moving in same direction or opposite direction will not be captured
    # negative means tackler is moving with more momentum/force than ball carrier
    df[f"{metric_type}_diff"] = df[f"{metric_type}_ball_carrier"] - df[f"{metric_type}"]
    # metric sum
    # I think this is better, see notebook for explanation and write better summary
    df[f"{metric_type}_sum"] = df[f"{metric_type}_ball_carrier"] + df[f"{metric_type}"]
    # x diff and y diff
    # force will be larger than ball carrier force if tackler is moving in opposite direction
    df[f"{metric_type}_x_diff"] = (
        df[f"{metric_type}_x_ball_carrier"] - df[f"{metric_type}_x"]
    )
    df[f"{metric_type}_y_diff"] = (
        df[f"{metric_type}_y_ball_carrier"] - df[f"{metric_type}_y"]
    )

    df[f"{metric_type}_x_sum"] = (
        df[f"{metric_type}_x_ball_carrier"] + df[f"{metric_type}_x"]
    )
    df[f"{metric_type}_y_sum"] = (
        df[f"{metric_type}_y_ball_carrier"] + df[f"{metric_type}_y"]
    )
    return df


def time_to_contact(df):
    """ Calculate the time to contact values based on direction and speed of ball carrier and
        defender.

    Args:
        df (pandas dataframe): player tracking dataframe with ball carrier details merged
            for each frame and distances to contact values calculated

    Returns:
        pandas dataframe: same dataframe with new columns
            ('tackler_time_to_contact', 'ball_carrier_time_to_contact', 'diff_time_to_contact')
    """
    df["tackler_time_to_contact"] = df["tackler_to_contact_dist"] / df["s"]
    df["ball_carrier_time_to_contact"] = (
        df["ball_carrier_to_contact_dist"] / df["s_ball_carrier"]
    )
    df["diff_time_to_contact"] = (
        df["tackler_time_to_contact"] - df["ball_carrier_time_to_contact"]
    )
    return df


def out_of_phase(df):
    """ Calculate the difference between a player's direction of movement and body orientation.

    Args:
        df (pandas dataframe): player tracking dataframe with trig calculations completed.

    Returns:
        pandas dataframe: same dataframe with new column 'in_phase'
    """
    df["in_phase"] = abs(df["dir_sin"] - df["o_sin"])
    return df


def ball_carrier_plane_of_contact(df):
    """ Calculate the force and momentum metrics based on the defender's contact angle with
        the ball carrier.

    Args:
        df (pandas dataframe): player tracking dataframe with ball carrier details merged
            for each frame, force/momentum metrics calculated, and the defender's contact angle
            with the ball carrier determined.

    Returns:
        pandas dataframe: same dataframe with new columns
            columns for contact angle and trig
            columns for directional force and relative directional force with ball carrier
            columns for directional momentum and relative directional momentum with ball carrier
    """
    df["contact_angle"] = df["dir_ball_carrier"] - df["dir"]

    df["contact_angle_cos"] = np.cos(np.radians(df["contact_angle"]))
    df["contact_angle_force"] = df["force"] * df["contact_angle_cos"]
    df["contact_angle_force_y"] = df["force"] * np.sin(df["contact_angle"])
    df["contact_angle_force_y_abs"] = abs(df["contact_angle_force_y"])

    df["contact_angle_force_diff"] = (
        df["contact_angle_force"] - df["force_ball_carrier"]
    )
    df["contact_angle_force_sum"] = df["contact_angle_force"] + df["force_ball_carrier"]

    df["contact_angle_momentum"] = df["momentum"] * df["contact_angle_cos"]
    df["contact_angle_momentum_y"] = df["momentum"] * np.sin(
        np.radians(df["contact_angle"])
    )
    df["contact_angle_momentum_y_abs"] = abs(df["contact_angle_momentum_y"])

    df["contact_angle_momentum_diff"] = (
        df["contact_angle_momentum"] - df["momentum_ball_carrier"]
    )
    df["contact_angle_momentum_sum"] = (
        df["contact_angle_momentum"] + df["momentum_ball_carrier"]
    )
    return df
