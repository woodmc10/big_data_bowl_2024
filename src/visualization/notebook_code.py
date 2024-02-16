import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image, ImageOps

from matplotlib.patches import Rectangle

plt.rcParams.update({"axes.titlesize": 20, "axes.labelsize": 14})
plt.rc("ytick", labelsize=14)
plt.rc("xtick", labelsize=14)
plt.rc("legend", fontsize=12)
plt.rc("legend", title_fontsize=14)
# plt.rcParams.keys

run_metrics_df = pd.read_csv("../data/processed/run_plays_12-22_about2yards.csv")

# Clean data
def clean_data(metrics_df):
    metrics_df["event"].replace("assist", "tackle", inplace=True)
    #     metrics_df.drop(metrics_df[metrics_df['event'] == 'forcedFumble'].index, inplace=True)
    metrics_df.drop(
        metrics_df[metrics_df["event"].isin(["forcedFumble", "None"])].index,
        inplace=True,
    )

    metrics_df["tackler_time_to_contact"].replace([np.inf, -np.inf], 1000, inplace=True)
    metrics_df["ball_carrier_time_to_contact"].replace(
        [np.inf, -np.inf], 1000, inplace=True
    )
    metrics_df["diff_time_to_contact"].replace([np.inf, -np.inf], 1000, inplace=True)

    # must be within field of play, and less than 5 seconds from contact point at current speed
    metrics_df["make_contact"] = (
        (metrics_df["x_contact"] < 110)
        & (metrics_df["x_contact"] > 0)
        & (abs(metrics_df["diff_time_to_contact"]) < 5)
    )

    metrics_df["in_field"] = (
        (metrics_df["x_contact"] < 110)
        & (metrics_df["x_contact"] > 0)
        & (metrics_df["y_contact"] < 53.3)
        & (metrics_df["y_contact"] > 0)
    )
    # reduce data to only contact in field of play
    metrics_df_in_field = metrics_df[
        metrics_df["in_field"] & (metrics_df["behind_player"] == False)
    ]
    return metrics_df_in_field


def plotting_changes(metrics_df):
    metrics_df["momentum_x_abs"] = abs(metrics_df["momentum_x"])
    metrics_df["momentum_x_abs_ball_carrier"] = abs(
        metrics_df["momentum_x_ball_carrier"]
    )
    metrics_df["contact_angle_momentum_abs"] = abs(metrics_df["contact_angle_momentum"])
    metrics_df["Outcome"] = metrics_df["event"].apply(
        lambda x: "Tackle" if x == "tackle" else "Missed Tackle"
    )
    metrics_df["Defender Momentum"] = metrics_df["momentum"]
    metrics_df["Ball Carrier Momentum"] = metrics_df["momentum_ball_carrier"]
    metrics_df["Defender Endzone Momentum (abs)"] = metrics_df["momentum_x_abs"]
    metrics_df["Ball Carrier Endzone Momentum (abs)"] = metrics_df[
        "momentum_x_abs_ball_carrier"
    ]
    metrics_df["Defender Sideline Momentum"] = metrics_df["momentum_y"]
    metrics_df["Ball Carrier Sideline Momentum"] = metrics_df["momentum_y_ball_carrier"]
    metrics_df["Defender Sideline Momentum (abs)"] = metrics_df["momentum_y_abs"]
    metrics_df["Ball Carrier Sideline Momentum (abs)"] = metrics_df[
        "momentum_y_abs_ball_carrier"
    ]
    metrics_df["Defender Perpendicular Momentum"] = metrics_df[
        "contact_angle_momentum_y"
    ]
    metrics_df["Defender Perpendicular Momentum (abs)"] = metrics_df[
        "contact_angle_momentum_y_abs"
    ]
    metrics_df["Defender Parallel Momentum (abs)"] = metrics_df[
        "contact_angle_momentum_abs"
    ]
    return metrics_df


run_metrics_df = plotting_changes(clean_data(run_metrics_df))

# Define plotting functions
def hist(df, metric, fig_name=None):
    sns.histplot(df, x=metric, hue="Outcome", kde=True)
    if fig_name:
        plt.savefig(fig_name)
    plt.show()


def violin(df, metric, fig_name=None):
    sns.violinplot(df, x=metric, y="Outcome")
    if fig_name:
        plt.savefig(fig_name, bbox_inches="tight")
    plt.show()


def box(df, metric, fig_name=None):
    sns.boxplot(df, x=metric, y="Outcome")
    if fig_name:
        plt.savefig(fig_name)
    plt.show()


