all_metric_categories  = {
    'Centre Back':
    {
        "Defensive": ["Dribbles Stopped%", "Aerial Win%", "PAdj Tackles", "PAdj Interceptions", "Aggressive Actions"],
        "Progressive": ["Key Passes", "OP F3 Passes", "Carry Length", "xGBuildup", "Long Ball%"], #key_passes is temp ; it needs to be replaced with passes %
        "Advanced": ["PAdj Clearances", "Blocks/Shot", "Ball Recoveries", "Defensive Regains", "Dispossessed"]
    },

    'Full Back':
    {
        "Defensive": ["Dribbles Stopped%", "Ball Recov. F2", "PAdj Tackles", "PAdj Interceptions", "Aggressive Actions"],
        "Progressive": ["OP F3 Passes", "Carry Length", "xGBuildup", "Crossing%", "Successful Crosses"],
        "Advanced": ["xG Assisted", "Dribbles", "Successful Dribbles", "PinTin", "Dispossessed"]
    },

    'Defensive Midfielder':
    {
        "Defensive": ["Dribbles Stopped%", "Defensive Actions", "PAdj Tackles", "PAdj Interceptions", "Aggressive Actions"],
        "Progressive": ["Key Passes", "OP F3 Passes", "Carry Length", "xGBuildup", "Long Ball%"], #key_passes is temp ; it needs to be replaced with passes %
        "Advanced": ["Aerial Win%", "Blocks/Shot", "Ball Recoveries", "Defensive Regains", "Dispossessed"]
    },

    'Winger':
    {
        "Attacking": ["xG/Shot", "xG", "Shots", "PinTin", "NP Goals"], #np_goals is temp ; it needs to be replaced with goals
        "Progressive": ["Successful Crosses", "Crossing%", "Key Passes", "Assists", "OP F3 Passes"],
        "Advanced": ["xG Assisted", "Dribbles", "Successful Dribbles", "Aggressive Actions", "Ball Recov. F2"]
    },

    'Centre Forward':
    {
        "Attacking": ["xG/Shot", "xG", "Shot Touch%", "Shooting%", "NP Goals"], #np_goals is temp ; it needs to be replaced with goals
        "Progressive": ["Key Passes", "PinTin", "OP F3 Passes", "Assists", "xG Assisted"],
        "Advanced": ["Aerial Win%", "Dribbles", "Successful Dribbles", "Aggressive Actions", "Ball Recov. F2"]
    },

    'Attacking Midfielder':
    {
        "Defensive": ["Dribbles Stopped%", "Defensive Actions", "PAdj Tackles", "PAdj Interceptions", "Aggressive Actions"],
        "Progressive": ["Key Passes", "OP F3 Passes", "Carry Length", "xGBuildup", "Long Ball%"], #key_passes is temp ; it needs to be replaced with passes %
        "Advanced": ["Aerial Win%", "Blocks/Shot", "Ball Recoveries", "Defensive Regains", "Dispossessed"]
    },
}

metrics_required = list(set(metric for role in all_metric_categories.values() for category in role.values() for metric in category))
