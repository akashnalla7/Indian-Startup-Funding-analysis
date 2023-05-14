import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("startup_cleaned.csv")

df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['year'] = df['date'].dt.year

# extracting month from date column
df['month'] = df['date'].dt.month

st.set_page_config(layout='wide')

def load_overall_analysis():

    st.title("Overall Analysis")
    col1,col2,col3,col4 = st.columns(4)
    

    with col1:
        # Total Investment
        total = round(df['amount'].sum())
        st.metric('Total (in Cr)', total )
    with col2:
        # Highest Investment
        max = df.groupby('startup')['amount'].max().sort_values(ascending = False).head(1)
        st.metric('Max (in Cr)', max.values[0] , max.index[0])
    with col3:
        # Avg funding
        avg_funding = round(df.groupby('startup')['amount'].sum().mean())
        st.metric("Avg Funding(in Cr)",avg_funding)
    with col4:
        # No. of startups funded
        n_startups = df['startup'].nunique()
        st.metric("Total Startups",n_startups)

    # month on month graphs
    st.subheader('Month on Month Graph')
    mom_bnt = st.selectbox('Select Type',['Total','Count'])
    
    #Total no.of startups by month on month
    if mom_bnt == 'Total':
        temp_df = df.groupby(['year','month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year','month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig , ax = plt.subplots(figsize=(10,5))
    ax.plot(temp_df['x_axis'],temp_df['amount'])
    ax.set_xlabel('Year')
    #ax.set_ylabel('Total No. of Startups')
    st.pyplot(fig)
    


def load_inverstor_details(investor):
    st.title(investor)
    # loading the Top 5 recent investments
    st.subheader('Most Recent Investments')
    top5_df = df[df['Investors'].str.contains(investor)].head()[['date','startup','vertical','City  Location','round','amount']]
    st.dataframe(top5_df)


    col1 , col2 = st.columns(2)
    with col1:
        # loading the Biggest investments
        st.subheader('Biggest Investments')
        big_df = df[df['Investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending = False).head()


        fig , ax = plt.subplots(figsize=(5,4))
        plot = ax.bar(big_df.index,big_df.values)
        ax.set_xlabel('StartUps')
        ax.set_ylabel('Amount (Cr)')
        ax.bar_label(plot,big_df.values)
        st.pyplot(fig)

    with col2:
        st.subheader('Sectors Invested in')
        vertical_series = df[df['Investors'].str.contains(investor)].groupby('vertical')['amount'].sum()

        fig1 , ax1 = plt.subplots(figsize=(3,5))
        plot = ax1.pie(vertical_series,labels=vertical_series.index,autopct='%0.01f%%')
        st.pyplot(fig1)

    col1 , col2 = st.columns(2)
    with col1:
        
        st.subheader('City')
        city_series = df[df['Investors'].str.contains(investor)].groupby('City  Location')['amount'].sum()

        fig2 , ax2 = plt.subplots(figsize=(3,5))
        plot = ax2.pie(city_series,labels=city_series.index,autopct='%0.01f%%')
        st.pyplot(fig2)

    with col2:
        st.subheader('Stage')
        stage_series = df[df['Investors'].str.contains(investor)].groupby('round')['amount'].sum()

        fig3 , ax3 = plt.subplots(figsize=(3,5))
        plot = ax3.pie(stage_series,labels=stage_series.index,autopct='%0.01f%%')
        st.pyplot(fig3)

    # Year on Year line Plot
    

    st.subheader('Year on Year Investments')
    yoy_df = df[df['Investors'].str.contains(investor)].groupby('year')['amount'].sum()


    fig4 , ax4 = plt.subplots(figsize=(10,5))
    plot = ax4.plot(yoy_df.index,yoy_df.values)
    ax4.set_xlabel('Year')
    ax4.set_ylabel('Amount (Cr)')
    
    st.pyplot(fig4)


st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','StartUp','Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'StartUp':
    st.sidebar.selectbox('Select StartUp',sorted(df["startup"].unique().tolist()))
    st.title("StartUp Analysis")
    btn1 = st.sidebar.button("Find StartUp Details")

else:
    seleted_investor = st.sidebar.selectbox('Select Investor',sorted(set(df["Investors"].str.split(',').sum())))
    st.title("Inveator Analysis")
    btn2 = st.sidebar.button("Find Investor Details")
    if btn2:
        load_inverstor_details(seleted_investor)