import pandas as pd
import matplotlib.pyplot as plt


def prepare_plot(df):
    df_clean = df.dropna().reset_index()
    df_clean["Industry"] = df_clean["Industry"].str.slice(start = 11)
    df_sum = df_clean.groupby("Industry").sum().reset_index()
    df_sum = df_sum[1:]
    
    df_sum_100 = df_sum.sort_values(by="Number of Applicants", ascending=False)
    df_sum_100 = df_sum_100[df_sum_100["Number of Applicants"] > 150]
    plt.barh(df_sum_100["Industry"], df_sum_100["Number of Applicants"])
    bar_width = 5 
    plt.title("number of applicants")

    df_count = df_clean.groupby("Industry").count().reset_index()
    df_count = df_count[1:]
    df_count_5 = df_count.sort_values(by="Row Number", ascending=False)
    df_count_5 = df_count_5[df_count_5["Row Number"] > 5]
    plt.barh(df_count_5["Industry"], df_count_5["Row Number"])
    bar_width = 5 
    plt.title("number of opening")

    column = ["Industry", "Number of Applicants", "Opening number"]
    df_combine = pd.concat([df_sum["Industry"], df_sum["Number of Applicants"], df_count["Row Number"]], axis=1)
    df_combine.columns = column
    df_combine["ratio"] = df_combine["Number of Applicants"] / df_combine["Opening number"]
    df_combine = df_combine.sort_values(by="ratio")
    df_ratio = df_combine[df_combine["ratio"] == min(df_combine["ratio"])]
    dic = df_ratio.set_index("Industry")["ratio"].to_dict()
    print(dic)




