# color scales: https://bsou.io/posts/color-gradients-with-python
import pandas as pd
import numpy as np
import random
from colour import Color
from collections import defaultdict, Counter
import datetime as dt
from dateutil.relativedelta import relativedelta
import dash
import dash_core_components as dcc
import dash_html_components as html

## Pastel color list
def get_random_color(pastel_factor = 0.5):
    return [(x+pastel_factor)/(1.0+pastel_factor) for x in [random.uniform(0,1.0) for i in [1,2,3]]]

def color_distance(c1,c2):
    return sum([abs(x[0]-x[1]) for x in zip(c1,c2)])

def generate_new_color(existing_colors, pastel_factor=0.5):
    max_distance = None
    best_color = None
    for i in range(0,100):
        color = get_random_color(pastel_factor = pastel_factor)
        if not existing_colors:
            return color
        best_distance = min([color_distance(color,c) for c in existing_colors])
        if not max_distance or best_distance > max_distance:
            max_distance = best_distance
            best_color = color
    return best_color

## Read in datasets/Data cleaning step
df = pd.read_csv("Dashboard/Annotated_Resumes.csv")
df_skills = pd.read_csv("Dashboard/data_engineering_extracted_skills_by_resume.csv", engine='python', names=[i for i in range(48)])
df_skills.set_index(0, inplace = True)
df_skills.index.name = "resume"

def hex_to_RGB(hex):
  ''' "#FFFFFF" -> [255,255,255] '''
  # Pass 16 to the integer function for change of base
  return [int(hex[i:i+2], 16) for i in range(1,6,2)]


def RGB_to_hex(RGB):
  ''' [255,255,255] -> "#FFFFFF" '''
  # Components need to be integers for hex to make sense
  RGB = [int(x) for x in RGB]
  return "#"+"".join(["0{0:x}".format(v) if v < 16 else
            "{0:x}".format(v) for v in RGB])

def color_dict(gradient):
  ''' Takes in a list of RGB sub-lists and returns dictionary of
    colors in RGB and hex form for use in a graphing function
    defined later on '''
  return {"hex":[RGB_to_hex(RGB) for RGB in gradient],
      "r":[RGB[0] for RGB in gradient],
      "g":[RGB[1] for RGB in gradient],
      "b":[RGB[2] for RGB in gradient]}


def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
  ''' returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF") '''
  # Starting and ending colors in RGB form
  s = hex_to_RGB(start_hex)
  f = hex_to_RGB(finish_hex)
  # Initilize a list of the output colors with the starting color
  RGB_list = [s]
  # Calcuate a color at each evenly spaced value of t from 1 to n
  for t in range(1, n):
    # Interpolate RGB vector for color at the current value of t
    curr_vector = [
      int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
      for j in range(3)
    ]
    # Add it to our list of output colors
    RGB_list.append(curr_vector)

  return color_dict(RGB_list)


def rand_hex_color(num=1):
  ''' Generate random hex colors, default is one,
      returning a string. If num is greater than
      1, an array of strings is returned. '''
  colors = [
    RGB_to_hex([x*255 for x in np.random.rand(3)])
    for i in range(num)
  ]
  if num == 1:
    return colors[0]
  else:
    return colors


def polylinear_gradient(colors, n):
  ''' returns a list of colors forming linear gradients between
      all sequential pairs of colors. "n" specifies the total
      number of desired output colors '''
  # The number of colors per individual linear gradient
  n_out = n
#   int(float(n) / (len(colors) - 1))
  # returns dictionary defined by color_dict()
  gradient_dict = linear_gradient(colors[0], colors[1], n_out)

  if len(colors) > 1:
    for col in range(1, len(colors) - 1):
      next = linear_gradient(colors[col], colors[col+1], n_out)
      for k in ("hex", "r", "g", "b"):
        # Exclude first point to avoid duplicates
        gradient_dict[k] += next[k][1:]

  return gradient_dict

def get_df():
    return df

def color_generator(n, interval=None):
    result = []

    random_number = random.randint(0,16777215)
    hex_number = str(hex(random_number))
    hex_number ='#'+ hex_number[2:]

    for i in range(n):
        random_number = random.randint(0,16777215)
        hex_number = str(hex(random_number))
        hex_number ='#'+ hex_number[2:]

        # to make sure each color is unique
        while hex_number in result:
            random_number = random.randint(0,16777215)
            hex_number = str(hex(random_number))
            hex_number ='#'+ hex_number[2:]
        result.append(hex_number)
    return result

