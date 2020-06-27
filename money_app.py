import pandas as pd
from flask import Flask, render_template, redirect, jsonify

app = Flask(__name__)

def graphData(money):
    
    #------------------------------------------- First Visualization ------------------------------------------------
    # Retrieve the earnings by sport per year
    yearly_Sport = pd.DataFrame(money.groupby(["Year", "Sport"])["Earnings (Millions of US$)"].sum()).unstack().droplevel(level=0, axis = 1)
    yearlySport = yearly_Sport.to_dict('index')
    
    # Retrieve the earnings by nationality per year
    yearly_Nationalities = pd.DataFrame(money.groupby(["Year", "Nationality"])["Earnings (Millions of US$)"].sum()).unstack().droplevel(level=0, axis = 1)
    yearlyNationalities = yearly_Nationalities.to_dict('index')

    # Retrieve the total earnings per year
    yearly_Earnings = pd.DataFrame(money.groupby(["Year"])["Earnings (Millions of US$)"].sum())
    yearlyEarnings = yearly_Earnings.to_json(orient = "table")
    
    # Total earnings per nationality & sort
    nationality_globalEarnings = pd.DataFrame(money.groupby(["Nationality"])["Earnings (Millions of US$)"].sum().sort_values(ascending = False))
    nationalityGlobalEarnings = nationality_globalEarnings.to_json(orient = "table")
    
    # Total earnings per sport & sort
    sports_globalEarnings = pd.DataFrame(money.groupby(["Sport"])["Earnings (Millions of US$)"].sum().sort_values(ascending = False))
    sportsGlobalEarnings = sports_globalEarnings.to_json(orient = "table")
    
    # Total earnings per athlete & sort
    athlete_earnings = pd.DataFrame(money.groupby(["Name"])["Earnings (Millions of US$)"].sum().sort_values(ascending = False))
    athleteEarnings = athlete_earnings.to_json(orient = "table")
    
    #------------------------------------------ Second Visualization -------------------------------------------------
    
    # Earnings per sport by year
    sports_specificEarnings = pd.DataFrame(money.groupby(["Sport", "Year"])["Earnings (Millions of US$)"].sum())
    sportSpecificEarnings = sports_specificEarnings.to_json(orient="table")

    # Rank count per sport
    sports_specificRanking = pd.DataFrame(money.groupby(["Sport"])["Rank"].value_counts()).rename(columns = {"Rank":"Count"})
    sportSpecificRanking = sports_specificRanking.to_json(orient = "table")

    # Total athletes per sport
    sports_Athletes = pd.DataFrame(money.groupby(["Sport"])["Name"].nunique())
    sportsAthletes = sports_Athletes.to_json(orient = "table")
    
    # Earnings per nationality by year
    nationality_specificEarnings = pd.DataFrame(money.groupby(["Nationality", "Year"])["Earnings (Millions of US$)"].sum())
    nationalitySpecificEarnings = nationality_specificEarnings.to_json(orient = "table")
    
    # Ranking count per nationality
    nationality_specificRanking = pd.DataFrame(money.groupby(["Nationality"])["Rank"].value_counts())
    nationality_specificRanking = nationality_specificRanking.rename(columns = {"Rank":"Count"})
    nationalitySpecificRanking = nationality_specificRanking.to_json(orient= "table")
    
    # Total atheletes per nationality
    nationality_Athletes = pd.DataFrame(money.groupby(["Nationality"])["Name"].nunique())
    nationalityAthletes = nationality_Athletes.to_json(orient = "table")
    
    # return [yearlySport, yearlyNation, yearlyEarnings, nationalityGlobalEarnings, sportsGlobalEarnings, athleteEarnings, sportSpecificEarnings, sportSpecificRanking, sportsAthletes, nationalitySpecificEarnings, nationalitySpecificRanking, nationalityAthletes]
    dictData = {
        "yearSport": yearlySport,
        "yearNation": yearlyNationalities
    }
    return jsonify(dictData)
     
@app.route("/")
def index():
    money = pd.read_csv("top_paid_clean.csv")
    data = graphData(money)
    # return render_template("index.html", data = data)
    return data
if __name__ == "__main__":
    app.run(debug = True)
