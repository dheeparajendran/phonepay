import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image

#STREAMLIT PART

#SQL connection

mydb = psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="guvi2024")

cursor=mydb.cursor()


st.set_page_config(layout="wide")

st.title(":orange[PHONEPE DATA VISUALIZATION AND EXPLORATION]")

selected = option_menu(None,
                       options = ["ABOUT","HOME","ANALYSIS","INSIGHTS"],
                       icons = ["bar-chart","house","toggles","at"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"container": {"width": "100%"},
                               "icon": {"color": "white", "font-size": "24px"},
                               "nav-link": {"font-size": "24px", "text-align": "center", "margin": "-2px"},
                               "nav-link-selected": {"background-color": "#6F36AD"}})
# ABOUT TAB

if selected == "ABOUT":

    col1, col2, = st.columns(2)
    
    st.image(r"C:/Users/user/OneDrive/Desktop/app_download_for_merchants_web-2x.png")
        
    with col1:
        st.subheader("PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
        
        st.download_button("Download PhonePe for Business","C:/Users/user/OneDrive/Desktop/download2.png")

    with col2:
        st.image("C:/Users/user/OneDrive/Desktop/Insurance-Data-On-Pulse-v2.1.webp")

# HOME TAB

if selected == "HOME":

    col1,col2 = st.columns(2)

    with col1:
          st.image("C:/Users/user/OneDrive/Desktop/spotlight_2.png", width=500)

    with col2:
        st.title(':violet[PHONEPE PULSE DATA VISUALISATION]')
        st.subheader(':violet[Phonepe Pulse]:')
        st.write('PhonePe Pulse is a feature offered by the Indian digital payments platform called PhonePe.PhonePe Pulse provides users with insights and trends related to their digital transactions and usage patterns on the PhonePe app.')
        st.subheader(':violet[Phonepe Pulse Data Visualisation]:')
        st.write('Data visualization refers to the graphical representation of data using charts, graphs, and other visual elements to facilitate understanding and analysis in a visually appealing manner.'
                 'The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.')
        st.markdown("## :violet[Done by] : dheepa R")


# ANALYSIS TAB

if selected == "ANALYSIS":

    st.title(':violet[ANALYSIS]')
    st.subheader('Analysis done on the basis of All India, States, and Top categories between 2018 and 2022')
    select = option_menu(None,
                         options=["AGGREGATE ANALYSIS", "MAP ANALYSIS", "TOP ANALYSIS"],
                         default_index=0,
                         orientation="horizontal",
                         styles={"container": {"width": "100%"},
                                 "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px"},
                                 "nav-link-selected": {"background-color": "#6F36AD"}})

    if select == "AGGREGATE ANALYSIS":

        tab1, tab2 = st.tabs(["Transaction Analysis", "User Analysis"])

        with tab1:
            
            col1, col2, col3 = st.columns(3)

            with col1:
                transaction_year = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022','2023'), key='transaction_year')

            with col2:
                transaction_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='transaction_qtr')

            with col3:
                transaction_type = st.selectbox('**Select Transaction type**',
                                                ('Recharge & bill payments', 'Peer-to-peer payments',
                                                'Merchant payments', 'Financial Services', 'Others'), key='transaction_type')

            
            # SQL Query

            # Transaction Analysis bar chart query for transaction amount
                
            cursor.execute(
                f"SELECT states, transaction_amount FROM aggregate_transaction "
                f"WHERE years = '{transaction_year}' "
                f"AND quarter = '{transaction_qtr}' "
                f"AND transaction_type = '{transaction_type}';"
            )

            in_tr_tab_qry_rslt = cursor.fetchall()

            df_in_tr_tab_qry_rslt_amount= pd.DataFrame(in_tr_tab_qry_rslt, columns=['State', 'Transaction_amount'])
            

        # Transaction Analysis bar chart query for transaction count

            cursor.execute(
                    f"SELECT states, transaction_count FROM aggregate_transaction "
                    f"WHERE years = '{transaction_year}' "
                    f"AND quarter = '{transaction_qtr}' "
                    f"AND transaction_type = '{transaction_type}';"
                )

            in_tr_tab_qry_rslt = cursor.fetchall()

            df_in_tr_tab_qry_rslt_count = pd.DataFrame(in_tr_tab_qry_rslt, columns=['State','Transaction_count'])
            
        # Transaction Analysis table query

            cursor.execute(
                f"SELECT states, transaction_count, transaction_amount FROM aggregate_transaction "
                f"WHERE years = '{transaction_year}' "
                f"AND quarter = '{transaction_qtr}' "
                f"AND transaction_type = '{transaction_type}';"
            )

            in_tr_anly_tab_qry_rslt = cursor.fetchall()

            df_in_tr_anly_tab_qry_rslt = pd.DataFrame(in_tr_anly_tab_qry_rslt,columns=['State', 'Transaction_count', 'Transaction_amount'])
            

            data1grp=df_in_tr_anly_tab_qry_rslt.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
            data1grp.reset_index(inplace=True)
            

            #GEO VISUALIZATION

            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response=requests.get(url)
            states_name = []
            data=json.loads(response.content)

            # Extract state names and sort them in alphabetical order

            state_names_tra = [feature['properties']['ST_NM'] for feature in data['features']]
            state_names_tra.sort()

            # Create a DataFrame with the state names column

            df_state_names_tra = pd.DataFrame({'State': state_names_tra})
            df_state_names_tra['Transaction_amount'] = df_in_tr_tab_qry_rslt_amount['Transaction_amount']
            df_state_names_tra['Transaction_count'] = df_in_tr_tab_qry_rslt_count['Transaction_count']


            fig_india = px.choropleth( df_state_names_tra,
                                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                    featureidkey='properties.ST_NM', locations='State', color='Transaction_amount',
                                    color_continuous_scale='thermal', title='Transaction Amount Analysis' )

            fig_india.update_geos(visible= False)

            fig_india.update_layout(title_font=dict(size=33), title_font_color='#AD71EF',height=800,geo=dict(
                                    center=dict(lon=78, lat=23),projection_scale=5))      # Increase the scale for a larger map
            st.plotly_chart(fig_india, use_container_width=True)
    

            fig_india1= px.choropleth(df_state_names_tra,
                                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                    featureidkey='properties.ST_NM', locations='State', color='Transaction_count',
                                    color_continuous_scale='rainbow', title='Transaction Count Analysis')

            fig_india1.update_geos(visible= False)

            fig_india1.update_layout(title_font=dict(size=33), title_font_color='#AD71EF',height=800,
                                    geo=dict(center=dict(lon=78, lat=23),projection_scale=5))      # Increase the scale for a larger map)
            st.plotly_chart(fig_india1, use_container_width=True)

            # ---------   /   All India Transaction Analysis Bar chart  /  ----- #

                        
            fig_amount=px.bar(data1grp, x= "State", y="Transaction_amount", title = "TRANSACTION AMOUNT",
                            color='Transaction_amount',height=700,color_continuous_scale='thermal')
            
            fig_amount.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(fig_amount, use_container_width=True)


            fig_count=px.bar(data1grp, x= "State", y="Transaction_count", title = "TRANSACTION COUNT",color='Transaction_count',
                            height=700,color_continuous_scale='rainbow')

            fig_count.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(fig_count, use_container_width=True)


        with tab2:
            col1, col2 = st.columns(2)
            # Your code for tab2

            with col1:
                trans_year = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022', '2023'), key='trans_year')

            with col2:
                transaction_qtr1 = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='transaction_qtr1')

                
            cursor.execute(f"SELECT states, Sum(transaction_count) as user_count FROM aggregate_user WHERE years = '{transaction_year}' AND quarter = '{transaction_qtr}' group by states;")

            in_us_tab_qry_rslt = cursor.fetchall()

            df_in_us_tab_qry_rslt = pd.DataFrame(in_us_tab_qry_rslt, columns=['State', 'User Count'])

            df_in_us_tab_qry_rslt1 = df_in_us_tab_qry_rslt.set_index(pd.Index(range(1, len(df_in_us_tab_qry_rslt) + 1)))

            # GEO VISUALIZATION FOR USER
            
            # Drop a State column from df_in_us_tab_qry_rslt
            df_in_us_tab_qry_rslt.drop(columns=['State'], inplace=True)

            # Clone the gio data
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data2 = json.loads(response.content)

            # Extract state names and sort them in alphabetical order
            state_names_use = [feature['properties']['ST_NM'] for feature in data2['features']]
            state_names_use.sort()

            # Create a DataFrame with the state names column
            df_state_names_use = pd.DataFrame({'State': state_names_use})

            # Combine the Gio State name with df_in_tr_tab_qry_rslt
            df_state_names_use['User Count'] = df_in_us_tab_qry_rslt

            df_state_names_use.to_csv('State_user.csv', index=False)

            # Read csv
            df_use = pd.read_csv('State_user.csv')

            # Geo plot
            fig_use = px.choropleth(
                df_use,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM', locations='State', color='User Count',
                color_continuous_scale='thermal', title='User Analysis')

            fig_use.update_geos(fitbounds="locations", visible=False)
            fig_use.update_layout(title_font=dict(size=33), title_font_color='#AD71EF', height=800)
            st.plotly_chart(fig_use, use_container_width=True)

            # ----   /   All India User Analysis Bar chart   /     -------- #

            df_in_us_tab_qry_rslt1['State'] = df_in_us_tab_qry_rslt1['State'].astype(str)
            df_in_us_tab_qry_rslt1['User Count'] = df_in_us_tab_qry_rslt1['User Count'].astype(int)

            df_in_us_tab_qry_rslt1_fig = px.bar(df_in_us_tab_qry_rslt1, x='State', y='User Count', color='User Count',
                                                color_continuous_scale='rainbow', title='User Analysis Chart',
                                                height=700 )

            df_in_us_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(df_in_us_tab_qry_rslt1_fig, use_container_width=True)
            
            col1,col2,col3 =st.columns(3)
            with col1:
                    states_tran = st.selectbox('**Select State**', (
                    'Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                    'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                    'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                    'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                    'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                    'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                    'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                    'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                    'Uttarakhand', 'West Bengal'), key='states_tran')
            
            
            with col2:
                    trans_year_pie = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022', '2023'), key='trans_year_pie')

            with col3:
                    transaction_qtr_pie = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='transaction_qtr_pie')

                        
            cursor.execute(f"SELECT DISTINCT brands, years,percentage,transaction_count FROM aggregate_user "
               f"WHERE years = {trans_year_pie} "
               f"AND quarter = {transaction_qtr_pie} "
               f"AND states = '{states_tran}';")

            brands_data = cursor.fetchall()
            df_brands = pd.DataFrame(brands_data, columns=['Brand', 'Year','Percentage','Transaction_count'])
            brand_counts = df_brands['Brand'].value_counts()

            # Plot the pie chart
            #distribution of transaction counts across different brands.
            fig_brand = px.pie(df_brands, values='Transaction_count', names='Brand', title='Transaction Count by Brand', hole=0.5)
            fig_brand.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(fig_brand)


    
    elif select == "MAP ANALYSIS":

        tab1, tab2 = st.tabs(["Transaction Analysis", "User Analysis"])
        
        with tab1:
            col1, col2, col3 = st.columns(3)  

            with col1:
                states_tran = st.selectbox('**Select State**', (
                'Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                'Uttarakhand', 'West Bengal'), key='states_tran')

            with col2:
                transaction_year = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='transaction_year')

            with col3:
                transaction_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='transaction_qtr')
             
            cursor.execute(f"SELECT districts, transaction_amount,transaction_count FROM map_transaction "
               f"WHERE states = '{states_tran}' "
               f"AND years = '{transaction_year}' "
               f"AND quarter = '{transaction_qtr}';")

            st_map_tab_bar_qry_rslt = cursor.fetchall()

            # Create a DataFrame from the fetched data

            df_map_tr_bar_qry_rslt_amount = pd.DataFrame(st_map_tab_bar_qry_rslt, columns=['Districts', 'Transaction_amount','Transaction_count'])


            df_st_tr_tab_bar_qry_rslt1_fig = px.bar(df_map_tr_bar_qry_rslt_amount, x='Transaction_amount',
                                                    y='Districts', color='Transaction_amount',
                                                    title= " DISTRICTS AND TRANSACTION AMOUNT", 
                                                    color_continuous_scale='sunset')
            
            df_st_tr_tab_bar_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(df_st_tr_tab_bar_qry_rslt1_fig, use_container_width=True)
            


            df_st_tr_tab_bar_qry_rslt1_fig1 = px.bar(df_map_tr_bar_qry_rslt_amount, x='Transaction_count',
                                                    y='Districts', color='Transaction_count',
                                                    title= "DISTRICTS AND TRANSACTION COUNT", 
                                                    color_continuous_scale='magma')
            
            df_st_tr_tab_bar_qry_rslt1_fig1.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(df_st_tr_tab_bar_qry_rslt1_fig1, use_container_width=True)
           
                        
        with tab2:
            col1, col2= st.columns(2)

            with col1:
                trans_year_user = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022', '2023'), key='trans_year_user')
                
            with col2:
                transaction_qtr1_user = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='transaction_qtr1_user')

            cursor.execute(f"SELECT states, registeredusers, appopens FROM map_user "
               f"WHERE years = {trans_year_user} "
               f"AND quarter = {transaction_qtr1_user};")

            
            st_map_tab_bar_qry_rslt = cursor.fetchall()

            df_map_appopens = pd.DataFrame(st_map_tab_bar_qry_rslt, columns=['States','RegisteredUsers',"AppOpens"])
            
            mpur_grp = df_map_appopens.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
            mpur_grp.reset_index(inplace= True)


            fig_line_1 = px.line( mpur_grp, x="States" ,y=["RegisteredUsers","AppOpens"],
                                title= "REGISTERED USER AND APPOPENS",width=1000,height = 800,markers= True,
                                color_discrete_sequence=px.colors.qualitative.Dark24_r)
            
            fig_line_1.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(fig_line_1, use_container_width=True)


    elif select == "TOP ANALYSIS":

        tab1, tab2 = st.tabs(["Transaction Analysis", "User Analysis"])
        
        with tab1:
            col1, col2, col3 = st.columns(3)

            with col1:
                states_tran = st.selectbox('**Select State**', (
                'Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                'Uttarakhand', 'West Bengal'), key='states_tran')

            with col2:
                transaction_year = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='transaction_year')

            with col3:
                
                transaction_qtr1_user = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='transaction_qtr1_user')

            #Top Transaction Analysis bar chart query
            cursor.execute(
                f"SELECT states, quarter,pincodes, transaction_count, transaction_amount FROM top_transaction "
                f"WHERE states = '{states_tran}' "
                f"AND years = '{transaction_year}';"
            )

            
            top_tr_tab_qry_rslt = cursor.fetchall()

            df_top_transaction= pd.DataFrame( top_tr_tab_qry_rslt, columns=['States','Quarter',"Pincodes","Transaction_count","Transaction_amount"])

            tiyg=df_top_transaction.groupby("Pincodes")[["Transaction_count","Transaction_amount"]].sum()
            tiyg.reset_index(inplace= True)

                    
            fig_top_tran_bar_1 = px.bar(df_top_transaction,x= "Quarter",y= "Transaction_amount",hover_data= "Pincodes",
                                title= "TRANSACTION AMOUNT",width=1000,color_discrete_sequence=px.colors.sequential.Magenta_r)
            
            fig_top_tran_bar_1.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart( fig_top_tran_bar_1)


            fig_Map_insur_bar_2 = px.bar(df_top_transaction,x= "Quarter",y= "Transaction_count",hover_data= "Pincodes",
                                    title= "TRANSACTION COUNT",width=1000,color_discrete_sequence=px.colors.sequential.Inferno_r)
            
            fig_Map_insur_bar_2.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(fig_Map_insur_bar_2)


                    
        with tab2:
            col1, col2 = st.columns(2)

            with col1:
                trans_year = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022', '2023'), key='trans_year')
            
            #Top User Analysis bar chart query
            cursor.execute(
                f"SELECT states, quarter, pincodes, registeredusers FROM top_user "
                f"WHERE years = '{trans_year}'; "
            )

            top_us_tab_qry_rslt = cursor.fetchall()

            df_top_user = pd.DataFrame(top_us_tab_qry_rslt, columns=['States', 'Quarter', 'Pincodes', 'RegisteredUsers'])

            # Group by States and Quarter and sum the RegisteredUsers
            trtusr_grp = df_top_user.groupby(["States", "Quarter"])["RegisteredUsers"].sum().reset_index()

            # Plot the first bar chart
            fig_top_plot1 = px.bar(df_top_user, x="States", y="RegisteredUsers", color="Quarter",
                                    title="REGISTERED USERS", width=1000, height=800,
                                    color_continuous_scale=px.colors.sequential.Pinkyl)
            
            
            fig_top_plot1.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(fig_top_plot1)

            # Plot the second bar chart
            fig_top_plot_2 = px.bar(df_top_user, x="Quarter", y="RegisteredUsers", title="REGISTERED USERS, PINCODES, QUARTER",
                                    width=1000, height=800, color="RegisteredUsers", hover_data="Pincodes",
                                    color_continuous_scale=px.colors.sequential.Magma)
            
            
            fig_top_plot_2.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(fig_top_plot_2)