def regression(df, metric, fig_name=None):
    ax = sns.scatterplot(
        df,
        x=f"Defender {metric}",
        y=f"Ball Carrier {metric}",
        hue="Outcome",
        hue_order=df["Outcome"].unique(),
        alpha=0.3,
    )
    for event_type in df["Outcome"].unique():
        plotting_df = df.copy()
        plotting_df = plotting_df[plotting_df["Outcome"] == event_type]
        sns.regplot(
            plotting_df,
            x=f"Defender {metric}",
            y=f"Ball Carrier {metric}",
            scatter=False,
        )
    if fig_name:
        plt.savefig(fig_name)
    plt.show()


def regression_2(df, metric1, metric2, fig_name=None):
    ax = sns.scatterplot(
        df,
        x=metric1,
        y=metric2,
        hue="Outcome",
        hue_order=df["Outcome"].unique(),
        alpha=0.3,
    )
    for event_type in df["Outcome"].unique():
        plotting_df = df.copy()
        plotting_df = plotting_df[plotting_df["Outcome"] == event_type]
        sns.regplot(plotting_df, x=metric1, y=metric2, scatter=False)
    if fig_name:
        plt.savefig(fig_name)
    plt.show()


def plot_joint(df, metric1, metric2, fig_name=None):
    ax = sns.jointplot(
        df,
        x=metric1,
        y=metric2,
        hue="Outcome",
        hue_order=df["Outcome"].unique(),
        alpha=0.3,
    )
    if fig_name:
        plt.savefig(fig_name, bbox_inches="tight")
    plt.show()


def quad_plot_momentum(plot_df, ax, x_column, y_column, legend=False):
    colors = ["darkorange", "royalblue"]
    markers = ["x", "+"]
    values = ["tackle", "pff_missedTackle"]
    labels = ["Tackle", "Missed Tackle"]

    for i, value in enumerate(values):
        ax = sns.regplot(
            x=x_column,
            y=y_column,
            ax=ax,
            color=colors[i],
            marker=markers[i],
            data=plot_df[plot_df.event == value],
            label=labels[i],
            scatter_kws={"alpha": 0.3},
        )


def helmet_title_imgs(adjust):
    if adjust == "two rows":
        adjust = [0.02, 0.06, 0.005]
    elif adjust == "three rows":
        adjust = [0, 0.06, 0]
    else:
        adjust = [0, 0, 0]
    img_helmet = Image.open("helmet.png")
    img_football = Image.open("football.png")

    im = img_helmet.convert("RGBA")
    data = np.array(im)  # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability
    # Replace black with red... (leaves alpha values alone...)
    white_areas = (red == 0) & (blue == 0) & (green == 0)
    data[..., :-1][white_areas.T] = (255, 0, 0)  # Transpose back needed
    img_helmet_red = Image.fromarray(data)

    imagebox_helmet_1 = OffsetImage(img_helmet, zoom=0.15 - adjust[0])
    ab_1 = AnnotationBbox(
        imagebox_helmet_1,
        (0.15, 0.87 + adjust[1]),
        xycoords="figure fraction",
        frameon=False,
    )

    imagebox_football_1 = OffsetImage(img_football, zoom=0.05 - adjust[2])
    ab_2 = AnnotationBbox(
        imagebox_football_1,
        (0.13, 0.87 + adjust[1]),
        xycoords="figure fraction",
        frameon=False,
    )

    imagebox_helmet_2 = OffsetImage(
        ImageOps.mirror(img_helmet_red), zoom=0.15 - adjust[0]
    )
    ab_3 = AnnotationBbox(
        imagebox_helmet_2,
        (0.32, 0.87 + adjust[1]),
        xycoords="figure fraction",
        frameon=False,
    )

    imagebox_helmet_3 = OffsetImage(img_helmet, zoom=0.15 - adjust[0])
    ab_4 = AnnotationBbox(
        imagebox_helmet_3,
        (0.62, 0.87 + adjust[1]),
        xycoords="figure fraction",
        frameon=False,
    )

    imagebox_football_2 = OffsetImage(img_football, zoom=0.05 - adjust[2])
    ab_5 = AnnotationBbox(
        imagebox_football_2,
        (0.6, 0.87 + adjust[1]),
        xycoords="figure fraction",
        frameon=False,
    )

    imagebox_helmet_4 = OffsetImage(img_helmet_red, zoom=0.15 - adjust[0])
    ab_6 = AnnotationBbox(
        imagebox_helmet_4,
        (0.78, 0.87 + adjust[1]),
        xycoords="figure fraction",
        frameon=False,
    )
    return ab_1, ab_2, ab_3, ab_4, ab_5, ab_6


