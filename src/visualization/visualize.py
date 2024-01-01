import plotly.graph_objects as go
import pandas as pd
import numpy as np

from PIL import Image


colors = {
    'ARI':"#97233F", 
    'ATL':"#A71930", 
    'BAL':'#241773', 
    'BUF':"#00338D", 
    'CAR':"#0085CA", 
    'CHI':"#C83803", 
    'CIN':"#FB4F14", 
    'CLE':"#311D00", 
    'DAL':'#003594',
    'DEN':"#FB4F14", 
    'DET':"#0076B6", 
    'GB':"#203731", 
    'HOU':"#03202F", 
    'IND':"#002C5F", 
    'JAX':"#9F792C", 
    'KC':"#E31837", 
    # 'LA':"#003594", 
    'LA':"#E31837", 
    'LAC':"#0080C6", 
    'LV':"#000000",
    'MIA':"#008E97", 
    'MIN':"#4F2683", 
    'NE':"#002244", 
    'NO':"#D3BC8D", 
    'NYG':"#0B2265", 
    'NYJ':"#125740", 
    'PHI':"#004C54", 
    'PIT':"#FFB612", 
    'SEA':"#69BE28", 
    'SF':"#AA0000",
    'TB':'#D50A0A', 
    'TEN':"#4B92DB", 
    'WAS':"#5A1414", 
    'football':'#CBB67C'
}

def show_frame(play_df, frame_num):
    """
    Visualize a single frame of a play.
    
    Parameters
    ----------
    play_df: pandas dataframe
        dataframe containing the only the play of interest
    frame_num: int
        frame number to visualize
    """
    fig = go.Figure(layout_yaxis_range=[0,53.3], layout_xaxis_range=[0,120])

    for team in play_df.club.unique():
        plot_df = play_df[(play_df.club==team)&(play_df.frameId==frame_num)]
        fig.add_trace(go.Scatter(
            x=plot_df["x"], y=plot_df["y"],
            mode = 'markers', name=team,
            marker_color=colors[team]
        ))
    fig.show()

