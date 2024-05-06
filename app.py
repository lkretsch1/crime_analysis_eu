#Import necessary libraries 
import streamlit as st 
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
import geopandas as gpd

#Set Streamlit Window 
st.set_page_config(layout="wide")

#Define Function
@st.cache_data
def load_crimes(file, region, country): 
    crimes = pd.read_csv(file)
    #Clean Up Dataframe 
    crimes = crimes.drop(["DATAFLOW", "LAST UPDATE", "freq", "OBS_FLAG"], axis=1)
    crimes = crimes.rename(columns={"TIME_PERIOD" : "Year", "OBS_VALUE" : "Crimes"})

    #Load Nuts Region Description
    nuts = pd.read_excel(region)
    #Clean Up Dataframe
    nuts[["geo", "Region"]] = nuts["Nuts3"].str.split("]", expand=True)
    nuts["geo"] = nuts["geo"].str.replace("[", "")
    nuts = nuts.drop(["Nuts3"], axis=1)
    #Join the Dataframes crimes and nuts
    crimes = pd.merge(crimes, nuts, left_on="geo", right_on="geo", how="left")
    #Determine whether Region is NUTS 1 Region, NUTS 2 Region, NUTS 3 Region or a country
    nuts_code = crimes["geo"].str.slice(2)
    code = []
    for n in nuts_code: 
        if len(n) ==1: 
            code.append(1)
        elif len(n) == 2: 
            code.append(2)
        elif len(n) == 3: 
            code.append(3)
        else: 
            code.append(0)
    #Append new information to dataframe
    crimes["Nuts_Region"] = code

    #Load Country Names 
    crimes["Country Code"] = crimes["geo"].str[:2]
    country = pd.read_excel(country) 
    country[["Country Code", "Country Name"]] = country["Country"].str.split("]", expand=True)
    country["Country Code"] = country["Country Code"].str.replace("[", "")
    country = country.drop(["Country"], axis=1)
    #Merge Dataframe Crimes and Country
    crimes = pd.merge(crimes, country, how="left")
    #Crimes: Change datatype to float
    crimes["Crimes"] = crimes["Crimes"].astype(float)
    return crimes

#Define Function to divide Regions into Nuts Level
@st.cache_data
def nuts_regions(df): 
    nuts_0 = df[df["Nuts_Region"]==0]
    nuts_1 = df[df["Nuts_Region"]==1]
    nuts_2 = df[df["Nuts_Region"]==2]
    nuts_3 = df[df["Nuts_Region"]==3]
    return nuts_0, nuts_1, nuts_2, nuts_3

#Defin Function to Split Dataframe into unit measures 
@st.cache_data 
def split_unit(df): 
    nr = df[df["unit"]=="NR"]
    p = df[df["unit"]=="P_HTHAB"]
    return nr, p

#Define Function to Load Shape file 
@st.cache_data 
def load_shape(file): 
    df = gpd.read_file(file)
    return df
    

#START STREAMLIT APP

#Import Dataframe 
crimes = load_crimes("data/estat_crim_gen_reg_en.csv", "data/NUTS3.xlsx","data/Countries.xlsx")
crimes_nr, crimes_p = split_unit(crimes)
nuts_0, nuts_1, nuts_2, nuts_3 = nuts_regions(crimes_nr)
nuts0_p, nuts1_p, nuts2_p, nuts3_p = nuts_regions(crimes_p)

#Load Shape FIle 
world = load_shape("data/Nuts3_Shape/NUTS_RG_20M_2021_3035.shp")

#Create Flag Dictionary
flags = {"Albania": "flags/Albania.png", "Austria": "flags/Austria.png", "Belgium": "flags/Belgium.png",
         "Bulgaria" : "flags/Bulgaria.png", "Croatia": "flags/Croatia.png", "Cyprus": "flags/Cyprus.png",
         "Czechia": "flags/Czechia.png", "Denmark":  "flags/Denmark.png","Estonia": "flags/Estonia.png", 
         "EU": "flags/EU.png","Finland" : "flags/Finland.png","Germany":  "flags/Germany.png", "France" : "flags/France.png", 
         "Greece": "flags/Greece.png","Hungary":  "flags/Hungary.png", "Iceland" : "flags/Iceland.png", 
         "Ireland" : "flags/Ireland.png", "Italy" : "flags/Italy.png", "Latvia":  "flags/Latvia.png", 
         "Liechtenstein": "flags/Liechtenstein.png", "Lithuania" : "flags/Lithuania.png",
         "Luxembourg": "flags/Luxembourg.png", "Malta": "flags/Malta.png", "Montenegro": "flags/Montenegro.png", 
         "Netherlands" : "flags/Netherlands.png", "Norway": "flags/Norway.png", "Poland": "flags/Poland.png",
          "Portugal": "flags/Portugal.png", "Romania": "flags/Romania.png", "Serbia": "flags/Serbia.png",
         "Slovakia":  "flags/Slovakia.png", "Slovenia" : "flags/Slovenia.png","Spain":  "flags/Spain.png", 
         "Sweden": "flags/Sweden.png", "Switzerland": "flags/Switzerland.png", "Türkiye": "flags/Türkiye.png"}

