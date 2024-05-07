# Analyzing Crimes in the EU
Analysis of police-recored offences by NUTS 3 regions in the EU from 2008 to 2022

## Introduction ℹ️

Crime analysis is a critical feature of modern policing strategies that is a form of proactive problem-solving and intelligence-led decision-making. Identifying trends and patterns overall, as well as within crime categories and regions, allow the police an effective resource allocation. Comparing different countries and regions in Europe may be used to evaluate effectiveness of policing and may foster collaborations to improve strategies in policing. 
As a civilian, this information can be useful for traveling or residential purposes. Being aware of a higher risk of crime, or a specific type of crime can help prevent crimes and becoming a victim of a crime.   

## Streamlit App 📱

Link to Streamlit App 
https://crimeanalysis-eu.streamlit.app/

The streamlit app is consists of three parts. First, NUTS-Regions as well as ICCS Codes are being defined and explained in order to understand the data that's being analyzed. A map visualizes the different NUTS-Regions and a filter can be used to specify on a single country. 
The second part of the streamlit app, focuses on analyzing the number of crimes by NUTS-Regions. A colored map allows an instant judgement of crime rates and filters can be used for a detailed analysis. Summary statistics as well as additional charts will add more detail to the analysis. 
The third and final part analyzes crime types by ICCS codes. Total, as well as yearly crime numbers are being displaed in the analysis, along with a map and filters. 

It is important to notice that the dataset is not complete. Not every region as reported every crime every year, thus a comparison can be difficult. This problem has been handled by computing average crime rates that takes the sum of crimes reported for that region and divides it by the number of times the region reported crimes. 

The streamlit app can be opened by running the app.py file as well. 

## Data Sources 🌐

The data with police recorded offenses has been retrieved from:  https://data.europa.eu/data/datasets/wzxbhifltwvee4h8tcdza?locale=en#
Different file formats are available for download. Using the csv file provides a cleaned and correctly formatted dataframe for the analysis. 

In order to transform geo codes in the crime dataset into region names, the data dictionary has been copied in an excel file by hand since no fitting dataset has been found.  
In addition to that, a shape file containing the locations of NUTS-Regions has been downloaded from the following page: 
https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts


## Future Work 🚀

The streamlit app works with data from 2008 to 2022. More recent data and more information about crimes would allow for a more accurate analysis. A possible extension of this app would be the incorporation of additional datasets, such as datasets about police resource allocation. Information on date and time of the reported offense would open the possibility to analyze crimes even further. 


