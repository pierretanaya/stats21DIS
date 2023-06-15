import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import io
import seaborn as sns

web_apps = st.sidebar.selectbox("Select Web Apps",
                                ("Exploratory Data Analysis", "Distributions"))


if web_apps == "Exploratory Data Analysis":

  uploaded_file = st.sidebar.file_uploader("Choose a file")

  if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file)
    show_df = st.checkbox("Show Data Frame", key="disabled")

    if show_df:
      st.write(df)
      st.write('Number of columns:', len(df.columns))
      st.write('Number of rows:', df[df.columns[1]].count())

      dtypes = df.dtypes
      num_numerical_vars = dtypes[(dtypes == 'int64') | (dtypes == 'float64')].count()
      st.write("Number of numerical variables:", num_numerical_vars)

      num_categorical_vars = dtypes[dtypes == 'object'].count()
      st.write("Number of categorical variables:", num_categorical_vars)

      num_boolean_vars = dtypes[dtypes == 'bool'].count()
      st.write("Number of boolean variables:", num_boolean_vars)
      

    column_type = st.sidebar.selectbox('Select Data Type',
                                       ("Numerical", "Categorical", "Bool", "Date"))

    if column_type == "Numerical":
      numerical_column = st.sidebar.selectbox(
          'Select a Column', df.select_dtypes(include=['int64', 'float64']).columns)


      # histogram
      choose_color = st.color_picker('Pick a Color', "#69b3a2")
      choose_opacity = st.slider(
          'Color Opacity', min_value=0.0, max_value=1.0, step=0.05)

      hist_bins = st.slider('Number of bins', min_value=5,
                            max_value=150, value=30)
      hist_title = st.text_input('Set Title', 'Histogram')
      hist_xtitle = st.text_input('Set x-axis Title', numerical_column)

      fig, ax = plt.subplots()
      ax.hist(df[numerical_column], bins=hist_bins,
              edgecolor="black", color=choose_color, alpha=choose_opacity)
      ax.set_title(hist_title)
      ax.set_xlabel(hist_xtitle)
      ax.set_ylabel('Count')

      st.pyplot(fig)
      filename = "plot.png"
      fig.savefig(filename,dpi = 300)

      # Display the download button
      with open("plot.png", "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name="flower.png",
            mime="image/png"
        )
      
      st.write("Count:", int(df[numerical_column].describe()[0]))
      st.write("Mean:", int(df[numerical_column].describe()[1]))
      st.write("Standard Deviation:", int(df[numerical_column].describe()[2]))
      st.write("Minimum:", int(df[numerical_column].describe()[3]))
      st.write("25th percentile:", int(df[numerical_column].describe()[4]))
      st.write("50th percentile:", int(df[numerical_column].describe()[5]))
      st.write("75th percentile:", int(df[numerical_column].describe()[6]))
      st.write("Maximum:", int(df[numerical_column].describe()[7]))
    
    
    if column_type == "Categorical":
      categorical_column = st.sidebar.selectbox(
                'Select a Column', df.select_dtypes(include=['object']).columns)
       
      column_data = df[categorical_column]

      category_counts = column_data.value_counts(normalize=True)

      proportions_table = pd.DataFrame({'Proportion': category_counts})
      st.write("Proportions of Each Category Level:")
      st.write(proportions_table)

      plt.figure(figsize=(8, 6))
      sns.countplot(data=df, x=categorical_column)
      plt.title("Bar Plot of " + categorical_column)
      plt.xlabel(categorical_column)
      plt.ylabel("Count")
      plt.xticks(rotation=45)
      
      fig = plt.gcf()
      st.pyplot(fig)