#SQL connection

mydb = psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="guvi2024")

cursor=mydb.cursor()

#aggregate_Transaction DF

cursor.execute("select * from aggregate_transaction")
mydb.commit()
table2=cursor.fetchall()

Aggr_transaction=pd.DataFrame(table2,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))


#aggregate_user DF

cursor.execute("select * from aggregate_user")
mydb.commit()
table3=cursor.fetchall()

Aggr_user=pd.DataFrame(table3,columns=("States","Years","Quarter","Brands","Transaction_count","Percentage"))


#Map transaction DF

cursor.execute("select * from map_transaction")
mydb.commit()
table5=cursor.fetchall()

map_transaction=pd.DataFrame(table5,columns=("States","Years","Quarter","District","Transaction_count","Transaction_amount"))


#Map User DF

cursor.execute("select * from map_user")
mydb.commit()
table6=cursor.fetchall()

map_user=pd.DataFrame(table6,columns=("States","Years","Quarter","District","RegisteredUsers","AppOpens"))


#Top transaction DF

cursor.execute("select * from top_transaction")
mydb.commit()
table8=cursor.fetchall()

top_transaction=pd.DataFrame(table8,columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))


#Top user DF

cursor.execute("select * from top_user")
mydb.commit()
table9=cursor.fetchall()