#Build Streamlit App 
#Header/ Title with Description
c1, c2,c3 = st.columns([0.1, 0.8, 0.1])
with c1: 
    st.image("flags/EU.png", use_column_width=True)
with c2: 
    st.markdown("""<h1 style='margin-top: -10px; text-align: center; color: black'>Analyzing Crimes in 
                EU-Regions</h1>""", unsafe_allow_html=True)   

    st.markdown("""<h4 style='margin-top: +10px; text-align: center; color: black;'>Analysis of 
                police-recorded offenses by NUTS-3 regions based on data provided by European 
                Commission - Eurostat.</h4>""",
                unsafe_allow_html=True)
with c3: 
    st.image("flags/EU.png",  use_column_width=True)

#Create Tabs 
tab1, tab2, tab3 = st.tabs(["Overview", "Analyzing NUTS-Regions", "Analyzing ICCS Crimes"])

#FIRST TAB
with tab1:  
    st.markdown("""<h2 style='margin-top: -10px;text-align: center; color: black'>Definitions</h2>""", 
            unsafe_allow_html=True)  
    #NUTS Definition
    st.markdown("""<h4 style='color: grey'>NUTS Definition</h4>""", unsafe_allow_html=True)
    st.markdown("""<div style='margin-top: -10px;border: 1px solid black; padding: 10px;text-align: center;
                '> The European Union has established a common classification of territorial units for 
                statistics, known as ‘NUTS’, in order to facilitate the collection, development and 
                publication of harmonised regional statistics in the EU. This hierarchical system is
                also used for socioeconomic analyses of the regions and the framing of interventions 
                in the context of EU cohesion policy.    -   Definition European Parlament</div>""",
                    unsafe_allow_html=True)
    

    col1, col2 = st.columns([0.6,0.4])

    with col1: 
        #Variable Selection
        st.markdown("""<h6 style='text-align: left;margin-top: +50px; color: grey'>Select or Change Variables for a Detailed 
        Analysis</h6>""", unsafe_allow_html=True)
        #Merge World Dataframe with Nuts_0 Dataframe to find missing values 
        check = world.merge(nuts_0, left_on='FID', right_on='geo', how='right')
        check = check.dropna()
        eu = pd.Series("EU")
        reg = pd.Series(check["Region"].unique()).sort_values()
        col = pd.concat([eu, reg]).reset_index(drop=True)
        country = st.selectbox("Choose a Country",col)
        level = st.selectbox("Choose a NUTS-Level", ["NUTS", "NUTS 1", "NUTS 2", "NUTS 3"])
        #Filter Dataframe for selected variables 
        if level == "NUTS": 
            nuts = nuts_0.dropna()
            if country != "EU": 
                nuts = nuts[nuts["Country Name"]==country]
        elif level=="NUTS 1":
            nuts = nuts_1.dropna()
            if country != "EU": 
                nuts = nuts[nuts["Country Name"]==country]
        elif level =="NUTS 2": 
            nuts = nuts_2.dropna()
            if country != "EU": 
                nuts = nuts[nuts["Country Name"]==country]
        elif level =="NUTS 3": 
            nuts = nuts_3.dropna()
            if country != "EU": 
                nuts= nuts[nuts["Country Name"]==country]
        #Merge Geopandas File for Map
        world_nuts = world.merge(nuts, left_on='FID', right_on='geo', how='right')
        #NUTS-Level Classification
        st.markdown("""<h5 style='text-align: left;margin-top: +50px; color: grey'>NUTS - Level Classification
                    </h5>""", unsafe_allow_html=True)
        st.write("""The NUTS classification is hierarchical in that it subdivides each Member State into
                    three levels: NUTS 1, NUTS 2 and NUTS 3. The second and third levels are subdivisions 
                    of the first and second levels.The current NUTS 2021 classification is valid from 
                    1 January 2021 and lists 92 regions at NUTS 1 level, 242 regions at NUTS 2 level and
                    1 166 regions at NUTS 3 level""")
        #Show Table with Classification Requirement 
        nuts_classification = pd.DataFrame()
        nuts_classification["NUTS Level"] = ["NUTS 1", "NUTS 2", "NUTS 3"]
        nuts_classification["Minimum Population"] = ["3 Million", "800 000", "150 000"]
        nuts_classification["Maximum Population"] = ["7 Million", "3 Million", "800 000"]
        st.table(nuts_classification)
        st.write("""If there is no administrative unit of a sufficient size in a Member State, the level
                    is established by aggregating a sufficient number of smaller contiguous administrative
                    units. These aggregated units are known as ‘non-administrative units’.""")
        st.write("""For more information visit:
            https://www.europarl.europa.eu/factsheets/en/sheet/99/common-classification-of-territorial-units-for-statistics-nuts-""")
    with col2: 
        #Create Map showing NUTS Regions at selected Level
        st.markdown(f"""<h5 style='margin-top: +80px;margin-bottom: -30px;text-align: center; color: black'>{level} - 
                Regions in {country} </h5>""", unsafe_allow_html=True) 
        # Plotting
        fig_0, ax_0 = plt.subplots(figsize=(15, 10))
        #world0.boundary.plot(ax=ax1, edgecolor="0.3")
        world_nuts.boundary.plot(ax=ax_0)
        world_nuts.plot(color="white", linewidth=0.8, ax=ax_0, edgecolor='0.8', legend=True)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        plt.axis('off')
        st.pyplot(fig_0)

    st.divider()

    #ICCS DEFINITION
    st.markdown("""<h4 style='color: grey'>ICCS Definition</h4>""", unsafe_allow_html=True)
    st.markdown("""<div style='margin-top: -10px;border: 1px solid black; padding: 10px;text-align: center;
                '> The International Classification of Crime for Statistical Purposes (ICCS) provides a
                comprehensive framework for producing statistics on crime and criminal justice. The ICCS
                is the first common framework to group all kinds of criminal offences into categories 
                that are useful for producing crime statistics all over the world.</div>""",
                unsafe_allow_html=True)
    c1, c2 = st.columns([0.5, 0.5])
    with c1: 
        #ICCS Categories
        st.markdown("""<h5 style='text-align: left;margin-top: +50px; color: grey'>ICCS Code Categories
                    </h5>""", unsafe_allow_html=True)
        st.markdown("""<p style='text-align: center; color: black;'>The numerical
                     coding of the categories is in accordance with their level in the classification: 
                     Level 1 categories are the broadest categories and have a two-digit code (e.g. 01);
                     Level 2 categories have a fourdigit code (e.g. 0101); Level 3 categories have a 
                     five-digit code (e.g. 01011); and Level 4 categories, the most detailed level, have
                     a six-digit code (e.g. 010111).</p>""",unsafe_allow_html=True)
        st.image("data/Screenshot 2024-04-27 192328.png")
    with c2:     
        #Create Dictionaries to explain ICCS Code in Dataset
        iccs_def = {"ICCS0101" : "Intentional homocide", "ICCS02011" : "Assult", "ICCS0401" : "Robbery",
                "ICCS0501" : "Burglary", "ICCS05012" : "Burglary of private residential premises", 
                "ICCS0502" : "Theft", "ICCS050211" : "Theft of motorized land vehicle"}
        iccs_def = pd.DataFrame(iccs_def.items(), columns=['ICCS', 'Description'])
        #Crime Definition
        iccs_def["Definition"] = ["""Unlawful death inflicted upon a person with the intent to cause death or serious
                    injury""", """Intentional or reckless application of physical force inflicted upon the
                    body of a person""", """Unlawfully taking or obtaining property with the use of force
                    or threat of force against a person with intent to permanently or temporarily withhold
                    it from a person or organization.""","""Gaining unauthorized access to a part of a 
                    building/dwelling or other premises with or without the use of force against the 
                    building/dwelling, with intent to committheft or when actually committing theft""", 
                    """Burglary of private residential premises""","""Unlawfully taking or obtaining of 
                    property with the intent to permanently withhold it from a person or organization 
                    without consent and without the use of force, threat of force or violence, coercion
                    or deception""", "Theft of a motorized land vehicle" ]
        st.markdown("""<h5 style='text-align: left;margin-top: +50px; color: grey'>ICCS Code Definitions
                    </h5>""", unsafe_allow_html=True)
        st.table(iccs_def)
    st.write("For more information visit: https://www.unodc.org/unodc/en/data-and-analysis/statistics/iccs.html")
    st.divider()

