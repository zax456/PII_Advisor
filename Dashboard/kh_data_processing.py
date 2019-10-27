import pandas as pd
import numpy as np
from collections import defaultdict
import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html

df = pd.read_csv("./annotated_resumes.csv")

## Cleaning start and end dates
df["start_date_new"] = df["start_date"].apply(lambda x: "present" if np.isnan(x) else str(int(x)).lower().strip() )
df["end_date"] = df["end_date"].apply(lambda x: str(x).lower().strip() if type(x) == str else "present")

def change_dates(df, column):
    if df[column].isnumeric() == True:
        return pd.to_datetime(df[column], format='%Y%m%d').date()
    elif df[column] == "present":
        return dt.datetime.now().date()
    elif df[column] != "nan":
        return dt.datetime.strptime(df[column], '%B %Y').date()

df['end_date_new']=df.apply(change_dates, axis=1, args=("end_date",))
df['start_date_new']=df.apply(change_dates, axis=1, args=("start_date_new",))

# drop old dates since its not required
df = df.drop(["start_date", "end_date"], axis=1)

# -----------------------------------------------------------------------------------------------------------------------------------

def get_df():
    return df

"""
Pie chart 1~
Category: Industry
Value: % of ppl whose latest job is in that industry
"""
def gen_chart_1():
    ## sort df according to descending start date
    df_sorted_date = df.sort_values("start_date_new", ascending=False)

    ## get first record of each unique resume
    df_sorted_date = df_sorted_date.drop_duplicates("resume")
    ## unique industries
    industries = df_sorted_date.industry.unique().tolist()
    industries = list(map(lambda x:x.lower().strip(), industries))

    ## get percentage of people in each industry (most recent job)
    percents = round(df_sorted_date["industry"].value_counts() / df_sorted_date.shape[0] * 100, 1) # dict format 
                                                                                                # key=industry : value=percent
    chart1_df = pd.DataFrame(data=percents)
    chart1_df.reset_index(inplace=True)
    chart1_df.columns = ["Industry","Percentage"]
    chart1_df.sort_values(by="Percentage", inplace=True, ascending=False)

    ## Final chart 1 dataframe
    return chart1_df


# -----------------------------------------------------------------------------------------------------------------------------------

"""
Bar Chart 4~
Takes in multiple industry and checks for each industry and for each person, what industry was the person in his/her previous job prior to his current industry
If the previous industry is the same as current industry, don't count it
Normalise count by total people in that selected industry

Table schema:
Previous Industry | current_industry_1 | current_industry_2 | current_industry_N-1
----------------------------------------------------------------
    Finance       |     20%             |          20%        |     (N-1)%
   Engineering    |     10%             |          30%        |     (N-1)%
        .
        .
        .
"""
def gen_chart_4(current_industry):
    # sort df according to descending start date
    df_sorted_date = df.sort_values("start_date_new", ascending=False)

    # for each resume, keeps the top 2 record
    df_current_job = pd.DataFrame(columns = df_sorted_date.columns.values.tolist()) # new dataframe to hold current job industry of each resume
    df_previous_job = pd.DataFrame(columns = df_sorted_date.columns.values.tolist()) # new dataframe to hold previous job industry of each resume
    df_groups = df_sorted_date.groupby("resume") # group records by resume id

    for name, group in df_groups:
        for i in range(group.shape[0]):
            if i == 0: df_current_job = df_current_job.append(group.iloc[i, :])
            elif i == 1: df_previous_job = df_previous_job.append(group.iloc[i, :])
            else: break

    df_current_job.reset_index(inplace=True, drop=True)
    df_previous_job.reset_index(inplace=True, drop=True)

    counts = defaultdict(lambda: defaultdict(int)) # {Eng:{Healthcare: 2}, Business:{Army: 10}, Tech:{Finance: 5}}
    for curr_industry in current_industry:
        # ppl's whose latest job is in current industry
        ppl_in_curr_industry = df_current_job.loc[df_current_job["industry"] == curr_industry, "resume"].values.tolist()
        # keep those that has a previous job b4
        ppl_in_curr_industry = [ppl for ppl in ppl_in_curr_industry if ppl in df_previous_job["resume"]] 

        # counts of people whose job is in selected industry
        total_ppl = df_current_job[ (df_current_job["industry"] == curr_industry) & (df_current_job["resume"].isin(ppl_in_curr_industry))].count().values[0] 
        for idx in ppl_in_curr_industry:
            # get previous industry counts for those in the selected industry
            prev_industry = df_previous_job.loc[df_previous_job["resume"] == idx, "industry"].values[0]
            counts[curr_industry][prev_industry] += 1

        
        # normalisation step - total previous / total current
        # print(curr_industry, total_ppl)
        for previous_industry in counts[curr_industry].keys():
            counts[curr_industry][previous_industry] /= total_ppl
            counts[curr_industry][previous_industry] = round(counts[curr_industry][previous_industry], 2)

    # TODO
    # after getting all selected industries previous percent, put them into a dataframe
    chart4_df = pd.DataFrame(counts)
    chart4_df.fillna(value = 0, inplace = True)

    return chart4_df.T

# -----------------------------------------------------------------------------------------------------------------------------------

"""
Donut chart 2~
Category: Years of exp
Value: % of ppl with those years of exp

1. To get years of experience for each resume 
    a) group the dataframe by the resume id, sort the group by start date in ascending order
    b) take the end date of the 1st record - start date of the last record in the group to get years of experience
2. Create a dataframe with unique resume id and store their respective years of experience
"""
def count_experience(group):
    group = group.sort_values(by="start_date_new", ascending=False)
    num_experience_years = group.iloc[0, 5].year - group.iloc[-1, 4].year # end date of latest job - start date of 1st job
    return num_experience_years

def gen_chart_2():
    years_of_exp = pd.DataFrame(df.groupby("resume").apply(lambda x: count_experience(x)), columns=["Years"])
    total = years_of_exp.shape[0]
    years_of_exp = years_of_exp.groupby("Years").agg(
        percentage = pd.NamedAgg(column="Years", aggfunc=lambda x: round(x.value_counts()/total*100, 2))
        )
    
    return years_of_exp