top_user=pd.DataFrame(table9,columns=("States","Years","Quarter","Pincodes","RegisteredUsers"))

#SQL connection

def top_chart_transaction_amount(table_name):
    mydb = psycopg2.connect(host="localhost",
                                user="postgres",
                                port="5432",
                                database="phonepe_data",
                                password="guvi2024")

    cursor=mydb.cursor()


#plot 1

    query1 = f'''select states,sum(transaction_amount) as transaction_amount
                from {table_name}
                group by states 
                order by transaction_amount desc
                limit 10;'''

    cursor.execute(query1)

    table= cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table,columns=("states","transaction_amount"))

    col1,col2 = st.columns(2)
    with col1:

        fig_amount=px.bar(df_1, x="states", y="transaction_amount", title = "TOP 10 OF TRANSACTION AMOUNT",hover_name="states",
                            height=650,width = 600,color_discrete_sequence=px.colors.sequential.Agsunset)
            
        st.plotly_chart(fig_amount)

#plot_2

    query2 = f'''select states,sum(transaction_amount) as transaction_amount
                from {table_name}
                group by states 
                order by transaction_amount 
                limit 10;'''

    cursor.execute(query2)

    table_1= cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_1,columns=("states","transaction_amount"))

    with col2:

        fig_amount_1=px.bar(df_2, x="states", y="transaction_amount", title = "LAST 10 OF TRANSACTION AMOUNT",hover_name="states",
                            height=650,width = 600,color_discrete_sequence=px.colors.sequential.Pinkyl_r)
            
        st.plotly_chart(fig_amount_1)