#ANALYSIS - CRIME 
with tab2: 
    
    #Missing Data Information
    st.markdown("""<h2 style='margin-top: -10px;text-align: center; color: black'>Analyzing Crimes by NUTS-Regions</h2>""", 
            unsafe_allow_html=True)
    with st.expander("IMPORTANT NOTICE"):
        st.markdown("""<h5 style='color: grey;text-align: center;'>Missing Data</h5>""", unsafe_allow_html=True)
        st.markdown("""<div style='margin-top: -10px;margin-bottom: +20px; border: 1px solid black; 
                padding: 10px;text-align: center;'>It is important to notice that data is missing for 
                some countries, for some crimes, and for some years. The tables below show the number of
                crimes (out of the seven) by country and year and the number of countries that reported 
                crimes by ICCS code. The tables give an overview of the missing data and can explain some 
                observable patterns in the data.</div>""",unsafe_allow_html=True)
        #Create Dataframe holding number of crime codes reported by each country each year
        missing = crimes_nr.dropna()
        missing = missing.groupby(["Country Code", "Year"], as_index=False)["iccs"].nunique()
        missing = missing.pivot(index="Country Code", columns=["Year"], values="iccs")
        missing = missing.fillna(0)
        missing = missing.astype(int)
        missing_styled = missing.style.background_gradient()
        #Create Dataframe holding number of countries reported crime code each year
        missing_iccs = crimes_nr.dropna()
        missing_iccs = missing_iccs.groupby(["iccs", "Year"], as_index=False)["Country Code"].nunique()
        missing_iccs = missing_iccs.pivot(index="iccs", columns=["Year"], values = "Country Code")
        missing_iccs = missing_iccs.astype(int)
        missing_iccs_styled = missing_iccs.style.background_gradient()

        c1, c2, c3 = st.columns((0.1,0.8,0.1))
        with c2: 
            #Print Dataframes
            st.markdown("""<h7 style='color: grey;text-align: center;'>Missing Data by Country</h7>""", unsafe_allow_html=True)
            st.dataframe(missing_styled, use_container_width=True)
            st.markdown("""<h7 style='color: grey;text-align: center;'>Missing Data by ICCS Code</h7>""", unsafe_allow_html=True)
            st.dataframe(missing_iccs_styled, use_container_width = True)
            
    #Analysis  
    col1, col2 = st.columns([0.4,0.6])
    with col2: 
        #Variable Selection
        st.markdown("""<h6 style='text-align: left;margin-top: +50px; color: grey'>Select or Change Variables for a Detailed 
        Analysis</h6>""", unsafe_allow_html=True)
        country_x = st.selectbox("Choose a Country: ",col)
        level_x = st.selectbox("Choose a NUTS-Level: ", ["NUTS", "NUTS 1", "NUTS 2", "NUTS 3"])
        if level_x == "NUTS": 
            nuts_0 = nuts_0.dropna()
            if country_x != "EU": 
                nuts_0 = nuts_0[nuts_0["Country Name"]==country_x]
            nuts_t2 = nuts_0

        elif level_x =="NUTS 1":
            nuts_1 = nuts_1.dropna()
            if country_x != "EU": 
                nuts_1 = nuts_1[nuts_1["Country Name"]==country_x]
            #Filter DataFrame: Average Number of Crimes by Region 
            nuts_t2 = nuts_1

        elif level_x =="NUTS 2": 
            nuts_2 = nuts_2.dropna()
            if country_x != "EU": 
                nuts_2 = nuts_2[nuts_2["Country Name"]==country_x]
            nuts_t2 = nuts_2

        elif level_x == "NUTS 3": 
            nuts_3 = nuts_3.dropna()
            if country_x != "EU": 
                nuts_3 = nuts_3[nuts_3["Country Name"]==country_x]
            nuts_t2 = nuts_3

        crimes_nuts = nuts_t2.groupby(["Region","geo", "iccs"], 
                                        as_index=False)["Crimes"].agg(["sum", "count"])
        crimes_nuts["Average"] = crimes_nuts["sum"]/crimes_nuts["count"]
        crimes_nuts= crimes_nuts.groupby(["Region", "geo"], 
                                            as_index=False)["Average"].sum().round(2)
        #Filter Dataframe: Number of Crimes by Category 
        iccs = nuts_t2.groupby(["Year"], as_index=False)["Crimes"].agg(["sum"])
        #Pivot Dataframe for Visualization Purposes
        #iccs_p = iccs.pivot(index="Year", values="sum").reset_index()
        #Filter Dataframe: Number of Regions that reported Crimes 
        crimes_reported = nuts_t2.groupby(["Year"], as_index=False)["Crimes"].count()

        world_crimes = world.merge(crimes_nuts, left_on='FID', right_on='geo', how='right')

        #Map Summary 
        st.markdown("""<h5 style='color: grey; margin-top: 30px'>Summary Statistics</h5>""", unsafe_allow_html=True)
        highest_crimes = crimes_nuts[crimes_nuts["Average"] == crimes_nuts["Average"].max()]
        country_h = highest_crimes["Region"].iloc[0]
        crime_max = crimes_nuts["Average"].max()
        if level_x == "NUTS": 
            if country_x !="EU": 
                c1, c2, c3, c4 = st.columns([0.1, 0.3, 0.3, 0.3])
                with c2: 
                    #st.markdown(f'<style = {css}></style>',unsafe_allow_html=True)
                    st.metric(""" Country""", country_h)
                    st.image(flags.get(country_h),width=100)
                    
                with c3: 
                    st.metric("Average Number of police recored offenses", crime_max)
                with c4: 
                    mi = iccs["Year"].min()
                    ma = iccs["Year"].max()
                    st.metric("Years of available data", f"{mi} - {ma}")
                c1, c2, c3 = st.columns([0.2,0.6,0.2])
                with c2: 
                    st.markdown(f"""<h5 style='margin-top: +80px;margin-bottom: -30px;text-align: center; color: black'>Total Number of 
                                reported crimes in {level_x} - Region in {country_h}</h5>""", 
                                unsafe_allow_html=True)
                    fig_5 = plt.figure(figsize=(10,5))
                    sns.barplot(data = iccs, x="Year",y="sum", palette="Blues_d")
                    plt.ylabel("# of crimes")
                    plt.xticks(rotation=45, fontsize=8)
                    st.pyplot(fig_5)
            else: 
                c1, c2, c3 = st.columns([0.1, 0.45, 0.45])
                with c2:
                    st.metric("Country with the Highest Average Number of reported Crimes", country_h)
                    st.image(flags.get(country_h), width=100)
                with c3: 
                    st.metric("Average Number of reported Crimes", crime_max)
        else: 
            if country_x == "EU": 
                st.write("Please Choose a country to see the graph")
            else: 
                crime_max = crimes_nuts["Average"].max()
                highest_crimes = crimes_nuts[crimes_nuts["Average"] == crimes_nuts["Average"].max()]
                region_h = highest_crimes["Region"].iloc[0]
                highest = nuts_t2[nuts_t2["Region"]==region_h]
                country_h = highest["Country Name"].iloc[0]
                highest_c = nuts_t2[nuts_t2["Country Name"]==country_h]
                df_highest = highest_c.groupby(["Region"], as_index=False)["Crimes"].agg(["sum", "count"])
                df_highest["Average"] = df_highest["sum"]/df_highest["count"]

                c1, c2 = st.columns([0.4, 0.6])
                c3, c4= st.columns([ 0.6, 0.4])
                with c1: 
                    st.metric("Country", country_h)
                    st.image(flags.get(country_h),width=100)
                with c2: 
                    st.metric("""Region with highest \n average number of crimes""", region_h)
                with c3: 
                    st.metric("Average Number of reported Crimes", crime_max)
                with c4: 
                    mi = iccs["Year"].min()
                    ma = iccs["Year"].max()
                    st.metric("Years of avialable data", f"{mi} - {ma}")
                c1, c2, c3 = st.columns([0.25, 0.5, 0.25])
                with c2: 
                    fig_4 = plt.figure()
                    df_highest = df_highest.sort_values(by="Average", ascending=False)
                    sns.barplot(data = df_highest, x="Region",y="Average", palette="Blues_d")
                    plt.title(f"Average Number of reported crimes in {level_x} - Region in {country_h}")
                    plt.ylabel("# of crimes")
                    plt.xticks(rotation=90, fontsize=8)
                    st.pyplot(fig_4)

    
    with col1: 
        st.markdown(f"""<h5 style='margin-top: +80px;margin-bottom: -30px;text-align: center; color: black'>Average Number of Crimes
         per Year by {level} - Region</h5>""", unsafe_allow_html=True)
        # Plotting
        fig_1, ax_1 = plt.subplots(figsize=(15, 10))
        world_crimes.boundary.plot(ax=ax_1)
        world_crimes.plot(column='Average', cmap='Blues', linewidth=0.8, ax=ax_1, edgecolor='0.5', legend=True)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        plt.axis('off')
        st.pyplot(fig_1)
        