def animate_play(tracking_df, play_df, players, gameId, playId):
    """
    Display an animation of the selected play.

    Parameters
    ----------
    tracking_df: pandas dataframe
        dataframe of tracking information that contains the given gameId and playId
    play_df: pandas dataframe
        dataframe containing play level information from each game
    players: pandas dataframe
        dataframe containing NFL player level information
    gameId: int
        numeric identifier of an NFL game
    playId: int
        numeric identifier of a play
    """
    #TODO: assert playId is present for given gameId
    selected_play_df = play_df[(play_df.playId==playId)&(play_df.gameId==gameId)].copy()
    
    tracking_players_df = pd.merge(tracking_df,players,how="left",on = "nflId", suffixes=[None, '_y'])
    
    selected_tracking_df = tracking_players_df[(tracking_players_df.playId==playId)&
                                                (tracking_players_df.gameId==gameId)].copy()

    sorted_frame_list = selected_tracking_df.frameId.unique()
    sorted_frame_list.sort()

    # get play General information 
    line_of_scrimmage = selected_play_df.absoluteYardlineNumber.values[0]
    first_down_marker = line_of_scrimmage + selected_play_df.yardsToGo.values[0]
    down = selected_play_df.down.values[0]
    quarter = selected_play_df.quarter.values[0]
    gameClock = selected_play_df.gameClock.values[0]
    playDescription = selected_play_df.playDescription.values[0]
    # Handle case where we have a really long Play Description and want to split it into two lines
    if len(playDescription.split(" "))>15 and len(playDescription)>115:
        playDescription = " ".join(playDescription.split(" ")[0:16]) + "<br>" + " ".join(playDescription.split(" ")[16:])

    # initialize plotly start and stop buttons for animation
    updatemenus_dict = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 100, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": 0}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]
    # initialize plotly slider to show frame position in animation
    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Frame:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }


    frames = []
    for frameId in sorted_frame_list:
        data = []
        # Add Numbers to Field 
        data.append(
            go.Scatter(
                x=np.arange(20,110,10), 
                y=[5]*len(np.arange(20,110,10)),
                mode='text',
                text=list(map(str,list(np.arange(20, 61, 10)-10)+list(np.arange(40, 9, -10)))),
                textfont_size = 30,
                textfont_family = "Courier New, monospace",
                textfont_color = "#ffffff",
                showlegend=False,
                hoverinfo='none'
            )
        )
        data.append(
            go.Scatter(
                x=np.arange(20,110,10), 
                y=[53.5-5]*len(np.arange(20,110,10)),
                mode='text',
                text=list(map(str,list(np.arange(20, 61, 10)-10)+list(np.arange(40, 9, -10)))),
                textfont_size = 30,
                textfont_family = "Courier New, monospace",
                textfont_color = "#ffffff",
                showlegend=False,
                hoverinfo='none'
            )
        )
        # Add line of scrimage 
        data.append(
            go.Scatter(
                x=[line_of_scrimmage,line_of_scrimmage], 
                y=[0,53.5],
                line_dash='dash',
                line_color='blue',
                showlegend=False,
                hoverinfo='none'
            )
        )
        # Add First down line 
        data.append(
            go.Scatter(
                x=[first_down_marker,first_down_marker], 
                y=[0,53.5],
                line_dash='dash',
                line_color='yellow',
                showlegend=False,
                hoverinfo='none'
            )
        )
        # Plot Players
        for team in selected_tracking_df.club.unique():
            plot_df = selected_tracking_df[(selected_tracking_df.club==team)&(selected_tracking_df.frameId==frameId)].copy()
            if team != "football":
                hover_text_array=[]
                for nflId in plot_df.nflId:
                    selected_player_df = plot_df[plot_df.nflId==nflId]
                    hover_text_array.append("nflId:{}<br>displayName:{}".format(selected_player_df["nflId"].values[0],
                                                                                      selected_player_df["displayName"].values[0]))
                data.append(go.Scatter(x=plot_df["x"], y=plot_df["y"],mode = 'markers',marker_color=colors[team],name=team,hovertext=hover_text_array,hoverinfo="text"))
            else:
                data.append(go.Scatter(x=plot_df["x"], y=plot_df["y"],mode = 'markers',marker_color=colors[team],name=team,hoverinfo='none'))
        # add frame to slider
        slider_step = {"args": [
            [frameId],
            {"frame": {"duration": 100, "redraw": False},
             "mode": "immediate",
             "transition": {"duration": 0}}
        ],
            "label": str(frameId),
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)
        frames.append(go.Frame(data=data, name=str(frameId)))

    scale=10
    layout = go.Layout(
        autosize=False,
        width=120*scale,
        height=60*scale,
        xaxis=dict(range=[0, 120], autorange=False, tickmode='array',tickvals=np.arange(10, 111, 5).tolist(),showticklabels=False),
        yaxis=dict(range=[0, 53.3], autorange=False,showgrid=False,showticklabels=False),

        plot_bgcolor='#00B140',
        # Create title and add play description at the bottom of the chart for better visual appeal
        title=f"GameId: {gameId}, PlayId: {playId}<br>{gameClock} {quarter}Q"+"<br>"*19+f"{playDescription}",
        updatemenus=updatemenus_dict,
        sliders = [sliders_dict]
    )

    fig = go.Figure(
        data=frames[0]["data"],
        layout= layout,
        frames=frames[1:]
    )
    # Create First Down Markers 
    for y_val in [0,53]:
        fig.add_annotation(
                x=first_down_marker,
                y=y_val,
                text=str(down),
                showarrow=False,
                font=dict(
                    family="Courier New, monospace",
                    size=16,
                    color="black"
                    ),
                align="center",
                bordercolor="black",
                borderwidth=2,
                borderpad=4,
                bgcolor="#ff7f0e",
                opacity=1
                )

    return fig

import matplotlib.pyplot as plt
 