#plot_3

    query3 = f'''select states,avg(transaction_amount) as transaction_amount
                from {table_name}
                group by states 
                order by transaction_amount;'''

    cursor.execute(query3)

    table_1= cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_1,columns=("states","transaction_amount"))


    fig_amount_2=px.bar(df_3, x="transaction_amount", y="states", title = "AVERAGE OF TRANSACTION AMOUNT",hover_name="states",orientation="h",
                        height=800,width = 900,color_discrete_sequence=px.colors.sequential.Bluered_r)
        
    st.plotly_chart(fig_amount_2)
    
#SQL connection

def top_chart_transaction_count(table_name):
    mydb = psycopg2.connect(host="localhost",
                            user="postgres",
                            port="5432",
                            database="phonepe_data",
                            password="guvi2024")

    cursor=mydb.cursor()

    #plot 1

    query1 = f'''select states,sum(transaction_count) as transaction_count
            from {table_name}
            group by states 
            order by transaction_count desc
            limit 10;'''

    cursor.execute(query1)

    table= cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table,columns=("states","transaction_count"))

    col1,col2 =st.columns(2)
    with col1:

        fig_amount=px.bar(df_1, x="states", y="transaction_count", title = "TOP 10 OF TRANSACTION COUNT",hover_name="states",
                        height=650,width = 600,color_discrete_sequence=px.colors.sequential.Agsunset)
        
        st.plotly_chart(fig_amount)

    #plot_2

    query2 = f'''select states,sum(transaction_count) as transaction_count
            from {table_name}
            group by states 
            order by transaction_count 
            limit 10;'''

    cursor.execute(query2)

    table_1= cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_1,columns=("states","transaction_count"))

    with col2:

        fig_amount=px.bar(df_2, x="states", y="transaction_count", title = "LAST 10 OF TRANSACTION COUNT",hover_name="states",
                        height=650,width = 600,color_discrete_sequence=px.colors.sequential.Pinkyl_r)
        
        st.plotly_chart(fig_amount)


    #plot_3

    query3 = f'''select states,avg(transaction_amount) as transaction_amount
                    from aggregate_transaction
                    group by states 
                    order by transaction_amount;'''

    cursor.execute(query3)

    table_1= cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_1,columns=("states","transaction_count"))

    fig_amount=px.bar(df_3, x="transaction_count", y="states", title = "AVERAGE OF TRANSACTION COUNT",hover_name="states",orientation="h",
                    height=650,width = 600,color_discrete_sequence=px.colors.sequential.Bluered_r)
    
    st.plotly_chart(fig_amount)


