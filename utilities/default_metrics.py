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
        "Progressive": ["Passing%", "OP F3 Passes", "Carry Length", "xGBuildup", "Long Ball%"],
        "Advanced": ["Aerial Win%", "Blocks/Shot", "Ball Recoveries", "Defensive Regains", "Dispossessed"]
    },

    'Winger':
    {
        "Attacking": ["xG/Shot", "xG", "Shots", "PinTin", "NP Goals"],
        "Progressive": ["Successful Crosses", "Crossing%", "Key Passes", "Assists", "OP F3 Passes"],
        "Advanced": ["xG Assisted", "Dribbles", "Successful Dribbles", "Aggressive Actions", "Ball Recov. F2"]
    },

    'Centre Forward':
    {
        "Attacking": ["Shots", "xG", "Shot Touch%", "Shooting%", "NP Goals"],
        "Progressive": ["Key Passes", "PinTin", "OP F3 Passes", "Assists", "xG Assisted"],
        "Advanced": ["Aerial Win%", "Dribbles", "Successful Dribbles", "Aggressive Actions", "Ball Recov. F2"]
    },

    'Attacking Midfielder':
    {
        "Defensive": ["Dribbles Stopped%", "Defensive Actions", "PAdj Tackles", "PAdj Interceptions", "Aggressive Actions"],
        "Progressive": ["Passing%", "OP F3 Passes", "Carry Length", "xGBuildup", "Long Ball%"], 
        "Advanced": ["Aerial Win%", "Blocks/Shot", "Ball Recoveries", "Defensive Regains", "Dispossessed"]
    },
}

metrics_required = list(set(metric for role in all_metric_categories.values() for category in role.values() for metric in category))
all_numeric_metrics = [
    "NP Goals",
    "xG",
    "xG/Shot",
    "Shots",
    "Shooting%",
    "Shot Touch%",
    "Assists",
    "xG Assisted",
    "Key Passes",
    "Scoring Contribution",
    "Dribbles",
    "Successful Dribbles",
    "Dispossessed",
    "PAdj Interceptions",
    "PAdj Clearances",
    "Defensive Actions",
    "Aggressive Actions",
    "Blocks/Shot",
    "Defensive Regains",
    "Ball Recov. F2",
    "Ball Recoveries",
    "PAdj Tackles",
    "Dribbles Stopped%",
    "Aerial Win%",
    "Passing%",
    "Long Ball%",
    "xGBuildup",
    "Carry Length",
    "OP F3 Passes",
    "PinTin",
    "Successful Crosses",
    "Crossing%"
]