def get_subset_resumes(skills_df, industry, df=df):
    """
    get resumes who belong to the selected industry. Resume is selected if he/she is still working in that industry as of date

    Input:
        :skills_df: df of resumes and their skillset extracted
        :industry: a string name of the interested industry
        :df: master dataset consiting of resume id, job history

    Output:
        :subset of skills_df with resume belonging to that industry
    """
    df = df.sort_values(["resume","start_date_new"], ascending=[True,False])
    
    df = df.loc[df["resume"]!=df["resume"].shift()] # compare the dataframe against the dataframe shifted by 1 rows to get the first consecutive row
                                                    # .shift() moves the values in a column/Series up or down
    
    s = df.loc[df["industry"] == industry]["resume"]
    subset = skills_df.loc[skills_df.index.isin(s)]
    return subset

def get_top_n(n=10):
    """
    helper function to get the top n industry (most frequently appearing in all resumes)
    Input:
        :nil
    Output:
        list of strings of the top 10 industries
    """
    top_industries = df["industry"].value_counts().nlargest(n).index.tolist()
    return top_industries

### Data Cleaning - Cleaning start and end dates
df["start_date_new"] = df["start_date"].apply(lambda x: np.nan if np.isnan(x) else str(int(x)).lower().strip() )
df["end_date"] = df["end_date"].apply(lambda x: str(x).lower().strip() if type(x) == str else "present")

def change_dates(df, axis):
    if axis == 0:
        if df.isnumeric() == True:
            return pd.to_datetime(df, format='%Y%m%d').date()
        elif df == "present":
            return dt.datetime.now().date()
        elif df != "nan":
            return dt.datetime.strptime(df, '%B %Y').date()
    elif axis == 1:
        if type(df["start_date_new"]) == float:
            return df["end_date_new"]
        elif df["start_date_new"].isnumeric() == True:
            return pd.to_datetime(df["start_date_new"], format='%Y%m%d').date()
        elif df["start_date_new"] == "present":
            return dt.datetime.now().date()
        elif df["start_date_new"] != "nan":
            return dt.datetime.strptime(df["start_date_new"], '%B %Y').date()

df['end_date_new']=df["end_date"].apply(change_dates, args=(0,))
df["start_date_new"] = df.apply(change_dates, axis=1, args=(1,))
# df['start_date_new']=df.apply(change_dates, axis=1, args=("start_date_new",))
# df= df.apply(change_dates, axis=1, args=("start_date_new",))


# drop old dates since its not required
df = df.drop(["start_date", "end_date"], axis=1)

# -----------------------------------------------------------------------------------------------------------------------------------
## Generating Chart functions
"""
Pie Chart 1~
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

def gen_chart_2(industry=None):
    if industry == None: # return % of years of experience for whole population
        years_of_exp = pd.DataFrame(df.groupby("resume").apply(lambda x: count_experience(x)), columns=["Years"])
        total = years_of_exp.shape[0]
        years_of_exp = years_of_exp.groupby("Years").agg(
            percentage = pd.NamedAgg(column="Years", aggfunc=lambda x: round(x.value_counts()/total*100, 2))
            )
        
        return years_of_exp
    else: # return % of years of experience for that industry
        years_of_exp = pd.DataFrame(df[df["industry"] == industry].groupby("resume").apply(lambda x: count_experience(x)), columns=["Years"])
        total = years_of_exp.shape[0]
        years_of_exp = years_of_exp.groupby("Years").agg(
            # normalise Years column and append them to column named 'percentage'
            percentage = pd.NamedAgg(column="Years", aggfunc=lambda x: round(x.value_counts()/total*100, 2))
            )
        years_of_exp.columns = [industry]

        return years_of_exp

# -----------------------------------------------------------------------------------------------------------------------------------
def gen_chart_3(industry=None):
    """
    Bar chart 3
    Category: Skill set
    Value: % of people with each of the top 10 skills
    """
    if industry == None: # get top 10 skills from whole population
        unique_skills = {} # dict to store counts of each skill

        # get all unique skills
        for i in range(len(df_skills.columns.tolist())):
            skills = df_skills.iloc[:, i].unique().tolist()
            if None in skills: # need to remove None from data
                skills.remove(None)
            for s in skills:
                unique_skills[s] = 0

        # get skills of each resume 
        # increase count of that skill in unique_skills dict
        for i in range(df_skills.shape[0]):
            skillsets = df_skills.iloc[i, :].unique().tolist()
            if None in skillsets: # need to remove None from data
                skillsets.remove(None)
            for skill in skillsets:
                unique_skills[skill] += 1
        
        ## Normalisation of counts
        # total resume in dataset
        unique_counts_resume = len(df_skills.index.tolist())
        # change counts to percentage
        unique_skills = {k: round(v/unique_counts_resume*100, 1) for k, v in unique_skills.items()}
        
        chart_3_df = pd.DataFrame(Counter(unique_skills).most_common(10), columns=["skill", "count"])
        chart_3_df.set_index("skill", inplace=True)
        chart_3_df["count"] = [str(i)+"%" for i in chart_3_df["count"].tolist()]
        return chart_3_df

    # get top 10 skills in selected industry    
    else:
        # subset df to resumes that belong to that industry
        subset_skills_df = get_subset_resumes(df_skills, industry)

        # dict to store counts of each skill
        unique_skills = {} 

        # get all unique skills
        for i in range(len(subset_skills_df.columns.tolist())):
            skills = subset_skills_df.iloc[:, i].unique().tolist()
            if None in skills: # need to remove None from data
                skills.remove(None)
            for s in skills:
                unique_skills[s] = 0

        # get skills of each resume 
        # increase count of that skill in unique_skills dict
        for i in range(subset_skills_df.shape[0]):
            skillsets = subset_skills_df.iloc[i, :].unique().tolist()
            if None in skillsets: # need to remove None from data
                skillsets.remove(None)
            for skill in skillsets:
                unique_skills[skill] += 1
        
        ## Normalisation of counts
        # total resume in dataset
        unique_counts_resume = len(subset_skills_df.index.tolist())
        # change counts to percentage
        unique_skills = {k: "{}%".format(str(round(v/unique_counts_resume*100, 2))) for k, v in unique_skills.items()}

        chart_3_df = pd.DataFrame(Counter(unique_skills).most_common(10), columns=["skill", "count"])
        chart_3_df.set_index("skill", inplace=True)
        chart_3_df["count"] = [str(i)+"%" for i in chart_3_df["count"].tolist()]
        return chart_3_df

# -----------------------------------------------------------------------------------------------------------------------------------
"""
Bar Chart 4~
Takes in multiple industry and checks for each industry and for each person, what industry was the person in their previous jobs prior to his current industry
If the previous industry is the same as selected industry, don't count it. 
Normalise count by total people in that selected industry