#SQL connection

def top_chart_registered_user(table_name,state):
    mydb = psycopg2.connect(host="localhost",
                            user="postgres",
                            port="5432",
                            database="phonepe_data",
                            password="guvi2024")

    cursor=mydb.cursor()

    #plot 1

    query1 = f'''select districts,sum(registeredusers) as registeredusers 
        from {table_name}
        where states='{state}'
        group by districts
        order by registeredusers desc
        limit 10;'''

    cursor.execute(query1)
    table= cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table,columns=("districts","registeredusers"))

    col1,col2 = st.columns(2)
    with col1:

        fig_amount=px.bar(df_1, x="districts", y="registeredusers", title = " TOP 10 OF REGISTERED USERS",hover_name="districts",
                        height=650,width = 600,color_discrete_sequence=px.colors.sequential.Agsunset)
        
        st.plotly_chart(fig_amount)

    #plot_2

    query2 = f'''select districts,sum(registeredusers) as registeredusers 
    from {table_name}
    where states='{state}'
    group by districts
    order by registeredusers 
    limit 10;'''

    cursor.execute(query2)

    table_1= cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_1,columns=("districts","registeredusers"))

    with col2:

        fig_amount=px.bar(df_2, x="districts", y="registeredusers", title = " LAST 10 OF REGISTERED USERS",hover_name="districts",
                        height=650,width = 600,color_discrete_sequence=px.colors.sequential.Tealgrn_r)
        
        st.plotly_chart(fig_amount)


    #plot_3

    query3 = f'''select districts,avg(registeredusers) as registeredusers 
        from {table_name}
        where states='{state}'
        group by districts
        order by registeredusers;'''

    cursor.execute(query3)
    table_1= cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table,columns=("districts","registeredusers"))

    fig_amount=px.bar(df_3, x="registeredusers", y="districts", title = " AVERAGE OF  OF REGISTERED USERS",hover_name="districts",orientation ="h",
                    height=650,width = 600,color_discrete_sequence=px.colors.sequential.Rainbow_r)
    
    st.plotly_chart(fig_amount)

