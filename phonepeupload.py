import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json

# DataFrame Creation

#SQL connection

mydb = psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="guvi2024")

cursor=mydb.cursor()

#aggregate_insurance DF

cursor.execute("select * from aggregate_insurance")
mydb.commit()
table1=cursor.fetchall()

Aggr_insurance=pd.DataFrame(table1,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

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


#Map Insurance DF

cursor.execute("select * from map_insurance")
mydb.commit()
table4=cursor.fetchall()

map_insurance=pd.DataFrame(table4,columns=("States","Years","Quarter","Districts","Transaction_count","Transaction_amount"))

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

#Top insurance DF

cursor.execute("select * from top_insurance")
mydb.commit()
table7=cursor.fetchall()

top_insurance=pd.DataFrame(table7,columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))

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

#Transaction Year Based 

def Transaction_amount_count_y(df, year):

    data1=df[df["Years"] == year]
    data1.reset_index(drop = True,inplace=True)

    data1grp=data1.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    data1grp.reset_index(inplace=True)

    col1, col2 = st.columns(2) 
    
    with col1:

        fig_amount=px.bar(data1grp, x= "States", y="Transaction_amount", title = f"{year} TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Agsunset,height=600,width=650)
    
        st.plotly_chart(fig_amount)

    with col2:

        fig_count=px.bar(data1grp, x= "States", y="Transaction_count", title =f"{year} TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Blugrn_r,height=600,width=650)
    
        st.plotly_chart(fig_count)

    col1,col2 = st.columns(2)
    with col1:
    
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        states_name = []
        data=json.loads(response.content)
        for feature in data["features"]:
            states_name.append(feature['properties']['ST_NM']) 

        states_name.sort()

        fig_india = px.choropleth(data1,geojson=data,locations="States",featureidkey='properties.ST_NM',
                                    color="Transaction_amount",color_continuous_scale="Rainbow",
                                    range_color=(data1["Transaction_amount"].min(),data1["Transaction_amount"].max()),
                                    hover_name="States",title=f"{year} TRANSACTION AMOUNT",fitbounds="locations",
                                    height=600,width=650 )
        fig_india.update_geos(visible= False)
        st.plotly_chart(fig_india)

    with col2:

        fig_india1= px.choropleth(data1,geojson=data,locations="States",featureidkey='properties.ST_NM',
                                    color="Transaction_count",color_continuous_scale="Rainbow",
                                    range_color=(data1["Transaction_count"].min(),data1["Transaction_count"].max()),
                                    hover_name="States",title=f"{year} TRANSACTION COUNT",fitbounds="locations",
                                    height=600,width=650 )
        fig_india1.update_geos(visible= False)
        st.plotly_chart(fig_india1)

    return data1

#Transaction Year Based in Quarter

def Transaction_amount_count_Y_Q(df,quarter):
    data1=df[df["Quarter"] == quarter]
    data1.reset_index(drop = True,inplace=True)

    data1grp=data1.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    data1grp.reset_index(inplace=True)

    col1, col2 = st.columns(2) 
    with col1:

        fig_amount=px.bar(data1grp, x= "States", y="Transaction_amount", title = f"{data1["Years"].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                       color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig_amount)

    with col2:
    
        fig_count=px.bar(data1grp, x= "States", y="Transaction_count", title = f"{data1["Years"].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Rainbow_r)
    
        st.plotly_chart(fig_count)


    col1,col2 = st.columns(2)
    with col1:

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        states_name = []
        data=json.loads(response.content)
        for feature in data["features"]:
            states_name.append(feature['properties']['ST_NM']) 

        states_name.sort()

        fig_india = px.choropleth(data1,geojson=data,locations="States",featureidkey='properties.ST_NM',
                                    color="Transaction_amount",color_continuous_scale="Rainbow",
                                    range_color=(data1["Transaction_amount"].min(),data1["Transaction_amount"].max()),
                                    hover_name="States",title=f"{data1["Years"].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",fitbounds="locations",
                                    height=700,width=700 )
        fig_india.update_geos(visible= False)
        
        st.plotly_chart(fig_india)

    with col2:

        fig_india1= px.choropleth(data1,geojson=data,locations="States",featureidkey='properties.ST_NM',
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(data1["Transaction_count"].min(),data1["Transaction_count"].max()),
                                hover_name="States",title=f"{data1["Years"].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",fitbounds="locations",
                                height=700,width=700 )
        fig_india1.update_geos(visible= False)

        st.plotly_chart(fig_india1)

    return data1

#Aggregate Transaction Types

def Aggre_Tran_Transaction_type(df,state):

    data1=df[df["States"] ==state]
    data1.reset_index(drop = True, inplace= True)

    data1grp=data1.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    data1grp.reset_index(inplace=True)

    col1,col2 = st.columns(2)
    with col1:

        fig_pie_1 = px.pie(data_frame=data1, names = "Transaction_type",values= "Transaction_amount",
                        width=600, title= f"{state.upper()} TRANSACTION AMOUNT",hole=0.5)

        st.plotly_chart(fig_pie_1)

    with col2:

        fig_pie_2 = px.pie(data_frame=data1, names = "Transaction_type",values= "Transaction_count",
                        width=600, title= f"{state.upper()} TRANSACTION COUNT",hole=0.5)

        st.plotly_chart(fig_pie_2)

#Aggregate _User_Analysis_Year

def Aggre_user_plot(df,year):
    aggusr=df[df["Years"]== year]
    aggusr.reset_index(drop= True,inplace = True)

    aggusr_grp = pd.DataFrame(aggusr.groupby("Brands")["Transaction_count"].sum())
    aggusr_grp.reset_index(inplace= True)

    fig_bar_1= px.bar(aggusr,x ="Brands",y="Transaction_count" ,title= f"{year} BRANDS AND TRANSACTION COUNT",
                    width=800,color_discrete_sequence=px.colors.sequential.Oranges_r,hover_name="Brands")

    st.plotly_chart(fig_bar_1)
    return aggusr

##Aggregate _User_Analysis _quarter

def Aggre_user_plot2(df,quarter):
    aggusr_Q=df[df["Quarter"]== quarter]
    aggusr_Q.reset_index(drop= True,inplace = True)


    aggusr_Q = pd.DataFrame(aggusr_Q.groupby("Brands")["Transaction_count"].sum())
    aggusr_Q.reset_index(inplace= True)


    fig_bar_1= px.bar(aggusr_Q,x ="Brands",y="Transaction_count" ,title= f"{quarter} QUARTER BRANDS AND TRANSACTION COUNT",
                    width=800,color_discrete_sequence=px.colors.sequential.haline_r)

    st.plotly_chart(fig_bar_1)

    return aggusr_Q


# Aggregate _User_Analysis Year_quarter_states

def Aggre_user_plot3(df,state):
    auyqs = df[df["State"] == state]
    auyqs.reset_index(drop=True, inplace=True)

    fig_line_1 = px.line(auyqs, x= "Brands",y="Transaction_count",hover_data="Percentage",
                        title= f"{state} BRANDS TRANSACTION COUNT PERCENTAGE",width=1000,markers= True)
    st.plotly_chart(fig_line_1)

# Map_insurance_district

def map_insurance_district(df,state):

    data1=df[df["States"] ==state]
    data1.reset_index(drop = True, inplace= True)

    data1grp=data1.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    data1grp.reset_index(inplace=True)

    col1,col2 = st.columns(2)
    with col1:

        fig_bar_1 = px.bar(data1grp, x="Transaction_amount", y ="District", orientation= "h",width=600,
                       title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.haline_r)
        st.plotly_chart(fig_bar_1)

    with col2:

        fig_bar_2 =  px.bar(data1grp, x="Transaction_count", y ="District", orientation= "h",width=600,
                       title=f"{state.upper()} DISTRICT AND TRANSACTION COUNT",color_discrete_sequence= px.colors.sequential.thermal)
        st.plotly_chart(fig_bar_2)

#Map_User_Analysis
        
def map_user_plot_1(df, year):
    mpur = df[df["Years"]== year]
    mpur.reset_index(drop= True,inplace = True)

    mpur_grp =mpur.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    mpur_grp.reset_index(inplace= True)


    fig_line_1 = px.line(mpur_grp, x= "States",y=["RegisteredUsers","AppOpens"],
                        title= f"{year} REGISTERED USER AND APPOPENS",width=900,height = 800,markers= True)
    st.plotly_chart(fig_line_1)

    return mpur


#Map_User_Analysis part2

def map_user_plot_2(df, quarter):
    mpurQ = df[df["Quarter"]== quarter]
    mpurQ.reset_index(drop= True,inplace = True)

    mpur_grp =mpurQ.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    mpur_grp.reset_index(inplace= True)


    fig_line_1 = px.line(mpur_grp, x= "States",y=["RegisteredUsers","AppOpens"],
                        title= f"{df["Years"].min()} YEAR {quarter} QUARTER REGISTERED USER AND APPOPENS",width=1000,height = 800,markers= True,
                        color_discrete_sequence= px.colors.sequential.Oranges_r)
    st.plotly_chart(fig_line_1)

    return mpurQ

#Map_User_Plot3

def map_user_plot3(df,state):
    muyqs_Q=df[df["States"]== state]
    muyqs_Q.reset_index(drop= True,inplace = True)

    col1,col2 = st.columns(2)
    with col1:

        fig_map_user_bar_1 = px.bar(muyqs_Q, x = "RegisteredUsers", y= "District", orientation= "h",
                                    title = f"{state.upper()} REGISTERED USER", height=600,color_discrete_sequence=px.colors.sequential.OrRd_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:

        fig_map_user_bar_2 = px.bar(muyqs_Q, x = "AppOpens", y= "District", orientation= "h",
                                title = f"{state.upper()} REGISTERED USER", height=600,color_discrete_sequence=px.colors.sequential.Magma_r)
    st.plotly_chart(fig_map_user_bar_2)

#Top_Insurance

def Top_insurance_plot_1(df,state):
    tiy = df[df["States"]== state]
    tiy.reset_index(drop= True,inplace = True)

    tiyg=tiy.groupby("Pincodes")[["Transaction_count","Transaction_amount"]].sum()
    tiyg.reset_index(inplace= True)

    col1,col2 = st.columns(2)
    with col1:

        fig_Map_insur_bar_1 = px.bar(tiyg,x= "Pincodes",y= "Transaction_amount",
                            title= "TRANSACTION AMOUNT",width=1000,color_discrete_sequence=px.colors.sequential.Magenta_r)
        st.plotly_chart(fig_Map_insur_bar_1)

    with col2:

        fig_Map_insur_bar_2 = px.bar(tiyg,x= "Pincodes",y= "Transaction_count",
                        title= "TRANSACTION COUNT",width=1000,color_discrete_sequence=px.colors.sequential.Inferno_r)
        st.plotly_chart(fig_Map_insur_bar_2)


#Top_Insurance

def Top_transaction_plot_1(df,state):
    tiy = df[df["States"]== state]
    tiy.reset_index(drop= True,inplace = True)

    tiyg=tiy.groupby("Pincodes")[["Transaction_count","Transaction_amount"]].sum()
    tiyg.reset_index(inplace= True)


    fig_Map_insur_bar_1 = px.bar(tiy,x= "Quarter",y= "Transaction_amount",hover_data= "Pincodes",
                        title= "TRANSACTION AMOUNT",width=1000,color_discrete_sequence=px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_Map_insur_bar_1)


    fig_Map_insur_bar_2 = px.bar(tiy,x= "Quarter",y= "Transaction_count",hover_data= "Pincodes",
                    title= "TRANSACTION COUNT",width=1000,color_discrete_sequence=px.colors.sequential.Inferno_r)
    st.plotly_chart(fig_Map_insur_bar_2)

#Top_User_insurance
    
def top_user_plot1(df,year):
    trtusr=df[df["Years"]== year]
    trtusr.reset_index(drop= True,inplace = True)

    trtusr_grp = pd.DataFrame(trtusr.groupby(["States","Quarter"])["RegisteredUsers"].sum())
    trtusr_grp.reset_index(inplace= True)

    fig_top_plot1= px.bar(trtusr_grp, x = "States", y = "RegisteredUsers",color= "Quarter",
                        title = f"{year} REGISTERED USERS",width=1000,height=800,color_discrete_sequence=px.colors.sequential.Pinkyl)
    st.plotly_chart(fig_top_plot1)
    
    return trtusr

#top_user_plot_2

def top_user_plot_2(df,state):
    tuys= df[df["States"]== state]
    tuys.reset_index(drop= True,inplace = True)

    fig_top_pot_2 = px.bar(tuys, x = "Quarter", y= "RegisteredUsers",title = "REGISTERED USERS , PINCODES , QUARTER",
                        width = 1000,height = 800,color = "RegisteredUsers",hover_data ="Pincodes",
                            color_continuous_scale= px.colors.sequential.Magma)
    st.plotly_chart(fig_top_pot_2)



def ques1():
    brand= Aggregate_user[["Brands","Transaction_count"]]
    brand1= brand.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Transaction_count", names= "Brands", color_discrete_sequence=px.colors.sequential.Rainbow_r,
                       title= "Top Mobile Brands of Transaction_count")
    return st.plotly_chart(fig_brands)

def ques2():
    lt= Aggregate_transaction[["States", "Transaction_amount"]]
    lt1= lt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "States", y= "Transaction_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques3():
    ht= Aggregate_transaction[["States", "Transaction_amount"]]
    ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_lts= px.bar(ht2, x= "States", y= "Transaction_amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)


def ques4():
    htd= Map_transaction[["District", "Transaction_amount"]]
    htd1= htd.groupby("District")["Transaction_amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.bar(htd2, x= "Transaction_amount", y= "District", title="TOP 10 DISTRICT OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Reds)
    return st.plotly_chart(fig_htd)

def ques5():
    htd= Map_transaction[["District", "Transaction_amount"]]
    htd1= htd.groupby("District")["Transaction_amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.bar(htd2, x= "Transaction_amount", y= "District", title="TOP 10 DISTRICT OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Reds)
    return st.plotly_chart(fig_htd)


def ques6():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.pie(sa2, names= "States", values= "AppOpens", title="Top 10 States With Phonepe users",hole=0.5,
                color_discrete_sequence= px.colors.sequential.Rainbow_r)
    return st.plotly_chart(fig_sa)

def ques7():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.pie(sa2, names= "States", values= "AppOpens", title="lowest 10 States With Phonepe users",hole=0.5,
                color_discrete_sequence= px.colors.sequential.Rainbow_r)
    return st.plotly_chart(fig_sa)

def ques8():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)

def ques9():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)


def ques10():
    dt= Map_transaction[["District", "Transaction_amount"]]
    dt1= dt.groupby("District")["Transaction_amount"].sum().sort_values(ascending=False)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.bar(dt2, x= "District", y= "Transaction_amount", title= "DISTRICT WITH HIGHEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Viridis)
    return st.plotly_chart(fig_dt)



#STREAMLIT PART

st.set_page_config(layout="wide") 
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    #st.write("Options")
    select = option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP CHARTS"])

if select=="HOME":
    
    col1,col2= st.columns(2)

    with col1:
        st.header(":violet[PHONEPE]")
        st.subheader(":red[INDIA'S BEST TRANSACTION APP]")
        st.markdown(":violet[INDIA'S  DIGITAL PAYMENT PLATFORM] ")

        st.write("****:blue[FEATURES]****")
        st.write("****100% Secure and Lightining Fast****")
        st.write("****Instant Money Transfer****")
        st.write("****Transfer Money upto 1 Lakhs in a Day****")
        st.write("****Banking 24/7****")
        st.write("****Get Cash Back****")
       
    with col2:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

elif select=="DATA EXPLORATION":
    
    tab1,tab2,tab3 = st.tabs(["Aggregate Analysis","Map Analysis","Top Analysis"])

    with tab1:

        method = st.radio("Select the method",["Insurance Analysis","Transaction Analysis","User Analysis"])
        
        if method == "Insurance Analysis":

            col1,col2 = st.columns(2)    # two seperate columns
            with col1:

                years = st.slider("Select the Year", Aggr_insurance["Years"].min(), Aggr_insurance["Years"].max(), Aggr_insurance["Years"].min()) 
            data_Y=Transaction_amount_count_y(Aggr_insurance,years)
    
            col1,col2 = st.columns(2)    # two seperate columns
            with col1:

                quarters = st.slider("Select the Quarter", data_Y["Quarter"].min(),  data_Y["Quarter"].max(),  data_Y["Quarter"].min())  
            Transaction_amount_count_Y_Q(data_Y,quarters)
    
        elif method == "Transaction Analysis":
            
            col1,col2=st.columns(2)
            with col1:

                years = st.slider("Select the Year", Aggr_transaction["Years"].min(), Aggr_transaction["Years"].max(), Aggr_transaction["Years"].min())  
            data_tran_Y=Transaction_amount_count_y(Aggr_transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State", data_tran_Y["States"].unique())

            Aggre_Tran_Transaction_type(data_tran_Y,states)

            col1,col2 = st.columns(2)    
            with col1:

                quarters = st.slider("Select the Quarter", data_tran_Y["Quarter"].min(), data_tran_Y["Quarter"].max(),data_tran_Y["Quarter"].min())  
            data_tran_Y_Q = Transaction_amount_count_Y_Q(data_tran_Y,quarters)
    
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_Ty", data_tran_Y_Q["States"].unique())

            Aggre_Tran_Transaction_type(data_tran_Y_Q, states)

        elif method == "User Analysis":

            col1,col2=st.columns(2)
            with col1:

                years = st.slider("Select the Year", Aggr_user["Years"].min(),Aggr_user["Years"].max(), Aggr_user["Years"].min())  
            Aggr_user_Y=Aggre_user_plot(Aggr_user,years)

            col1,col2 = st.columns(2)    
            with col1:

                quarters = st.slider("Select the Quarter",  Aggr_user_Y["Quarter"].min(), Aggr_user_Y["Quarter"].max(), Aggr_user_Y["Quarter"].min())  
            Aggr_user_Y_Q = Aggre_user_plot2(Aggr_user_Y,quarters)
    
            col1,col2=st.columns(2)
            with col1:
               states=st.selectbox("Select The Statewise", Aggr_user_Y_Q.loc["States"].unique())
            Aggre_user_plot3(Aggr_user_Y_Q,states)

           

    with tab2:

        method2 = st.radio("Select the method",["Map Insurance","Map Transaction","Map User"])
                    
        if method2 == "Map Insurance":

            col1,col2=st.columns(2)
            with col1:

                years = st.slider("Select the Year_Ins", map_insurance["Years"].min(),  map_insurance["Years"].max(),  map_insurance["Years"].min())  
            map_insurance_tac_Y=Transaction_amount_count_y(map_insurance,years)
 
            col1,col2=st.columns(2)
            with col1:

                states=st.selectbox("Select The State", map_insurance_tac_Y["States"].unique())

            map_insurance_district(map_insurance_tac_Y,states)

            col1,col2 = st.columns(2)    
            with col1:

                quarters = st.slider("Select the Quarter_map", map_insurance_tac_Y["Quarter"].min(),map_insurance_tac_Y ["Quarter"].max(),map_insurance_tac_Y["Quarter"].min())  
            map_insurance__tran_Y_Q = Transaction_amount_count_Y_Q(map_insurance_tac_Y,quarters)
    
            col1,col2=st.columns(2)
           
            with col1:
                states=st.selectbox("Select The State_T", map_insurance__tran_Y_Q["States"].unique())
            map_insurance_district(map_insurance__tran_Y_Q , states)

        elif method2 == "Map Transaction":
            
            
            col1,col2=st.columns(2)
            with col1:

                years = st.slider("Select the Year_trans", map_transaction["Years"].min(),  map_transaction["Years"].max(), map_transaction["Years"].min())  
            map_transaction_tac_Y=Transaction_amount_count_y(map_transaction,years)
 
            col1,col2=st.columns(2)
            with col1:

                states=st.selectbox("Select The State_Tran", map_transaction_tac_Y["States"].unique())

            map_insurance_district(map_transaction_tac_Y,states)

            col1,col2 = st.columns(2)    
            with col1:

                quarters = st.slider("Select the Quarter_map", map_transaction_tac_Y["Quarter"].min(),map_transaction_tac_Y ["Quarter"].max(),map_transaction_tac_Y["Quarter"].min())  
            map_transaction__tran_Y_Q = Transaction_amount_count_Y_Q(map_transaction_tac_Y,quarters)
    
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_T", map_transaction__tran_Y_Q["States"].unique())

            map_insurance_district(map_transaction__tran_Y_Q, states)

        elif method2 == "Map User":
            
            col1,col2=st.columns(2)
            with col1:

                years = st.slider("Select the Year_trans", map_user["Years"].min(),  map_user["Years"].max(), map_user["Years"].min())  
            map_user_Y=map_user_plot_1(map_user,years)

            col1,col2 = st.columns(2)    
            with col1:

                quarters = st.slider("Select the Quarter_map",  map_user_Y["Quarter"].min(), map_user_Y ["Quarter"].max(), map_user_Y["Quarter"].min())  
            map_user_Y_Q = map_user_plot_2(map_user_Y,quarters)
    
            
            col1,col2=st.columns(2)
            with col1:

                states=st.selectbox("Select The States", map_user_Y_Q["States"].unique())
            map_user_plot3(map_user_Y_Q,states)

    with tab3:

        method3 = st.radio("Select the method",["Top Insurance","Top Transaction","Top User"])
        
        if method3 == "Top Insurance":

            col1,col2=st.columns(2)
            with col1:

                years = st.slider("Select the Year_top insurance", top_insurance["Years"].min(),  top_insurance["Years"].max(), top_insurance["Years"].min())  
            top_insur_tac_Y = Transaction_amount_count_y(top_insurance,years)
            
            col1,col2=st.columns(2)
            with col1:

                states=st.selectbox("Select The States_ti",top_insur_tac_Y["States"].unique())
            Top_insurance_plot_1(top_insur_tac_Y,states)

            col1,col2 = st.columns(2)    
            with col1:

                quarters = st.slider("Select the Quarter_map",  top_insur_tac_Y["Quarter"].min(),top_insur_tac_Y["Quarter"].max(),top_insur_tac_Y["Quarter"].min())  
            top_insur_tac_Y_Q = Transaction_amount_count_Y_Q(top_insur_tac_Y,quarters)
    
    
        elif method3 == "Top Transaction":
           
            col1,col2=st.columns(2)
            with col1:

                years = st.slider("Select the Year_top transaction", top_transaction["Years"].min(), top_transaction ["Years"].max(),top_transaction["Years"].min())  
            top_transaction_tac_Y = Transaction_amount_count_y(top_transaction,years)
            
            col1,col2=st.columns(2)
            with col1:

                states=st.selectbox("Select The States_t",top_transaction_tac_Y["States"].unique())
            Top_insurance_plot_1(top_transaction_tac_Y,states)

            col1,col2 = st.columns(2)    
            with col1:

                quarters = st.slider("Select the Quarter_top",top_transaction_tac_Y["Quarter"].min(), top_transaction_tac_Y["Quarter"].max(), top_transaction_tac_Y["Quarter"].min())  
            top_insur_tac_Y_Q = Transaction_amount_count_Y_Q(top_transaction_tac_Y,quarters)
    
    
        elif method3 == "Top User":
            
            col1,col2=st.columns(2)
            with col1:

                years = st.slider("Select the Year_user",top_user["Years"].min(),  top_user["Years"].max(), top_user["Years"].min())  
            top_user_Y = top_user_plot1(top_user,years)

            
            col1,col2=st.columns(2)
            with col1:

                states=st.selectbox("Select The States_t", top_user_Y["States"].unique())
            top_user_plot_2(top_user_Y,states)


elif select=="TOP CHARTS":

   ques= st.selectbox("**Select the Question**",['Top Brands Of Mobiles Used',
                                                 'States With Lowest Trasaction Amount',
                                                 'States With Highest Trasaction Amount',
                                                 'District With Highest Transaction Amount',
                                                 'District With Lowest Transaction Amount',
                                                 'Top 10 States With Phonepe users',
                                                 'Least 10 States With Phonepe users',
                                                 'States With Lowest Trasaction Count',
                                                 'States With Highest Trasaction Count',
                                                 'Top 50 District With Highest Transaction Amount'])

    if ques=="Top Brands Of Mobiles Used":
        ques1()

    elif ques=="States With Lowest Trasaction Amount":
        ques2()

    elif ques=="States With Highest Trasaction Amount":
        ques3()

    elif ques=="District With Highest Transaction Amount":
        ques4()

    elif ques=="District With Lowest Transaction Amount":
        ques5()

    elif ques=="Top 10 States With Phonepe users":
        ques6()

    elif ques=="Least 10 States With Phonepe users":
        ques7()

    elif ques=="States With Lowest Trasaction Count":
        ques8()

    elif ques=="States With Highest Trasaction Count":
        ques9()


    elif ques=="Top 50 District With Highest Transaction Amount":
        ques10()
    