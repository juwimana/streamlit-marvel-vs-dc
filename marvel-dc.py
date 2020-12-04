import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import datetime
import streamlit as st 

st.set_page_config(page_title='Marvel-DC Analysis', page_icon='🦸🏿‍♂️')


st.title("Marvel vs. DC Analysis")


@st.cache(allow_output_mutation=True)
def load_data():
	movies = pd.read_csv("https://raw.githubusercontent.com/juwimana/Web-Scraping/master/Marvel_DC.csv")
	return movies


movies = load_data()
show_data = st.beta_expander(f"Marvel-DC Dataset",expanded=True)
show_data.dataframe(movies)


#Formart Release Year
movies["Release Year"] = movies["Release Year"].apply(lambda x:\
						 datetime.datetime.strptime(str(x),"%Y").year)


summary_average = st.beta_expander(f"Summary Average Rating and Running Time by Universe", expanded=False)
summary_average.write(movies.groupby(["Universe"])[["IMDB Rating", "Metascore",\
						"Running Time (minutes)"]].agg(np.mean))


st.subheader("Filter:")
feature = st.selectbox("Feature:", ("IMDB Rating","Metascore",\
		   "Running Time (minutes)", "Domestic Revenue"))
year = st.number_input("Year:", min_value=movies["Release Year"].min(),\
	   max_value=movies["Release Year"].max(), value=2010, step=1)


average_bar_plot =st.beta_expander(f"{year} Average {feature}",expanded=False) 
fig, ax = plt.subplots(figsize = (20,10))
ax = movies[movies["Release Year"]==year].groupby(["Universe"])\
 					[feature].agg(np.mean).plot(kind = "barh")
average_bar_plot.pyplot(fig)


df = movies[["Release Year","Title","IMDB Rating","Metascore","Domestic Revenue",\
			"Universe", "Running Time (minutes)"]]
df_marvel = df[df["Universe"]=="Marvel"]
df_marvel = df_marvel.drop(columns="Universe")
df_marvel = df_marvel.groupby("Release Year").agg(np.mean)
df_dc = df[df["Universe"]=="DC"]
df_dc = df_dc.drop(columns="Universe")
df_dc = df_dc.groupby("Release Year").agg(np.mean)


trend_over_time = st.beta_expander(f"Comparing DC and Marvel {feature} Trend Over Time",expanded=False)
fig1, ax1 = plt.subplots(figsize = (20,10))
ax1.plot(df_marvel[feature],color="red", alpha=1.5,label="Marvel")
ax1.plot(df_dc[feature],color="blue",label="DC")
ax1.legend(loc="best")
trend_over_time.pyplot(fig1)


count_movies_by_year_marvel = df[df["Universe"]=="Marvel"]
count_movies_by_year_marvel = count_movies_by_year_marvel.drop(\
							   columns="Universe")[["Release Year",\
                               "Title"]].groupby("Release Year").count()
count_movies_by_year_marvel = count_movies_by_year_marvel.rename(\
							  columns={"Title":"Count"})

count_movies_by_year_dc = df[df["Universe"]=="DC"]
count_movies_by_year_dc = count_movies_by_year_dc.drop(\
						  columns="Universe")[["Release Year",\
                          "Title"]].groupby("Release Year").count()
count_movies_by_year_dc = count_movies_by_year_dc.rename(columns={\
						  "Title":"Count"})


total_movies_universe = st.beta_expander("Comparing Total Number of Movies by Universe since {}".format(movies["Release Year"].min()),expanded=False)
fig_count_movies, ax_count_movies = plt.subplots(figsize=(20,10))
ax_count_movies.plot(count_movies_by_year_marvel,color="#cf2213",label="Marvel")
ax_count_movies.plot(count_movies_by_year_dc,color="#000000",label="DC")
ax_count_movies.legend(loc="best")
ax_count_movies.set_xlabel("Year")
ax_count_movies.set_ylabel("Count")
total_movies_universe.pyplot(fig_count_movies)


universe = st.selectbox("Universe", ("DC", "Marvel"))
top_5 = st.beta_expander(f"{universe} Top 5 Highest Domestic Revenue Movies", expanded=False)
highest_gross=df[df["Universe"]==universe].sort_values(by="Domestic Revenue",\
			   ascending=False).head(5)
highest_gross["Domestic Revenue"] = highest_gross["Domestic Revenue"]\
			   .apply(lambda x: "${:,.0f}".format(x))
top_5.dataframe(highest_gross.sort_values(by="Domestic Revenue",\
		 ascending=False).set_index('Release Year'))


most_appearances = st.beta_expander(f"{universe} Most Appearances by an Actor",expanded=False)
#Most appearance in Marvel movies in a star role
df_stars = pd.concat([movies[movies["Universe"]==universe]["Stars"].str.split(",",expand=True)[0],\
		   movies[movies["Universe"]==universe]["Stars"].str.split(",",expand=True)[1]\
		   ,movies[movies["Universe"]==universe]["Stars"].str.split(",",expand=True)[2]],axis=0)
df_stars = df_stars.str.strip()


#Plot
fig_appearances_marvel, ax_appearances_marvel = plt.subplots(figsize=(14,6))
ax = df_stars.value_counts(sort=True).nlargest(10).plot(kind='barh',color="#CB4335" )
plt.gca().invert_yaxis()
plt.ylabel(f"{universe} Actor")
plt.xlabel(f"Number of Appearances in the {universe} Universe")
plt.title(f"Top Ten Actors in the {universe} Universe by Number of Appearances")
for i in ax.patches:
    # get_width pulls left or right; get_y pushes up or down
    ax.text(i.get_width()+.1, i.get_y()+.31, \
            str(round((i.get_width()), 10)), fontsize=10.5, color="#34495E")
most_appearances.pyplot(fig_appearances_marvel)


top_grossing = st.beta_expander(f"Top Grossing Movie by Year")
top_gross_by_year = df[df.groupby("Release Year")["Domestic Revenue"].transform(max)\
                       == df['Domestic Revenue']].sort_values(by = "Release Year",ascending =False)
top_gross_by_year["Domestic Revenue"] = top_gross_by_year["Domestic Revenue"].apply(lambda x:\
                                                                                    "${:,.0f}".format(x))
top_gross_by_year =  top_gross_by_year.reset_index(drop=True, inplace=False)
top_grossing.dataframe(top_gross_by_year.set_index('Release Year').head(32))