#SQL connection

def top_chart_appopens(table_name,state):
    mydb = psycopg2.connect(host="localhost",
                            user="postgres",
                            port="5432",
                            database="phonepe_data",
                            password="guvi2024")

    cursor=mydb.cursor()

    #plot 1

    query1 = f'''select districts,sum(appopens) as appopens 
        from {table_name}
        where states='{state}'
        group by districts
        order by appopens desc
        limit 10;'''

    cursor.execute(query1)
    table= cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table,columns=("districts","appopens"))

    col1,col2 =st.columns(2)
    with col1:

        fig_amount=px.bar(df_1, x="districts", y="appopens", title = " TOP 10 OF APP OPENS",hover_name="districts",
                        height=650,width = 600,color_discrete_sequence=px.colors.sequential.Agsunset)
        
        st.plotly_chart(fig_amount)

    #plot_2

    query2 = f'''select districts,sum(appopens) as appopens
                from {table_name}
                where states='{state}'
                group by districts
                order by appopens
                limit 10;'''

    cursor.execute(query2)

    table_1= cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_1,columns=("districts","appopens"))

    with col2:
        fig_amount=px.bar(df_2, x="districts", y="appopens", title = " LAST 10 OF APP OPENS",hover_name="districts",
                        height=650,width = 600,color_discrete_sequence=px.colors.sequential.Pinkyl_r)
        
        st.plotly_chart(fig_amount)


    #plot_3

    query3 = f'''select districts,avg(registeredusers) as appopens
        from {table_name}
        where states='{state}'
        group by districts
        order by appopens;'''

    cursor.execute(query3)
    table_1= cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table,columns=("districts","appopens"))

    fig_amount=px.bar(df_3, x="appopens", y="districts", title = " AVERAGE OF  OF APP OPENS",hover_name="districts",orientation ="h",
                    height=650,width = 600,color_discrete_sequence=px.colors.sequential.Bluered_r)
    
    st.plotly_chart(fig_amount)


