import pandas as pd
from InquirerPy import inquirer
from pathlib import Path


# basepath variable
base_path = Path(
    r"C:\Users\Tom\AppData\Local\Solecismic Software\Front Office Football Eight\leaguedata"
)
# giving list of league names from directory
paths = [path.name for path in base_path.iterdir()]
# tab through the available leagues for selection.
selected_league = inquirer.select(
    message="Please select the league you would like:", choices=paths
).execute()
# import original csv
df_original = pd.read_csv(base_path / selected_league / "standings.csv")
# define year for dataframe
input_year = int(
    inquirer.number(message="Please enter the year you want to generate for:").execute()
)

# chaining - Pandas concept (read more) - create new dataframe by altering old dataframe
df_new = (
    # original df reference for chaining.
    df_original
    # remove columns not needed
    .drop(
        labels=[
            "Place",
            "Ties",
            "Note",
            "Conference_Wins",
            "Conference_Losses",
            "Conference_Ties",
            "Division_Wins",
            "Division_Losses",
            "Division_Ties",
        ],
        axis=1,
    )
    # set desired year for dataset via input from user.
    .loc[lambda df: df.Year == input_year]
    # calculation for expected wins using PF & PA stored in new variable/applied to df.
    .assign(
        Exp_Wins=lambda df: (
            (
                (df["Points_Scored"] ** 2.37)
                / (df["Points_Scored"] ** 2.37 + df["Points_Allowed"] ** 2.37)
                * (df["Wins"] + df["Losses"])

            )
            .round(0)
            .astype(int)
        )
    ).assign(
        Exp_Losses=lambda df: (df["Wins"] + df["Losses"]) - df.Exp_Wins  # calculate expected losses
    )
)
# Reorder the columns as desired.
columns = [
    "Year",
    "Division",
    "Team",
    "Wins",
    "Losses",
    "Exp_Wins",
    "Exp_Losses",
    "Points_Scored",
    "Points_Allowed",
]
df_new = df_new[columns]
# list containing team name conversions for Imperial league.
Imperial_team_names = {
    0: "Calgary Stampeders",
    1: "San Antonio Storm",
    2: "London Monarchs",
    3: "Columbia Chicharrones",
    4: "Tulsa Tequila Worms",
    5: "Madison Demons",
    6: "State College (PA) Stagz",
    7: "Texas Bulldogs",
    8: "Las Vegas Hookers",
    9: "Lansing Ogres",
    10: "Dakota Spirit",
    11: "Houston Renegades",
    12: "Miami Vice",
    13: "Portland Express",
    14: "Hartford Whalers",
    15: "Pittsburgh Pythons",
    16: "West Virginia Beasts",
    17: "Georgia Generals",
    18: "Florida Piranha",
    19: "Norfolk Vipers",
    20: "Los Angeles Matadors",
    21: "Kansas City Owls",
    22: "Montreal Firebirds",
    23: "Alaska Polar Bears",
    24: "Colorado Knights",
    25: "Salt Lake City Stallions",
    26: "Vancouver Killer Whales",
    27: "McAllen Lancers",
    28: "Raleigh Armada",
    29: "Boston Pikes",
    30: "Iowa City Tribe",
    31: "Murfreesboro Mules",
}
# RZB team names.
RZB_team_names = {
    0: "Arizona Cardinals",
    1: "Atlanta Falcons",
    2: "Baltimore Ravens",
    3: "Buffalo Bills",
    4: "Carolina Panthers",
    5: "Chicago Bears",
    6: "Cincinnati Bengals",
    7: "Dallas Cowboys",
    8: "Denver Broncos",
    9: "Detroit Lions",
    10: "Green Bay Packers",
    11: "Indianapolis Colts",
    12: "Jacksonville Jaguars",
    13: "Kansas City Chiefs",
    14: "Miami Dolphins",
    15: "Minnesota Vikings",
    16: "New England Patriots",
    17: "New Orleans Saints",
    18: "New York Giants",
    19: "New Jersey Jets",
    20: "Las Vegas Raiders",
    21: "Philadelphia Eagles",
    22: "Pittsburgh Steelers",
    23: "Los Angeles Chargers",
    24: "Seattle Seahawks",
    25: "San Francisco 49ers",
    26: "Los Angeles Rams",
    27: "Tampa Bay Buccaneers",
    28: "Tennessee Titans",
    29: "Washington Redskins",
    30: "Cleveland Browns",
    31: "Houston Texans",
}
df_new.Team = df_new.Team.map(
    Imperial_team_names if selected_league == "Imperial" else RZB_team_names
)
print(df_new)

df_new.to_csv(f"pythag_record_{selected_league}_{input_year}.csv", index=False)