def endzone_plot(sampled_df, fig_name=None):
    ab_1, ab_2, ab_3, ab_4, ab_5, ab_6 = helmet_title_imgs(adjust="one row")
    fig, ax = plt.subplots(1, 2, figsize=(11, 6))
    plt.subplots_adjust(top=5 / 7, hspace=2 / 7, wspace=0.4)
    plot_1_df = sampled_df[
        (sampled_df["momentum_x"] > 0) & (sampled_df["momentum_x_ball_carrier"] > 0)
    ]
    quad_plot_momentum(
        plot_1_df,
        ax[1],
        "Defender Endzone Momentum (abs)",
        "Ball Carrier Endzone Momentum (abs)",
    )
    plot_2_df = sampled_df[
        (sampled_df["momentum_x"] < 0) & (sampled_df["momentum_x_ball_carrier"] > 0)
    ]
    quad_plot_momentum(
        plot_2_df,
        ax[0],
        "Defender Endzone Momentum (abs)",
        "Ball Carrier Endzone Momentum (abs)",
    )
    handles, labels = ax[1].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.51, 0.85))
    ax[0].add_artist(ab_1)
    ax[0].add_artist(ab_2)
    ax[0].add_artist(ab_3)
    ax[0].add_artist(ab_4)
    ax[0].add_artist(ab_5)
    ax[0].add_artist(ab_6)
    if fig_name:
        plt.savefig(fig_name, bbox_inches="tight")


def parallel_plot(sampled_df, fig_name=None):
    ab_1, ab_2, ab_3, ab_4, ab_5, ab_6 = helmet_title_imgs(adjust="two rows")
    fig, ax = plt.subplots(2, 2, figsize=(11, 11))
    plt.subplots_adjust(wspace=0.3)
    plot_1_df = sampled_df[sampled_df["contact_angle_momentum"] > 0]
    quad_plot_momentum(
        plot_1_df, ax[0, 1], "Defender Parallel Momentum (abs)", "Ball Carrier Momentum"
    )
    plot_2_df = sampled_df[(sampled_df["contact_angle_momentum"] < 0)]
    quad_plot_momentum(
        plot_2_df, ax[0, 0], "Defender Parallel Momentum (abs)", "Ball Carrier Momentum"
    )
    plot_3_df = sampled_df[
        (sampled_df["momentum_x"] > 0) & (sampled_df["momentum_x_ball_carrier"] > 0)
    ]
    quad_plot_momentum(
        plot_3_df,
        ax[1, 1],
        "Defender Endzone Momentum (abs)",
        "Ball Carrier Endzone Momentum (abs)",
    )
    plot_4_df = sampled_df[
        (sampled_df["momentum_x"] < 0) & (sampled_df["momentum_x_ball_carrier"] > 0)
    ]
    quad_plot_momentum(
        plot_4_df,
        ax[1, 0],
        "Defender Endzone Momentum (abs)",
        "Ball Carrier Endzone Momentum (abs)",
    )
    handles, labels = ax[0, 1].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper right")
    ax[0, 0].add_artist(ab_1)
    ax[0, 0].add_artist(ab_2)
    ax[0, 0].add_artist(ab_3)
    ax[0, 0].add_artist(ab_4)
    ax[0, 0].add_artist(ab_5)
    ax[0, 0].add_artist(ab_6)
    if fig_name:
        plt.savefig(fig_name)