#SQL connection

def top_chart_registeredusers(table_name):
    mydb = psycopg2.connect(host="localhost",
                            user="postgres",
                            port="5432",
                            database="phonepe_data",
                            password="guvi2024")

    cursor=mydb.cursor()

    #plot 1

    query1 = f'''select states,sum(registeredusers) as registeredusers 
                from {table_name}
                group by states
                order by registeredusers desc
                limit 10;'''


    cursor.execute(query1)
    table= cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table,columns=("states","registeredusers"))

    col1,col2 = st.columns(2)
    with col1:

        fig_amount=px.bar(df_1, x="states", y="registeredusers", title = " TOP 10 OF REGISTERED USERS",hover_name="states",
                        height=650,width = 600,color_discrete_sequence=px.colors.sequential.Agsunset)
        
        st.plotly_chart(fig_amount)

    #plot_2

    query2 = f'''select states,sum(registeredusers) as registeredusers 
                from {table_name}
                group by states
                order by registeredusers 
                limit 10;'''

    cursor.execute(query2)

    table_1= cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_1,columns=("states","registeredusers"))

    with col2:

        fig_amount=px.bar(df_2, x="states", y="registeredusers", title = " LAST 10 OF REGISTERED USERS",hover_name="states",
                        height=650,width = 600,color_discrete_sequence=px.colors.sequential.Pinkyl_r)
        
        st.plotly_chart(fig_amount)


    #plot_3

    query3 = f'''select states,avg(registeredusers) as registeredusers 
                from {table_name}
                group by states
                order by registeredusers;'''

    cursor.execute(query3)
    table_1= cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table,columns=("states","registeredusers"))

    fig_amount=px.bar(df_3, x="registeredusers", y="states", title = " AVERAGE OF REGISTERED USERS",hover_name="states",orientation="h",
                    height=650,width = 600,color_discrete_sequence=px.colors.sequential.Bluered_r)
    
    st.plotly_chart(fig_amount)