#ICCS Code ANALYSIS
with tab3: 
    st.markdown("""<h2 style='margin-top: -10px;text-align: center; color: black'>Analyzing Crimes by ICCS Code</h2>""", 
            unsafe_allow_html=True)
    #Missing Data Information
    with st.expander("IMPORTANT NOTICE"):
        st.markdown("""<h5 style='color: grey;text-align: center;'>Missing Data</h5>""", unsafe_allow_html=True)
        st.markdown("""<div style='margin-top: -10px;margin-bottom: +20px; border: 1px solid black; 
                padding: 10px;text-align: center;'>It is important to notice that data is missing for 
                some countries, for some crimes, and for some years. The tables below show the number of
                crimes (out of the seven) by country and year and the number of countries that reported 
                crimes by ICCS code. The tables give an overview of the missing data and can explain some 
                observable patterns in the data.</div>""",unsafe_allow_html=True)
        missing = crimes_nr.dropna()
        missing = missing.groupby(["Country Code", "Year"], as_index=False)["iccs"].nunique()
        missing = missing.pivot(index="Country Code", columns=["Year"], values="iccs")
        missing = missing.fillna(0)
        missing = missing.astype(int)
        missing_styled = missing.style.background_gradient()

        missing_iccs = crimes_nr.dropna()
        missing_iccs = missing_iccs.groupby(["iccs", "Year"], as_index=False)["Country Code"].nunique()
        missing_iccs = missing_iccs.pivot(index="iccs", columns=["Year"], values = "Country Code")
        missing_iccs = missing_iccs.astype(int)
        missing_iccs_styled = missing_iccs.style.background_gradient()
        c1, c2, c3 = st.columns((0.1,0.8,0.1))
        with c2: 
            st.markdown("""<h7 style='color: grey;text-align: center;'>Missing Data by Country</h7>""", unsafe_allow_html=True)
            st.dataframe(missing_styled, use_container_width=True)
            st.markdown("""<h7 style='color: grey;text-align: center;'>Missing Data by ICCS Code</h7>""", unsafe_allow_html=True)
            st.dataframe(missing_iccs_styled, use_container_width = True)

    st.divider()
    #Analysis  
    
    #Plot Total Number of Crimes reported by ICCS Code
    co1, co2, co3 = st.columns([0.3, 0.1, 0.6])
    with co1: 
        st.markdown("""<h5 style='margin-top: +50px;margin-bottom: -30px;text-align: center; color: black'>Total Number of Crimes 
        reported by ICCS Code</h5>""", unsafe_allow_html=True)
        iccs_t3 = crimes_nr.groupby(["iccs"], as_index=False)["Crimes"].sum()
        iccs_t3 = iccs_t3.sort_values(by="Crimes", ascending=False)
        fig_x = plt.figure()
        sns.barplot(data=iccs_t3, x="iccs", y="Crimes", palette="Blues_d")
        plt.xticks(rotation=45)
        plt.xlabel("ICCS Code")
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        st.pyplot(fig_x)

    with co3: 
        #Iccs Crime Code Definition
        st.markdown("""<h5 style='color: grey'>ICCS - ICCS Crime Code Definitions</h5>""", unsafe_allow_html=True)
        for i in iccs_def["ICCS"]: 
            df_def = iccs_def[iccs_def["ICCS"]==i]
            title = df_def["Description"].iloc[0]
            def_i = df_def["Definition"].iloc[0]
            st.markdown(f"""<p style='color: black'>{i} **{title}** - Definition: {def_i}</p>""", unsafe_allow_html=True)

    st.divider()
    #Analysis by Region
    st.markdown("""<h3 style='text-align: center;margin-bottom: +10px; color: black'>ICCS Code Analysis NUTS - Regions</h3>""", 
            unsafe_allow_html=True)
    
    col1, col2 = st.columns([0.55, 0.45])

    with col1: 
        #Variable Selection
        st.markdown("""<h6 style='text-align: left;margin-top: +50px; color: grey'>Select or Change Variables for a Detailed 
        Analysis</h6>""", 
            unsafe_allow_html=True)
        country_y = st.selectbox("Choose a Country  ",col)
        level_y = st.selectbox("Choose a NUTS - Level ", ["NUTS", "NUTS 1", "NUTS 2", "NUTS 3"])
        iccs = pd.Series(nuts_0["iccs"].unique()).sort_values()
        crime = st.multiselect("Select one or multiple ICCS - Crime Codes: ", iccs)
        #Choose Dataframe based on unit measure and Nuts Level
        if level_y == "NUTS": 
            df_crime = nuts_0
        elif level_y == "NUTS 1": 
            df_crime = nuts_1 
        elif level_y == "NUTS 2": 
            df_crime = nuts_2
        else: 
            df_crime = nuts_3 
    
        if country_y != "EU": 
            df_crime = df_crime[df_crime["Country Name"]==country_y]
        #Filter Dataframe by Iccs
        if len(crime) != 0: 
            df_crime = df_crime[df_crime["iccs"].isin(crime)]
        st.markdown(f"""<h5 style='margin-top: +20px;margin-bottom: -30px;text-align: center; color: black'>Number of Crimes per
         Year by {level_y} - Region {crime}</h5>""", unsafe_allow_html=True)
        crimes_year = df_crime.groupby(["Year", "iccs"], as_index=False)["Crimes"].sum()
        fig_3 = plt.figure(figsize=(10,5))
        ax = sns.barplot(data=crimes_year, x="Year", y="Crimes", hue="iccs", palette="Blues_d")
        sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
        plt.ylabel("# of Crimes")
        plt.xticks(rotation=45)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        st.pyplot(fig_3)
    
    with col2: 
        st.markdown(f"""<h5 style='margin-top: +120px;margin-bottom: -30px;text-align: center; color: black'>Average Crimes by {level_y} 
        - Region {crime}</h5>""", unsafe_allow_html=True)
        #Dataframe 
        crimes_iccs = df_crime.groupby(["Region","geo"], 
                                        as_index=False)["Crimes"].agg(["count", "sum"])
        crimes_iccs["Average"] = crimes_iccs["sum"]/crimes_iccs["count"] 
        iccs_plot = crimes_iccs[crimes_iccs.groupby(['Region', 'geo'])['Average'].transform(max) == crimes_iccs['Average']]
        #Filter Dataframe: Number of Regions that reported Crimes 
        crimes_reported = df_crime.groupby(["Year"], as_index=False)["Crimes"].count()

        world_iccs = world.merge(crimes_iccs, left_on='FID', right_on='geo', how='right')
        # Plotting
        fig_2, ax_2 = plt.subplots(figsize=(15, 10))
        #world0.boundary.plot(ax=ax1, edgecolor="0.3")
        world_iccs.boundary.plot(ax=ax_1)
        world_iccs.plot(column='Average', cmap='Blues', linewidth=0.8, ax=ax_2, edgecolor='0.5', legend=True)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        plt.axis('off')
        st.pyplot(fig_2)
    
    #c1, c2, c3 = st.columns([0.25, 0.5, 0.25])
    #Plot Crimes by Year 
    #with c2: 
        
    st.divider()



#Formatting st.Image and st.Metric
st.markdown(
    """
    <style>
        [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
)

st.markdown(
    """
    <style>
        [data-testid=stMetric]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
)

st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        font-size: 30px;
    }
    </style>
    """, unsafe_allow_html=True) 

st.markdown("""
    <style>
    [data-testid="stMetricLabel"] {
        font-size: 50px;
        text-align: center;
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 100%;
        overflow-wrap: break-word;
    }
    </style>
    """, unsafe_allow_html=True) 


    