def parallel_plot_2(sampled_df, fig_name=None):
    ab_1, ab_2, ab_3, ab_4, ab_5, ab_6 = helmet_title_imgs(adjust="one row")
    fig, ax = plt.subplots(1, 2, figsize=(11, 6))
    plt.subplots_adjust(top=5 / 7, hspace=2 / 7, wspace=0.4)
    plot_1_df = sampled_df[sampled_df["contact_angle_momentum"] > 0]
    quad_plot_momentum(
        plot_1_df, ax[1], "Defender Parallel Momentum (abs)", "Ball Carrier Momentum"
    )
    plot_2_df = sampled_df[(sampled_df["contact_angle_momentum"] < 0)]
    quad_plot_momentum(
        plot_2_df, ax[0], "Defender Parallel Momentum (abs)", "Ball Carrier Momentum"
    )
    handles, labels = ax[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper right", bbox_to_anchor=(0.6, 0.85))
    ax[0].add_artist(ab_1)
    ax[0].add_artist(ab_2)
    ax[0].add_artist(ab_3)
    ax[0].add_artist(ab_4)
    ax[0].add_artist(ab_5)
    ax[0].add_artist(ab_6)

    rect_1 = Rectangle((0, 100), 1030, 400, edgecolor="red", facecolor="none")
    rect_2 = Rectangle((0, 50), 1500, 450, edgecolor="red", facecolor="none")
    ax[0].add_artist(rect_1)
    ax[1].add_artist(rect_2)
    if fig_name:
        plt.savefig(fig_name, bbox_inches="tight")


def xy_plots(fig_name=None):
    ab_1, ab_2, ab_3, ab_4, ab_5, ab_6 = helmet_title_imgs(adjust="three rows")
    fig, ax = plt.subplots(3, 2, figsize=(11, 16))
    plt.subplots_adjust(wspace=0.3)
    plot_1_df = sampled_df[sampled_df["contact_angle_momentum"] > 0]
    quad_plot_momentum(
        plot_1_df,
        ax[2, 1],
        "Defender Parallel Momentum (abs)",
        "Defender Perpendicular Momentum (abs)",
        True,
    )
    plot_2_df = sampled_df[(sampled_df["contact_angle_momentum"] < 0)]
    quad_plot_momentum(
        plot_2_df,
        ax[2, 0],
        "Defender Parallel Momentum (abs)",
        "Defender Perpendicular Momentum (abs)",
    )
    plot_3_df = sampled_df[sampled_df["momentum_x"] > 0]
    quad_plot_momentum(
        plot_3_df,
        ax[1, 1],
        "Defender Endzone Momentum (abs)",
        "Defender Sideline Momentum (abs)",
    )
    plot_4_df = sampled_df[(sampled_df["momentum_x"] < 0)]
    quad_plot_momentum(
        plot_4_df,
        ax[1, 0],
        "Defender Endzone Momentum (abs)",
        "Defender Sideline Momentum (abs)",
    )
    plot_5_df = sampled_df[sampled_df["momentum_x_ball_carrier"] > 0]
    quad_plot_momentum(
        plot_5_df,
        ax[0, 1],
        "Ball Carrier Endzone Momentum (abs)",
        "Ball Carrier Sideline Momentum (abs)",
    )
    plot_6_df = sampled_df[(sampled_df["momentum_x_ball_carrier"] < 0)]
    quad_plot_momentum(
        plot_6_df,
        ax[0, 0],
        "Ball Carrier Endzone Momentum (abs)",
        "Ball Carrier Sideline Momentum (abs)",
    )
    handles, labels = ax[0, 1].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper right")
    ax[0, 0].add_artist(ab_1)
    ax[0, 0].add_artist(ab_2)
    ax[0, 0].add_artist(ab_3)
    ax[0, 0].add_artist(ab_4)
    ax[0, 0].add_artist(ab_5)
    ax[0, 0].add_artist(ab_6)
    if fig_name:
        plt.savefig(fig_name)


def plane_comparison(run_metrics_df, fig_name=None):
    defender_id = 42381.0
    defender_df = run_metrics_df[run_metrics_df["nflId"] == defender_id]

    fig, axes = plt.subplots(
        nrows=1, ncols=2, figsize=(11, 5), subplot_kw={"projection": "polar"}
    )
    plt.subplots_adjust(wspace=0.3)
    r = defender_df.momentum
    area = defender_df.momentum / 2
    colors = defender_df.apply(
        lambda x: "orange" if x.event == "tackle" else "blue", axis=1
    )
    theta_1 = np.radians(90 - defender_df.dir)
    theta_2 = np.radians(defender_df.contact_angle)

    axes[0].bar(theta_1, r, width=0.1, color=colors, alpha=0.3)
    axes[1].bar(theta_2, r, width=0.1, color=colors, alpha=0.3)

    # axes[0].scatter(theta_1, r, c=colors, s=area, alpha=0.3)
    # axes[1].scatter(theta_2, r, c=colors, s=area, alpha=0.3)

    # Format Axes
    for ax in axes:
        ax.set_rorigin(-800)
        ax.set_rticks([0, 400, 800, 1200, 1600])  # Less radial ticks
        #     ax.set_rlabel_position(90)  # Move radial labels away from plotted line
        ax.grid(True)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        # removing tick labels shifted the plot so icons will be shifted with math

    # Add Legend
    colors = {
        "Tackle": (1.0, 0.6470588235294118, 0.0, 0.3),
        "Missed Tackle": (0.0, 0.0, 1.0, 0.3),
    }
    labels = list(colors.keys())
    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
    angle = np.deg2rad(180)
    plt.legend(
        handles,
        labels,
        loc="lower left",
        bbox_to_anchor=(0.09 + np.cos(angle) / 2, 0.76 + np.sin(angle) / 2),
    )

    # Add Helmet Icons
    img_helmet = Image.open("helmet.png")
    img_football = Image.open("football.png")
    img_field = Image.open("football_field.jpeg")

    im = img_helmet.convert("RGBA")
    data = np.array(im)  # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability
    # Replace black with red... (leaves alpha values alone...)
    white_areas = (red == 0) & (blue == 0) & (green == 0)
    data[..., :-1][white_areas.T] = (255, 0, 0)  # Transpose back needed
    img_helmet_red = Image.fromarray(data)

    imagebox_helmet_1 = OffsetImage(img_helmet_red, zoom=0.09)
    ab_1 = AnnotationBbox(
        imagebox_helmet_1, (0.5, 0.5), xycoords="axes fraction", frameon=False
    )
    axes[0].add_artist(ab_1)

    imagebox_helmet_2 = OffsetImage(img_helmet_red, zoom=0.09)
    ab_2 = AnnotationBbox(
        imagebox_helmet_2, (0.5, 0.5), xycoords="axes fraction", frameon=False
    )
    axes[1].add_artist(ab_2)

    # Add Titles
    axes[0].set_title("Plane of Field")
    axes[1].set_title("Plane of Ball Carrier")

    # Add Title Icons
    imagebox_helmet_3 = OffsetImage(img_helmet, zoom=0.09)
    ab_3 = AnnotationBbox(
        imagebox_helmet_3,
        (0 - 0.04, 1.1 - 0.06),
        xycoords="axes fraction",
        frameon=False,
    )
    axes[1].add_artist(ab_3)

    imagebox_football_1 = OffsetImage(img_football, zoom=0.03)
    ab_4 = AnnotationBbox(
        imagebox_football_1,
        (-0.04 - 0.04, 1.1 - 0.06),
        xycoords="axes fraction",
        frameon=False,
    )
    axes[1].add_artist(ab_4)

    imagebox_field_1 = OffsetImage(img_field, zoom=0.4 - 0.05)
    ab_5 = AnnotationBbox(
        imagebox_field_1,
        (-0.04 + 0.01, 1.1 - 0.05),
        xycoords="axes fraction",
        frameon=False,
    )
    axes[0].add_artist(ab_5)

    # Add Direction Icons
    imagebox_helmet_4 = OffsetImage(img_helmet, zoom=0.045)
    ab_6 = AnnotationBbox(
        imagebox_helmet_4, (1, 0.5), xycoords="axes fraction", frameon=False
    )
    axes[1].add_artist(ab_6)

    imagebox_football_2 = OffsetImage(img_football, zoom=0.015)
    ab_7 = AnnotationBbox(
        imagebox_football_2, (0.98, 0.5), xycoords="axes fraction", frameon=False
    )
    axes[1].add_artist(ab_7)

    fig.text(
        0.45,
        0.4,
        "TOUCHDOWN",
        fontsize=10,
        backgroundcolor="green",
        c="white",
        rotation=-90,
        fontweight="extra bold",
        horizontalalignment="center",
    )

    fig.text(
        0.515, 0.15, "OLB Preston Smith", fontsize=14, horizontalalignment="center"
    )
    if fig_name:
        plt.savefig(fig_name)


def some_code():
    run_metrics_df = run_metrics_df[run_metrics_df["event"] != "None"]
    player_tackles = run_metrics_df.groupby(["nflId", "event"], as_index=False)[
        "playId"
    ].agg({"playId": "count"})
    player_tackles.rename({"playId": "count"}, axis=1, inplace=True)
    player_tackles["percent"] = player_tackles["count"] / player_tackles.groupby(
        "nflId"
    )["count"].transform("sum")
    player_pivot = player_tackles.pivot(
        columns="event", index="nflId", values=["count", "percent"]
    ).dropna()
    m = {t: "_".join(t) for t in player_pivot.columns}
    player_pivot = player_pivot.groupby(m, axis=1).mean()
    player_pivot.sort_values("count_pff_missedTackle").tail(10)


def down_sample(run_metrics_df):
    sampled_df = run_metrics_df.groupby("event").apply(
        lambda x: x.sample(n=629, random_state=42)
    )
    sampled_df = sampled_df[sampled_df["event"] != "None"]

    sampled_df_2 = run_metrics_df.groupby("event").apply(lambda x: x.sample(n=629))
    sampled_df_2 = sampled_df_2[sampled_df_2["event"] != "None"]

    sampled_df["momentum_x_abs"] = abs(sampled_df["momentum_x"])
    sampled_df["momentum_x_abs_ball_carrier"] = abs(
        sampled_df["momentum_x_ball_carrier"]
    )
    sampled_df["contact_angle_momentum_abs"] = abs(sampled_df["contact_angle_momentum"])

    return sampled_df