if selected =="INSIGHTS":

    st.title(':violet[BASIC INSIGHTS]')
    st.subheader(":violet[The basic insights are derived from the Analysis of the Phonepe Pulse data. It provides a clear idea about the analysed data.]")

    question = st.selectbox("Select the Question",["1.Transaction Amount of Aggregated Transaction",
                                                "2.Transaction Amount  of Map Transaction",
                                                "3.Transaction Amount  of Top Transaction",
                                                "4.Transaction Count of Aggregated Transaction",
                                                "5.Transaction Count of Map Transaction",
                                                "6.Transaction Count of Top Transaction",
                                                "7.Transaction Count of Aggregated User",
                                                "8.Registered Users of Map user",
                                                "9.App opens of Map User",
                                                "10.Registered users of Top Users"
                                            ])

    if question == "1.Transaction Amount of Aggregated Transaction":
        
        st.subheader("TRANSACTION AMOUNT")

        top_chart_transaction_amount("aggregate_transaction")
       

    elif question == "2.Transaction Amount  of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT")

        top_chart_transaction_amount("map_transaction")
       
    elif question == "3.Transaction Amount  of Top Transaction":
        
        st.subheader("TRANSACTION AMOUNT")

        top_chart_transaction_amount("top_transaction")


    elif question == "4.Transaction Count of Aggregated Transaction":
        
        st.subheader("TRANSACTION COUNT")
        
        top_chart_transaction_count("aggregate_transaction")

    elif question == "5.Transaction Count of Map Transaction":
        
        st.subheader("TRANSACTION COUNT")
        
        top_chart_transaction_count("map_transaction")


    elif question == "6.Transaction Count of Top Transaction":
        
        st.subheader("TRANSACTION COUNT")
        
        top_chart_transaction_count("top_transaction")

    
    elif question == "7.Transaction Count of Aggregated User":
        
        st.subheader("TRANSACTION COUNT")
        
        top_chart_transaction_count("top_transaction")

    
    elif question == "8.Registered Users of Map user":
        
        states= st.selectbox("SELECT THE STATES",map_user["States"].unique())
        st.subheader("REGISTERED USERS")
        top_chart_registered_user("map_user", states)

    
    elif question == "9.App opens of Map User":
        
        states= st.selectbox("SELECT THE STATES",map_user["States"].unique())
        st.subheader("APP OPENS")
        top_chart_appopens("map_user", states)

    elif question ==  "10.Registered users of Top Users":
        
        st.subheader("REGISTERED USERS")
        top_chart_registeredusers("top_user")

            