# starter code for plotting lines for showing tackler - ball carrier contact point
def plot_line(slope, point):
    """
    This function plots a line on a graph based on the given slope and point.
    
    Parameters:
    slope (float): The slope of the line
    point (tuple): The coordinates of a point on the line (x, y)
    
    Returns:
    None
    """
    try:
        # Check if the slope is a number
        if not isinstance(slope, (int, float)):
            raise TypeError("The slope must be a number")
        
        # Check if the point is a tuple with two elements
        if not isinstance(point, tuple) or len(point) != 2:
            raise TypeError("The point must be a tuple with two elements")
        
        # Extract the coordinates from the point
        x, y = point
        
        # Generate x-values for the line
        x_values = range(0, 120)
        
        # Calculate y-values for the line using the slope-intercept form
        y_values = [slope * (x_val - x) + y for x_val in x_values]
        
        # Plot the line
        plt.plot(x_values, y_values)
        plt.scatter(x, y)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Line Plot')
        plt.grid(True)
        plt.axis([0, 120, 0, 53])
        plt.show()
        
    except TypeError as e:
        # Log the error
        print(f"Error: {e}")


def animate_frame(tracking_df, play_df, players, gameId, playId, frameId, defender, animation_image):
    """
    Display an animation of the selected play.

    Parameters
    ----------
    tracking_df: pandas dataframe
        dataframe of tracking information that contains the given gameId and playId
    play_df: pandas dataframe
        dataframe containing play level information from each game
    players: pandas dataframe
        dataframe containing NFL player level information
    gameId: int
        numeric identifier of an NFL game
    playId: int
        numeric identifier of a play
    frameId: int
        numeric identifier of a frame
    defender: int or float
        numeric identifier of primary defender for the frame
    animation_image: int
        numeric identifier of the animation image order for building explanation animation
    arrows: bool
        if True plot arrows for players directions
    """
    #TODO: assert playId is present for given gameId
    selected_play_df = play_df[(play_df.playId==playId)&(play_df.gameId==gameId)].copy()
    
    tracking_players_df = pd.merge(tracking_df,players,how="left",on = "nflId", suffixes=[None, '_y'])
    
    selected_tracking_df = tracking_players_df[(tracking_players_df.playId==playId)&
                                                (tracking_players_df.gameId==gameId)].copy()


    # get play General information 
    line_of_scrimmage = selected_play_df.absoluteYardlineNumber.values[0]
    first_down_marker = line_of_scrimmage + selected_play_df.yardsToGo.values[0]
    down = selected_play_df.down.values[0]
    ball_carrier = selected_play_df.ballCarrierId.values[0]

    ball_carrier_df = selected_tracking_df[(selected_tracking_df.frameId == frameId) &
                                           (selected_tracking_df.nflId == ball_carrier)]

    ball_carrier_x = ball_carrier_df['x'].values[0]
    ball_carrier_y = ball_carrier_df['y'].values[0]
    # transform ball carrier direction into counter clockwise from x-axis
    ball_carrier_dir_deg = 90 - ball_carrier_df['dir'].values[0]
    ball_carrier_dir = np.radians(ball_carrier_dir_deg)

    defender_df = selected_tracking_df[(selected_tracking_df.frameId == frameId) &
                                       (selected_tracking_df.nflId == defender)]

    defender_x = defender_df['x'].values[0]
    defender_y = defender_df['y'].values[0]
    
    # contact angle = dir ball carrier - dir defender
    contact_angle = ball_carrier_df['dir'].values[0] - defender_df['dir'].values[0]
    contact_angle_rad = np.radians(contact_angle)

    """
    Frames
    1 - all players
    2 - ball carrier and defender only
    3 - add arrows
    4 - zoom
    5 - add plane of field
    6 - reduce the visual to just the ball carrier
    7 - how the decomposed momentum in the sideline and endzone directions
    8 - return to frame 5
    9 - add plane of ball carrier
    10 - zoom again
    11 - rotate
    12 - reduce to only the defender
    13 - show decomposed momentum of defender
    """
    two_player_image = 2
    arrow_image = 3
    first_zoom_image = 4
    plane_of_field_image = 5
    field_decompose_image = 7
    plane_of_ball_carrier_image = 9
    second_zoom_image = 10
    rotate_image = 11
    bc_decompose_image = 13
    drop_defender_images = [6, 7]
    drop_ball_carrier_images = [12, 13]

    # Set Animation Frame Values for Zooming
    if animation_image < first_zoom_image:
        # create a square at full size
        layout_x_range = [ball_carrier_x - 53.3/2, ball_carrier_x + 53.3/2]
        layout_y_range = [0, 53.3]
        first_down_markers = [0, 53.3]
        top_number_markers = [5]*len(np.arange(20,110,10))
        bottom_number_markers = [53.3-5]*len(np.arange(20,110,10))
        helmet_size = 2
        ball_carrier_plane_annotation_size = 10
    elif animation_image < second_zoom_image:
        layout_x_range = [ball_carrier_x - 12, ball_carrier_x + 12]
        layout_y_range = [ball_carrier_y - 12, ball_carrier_y + 12]
        first_down_markers = [ball_carrier_y - 11.5, ball_carrier_y + 11.5]
        top_number_markers = [ball_carrier_y - 10]*len(np.arange(20,110,10))
        bottom_number_markers = [ball_carrier_y + 10]*len(np.arange(20,110,10))
        helmet_size = 2
        ball_carrier_plane_annotation_size = 10
    else:
        layout_x_range = [ball_carrier_x - 6.8, ball_carrier_x + 6.8]
        layout_y_range = [ball_carrier_y - 6.8, ball_carrier_y + 6.8]
        first_down_markers = [ball_carrier_y - 6.5, ball_carrier_y + 6.5]
        top_number_markers = [ball_carrier_y - 6]*len(np.arange(20,110,10))
        bottom_number_markers = [ball_carrier_y + 6]*len(np.arange(20,110,10))
        helmet_size = 1.25
        ball_carrier_plane_annotation_size = 20
        pass
    
    frames = []
    data = []
    # Add Numbers to Field 
    data.append(
        go.Scatter(
            x=np.arange(20,110,10), 
            y=top_number_markers,
            mode='text',
            text=list(map(str,list(np.arange(20, 61, 10)-10)+list(np.arange(40, 9, -10)))),
            textfont_size = 30,
            textfont_family = "Courier New, monospace",
            textfont_color = "#ffffff",
            showlegend=False,
            hoverinfo='none'
        )
    )
    data.append(
        go.Scatter(
            x=np.arange(20,110,10), 
            y=bottom_number_markers,
            mode='text',
            text=list(map(str,list(np.arange(20, 61, 10)-10)+list(np.arange(40, 9, -10)))),
            textfont_size = 30,
            textfont_family = "Courier New, monospace",
            textfont_color = "#ffffff",
            showlegend=False,
            hoverinfo='none'
        )
    )
    # Add line of scrimage 
    data.append(
        go.Scatter(
            x=[line_of_scrimmage,line_of_scrimmage], 
            y=[0,53.5],
            line_dash='dash',
            line_color='black',
            showlegend=False,
            hoverinfo='none'
        )
    )
    # Add First down line 
    data.append(
        go.Scatter(
            x=[first_down_marker,first_down_marker], 
            y=[0,53.5],
            line_dash='dash',
            line_color='yellow',
            showlegend=False,
            hoverinfo='none'
        )
    )

    # set values for plane of ball carrier
    shift_scale = 4
    x1 = -shift_scale * np.cos(ball_carrier_dir) + shift_scale * np.sin(ball_carrier_dir) + ball_carrier_x
    x2 = -shift_scale * np.cos(ball_carrier_dir) - shift_scale * np.sin(ball_carrier_dir) + ball_carrier_x
    x3 = shift_scale * np.cos(ball_carrier_dir) + shift_scale * np.sin(ball_carrier_dir) + ball_carrier_x

    y1 = -shift_scale * np.sin(ball_carrier_dir) - shift_scale * np.cos(ball_carrier_dir) + ball_carrier_y
    y2 = -shift_scale * np.sin(ball_carrier_dir) + shift_scale * np.cos(ball_carrier_dir) + ball_carrier_y
    y3 = shift_scale * np.sin(ball_carrier_dir) - shift_scale * np.cos(ball_carrier_dir) + ball_carrier_y


    if animation_image >= plane_of_field_image:
        # Add Field of Play Square
        print(animation_image)
        data.append(
            go.Scatter(
                x=[ball_carrier_x - 7, ball_carrier_x - 7],
                y=[ball_carrier_y - 7, ball_carrier_y + 7],
                # line_dash='dot',
                line_color='white',
                marker=dict(size=10,symbol= "arrow-bar-up", angleref="previous"),
                showlegend=False,
                hoverinfo='none',
                text=['Endzone Momentum', None]
            )
        )
        data.append(
            go.Scatter(
                x=[ball_carrier_x - 7, ball_carrier_x + 7], 
                y=[ball_carrier_y - 7, ball_carrier_y - 7],
                # line_dash='dot',
                line_color='white',
                marker=dict(size=10,symbol= "arrow-bar-up", angleref="previous"),
                showlegend=False,
                hoverinfo='none'
            )
        )

    if animation_image >= plane_of_ball_carrier_image:
        # Add Plane of Ball Carrier Square
        data.append(
            go.Scatter(
                x=[x1, x2], 
                y=[y1, y2],
                line_dash='dot',
                line_color='red',
                marker=dict(size=10,symbol= "arrow-bar-up", angleref="previous"),
                showlegend=False,
                hoverinfo='none'
            )
        )
        data.append(
            go.Scatter(
                x=[x1, x3], 
                y=[y1, y3],
                line_dash='dot',
                line_color='red',
                marker=dict(size=10,symbol= "arrow-bar-up", angleref="previous"),
                showlegend=False,
                hoverinfo='none'
            )
        )

    # Plot Players
    for team in selected_tracking_df.club.unique():
        plot_df = selected_tracking_df[(selected_tracking_df.club==team)&(selected_tracking_df.frameId==frameId)].copy()
        if animation_image >= two_player_image:
            plot_df = plot_df[plot_df.nflId.isin([ball_carrier, defender])]
        if animation_image in drop_defender_images:
            plot_df = plot_df[plot_df.nflId == ball_carrier]
        elif animation_image in drop_ball_carrier_images:
            plot_df = plot_df[plot_df.nflId == defender]
        
        if len(plot_df) == 0:
            continue
        if team != "football":
            hover_text_array=[]
            for nflId in plot_df.nflId:
                
                selected_player_df = plot_df[plot_df.nflId==nflId]
                hover_text_array.append("nflId:{}<br>displayName:{}".format(selected_player_df["nflId"].values[0],
                                                                            selected_player_df["displayName"].values[0]))
            data.append(go.Scatter(x=plot_df["x"], 
                                   y=plot_df["y"],
                                   mode='markers',
                                   marker_color=colors[team],
                                   name=team,
                                   hovertext=hover_text_array,
                                   hoverinfo="text"))

            if animation_image >= arrow_image:
                dir_radians = np.radians(90 - plot_df["dir"])
                plot_df["x_change"] = plot_df["x"] + (plot_df["s"] * np.cos(dir_radians))
                plot_df["y_change"] = plot_df["y"] + (plot_df["s"] * np.sin(dir_radians))
                
                x_diffs = plot_df[["x", "x_change"]].values.tolist()
                y_diffs = plot_df[["y", "y_change"]].values.tolist()
                
                for index, _ in enumerate(x_diffs):
                    data.append(go.Scatter(x=x_diffs[index], 
                                            y=y_diffs[index],
                                            marker=dict(size=10,symbol= "arrow-bar-up", angleref="previous"),
                                            showlegend=False,
                                            line_color=colors[team],
                                            hoverinfo='none'
                                            ))

                # decompose momentum in plane of field
                x_endzone = plot_df[['x', 'x_change']].values.tolist()
                y_endzone = plot_df[['y', 'y']].values.tolist()
                x_sideline = plot_df[['x', 'x']].values.tolist()
                y_sideline = plot_df[['y', 'y_change']].values.tolist()

                if animation_image == field_decompose_image:
                    for index, _ in enumerate(x_endzone):
                        data.append(go.Scatter(x=x_endzone[index], 
                                                y=y_endzone[index],
                                                marker=dict(size=10,symbol= "arrow-bar-up", angleref="previous"),
                                                showlegend=False,
                                                line_color='white',
                                                hoverinfo='none'
                                                ))
                        data.append(go.Scatter(x=x_sideline[index], 
                                                y=y_sideline[index],
                                                marker=dict(size=10,symbol= "arrow-bar-up", angleref="previous"),
                                                showlegend=False,
                                                line_color='white',
                                                hoverinfo='none'
                                                ))
                        
                # decompose momentum in plane of ball carrier
                        
                plot_df["x_change_bc"] = plot_df["x"] + (plot_df["s"] * np.cos(contact_angle_rad)) 
                plot_df["y_change_bc"] = plot_df["y"] + (plot_df["s"] * np.sin(contact_angle_rad))

                plot_df['parallel_point'] = plot_df.apply(lambda x: rotate_point(x['x'],
                                                                                 x['y'],
                                                                                 x['x_change_bc'],
                                                                                 x['y'],
                                                                                 ball_carrier_dir),
                                                          axis=1)
                plot_df['perpendicular_point'] = plot_df.apply(lambda x: rotate_point(x['x'],
                                                                                      x['y'],
                                                                                      x['x'],
                                                                                      x['y_change_bc'],
                                                                                      ball_carrier_dir),
                                                               axis=1)
                
                plot_df[['x_parallel_point', 'y_parallel_point']] = pd.DataFrame(
                    plot_df['parallel_point'].tolist(), index=plot_df.index
                    )
                plot_df[['x_perpendicular_point', 'y_perpendicular_point']] = pd.DataFrame(
                    plot_df['perpendicular_point'].tolist(), index=plot_df.index
                    )

                x_parallel = plot_df[['x', 'x_parallel_point']].values.tolist()
                y_parallel = plot_df[['y', 'y_parallel_point']].values.tolist()
                x_perpendicular = plot_df[['x', 'x_perpendicular_point']].values.tolist()
                y_perpendicular = plot_df[['y', 'y_perpendicular_point']].values.tolist()


                if animation_image == bc_decompose_image:
                    #TODO: make dotted line
                    for index, _ in enumerate(x_endzone):
                        data.append(go.Scatter(x=x_parallel[index], 
                                                y=y_parallel[index],
                                                marker=dict(size=10,symbol= "arrow-bar-up", angleref="previous"),
                                                showlegend=False,
                                                line_dash='dot',
                                                line_color='red',
                                                hoverinfo='none'
                                                ))
                        data.append(go.Scatter(x=x_perpendicular[index], 
                                                y=y_perpendicular[index],
                                                marker=dict(size=10,symbol= "arrow-bar-up", angleref="previous"),
                                                showlegend=False,
                                                line_dash='dot',
                                                line_color='red',
                                                hoverinfo='none'
                                                ))
        else:
            data.append(go.Scatter(x=plot_df["x"], 
                                   y=plot_df["y"],
                                   mode='markers',
                                   marker_color=colors[team],
                                   name=team,
                                   hoverinfo='none'))
    
    frames.append(go.Frame(data=data, name=str(frameId)))

    
    scale=10
    layout = go.Layout(
        autosize=False,
        width=60*scale,
        height=60*scale,
        xaxis=dict(range=layout_x_range, autorange=False, tickmode='array',tickvals=np.arange(10, 111, 5).tolist(),showticklabels=False),
        yaxis=dict(range=layout_y_range, autorange=False,showgrid=False,showticklabels=False),

        plot_bgcolor='#00B140',
        # Create title and add play description at the bottom of the chart for better visual appeal
        # title=f"GameId: {gameId}, PlayId: {playId}<br>{gameClock} {quarter}Q"+"<br>"*19+f"{playDescription}",
        # updatemenus=updatemenus_dict,
        # sliders = [sliders_dict]
        showlegend=False
    )

    fig = go.Figure(
        data=frames[0]["data"],
        layout= layout,
        frames=frames[1:]
    )
    # Create First Down Markers 
    for y_val in first_down_markers:
        fig.add_annotation(
                x=line_of_scrimmage,
                y=y_val,
                text=str(down),
                showarrow=False,
                font=dict(
                    family="Arial Black",
                    size=14,
                    color="#ff7f0e"
                    ),
                align="center",
                bordercolor="black",
                borderwidth=0,
                borderpad=2,
                bgcolor="black",
                opacity=1
                )
    
    if animation_image >= plane_of_field_image:
        # Add Axes Annotations
            # Plane of Field
        fig.add_annotation(
            x=ball_carrier_x,
            y=ball_carrier_y - 8,
            text='Endzone Momentum',
            showarrow=False,
            font=dict(
                family="Droid Sans",
                size=20,
                color="white"
                ),
            align="center"
        )

        fig.add_annotation(
            x=ball_carrier_x - 8,
            y=ball_carrier_y,
            text='Sideline Momentum',
            textangle=-90,
            showarrow=False,
            font=dict(
                family="Droid Sans",
                size=20,
                color="white"
                ),
            align="center"
        )
    
    if animation_image >= plane_of_ball_carrier_image:
    # Plane of Ball Carrier Axes Labels
        fig.add_annotation(
            x=(x3 - x1)/3 + x1,
            y=(y3 - y1)/3 + y1 - 1,
            text='Parallel Momentum',
            showarrow=False,
            font=dict(
                family="Droid Sans",
                size=ball_carrier_plane_annotation_size,
                color="Red"
                ),
            align="center",
            textangle=-ball_carrier_dir_deg - 1
        )

        fig.add_annotation(
            x=(x2 - x1)/2 + x1 - 1,
            y=(y2 - y1)/2 + y1,
            text='Perpendicular Momentum',
            showarrow=False,
            font=dict(
                family="Droid Sans",
                size=ball_carrier_plane_annotation_size,
                color="Red"
                ),
            align="center",
            textangle=271 - ball_carrier_dir_deg
        )

    if animation_image >= two_player_image:
    # Add ball and helmet icon to indicate ball carrier and tackler
        if animation_image not in drop_ball_carrier_images:
            fig.add_layout_image(
                dict(
                    source=Image.open("../notebooks/football.png"),
                    xref='x',
                    yref='y',
                    xanchor='center',
                    yanchor='middle',
                    sizex=0.8*helmet_size,
                    sizey=0.8*helmet_size,
                    x=ball_carrier_x,
                    y=ball_carrier_y
                )
            )

        if animation_image not in drop_defender_images:
            fig.add_layout_image(
                dict(
                    source=Image.open("../notebooks/helmet.png"),
                    xref='x',
                    yref='y',
                    xanchor='center',
                    yanchor='middle',
                    sizex=helmet_size,
                    sizey=helmet_size,
                    x=defender_x,
                    y=defender_y
                )
            )
    
    return fig

# add sideline numbers to zoomed image
# parallel and perpendicular momentum

def rotate_point(h, k, x, y, angle):
    """_summary_

    Args:
        h, k: 
            anchor to set rotation
        x, y: 
            point to rotate around anchor
        angle (radians): 
            angle indicating amount of roation (ball_carrier_dir)
    """

    x1 = (x - h) * np.cos(angle) - (y - k) * np.sin(angle) + h
    y1 = (x - h) * np.sin(angle) + (y - k) * np.cos(angle) + k

    return (x1, y1)