Table schema:
Selected Industry | previous_industry_1 | previous_industry_2 | previous_industry_N-1
----------------------------------------------------------------
    Finance       |     20%             |          20%        |     (N-1)%
   Engineering    |     10%             |          30%        |     (N-1)%
        .
        .
        .
"""
def gen_chart_4(current_industry=None):

    if current_industry == None:
        current_industry = get_top_n()

    # sort df according to descending start date
    df_sorted_date = df.sort_values("start_date_new", ascending=False)

    # for each resume, keeps the top 2 record
    df_current_job = pd.DataFrame(columns = df_sorted_date.columns.values.tolist()) # new dataframe to hold current job industry of each resume
    df_previous_job = pd.DataFrame(columns = df_sorted_date.columns.values.tolist()) # new dataframe to hold previous job industry of each resume
    df_groups = df_sorted_date.groupby("resume") # group records by resume id

    for name, group in df_groups:
        resume_curr_industry = group["industry"].iloc[0]
        for i in range(group.shape[0]):
            if i == 0: 
                df_current_job = df_current_job.append(group.iloc[i, :])

            elif ( (df_previous_job["resume"].isin([name]).any() == False) and 
                  (group["industry"].iloc[i] != resume_curr_industry)): # if the person has a previous job that is of a different industry and is not in recorded yet
                df_previous_job = df_previous_job.append(group.iloc[i, :])
                break

    df_current_job.reset_index(inplace=True, drop=True)
    df_previous_job.reset_index(inplace=True, drop=True)

    # use defaultdict to auto create new keys in dict
    counts = defaultdict(lambda: defaultdict(int)) # {Eng:{Healthcare: 2}, Business:{Army: 10}, Tech:{Finance: 5}}
    for curr_industry in current_industry:
        # ppl's whose latest job is in current industry
        ppl_in_curr_industry = df_current_job.loc[df_current_job["industry"] == curr_industry, "resume"].values.tolist()
        # keep those that has a previous job b4
        ppl_in_curr_industry = [ppl for ppl in ppl_in_curr_industry if df_previous_job["resume"].isin([ppl]).any()] 

        # counts of people whose job is in selected industry
        total_ppl = df_current_job[ (df_current_job["industry"] == curr_industry) & (df_current_job["resume"].isin(ppl_in_curr_industry))].count().values[0] 
        for idx in ppl_in_curr_industry:
            # get previous industry counts for those in the selected industry
            prev_industry = df_previous_job.loc[df_previous_job["resume"] == idx, "industry"].values[0] # TODO Debug this
            counts[curr_industry][prev_industry] += 1

        
        # normalisation step - total previous / total current
        for previous_industry in counts[curr_industry].keys():
            counts[curr_industry][previous_industry] /= total_ppl
            counts[curr_industry][previous_industry] = round(counts[curr_industry][previous_industry], 2)

    # after getting all selected industries previous percent, put them into a dataframe
    chart4_df = pd.DataFrame(counts)
    chart4_df.fillna(value = 0, inplace = True)

    return chart4_df.T

# -----------------------------------------------------------------------------------------------------------------------------------
def gen_chart_5(industries=None):
    """
    Bar chart 5
    Y-axis: # of ppl
    X-axis 1: Industry
    X-axis 2: Skills (top 10 in that industry)
    """
    if industries == None:
        industries = get_top_n() # get top 10 industries

    # create the initial dataframe of skill counts
    chart_5_df = gen_chart_3(industries[0])
    for i in range(1, len(industries)):
        tmp = gen_chart_3(industries[i])
        chart_5_df = pd.concat([chart_5_df, tmp], axis = 1)
    
    chart_5_df.columns = industries
    chart_5_df.fillna(0, inplace=True)
    return chart_5_df

# -----------------------------------------------------------------------------------------------------------------------------------
"""
Stacked Bar chart 6

Y-axis: Industry
X-axis: % of ppl with Z years of experience 

Table schema:
    Years | Business | Tech   | ... | N industry 
     0    |   10     |   20   | ... |  5
     1    |   5      |   5    | ... |  10
                     .
                     .
                     .

Input:
    :Industries: list of strings of industry from user selection
Output:
    A dataframe with the mentioned table schema
        :rows - industry selected
        :columns - different years of experience
"""
def gen_chart_6(industries=None):
    years_df = ""
    for selected_ind in industries:
        tmp_df = gen_chart_2(selected_ind)
        if type(years_df) == str:
            years_df = tmp_df
        else:
            years_df = pd.concat([years_df, tmp_df], axis=1)

    years_df.fillna(0, inplace=True)
    return years_df

# -----------------------------------------------------------------------------------------------------------------------------------
"""
Stacked bar chart 7
Y-axis: Industry
X-axis: # of ppl (category: avg job duration)

Table schema:
Avg job duration (year) | selected_industry_1 | selected_industry_2 | selected_industry_N
        1               |           30%        |         10%        |         20%
        2               |           10%        |         5%         |         60%
                                            .
                                            .
                                            .
        n               |           1%         |          2%        |          1%
"""
def gen_chart_7(industries=None):
    """
    How I process the dataset:
    groupby industry to get all records who worked in that industry
    groupby resume to get duration that person stayed in that industry
    sort in start_date descending order 
    first record end_date - last record start_date = duration stayed in that industry
    """
    if industries == None:
        industries = get_top_n()

    industry_groupby = df.groupby("industry")
    
    chart_7_df = defaultdict(lambda :defaultdict(int))
    for selected_industry, ind_grp in industry_groupby.groups.items():

        # process the selected industries
        if selected_industry in industries:
            all_resume_ids = df[df.index.isin(ind_grp)] # all ppl who was/currently in this industry

            # total ppl currently in selected industry
            total_ppl_in_industry = all_resume_ids[all_resume_ids["end_date_new"] == dt.datetime.now().date()]["resume"].unique().shape[0]

            resume_groupby = all_resume_ids.groupby("resume")
            for res_id, job_hists in resume_groupby:
                job_hists = job_hists[job_hists["end_date_new"] == dt.datetime.now().date()]

                # if shape[0] == 0, this person is no longer in the industry
                if job_hists.shape[0] == 0:
                    continue
                job_hists = job_hists.sort_values("start_date_new", ascending=False).reset_index(drop=True)
                
                # the duration that person stayed in this industry = end date of latest job - start date of first job
                duration = job_hists.iloc[0, 5].year - job_hists.iloc[-1, 4].year
                # average job duration = total duration / total jobs taken
                avg_duration = int(duration / job_hists.shape[0])
                # increase count of this avg job duration
                chart_7_df[selected_industry][avg_duration] += 1

            # normalise counts into percentage
            for year in chart_7_df[selected_industry]:
                chart_7_df[selected_industry][year] = round(chart_7_df[selected_industry][year] / total_ppl_in_industry*100, 2)

    chart_7_df = pd.DataFrame(chart_7_df)
    chart_7_df.fillna(0, inplace=True)
    # print([chart_7_df.loc[:, chart_7_df.columns.values].sum()])
    chart_7_df.index.name = 'avg_duration'
    return chart_7_df.sort_index()
