# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 15:36:11 2023

@author: Nobert Turihohabwe
"""
#pip install streamlit
import streamlit as st
import pandas as pd
import numpy as np


       

#Develop DashBoard
st.header('Project Analytica (MSE Recovery Fund)')


#Add Sidebar to DashBoard
add_sidebar = st.sidebar.selectbox('Category',('About The Fund','Data_Cleaning','Impact Measurement','PFI Comparison'))

if add_sidebar == 'About The Fund':
    st.write('The Micro and Small Enterprises (MSE) Recovery Fund is a 5-year, USD 20MN (approximately UGX 70 Bn)',
             'initiative under the Mastercard Foundation Young Africa Works program, established in partnership with',
             ' Financial Sector Deepening (FSD) Uganda to offset the shocks of the COVID-19 pandemic on the economy of',
             ' Uganda through investments in Micro and Small Enterprises, via Tier III and Tier IV financial institutions.')




#Develop Impact Measurement DashBoard
if add_sidebar == 'Impact Measurement':
    st.subheader('Impact Measurement: To be completed')

    
    

#Develop PFI Comparison DashBoard
if add_sidebar == 'PFI Comparison':
    st.write('PFI Comparison: To be Completed')



#Develop Data Cleaning DashBoard
if add_sidebar == 'Data_Cleaning':
    st.subheader('Import file to clean')
    
    #Add file uploader widget
    uploaded_file = st.file_uploader("Choose an excel file", type="xlsx")
    
    if uploaded_file is not None:
        # Read the file file into a DataFrame
        df = pd.read_excel(uploaded_file)
        lender = df['lender'].iloc[0]
    
        # Display the DataFrame
        st.subheader("Preview of the raw data:")
        st.write("The shape is: ",df.shape)
        st.write("The lender is :",lender)
        st.write(df.head())
        
        
        #Add Data Cleaning Button
        if st.button("Click to Clean Data"):
            
            #Clean the data
            
            
             

            #Data Cleaning Code for Butuuro SACCO                   
            if df['lender'].iloc[0] == 'Butuuro SACCO':
        
                df["Sector"] = df['Line_of_business'] + " " + df['Loan_purpose']
                df["Loan_ID"] = df["Loan_ID"].astype(str)
                df["Borrower_ID"] = df["Borrower_ID"].astype(str)
                df["Date_of_birth"] = pd.to_datetime(df["Date_of_birth"],format='mixed')
                #df['Date_of_loan_issue'] = (df['Date_of_loan_issue'].str.replace(' 00:00:00','')).str.replace(' ','')
                df["Date_of_loan_issue"] = pd.to_datetime(df["Date_of_loan_issue"], format='mixed')#, dayfirst=False)
                df["Date_of_repayments_commencement"] = pd.to_datetime(df["Date_of_repayments_commencement"],format='mixed')
                df["Expected_monthly_installment"] = df["Expected_monthly_installment"].astype(int)
                df["Age"] = (((df["Date_of_loan_issue"] - df["Date_of_birth"]).dt.days)//365.25).astype(int)
                df = df.drop(columns =['id','name_of_borrower', 'email_of_borrower', 'highest_education_level','Line_of_business', 'Loan_purpose',
                                                   'employment_status', 'Loan_term_value','created','NIN', 'Phone_number',"Date_of_birth"])
                df['Interest_rate'] = df['Interest_rate']*12/100
                df["Loan_type"] = df["Loan_type"].str.replace(" Client", "")
                #Add Age Group
                df["Age_Group"] = np.where(df["Age"] > 35, "Non Youth", "Youth")
                
                #Add Sector
                # Create a dictionary of sectors and their key words
                sector_keywords = {
                    'Other': ['purchase of assets', 'marketing', 'restructuring of facility','memebership organisations','auto richshaw',
                              'portfolio', 'Portfolio Concentration', 'other activities', 'other services buying stock'],
                    'Enterprise/Business Development': ["trade",'merchandise','fertilizer & insecticide','stall','cottage industry',
                                                        'trading','retail','boutique','wholesale','hawk','business','working capital', 'sell',
                                                        'shop', 'agribusiness','buying stock','textiles,apparel and leather clothing',
                                                       'super market','buusiness'],
                    'Agriculture': ['agricult','crops', 'productionmaize','production rice', 'agro products','animal', 'farm', 'rearing', 
                                    'vegetable', 'fish','poultry','coffee','beef','cattle','banana','livestock','agro input','maize',
                                    'sugar cane production','diary production','fattening'],
                    'Technology': ['technology', 'software', 'hardware'],
                    'Finance / Financial Services': ['financ', 'banking', 'investment', 'mobile money', 'loan'],
                    'Health': ['health', 'medical', 'pharmac', 'diagnos'],
                    'Food & Beverage': ['bakery','maize processing','confection', 'fast food', 'restaurant', 'baker', 'cook'],
                    'Manufacturing': ['manufactur','factory'],
                    'Education & Skills': ['educat','school','tuition','train'],
                    'Refugees & Displaced Populations': ['refugee'],
                    'Tourism & Hospitality': ['hotel'],
                    'Innovation': ['handicraft', 'furniture','bamboo'],
                    'Services': ['saloon','laundry','mechanic', 'tailor', 'beauty', 'print', 'weaving'],
                    'Energy': ["coal", 'oil mill','energy'],
                    'Digital Economy': ["fax", 'digital economy'],
                    'Construction & Estates': ["rent",'construct', 'estate','house renovation','house completion'],
                    'Transport': ['transport', 'boda', 'motorcycle'],
                    'Mining': ['mining', 'mineral','quarry'],
                    # Add more sectors and their associated keywords as needed
                }
                
                # Create a new column 'sector' and initialize with 'Other'
                df['sector'] = 'not_defined'
                
                # Iterate over each row in the DataFrame
                for index, row in df.iterrows():
                    line_of_business = row['Sector'].lower()
                    
                    # Check for each sector's keywords in the 'line_of_business' column
                    for sector, keywords in sector_keywords.items():
                        for keyword in keywords:
                            if keyword in line_of_business:
                                df.at[index, 'sector'] = sector
                                break  # Exit the loop once a district is identified for the current row
                
                df.drop(columns="Sector", inplace=True)
                df.rename(columns={'sector': 'Sector'}, inplace=True)
        
        
        
                #Add Districts
                # Define your Districts and corresponding keywords
                district_keywords = {
                        'Kiruhura': ['kiruhura', 'kasaana', 'kinoni', 'rushere', 'kyabagyenyi','shwerenkye','kayonza', 'kikatsi',
                                     'kihwa','kiguma','burunga','rwanyangwe','nyakashashara','ekikoni'],
                        'Ibanda': ['ibanda', 'katongore','bihanga', 'rwetweka','mushunga','ishongororo', 'kikyenkye','nyakigando','nyarukiika',
                                   'kagongo','bwengure','kabaare'],
                        'Bushenyi': ['ishaka', 'bushenyi', 'kijumo','kabare','kakanju', 'nyamirembe','nkanga','nyabubare','bwekingo'],
                        'Isingiro': ['isingiro', 'bushozi','Kabaare','ngarama','rwembogo','kabuyanda'],
                        'Kazo': ['kazo', 'magondo', 'rwemikoma', 'kyabahura' 'Kyenshebashebe','ntambazi','kyabahura'],
                        'Kibingo': ['buringo', 'masheruka','bwayegamba'],
                        'Sheema': ['sheema','kabwohe', 'rwanama','mashojwa'],
                        'Ntungamo': ['ntungamo','kyaruhanga','rubaare','katomi'],
                        'Rukiga': ['rukiga', 'nyakambu','rwenyangye','kamwezi'],
                        'Kagadi':['kagadi'],
                        'Kabale': ['kabale', 'nyakashebeya'],
                        'Rubirizi': ['rubirizi','kichwamba'],
                        'Lyantonde': ['lyantonde'],
                        'Mubende': ['mubende'],
                        'Kitagwenda': ['kitagwenda'],
                        'Lwengo': ['lwengo'],
                        'Mayuge': ['mayuge'],
                        'Sironko': ['sironko'],
                        'Kibaale': ['kibale', 'kibaale'],
                        'Bukomansimbi': ['bukomansimbi'],
                        'Budaka': ['budaka'],
                        'Kole': ['kole'],
                        'Fort Portal':['fort portal'],
                        'Kanungu': ['kanungu'],
                        'Mitooma': ['mitooma']
                    
                    # Add more districts and their associated keywords as needed
                }
                
                # Create a new column 'district' and initialize with 'Other'
                df['District'] = 'Other'
                
                # Iterate over each row in the DataFrame
                for index, row in df.iterrows():
                    location = row['Location_of_borrower'].lower()
                    
                    # Check for each sector's keywords in the 'location' column
                    for district, keywords in district_keywords.items():
                        for keyword in keywords:
                            if keyword in location:
                                df.at[index, 'District'] = district
                                break  # Exit the loop once a sector is identified for the current row
                
                #Add Regions
                region_keywords = {
                        'Western': ['mbarara','fort portal','kagadi','kabale','rukungiri','ibanda','bushenyi','hoima','kyenjojo','kasese',
                                    'masindi','sheema','isingiro','buhweju','kibaale','kitagwenda','kamwenge','rubanda','ntungamo','kiruhura',
                                   'bundibugyo','kiryandongo','rubirizi','bunyangabu','rukiga','kyegegwa','kanungu','kazo','mitooma','kabalore',
                                   'kibingo','kabarole'],
                
                    # Add more regions and their associated keywords as needed
                }
                
                # Create a new column 'region' and initialize with 'Other'
                df['Region'] = 'Other'
                
                # Iterate over each row in the DataFrame
                for index, row in df.iterrows():
                    location = row['District'].lower()
                    
                    # Check for each district's keywords in the 'District' column
                    for region, district in region_keywords.items():
                        for keyword in district:
                            if keyword in location:
                                df.at[index, 'Region'] = region
                                break  # Exit the loop once a Region is identified for the current row

             


            #Data Cleaning Code for Finca
            elif df['lender'].iloc[0] == 'FINCA Uganda':
               
                #combine line of business and loan purpose to create sector
                df['Sector']= df['Line_of_business'] + " "+ df['Loan_purpose']
                df=df.drop(columns=['id','name_of_borrower','email_of_borrower','highest_education_level','employment_status',
                    'created','Date_of_birth','Loan_term_value','Line_of_business','Loan_purpose','NIN', 'Phone_number'])

                #align date columns
                df['Date_of_loan_issue']=pd.to_datetime(df['Date_of_loan_issue'])
                df['Date_of_repayments_commencement']=pd.to_datetime(df['Date_of_repayments_commencement'])
                
                #remove units in tenure of loans
                df['Tenure_of_loan']= df['Tenure_of_loan'].str.replace(' Month(s)','',regex=False).astype('Int64')
                
                #remove 'loans' in loan type
                df['Loan_type']= df['Loan_type'].str.replace(' loan','',regex=False)
                
                #change M to male and F to female
                df['Gender']= df['Gender'].str.replace('F','Female',regex=False)
                df['Gender']= df['Gender'].str.replace('M','Male',regex=False)
                
                #change interest rate to % without units
                df['Interest_rate']= (df['Interest_rate'].str.replace('%','',regex=False).astype(float))/100
                
                #change Expected_number_of_installments, Number_of_employees, Annual_revenue_of_borrower, Length_of_time_running, Person_with_disabilities, Number_of_employees_that_are_refugees, Number_of_female_employees, Previously_unemployed, Number_of_employees_with_disabilities to integers
                df['Expected_number_of_installments']= df['Expected_number_of_installments'].str.replace(' Month(s)','',regex=False).astype('Int64')
                df['Number_of_employees']= df['Number_of_employees'].round(0).astype('Int64')
                df['Annual_revenue_of_borrower']= df['Annual_revenue_of_borrower'].astype('Int64')
                df['Length_of_time_running']= df['Length_of_time_running'].astype('Int64')
                df['Person_with_disabilities']= df['Person_with_disabilities'].astype('str')
                df['Number_of_employees_that_are_refugees']= df['Number_of_employees_that_are_refugees'].round(0).astype('Int64')
                df['Number_of_female_employees']= df['Number_of_female_employees'].astype('Int64')
                df['Previously_unemployed']= df['Previously_unemployed'].astype('Int64')
                df['Number_of_employees_with_disabilities']= df['Number_of_employees_with_disabilities'].astype('Int64')
                
                #change Loan_ID and Borrower_ID to string
                df['Loan_ID']= df['Loan_ID'].astype('str')
                df['Borrower_ID']= df['Borrower_ID'].astype('str')

            
                # Create age group column
                df["Age_Group"] = np.where(df["Age"] > 35, "Non Youth", "Youth")
                
                
                
                
                # Create a dictionary of sectors and their key words
                sector_keywords = {
                    'Other': ['other','purchase of assets', 'marketing', 'restructuring of facility','memebership organisations','auto richshaw',
                              'portfolio', 'Portfolio Concentration', 'other activities', 'other services buying stock','other other'],
                    'Enterprise/Business Development': ["trade",'merchandise','fertilizer & insecticide','stall','cottage industry',
                                                        'trading','retail','boutique','wholesale','hawk','business','working capital', 'sell',
                                                        'shop', 'agribusiness','buying stock','textiles,apparel and leather clothing','textile'],
                    'Agriculture': ['agricult','crops', 'productionmaize','production rice', 'agro products','animal', 'farm', 'rearing', 
                                    'vegetable', 'fish','poultry','coffee','beef','cattle','banana','livestock','agro input','maize',
                                    'sugar cane production','diary production','fattening','irish','legume'],
                    'Technology': ['technology', 'software', 'hardware'],
                    'Finance / Financial Services': ['financ', 'banking', 'investment', 'mobile money', 'loan'],
                    'Health': ['health', 'medical', 'pharmac', 'diagnos'],
                    'Food & Beverage': ['bakery','maize processing','confection', 'fast food', 'restaurant', 'baker', 'cook','bar','disco','beverage'],
                    'Manufacturing': ['manufactur','factory'],
                    'Education & Skills': ['educat','school','tuition','train'],
                    'Refugees & Displaced Populations': ['refugee'],
                    'Tourism & Hospitality': ['hotel','tour'],
                    'Innovation': ['handicraft', 'furniture','bamboo'],
                    'Services': ['airtime','welding','saloon','laundry','mechanic', 'tailor', 'beauty', 'print', 'weaving'],
                    'Energy': ["coal", 'oil mill','energy'],
                    'Digital Economy': ["fax", 'digital economy'],
                    'Construction & Estates': ["rent",'construct', 'estate','house renovation','house completion','carpentry', 'house improveme'],
                    'Transport': ['transport', 'boda', 'motorcycle'],
                    'Mining': ['mining', 'mineral','quarry'],
                    # Add more sectors and their associated keywords as needed
                }
                
                # Create a new column 'sector' and initialize with 'Other'
                df['sector'] = 'not_defined'
                
                # Iterate over each row in the DataFrame
                for index, row in df.iterrows():
                    line_of_business = row['Sector'].lower()
                    
                    # Check for each sector's keywords in the 'line_of_business' column
                    for sector, keywords in sector_keywords.items():
                        for keyword in keywords:
                            if keyword in line_of_business:
                                df.at[index, 'sector'] = sector
                                break  # Exit the loop once a sector is identified for the current row
                            
                
                df.drop(columns="Sector", inplace=True)
                df.rename(columns={'sector': 'Sector'}, inplace=True)
                
                
                
                
                # Define your Districts and corresponding keywords
                district_keywords = {
                        'Mbarara': ['mbarara', 'kinoni t/c', 'kitunguru', 'ruhunga','rubaya', 'bwizibwera', 'kakoba', 'rwebishekye', 
                                    'rwanyamahembe', 'kakoba', 'rwentondo', 'rubingo','rukiro', 'kashari', 'rwentojo', 'nyarubungo','bukiro',
                                    'katyazo', 'rutooma', 'ngango','kagongi', 'nkaaka', 'rugarama','katete','nyamitanga', 'mwizi','rwampara',
                                    'omukagyera,','mirongo','Kashare', 'omukagyera','kamushoko', 'bubaare','kyantamba', 'rwanyampazi','kamukuzi',
                                   'kashaka','kobwoba','igorora t/c','ntuura','kashenyi','nyabisirira','rubindi','byanamira','nchune','kariro',
                                    'rwebikoona','mitoozo','bunenero','nyantungu'],
                        'Kampala': ['kampala', 'ben kiwanuka', 'nateete', 'katwe','city centre','kawempe','kabalagala','nakulabye','nakawa',
                                    'entebbe road','wandegeya', 'ntinda', 'acacia', 'bukoto'],
                        'Kiruhura': ['kiruhura', 'kasaana', 'kinoni', 'rushere', 'kyabagyenyi','shwerenkye','kayonza', 'kikatsi',
                                     'kihwa','kiguma','burunga','rwanyangwe','nyakashashara','ekikoni'],
                        'Ibanda': ['ibanda', 'katongore','bihanga', 'rwetweka','mushunga','ishongororo', 'kikyenkye','nyakigando','nyarukiika',
                                   'kagongo','bwengure','kabaare'],
                        'Bushenyi': ['ishaka', 'bushenyi', 'kijumo','kabare','kakanju', 'nyamirembe','nkanga','nyabubare','bwekingo'],
                        'Isingiro': ['isingiro', 'bushozi','Kabaare','ngarama','rwembogo','kabuyanda'],
                        'Kazo': ['kazo', 'magondo', 'rwemikoma', 'kyabahura' 'Kyenshebashebe','ntambazi','kyabahura'],
                        'Wakiso': ['wakiso', 'kyaliwajjala', 'nansana', 'entebbe', 'abayita', 'kireka'],
                        'Kibingo': ['buringo', 'masheruka','bwayegamba'],
                        'Sheema': ['sheema','kabwohe', 'rwanama','mashojwa'],
                        'Ntungamo': ['ntungamo','kyaruhanga','rubaare','katomi'],
                        'Rukiga': ['rukiga', 'nyakambu','rwenyangye','kamwezi'],
                        'Kamwenge': ['kamwenge', 'kyabandara','bwizi t c'],
                        'Masaka': ['masaka'],
                        'Rukungiri': ['rukungiri'],
                        'Iganga': ['iganga'],
                        'Buikwe': ['buikwe','lugazi'],
                        'Bugiri': ['bugiri'],
                        'Soroti': ['soroti'],
                        'Kagadi':['kagadi'],
                        'Kabale': ['kabale', 'nyakashebeya'],
                        'Gulu': ['gulu'],
                        'Kayunga': ['kayunga'],
                        'Mbale': ['mbale'],
                        'Pader': ['pader'],
                        'Kamuli': ['kamuli'],
                        'Namayingo': ['namayingo'],
                        'Koboko': ['koboko'],
                        'Mityana': ['mityana'],
                        'Hoima': ['hoima'],
                        'Nakasongola': ['nakasongola'],
                        'Kasese': ['kasese', 'bwera'],
                        'Lira': ['lira'],
                        'Mukono': ['mukono'],
                        'Kyenjojo': ['kyenjojo'],
                        'Masindi': ['masindi'],
                        'Buhweju': ['buhweju','kabegaramire'],
                        'Butambala': ['butambala','kalamba'],
                        'Rakai': ['rakai'],
                        'Mpigi': ['mpigi'],
                        'Sembabule': ['sembabule', 'sembambule'],
                        'Arua': ['arua'],
                        'Rubanda': ['rubanda'],
                        'Gomba': ['gomba'],
                        'Bundibugyo': ['bundibugyo'],
                        'Kiryandongo': ['kiryandongo', 'bweyale'],
                        'Oyam': ['oyam'],
                        'Mitooma': ['mitooma'],
                        'Rubirizi': ['rubirizi','kichwamba'],
                        'Lyantonde': ['lyantonde'],
                        'Bukwo': ['bukwo','bukwa'],
                        'Busia': ['busia'],
                        'Mubende': ['mubende'],
                        'Kitagwenda': ['kitagwenda'],
                        'Lwengo': ['lwengo'],
                        'Mayuge': ['mayuge'],
                        'Sironko': ['sironko'],
                        'Kibaale': ['kibale', 'kibaale'],
                        'Bukomansimbi': ['bukomansimbi'],
                        'Budaka': ['budaka'],
                        'Kole': ['kole'],
                        'Fort Portal':['fort portal'],
                        'Bulambuli': ['bulambuli'],
                        'Luwero': ['luwero'],
                        'Tororo': ['tororo'],
                        'Serere': ['serere'],
                        'Bunyangabu': ['bunyangabu'],
                        'Pallisa': ['pallisa'],
                        'Manafwa': ['manafwa'],
                        'Kalungu': ['kalungu'],
                        'Kyegegwa': ['kyegegwa'],
                        'Kumi': ['kumi'],
                        'Kakumiro': ['kakumiro'],
                        'Kitgum': ['kitgum'],
                        'Kanungu': ['kanungu'],
                        'Kiboga': ['kiboga'],
                        'Kapchorwa': ['kapchorwa'],
                        'Kaliro': ['kaliro'],
                        'Dokolo': ['dokolo'],
                        'Apac': ['apac'],
                        'Kabalore': ['nyamirima'],
                        'Zombo': ['zombo'],
                        'Nebbi': ['nebbi'],
                        'Alebtong':['alebtong'],
                        'Kibuku':['kibuku'],
                        'Kyotera': ['kyotera','buwenge'],
                        'Jinja': ['jinja'],
                        'Kabarole': ['kabarole'],
                        'Buvuma': ['buvuma'],
                        'Notavailable': ['notavailable']
                    
                    # Add more districts and their associated keywords as needed
                }
                
                # Create a new column 'district' and initialize with 'Other'
                df['District'] = 'Other'
                
                # Iterate over each row in the DataFrame
                for index, row in df.iterrows():
                    location = row['Location_of_borrower'].lower()
                    
                    # Check for each sector's keywords in the 'location' column
                    for district, keywords in district_keywords.items():
                        for keyword in keywords:
                            if keyword in location:
                                df.at[index, 'District'] = district
                                break  # Exit the loop once a sector is identified for the current row




                region_keywords = {
                        'Western': ['mbarara','fort portal','kagadi','kabale','rukungiri','ibanda','bushenyi','hoima','kyenjojo','kasese',
                                    'masindi','sheema','isingiro','buhweju','kibaale','kitagwenda','kamwenge','rubanda','ntungamo','kiruhura',
                                   'bundibugyo','kiryandongo','rubirizi','bunyangabu','rukiga','kyegegwa','kanungu','kazo','mitooma','kabalore',
                                   'kibingo','kabarole'],
                        'Eastern': ['jinja','iganga','bugiri','soroti','mbale','kamuli','namayingo','sironko','budaka','busia','bukwo',
                                    'bulambuli','tororo','serere','pallisa','manafwa','kumi','kapchorwa','kaliro','kibuku'],
                        'Central': ['kampala','luwero','kyotera','masaka','kayunga','mityana','sembabule','nakasongola','mukono','bukomansimbi',
                                   'rakai','wakiso','mpigi','buikwe','gomba','lwengo','mayuge','butambala','lyantonde','mubende','kalungu',
                                    'kiboga','butambala','buvuma'],
                        'Northern': ['gulu','pader','koboko','lira','arua','oyam','kole','zombo','nebbi','kitgum','dokolo','apac','alebtong'],
                        'Other': ['notavailable']
                
                    # Add more regions and their associated keywords as needed
                }
                
                # Create a new column 'region' and initialize with 'Other'
                df['Region'] = 'Other'
                
                # Iterate over each row in the DataFrame
                for index, row in df.iterrows():
                    location = row['District'].lower()
                    
                    # Check for each district's keywords in the 'District' column
                    for region, district in region_keywords.items():
                        for keyword in district:
                            if keyword in location:
                                df.at[index, 'Region'] = region
                                break  # Exit the loop once a sector is identified for the current row







            
            #Data Cleaning Code for Lyamujungu SACCO
            elif df['lender'].iloc[0] == 'Lyamujungu SACCO':
                
                df["Sector"] = df['Line_of_business'] + ' ' + df['Loan_purpose']
                df = df.drop(columns =['id','name_of_borrower', 'email_of_borrower', 'highest_education_level','employment_status',
                                           'Date_of_birth','Loan_term_value','created','NIN', 'Phone_number','Line_of_business','Loan_purpose'])
                df['Number_of_youth_employees'] = pd.to_numeric(df['Number_of_youth_employees'] ,errors='coerce')
                df['Number_of_employees_that_are_refugees'] = pd.to_numeric(df['Number_of_employees_that_are_refugees'] ,errors='coerce')
                df['Number_of_female_employees'] = pd.to_numeric(df['Number_of_female_employees'] ,errors='coerce')
                df['Previously_unemployed'] = pd.to_numeric(df['Previously_unemployed'] ,errors='coerce')
                df['Number_of_employees_with_disabilities'] = pd.to_numeric(df['Number_of_employees_with_disabilities'] ,errors='coerce')
                df['Interest_rate'] = df['Interest_rate']/100
                df['Loan_product_name'] = df['Loan_product_name'].str.replace("1-1-2-20 ","")
                df["Date_of_loan_issue"] = pd.to_datetime(df["Date_of_loan_issue"])
                
                df["Length_of_time_running"] = pd.to_datetime(df["Length_of_time_running"], errors='coerce')
                df["Length_of_time_running"] = df["Date_of_loan_issue"] - df["Length_of_time_running"]
                df["Length_of_time_running"] = (df["Length_of_time_running"].dt.days//365).astype("Int64")
                df["Date_of_repayments_commencement"] = pd.to_datetime(df["Date_of_repayments_commencement"], errors='coerce')
                df['Tenure_of_loan'] = (df['Tenure_of_loan']/30).astype(int)
                df['Rural_urban'] = df['Rural_urban'].replace("0","")
                df['Number_of_employees'] = (pd.to_numeric(df['Number_of_employees'], errors='coerce')).astype("Int64")
                df['Loan_amount'] = pd.to_numeric(df['Loan_amount'].str.replace(",","")).astype(int)
                df['Expected_monthly_installment'] = pd.to_numeric(df['Expected_monthly_installment'].str.replace(",","")).astype(int)
                df['Person_with_disabilities'] = df['Person_with_disabilities'].str.replace('false','No')
                df["Annual_revenue_of_borrower"] = pd.to_numeric(df["Annual_revenue_of_borrower"], errors='coerce')
                df["Annual_revenue_of_borrower"] = df["Annual_revenue_of_borrower"].astype("Int64")
                df["Age_Group"] = np.where(df["Age"] > 35, "Non Youth", "Youth")
                
                #AddSectors
                # Create a dictionary of sectors and their key words
                sector_keywords = {
                    'Other': ['purchase of assets', 'marketing', 'restructuring of facility','memebership organisations','auto richshaw',
                              'portfolio', 'Portfolio Concentration', 'other activities', 'other services buying stock'],
                    'Enterprise/Business Development': ["trade",'merchandise','fertilizer & insecticide','stall','cottage industry',
                                                        'trading','retail','boutique','wholesale','hawk','business','working capital', 'sell',
                                                        'shop', 'agribusiness','buying stock','textiles,apparel and leather clothing',
                                                       'super market'],
                    'Agriculture': ['agricult','crops', 'productionmaize','production rice', 'agro products','animal', 'farm', 'rearing', 
                                    'vegetable', 'fish','poultry','coffee','beef','cattle','banana','livestock','agro input','maize',
                                    'sugar cane production','diary production','fattening'],
                    'Technology': ['technology', 'software', 'hardware'],
                    'Finance / Financial Services': ['financ', 'banking', 'investment', 'mobile money', 'loan'],
                    'Health': ['health', 'medical', 'pharmac', 'diagnos'],
                    'Food & Beverage': ['bakery','maize processing','confection', 'fast food', 'restaurant', 'baker', 'cook'],
                    'Manufacturing': ['manufactur','factory'],
                    'Education & Skills': ['educat','school','tuition','train'],
                    'Refugees & Displaced Populations': ['refugee'],
                    'Tourism & Hospitality': ['hotel'],
                    'Innovation': ['handicraft', 'furniture','bamboo'],
                    'Services': ['saloon','laundry','mechanic', 'tailor', 'beauty', 'print', 'weaving'],
                    'Energy': ["coal", 'oil mill','energy'],
                    'Digital Economy': ["fax", 'digital economy'],
                    'Construction & Estates': ["rent",'construct', 'estate','house renovation','house completion'],
                    'Transport': ['transport', 'boda', 'motorcycle'],
                    'Mining': ['mining', 'mineral','quarry'],
                    # Add more sectors and their associated keywords as needed
                }
                
                # Create a new column 'sector' and initialize with 'Other'
                df['sector'] = 'not_defined'
                
                # Iterate over each row in the DataFrame
                for index, row in df.iterrows():
                    line_of_business = row['Sector'].lower()
                    
                    # Check for each sector's keywords in the 'line_of_business' column
                    for sector, keywords in sector_keywords.items():
                        for keyword in keywords:
                            if keyword in line_of_business:
                                df.at[index, 'sector'] = sector
                                break  # Exit the loop once a sector is identified for the current row
            
                df.drop(columns="Sector", inplace=True)
                df.rename(columns={'sector': 'Sector'}, inplace=True)
            
            
                #Add Districts
                # Define your Districts and corresponding keywords
                district_keywords = {
                        'Kiruhura': ['kiruhura', 'kasaana', 'kinoni', 'rushere', 'kyabagyenyi','shwerenkye','kayonza', 'kikatsi',
                                     'kihwa','kiguma','burunga','rwanyangwe','nyakashashara','ekikoni'],
                        'Ibanda': ['ibanda', 'katongore','bihanga', 'rwetweka','mushunga','ishongororo', 'kikyenkye','nyakigando','nyarukiika',
                                   'kagongo','bwengure','kabaare'],
                        'Bushenyi': ['ishaka', 'bushenyi', 'kijumo','kabare','kakanju', 'nyamirembe','nkanga','nyabubare','bwekingo'],
                        'Isingiro': ['isingiro', 'bushozi','Kabaare','ngarama','rwembogo','kabuyanda'],
                        'Kazo': ['kazo', 'magondo', 'rwemikoma', 'kyabahura' 'Kyenshebashebe','ntambazi','kyabahura'],
                        'Kibingo': ['buringo', 'masheruka','bwayegamba'],
                        'Sheema': ['sheema','kabwohe', 'rwanama','mashojwa'],
                        'Ntungamo': ['ntungamo','kyaruhanga','rubaare','katomi'],
                        'Rukiga': ['rukiga', 'nyakambu','rwenyangye','kamwezi'],
                        'Kagadi':['kagadi'],
                        'Kabale': ['kabale', 'nyakashebeya'],
                        'Rubirizi': ['rubirizi','kichwamba'],
                        'Lyantonde': ['lyantonde'],
                        'Mubende': ['mubende'],
                        'Kitagwenda': ['kitagwenda'],
                        'Lwengo': ['lwengo'],
                        'Mayuge': ['mayuge'],
                        'Sironko': ['sironko'],
                        'Kibaale': ['kibale', 'kibaale'],
                        'Bukomansimbi': ['bukomansimbi'],
                        'Budaka': ['budaka'],
                        'Kole': ['kole'],
                        'Fort Portal':['fort portal'],
                        'Kanungu': ['kanungu']
                    
                    # Add more districts and their associated keywords as needed
                }
                
                # Create a new column 'district' and initialize with 'Other'
                df['District'] = 'Other'
                
                # Iterate over each row in the DataFrame
                for index, row in df.iterrows():
                    location = row['Location_of_borrower'].lower()
                    
                    # Check for each district's keywords in the 'location' column
                    for district, keywords in district_keywords.items():
                        for keyword in keywords:
                            if keyword in location:
                                df.at[index, 'District'] = district
                                break  # Exit the loop once a district is identified for the current row
            
                #Add Regions:
                region_keywords = {
                        'Western': ['mbarara','fort portal','kagadi','kabale','rukungiri','ibanda','bushenyi','hoima','kyenjojo','kasese',
                                    'masindi','sheema','isingiro','buhweju','kibaale','kitagwenda','kamwenge','rubanda','ntungamo','kiruhura',
                                   'bundibugyo','kiryandongo','rubirizi','bunyangabu','rukiga','kyegegwa','kanungu','kazo','mitooma','kabalore',
                                   'kibingo','kabarole'],
                
                    # Add more regions and their associated keywords as needed
                }
                
                # Create a new column 'region' and initialize with 'Other'
                df['Region'] = 'Other'
                
                # Iterate over each row in the DataFrame
                for index, row in df.iterrows():
                    location = row['District'].lower()
                    
                    # Check for each district's keywords in the 'District' column
                    for region, district in region_keywords.items():
                        for keyword in district:
                            if keyword in location:
                                df.at[index, 'Region'] = region
                                break  # Exit the loop once a Region is identified for the current row
                                
                                
                                
                                
                                
                                
                                
            #Data Cleaning Code for Flow Uganda                   
            elif df['lender'].iloc[0] == 'Flow Uganda':
                #to the Flow_Data DataFrame and drop the Original Columns
                df["Sector"] = df['Line_of_business'] + " " + df['Loan_purpose']
                df = df.drop(columns =['id','name_of_borrower', 'email_of_borrower', 'highest_education_level','Line_of_business', 'Loan_purpose',
                                           'employment_status', 'Loan_term_value','created','NIN', 'Phone_number', "Date_of_birth"])
                
                #Convert Duration to Total Years
                df['Length_of_time_running'] = df['Length_of_time_running'].fillna(' ')
                def convert_to_years(duration):
                    parts = duration.split()
                    if len(parts) == 4:
                        total_years = int(parts[0]) + int(parts[2])//12
                    elif len(parts) == 2 and parts[1] == 'months':
                        total_years = int(parts[0])//12
                    else:
                        total_years = 0
                    return total_years
                
                # Apply the function to the 'duration' column
                df['Length_of_time_running'] = df['Length_of_time_running'].apply(convert_to_years)
                #Change Data Type
                df["Date_of_loan_issue"] = pd.to_datetime(df["Date_of_loan_issue"])
                df["Date_of_repayments_commencement"] = pd.to_datetime(df["Date_of_repayments_commencement"])
                df['Gender'] = df['Gender'].str.title()
                df['Tenure_of_loan'] = (df['Tenure_of_loan']/30).round(2)
                df['Interest_rate'] = (df['Interest_rate']/df['Loan_amount'])*12/df['Tenure_of_loan']
                df['Loan_type'] = df['Loan_type'].replace('SME','')
                df['Age'] = df['Age'].astype(int)
                df["Person_with_disabilities"] = df["Person_with_disabilities"].str.title()
                
                #Add Age Group Column 
                df["Age_Group"] = np.where(df["Age"] > 35, "Non Youth", "Youth")
                

                # Create a dictionary of sectors and their key words
                sector_keywords = {
                    'Other': ['purchase of assets', 'marketing', 'restructuring of facility','memebership organisations','auto richshaw',
                              'portfolio', 'Portfolio Concentration', 'other activities', 'other services buying stock'],
                    'Enterprise/Business Development': ["trade",'merchandise','fertilizer & insecticide','stall','cottage industry',
                                                        'trading','retail','boutique','wholesale','hawk','business','working capital', 'sell',
                                                        'shop', 'agribusiness','buying stock','textiles,apparel and leather clothing',
                                                       'super market'],
                    'Agriculture': ['agricult','crops', 'productionmaize','production rice', 'agro products','animal', 'farm', 'rearing', 
                                    'vegetable', 'fish','poultry','coffee','beef','cattle','banana','livestock','agro input','maize',
                                    'sugar cane production','diary production','fattening'],
                    'Technology': ['technology', 'software', 'hardware'],
                    'Finance / Financial Services': ['financ', 'banking', 'investment', 'mobile money', 'loan'],
                    'Health': ['health', 'medical', 'pharmac', 'diagnos'],
                    'Food & Beverage': ['bakery','maize processing','confection', 'fast food', 'restaurant', 'baker', 'cook'],
                    'Manufacturing': ['manufactur','factory'],
                    'Education & Skills': ['educat','school','tuition','train'],
                    'Refugees & Displaced Populations': ['refugee'],
                    'Tourism & Hospitality': ['hotel'],
                    'Innovation': ['handicraft', 'furniture','bamboo'],
                    'Services': ['saloon','laundry','mechanic', 'tailor', 'beauty', 'print', 'weaving'],
                    'Energy': ["coal", 'oil mill','energy'],
                    'Digital Economy': ["fax", 'digital economy'],
                    'Construction & Estates': ["rent",'construct', 'estate','house renovation','house completion'],
                    'Transport': ['transport', 'boda', 'motorcycle'],
                    'Mining': ['mining', 'mineral','quarry'],
                    # Add more sectors and their associated keywords as needed
                }
                
                # Create a new column 'sector' and initialize with 'Other'
                df['sector'] = 'not_defined'
                
                # Iterate over each row in the DataFrame
                for index, row in df.iterrows():
                    line_of_business = row['Sector'].lower()
                    
                    # Check for each sector's keywords in the 'line_of_business' column
                    for sector, keywords in sector_keywords.items():
                        for keyword in keywords:
                            if keyword in line_of_business:
                                df.at[index, 'sector'] = sector
                                break  # Exit the loop once a sector is identified for the current row
                                                


                # Delete the Original 'Sector' Column
                df.drop(columns="Sector", inplace=True)
                df.rename(columns={'sector': 'Sector'}, inplace=True)
                
                
                
                # Define your Districts and corresponding keywords
                district_keywords = {
                        "Moyo": ["moyo"],
                        'Buikwe': ['buikwe','lugazi'],
                        'Bugiri': ['bugiri'],
                        'Soroti': ['soroti'],
                        'Kagadi':['kagadi'],
                        'Gulu': ['gulu'],
                        'Kayunga': ['kayunga'],
                        'Mbale': ['mbale'],
                        'Pader': ['pader'],
                        'Kamuli': ['kamuli'],
                        'Namayingo': ['namayingo'],
                        'Koboko': ['koboko'],
                        'Mityana': ['mityana'],
                        'Hoima': ['hoima'],
                        'Nakasongola': ['nakasongola'],
                        'Lira': ['lira'],
                        'Butambala': ['butambala','kalamba'],
                        'Rakai': ['rakai'],
                        'Mpigi': ['mpigi'],
                        'Sembabule': ['sembabule', 'sembambule'],
                        'Arua': ['arua'],
                        'Gomba': ['gomba'],
                        'Bundibugyo': ['bundibugyo'],
                        'Kiryandongo': ['kiryandongo', 'bweyale'],
                        'Oyam': ['oyam'],
                        'Bukwo': ['bukwo','bukwa'],
                        'Lwengo': ['lwengo'],
                        'Mayuge': ['mayuge'],
                        'Sironko': ['sironko'],
                        'Kibaale': ['kibale', 'kibaale'],
                        'Bukomansimbi': ['bukomansimbi'],
                        'Budaka': ['budaka'],
                        'Bulambuli': ['bulambuli'],
                        'Luwero': ['luwero'],
                        'Tororo': ['tororo'],
                        'Serere': ['serere'],
                        'Bunyangabu': ['bunyangabu'],
                        'Pallisa': ['pallisa'],
                        'Manafwa': ['manafwa'],
                        'Kalungu': ['kalungu'],
                        'Kyegegwa': ['kyegegwa','kyeggegwa'],
                        'Kumi': ['kumi'],
                        'Kakumiro': ['kakumiro'],
                        'Kitgum': ['kitgum'],
                        'Kanungu': ['kanungu'],
                        'Kiboga': ['kiboga'],
                        'Kapchorwa': ['kapchorwa'],
                        'Kaliro': ['kaliro'],
                        'Dokolo': ['dokolo'],
                        'Apac': ['apac'],
                        'Kabalore': ['nyamirima'],
                        'Zombo': ['zombo'],
                        'Nebbi': ['nebbi'],
                        'Alebtong':['alebtong'],
                        'Kibuku':['kibuku'],
                        'Kyotera': ['kyotera','buwenge'],
                        'Jinja': ['jinja'],
                        'Kabarole': ['kabarole'],
                        'Buvuma': ['buvuma'],
                        "Yumbe": ["yumbe"],
                        "Obongi": ["obongi"],
                        "Adjumani": ["adjumani"],
                        "Amuru": ["amuru"],
                        "Katakwi": ["katakwii"],
                        "Amuria": ["amuria"],
                        "Bududa": ["bududa"],
                        'Bukedea': ["bukedea"],
                        "Nakaseke": ["nakaseke"],
                        "Omoro": ["omoro"],
                        "Kyankwanzi": ["kyankwanzi"],
                        "Kasanda": ["kasanda"],
                        'Kaberamaido': ['kaberamaido'],
                        'Luuka': ['luuka'],
                        'Butaleja': ['butaleja'],
                        'Amolatar': ['amolatar'],
                        'Iganga': ['iganga'],
                        'Buyende': ['buyende'],
                        'Ngora': ['ngora'],
                        'Busia': ['busia']
    
                    # Add more districts and their associated keywords as needed
                }
                
                # Create a new column 'district' and initialize with 'Other'
                df['District'] = 'Other'
                
                # Iterate over each row in the DataFrame
                for index, row in df.iterrows():
                    location = row['Location_of_borrower'].lower()
                    
                    # Check for each sector's keywords in the 'location' column
                    for district, keywords in district_keywords.items():
                        for keyword in keywords:
                            if keyword in location:
                                df.at[index, 'District'] = district
                                break  # Exit the loop once a sector is identified for the current row
                


                region_keywords = {
                
                        'Eastern': ['jinja','iganga','bugiri','soroti','mbale','kamuli','namayingo','sironko','budaka','busia','bukwo',
                                    'bulambuli','tororo','serere','pallisa','manafwa','kumi','kapchorwa','kaliro','kibuku','katakwi',"amuria",
                                   "bududa",'bukedea','luuka', 'kaberamaido','butaleja','iganga','ngora','buikwe','mayuge'],
                
                        'Northern': ['gulu','pader','koboko','lira','arua','oyam','kole','zombo','nebbi','kitgum','dokolo','apac','alebtong',
                                    'yumbe',"obongi","moyo", 'adjumani','omoro','amuru','amolatar']
                
                    # Add more regions and their associated keywords as needed
                }
                
                # Create a new column 'region' and initialize with 'Other'
                df['Region'] = 'Other'
                
                # Iterate over each row in the DataFrame
                for index, row in df.iterrows():
                    location = row['District'].lower()
                    
                    # Check for each district's keywords in the 'District' column
                    for region, district in region_keywords.items():
                        for keyword in district:
                            if keyword in location:
                                df.at[index, 'Region'] = region
                                break  # Exit the loop once a sector is identified for the current row
                






            #Data Cleaning Code for Vision Fund                   
            else:
                df["Sector"] = df['Line_of_business'] + " " + df['Loan_purpose']
                df = df.drop(columns = ['Line_of_business', 'Loan_purpose'])
                df = df.drop(columns =['id','name_of_borrower', 'email_of_borrower', 'highest_education_level',
                                           'employment_status', 'Loan_term_value','created','NIN', 'Phone_number',"Date_of_birth"])
                df["Borrower_ID"] = df["Borrower_ID"].astype(str)
                df["Date_of_loan_issue"] = pd.to_datetime(df["Date_of_loan_issue"])
                df["Date_of_repayments_commencement"] = pd.to_datetime(df["Date_of_repayments_commencement"])
                df['Interest_rate'] = df['Interest_rate']*12/100
                df["Gender"] = df["Gender"].str.title()
                df["Person_with_disabilities"] = df["Person_with_disabilities"].str.title()
                df["Rural_urban"] = df["Rural_urban"].str.title()
                df["Length_of_time_running"] = df["Length_of_time_running"]//12
                
                #Add Age Group Column 
                df["Age_Group"] = np.where(df["Age"] > 35, "Non Youth", "Youth")
                
                
                # Create a dictionary of sectors and their key words
                sector_keywords = {
                    'Other': ['purchase of assets', 'marketing', 'restructuring of facility','memebership organisations','auto richshaw',
                              'portfolio', 'Portfolio Concentration', 'other activities', 'other services buying stock'],
                    'Enterprise/Business Development': ["trade",'merchandise','fertilizer & insecticide','stall','cottage industry',
                                                        'trading','retail','boutique','wholesale','hawk','business','working capital', 'sell',
                                                        'shop', 'agribusiness','buying stock','textiles,apparel and leather clothing',
                                                       'super market'],
                    'Agriculture': ['agricult','crops', 'productionmaize','production rice', 'agro products','animal', 'farm', 'rearing', 
                                    'vegetable', 'fish','poultry','coffee','beef','cattle','banana','livestock','agro input','maize',
                                    'sugar cane production','diary production','fattening'],
                    'Technology': ['technology', 'software', 'hardware'],
                    'Finance / Financial Services': ['financ', 'banking', 'investment', 'mobile money', 'loan'],
                    'Health': ['health', 'medical', 'pharmac', 'diagnos'],
                    'Food & Beverage': ['bakery','maize processing','confection', 'fast food', 'restaurant', 'baker', 'cook'],
                    'Manufacturing': ['manufactur','factory'],
                    'Education & Skills': ['educat','school','tuition','train'],
                    'Refugees & Displaced Populations': ['refugee'],
                    'Tourism & Hospitality': ['hotel'],
                    'Innovation': ['handicraft', 'furniture','bamboo'],
                    'Services': ['saloon','laundry','mechanic', 'tailor', 'beauty', 'print', 'weaving'],
                    'Energy': ["coal", 'oil mill','energy'],
                    'Digital Economy': ["fax", 'digital economy'],
                    'Construction & Estates': ["rent",'construct', 'estate','house renovation','house completion'],
                    'Transport': ['transport', 'boda', 'motorcycle'],
                    'Mining': ['mining', 'mineral','quarry'],
                    # Add more sectors and their associated keywords as needed
                }
                
                # Create a new column 'sector' and initialize with 'Other'
                df['sector'] = 'not_defined'
                
                # Iterate over each row in the DataFrame
                for index, row in df.iterrows():
                    line_of_business = row['Sector'].lower()
                    
                    # Check for each sector's keywords in the 'line_of_business' column
                    for sector, keywords in sector_keywords.items():
                        for keyword in keywords:
                            if keyword in line_of_business:
                                df.at[index, 'sector'] = sector
                                break  # Exit the loop once a sector is identified for the current row

                # Delete the Original 'Sector' Column
                df.drop(columns="Sector", inplace=True)
                df.rename(columns={'sector': 'Sector'}, inplace=True)



                # Define your Districts and corresponding keywords
                district_keywords = {
                        "Moyo": ["moyo"],
                        'Mbarara': ['mbarara'],
                        'Kampala': ['kampala'],
                        'Kiruhura': ['kiruhura'],
                        'Ibanda': ['ibanda'],
                        'Bushenyi': ['ishaka', 'bushenyi'],
                        'Isingiro': ['isingiro'],
                        'Kazo': ['kazo'],
                        'Wakiso': ['wakiso', 'kyaliwajjala', 'nansana', 'entebbe', 'abayita', 'kireka'],
                        'Kibingo': ['buringo', 'masheruka','bwayegamba'],
                        'Sheema': ['sheema','kabwohe', 'rwanama','mashojwa'],
                        'Ntungamo': ['ntungamo','kyaruhanga','rubaare','katomi'],
                        'Rukiga': ['rukiga', 'nyakambu','rwenyangye','kamwezi'],
                        'Kamwenge': ['kamwenge', 'kyabandara','bwizi t c'],
                        'Masaka': ['masaka'],
                        'Rukungiri': ['rukungiri'],
                        'Iganga': ['iganga'],
                        'Buikwe': ['buikwe','lugazi'],
                        'Bugiri': ['bugiri'],
                        'Soroti': ['soroti'],
                        'Kagadi':['kagadi'],
                        'Kabale': ['kabale', 'nyakashebeya'],
                        'Gulu': ['gulu'],
                        'Kayunga': ['kayunga'],
                        'Mbale': ['mbale'],
                        'Pader': ['pader'],
                        'Kamuli': ['kamuli'],
                        'Namayingo': ['namayingo'],
                        'Koboko': ['koboko'],
                        'Mityana': ['mityana'],
                        'Hoima': ['hoima'],
                        'Nakasongola': ['nakasongola'],
                        'Kasese': ['kasese', 'bwera'],
                        'Lira': ['lira'],
                        'Mukono': ['mukono'],
                        'Kyenjojo': ['kyenjojo'],
                        'Masindi': ['masindi'],
                        'Buhweju': ['buhweju','kabegaramire'],
                        'Butambala': ['butambala','kalamba'],
                        'Rakai': ['rakai'],
                        'Mpigi': ['mpigi'],
                        'Sembabule': ['sembabule', 'sembambule'],
                        'Arua': ['arua'],
                        'Rubanda': ['rubanda'],
                        'Gomba': ['gomba'],
                        'Bundibugyo': ['bundibugyo'],
                        'Kiryandongo': ['kiryandongo', 'bweyale'],
                        'Oyam': ['oyam'],
                        'Mitooma': ['mitooma'],
                        'Rubirizi': ['rubirizi','kichwamba'],
                        'Lyantonde': ['lyantonde'],
                        'Bukwo': ['bukwo','bukwa'],
                        'Busia': ['busia'],
                        'Mubende': ['mubende'],
                        'Kitagwenda': ['kitagwenda'],
                        'Lwengo': ['lwengo'],
                        'Mayuge': ['mayuge'],
                        'Sironko': ['sironko'],
                        'Kibaale': ['kibale', 'kibaale'],
                        'Bukomansimbi': ['bukomansimbi'],
                        'Budaka': ['budaka'],
                        'Kole': ['kole'],
                        'Fort Portal':['fort portal'],
                        'Bulambuli': ['bulambuli'],
                        'Luwero': ['luwero'],
                        'Tororo': ['tororo'],
                        'Serere': ['serere'],
                        'Bunyangabu': ['bunyangabu'],
                        'Pallisa': ['pallisa'],
                        'Manafwa': ['manafwa'],
                        'Kalungu': ['kalungu'],
                        'Kyegegwa': ['kyegegwa','kyeggegwa'],
                        'Kumi': ['kumi'],
                        'Kakumiro': ['kakumiro'],
                        'Kitgum': ['kitgum'],
                        'Kanungu': ['kanungu'],
                        'Kiboga': ['kiboga'],
                        'Kapchorwa': ['kapchorwa'],
                        'Kaliro': ['kaliro'],
                        'Dokolo': ['dokolo'],
                        'Apac': ['apac'],
                        'Kabalore': ['nyamirima'],
                        'Zombo': ['zombo'],
                        'Nebbi': ['nebbi'],
                        'Alebtong':['alebtong'],
                        'Kibuku':['kibuku'],
                        'Kyotera': ['kyotera','buwenge'],
                        'Jinja': ['jinja'],
                        'Kabarole': ['kabarole'],
                        'Buvuma': ['buvuma'],
                        "Yumbe": ["yumbe"],
                        "Obongi": ["obongi"],
                        "Adjumani": ["adjumani"],
                        "Amuru": ["amuru"],
                        "Katakwi": ["katakwii"],
                        "Amuria": ["amuria"],
                        "Bududa": ["bududa"],
                        'Bukedea': ["bukedea"],
                        "Nakaseke": ["nakaseke"],
                        "Omoro": ["omoro"],
                        "Kyankwanzi": ["kyankwanzi"],
                        "Kasanda": ["kasanda"],
                        'Luuka': ['luuka'],
                        'Kaberamaido':['kaberimaido']
                        
                    # Add more districts and their associated keywords as needed
                }
                
                # Create a new column 'district' and initialize with 'Other'
                df['District'] = 'Other'
                
                # Iterate over each row in the DataFrame
                for index, row in df.iterrows():
                    location = row['Location_of_borrower'].lower()
                    
                    # Check for each sector's keywords in the 'location' column
                    for district, keywords in district_keywords.items():
                        for keyword in keywords:
                            if keyword in location:
                                df.at[index, 'District'] = district
                                break  # Exit the loop once a sector is identified for the current row
                
                

                region_keywords = {
                        'Western': ['mbarara','fort portal','kagadi','kabale','rukungiri','ibanda','bushenyi','hoima','kyenjojo','kasese',
                                    'masindi','sheema','isingiro','buhweju','kibaale','kitagwenda','kamwenge','rubanda','ntungamo','kiruhura',
                                   'bundibugyo','kiryandongo','rubirizi','bunyangabu','rukiga','kyegegwa','kanungu','kazo','mitooma','kabalore',
                                   'kibingo','kabarole'],
                        'Eastern': ['jinja','iganga','bugiri','soroti','mbale','kamuli','namayingo','sironko','budaka','busia','bukwo',
                                    'bulambuli','tororo','serere','pallisa','manafwa','kumi','kapchorwa','kaliro','kibuku','katakwi',"amuria",
                                   "bududa",'bukedea','luuka','kaberamaido'],
                        'Central': ['kampala','luwero','kyotera','masaka','kayunga','mityana','sembabule','nakasongola','mukono','bukomansimbi',
                                   'rakai','wakiso','mpigi','buikwe','gomba','lwengo','mayuge','butambala','lyantonde','mubende','kalungu',
                                    'kiboga','butambala','buvuma','nakaseke','kyankwanzi','kasanda'],
                        'Northern': ['gulu','pader','koboko','lira','arua','oyam','kole','zombo','nebbi','kitgum','dokolo','apac','alebtong',
                                    'yumbe',"obongi","moyo", 'adjumani','omoro','amuru']
                
                    # Add more regions and their associated keywords as needed
                }
                
                # Create a new column 'region' and initialize with 'Other'
                df['Region'] = 'Other'
                
                # Iterate over each row in the DataFrame
                for index, row in df.iterrows():
                    location = row['District'].lower()
                    
                    # Check for each district's keywords in the 'District' column
                    for region, district in region_keywords.items():
                        for keyword in district:
                            if keyword in location:
                                df.at[index, 'Region'] = region
                                break  # Exit the loop once a sector is identified for the current row
                
                
                
                
                


            #Print the cleaned dataframe
            st.subheader('Preview the Clean Data')
            st.write('The shape is: ',df.shape)
            st.write(df.head())
            
            
            #Export Clean File
            st.subheader('Export Clean File')
            
            # Create an expandable section for additional export options
            with st.expander("Export Clean Data"):
                
                lender = df['lender'].iloc[0]
                import calendar
                month = calendar.month_name[df.iloc[1,1]]
                #Add button to Download Data
                st.download_button(
                    label="Click to Download Clean File",
                    data=df.to_csv(index=False),  # Convert DataFrame to Excel data
                    file_name= f"{lender}_{month}_Clean_Data.csv",  # Set file name
                )
                
                
                
            
            #Add Portfolio Monitoring Fields
            st.subheader('Portfolio Monitoring')
            st.write('Impact Measurement')
            
            #Add Columns
            col1, col2, col3 = st.columns(3)
            with col1:
                Loans = df['Loan_ID'].count()
                st.metric('Number of Loans', Loans,0)
            with col2:
                Amount = format(df['Loan_amount'].sum(), ',')
                st.metric('Loan Amount (UGX)', Amount, 0)
            with col3:
                Ticket = format(round(df['Loan_amount'].mean(),0), ',')
                st.metric('Avg Tickets (UGX)', Ticket, 0)
            with col1:
                Interest = round((df['Interest_rate'].mean())*100,1)
                st.metric('Average Interest (%)', Interest, 0)
            with col2:
                Gender = pd.DataFrame(df.groupby(by ='Gender').count()['year']).rename(columns = {'year':'Number'})
                Women = (Gender.iloc[0,0]/(Gender['Number'].sum())*100).round(1)
                st.metric('Pct Women (%)', Women, 0)
            with col3:
                Age_Group = pd.DataFrame(df.groupby(by ='Age_Group').count()['year']).rename(columns = {'year':'Number'})
                Youths = (Age_Group.iloc[-1,0]/(Age_Group['Number'].sum())*100).round(1)
                st.metric('Pct Youths (%)', Youths, 0)
                
            st.subheader('Loan Type')
            Loan_type = pd.DataFrame(df['Loan_type'].unique()).rename(columns = {0:'Loan Type'})
            st.write(Loan_type)
            
            st.subheader('Number of Women Borrowers')
            Gender_df = pd.DataFrame(df.groupby('Gender')['Loan_amount'].count())
            Gender_df = Gender_df.rename(columns = {"Loan_amount":"Number"})
            Gender_df["Percent (%)"] = (Gender_df["Number"]*100/sum(Gender_df["Number"])).round(2)
            st.write(Gender_df)
            
            st.subheader('Number of Youth Borrowers')
            Age_Group_df = pd.DataFrame(df.groupby('Age_Group')['Loan_amount'].count())
            Age_Group_df = Age_Group_df.rename(columns = {"Loan_amount":"Number"})
            Age_Group_df["Percent (%)"] = (Age_Group_df["Number"]*100/sum(Age_Group_df["Number"])).round(2)
            st.write(Age_Group_df)
            
            st.subheader('Economic Sectors Served')
            Sector_df = pd.DataFrame(df.groupby('Sector')['Loan_amount'].count())
            Sector_df = Sector_df.rename(columns = {"Loan_amount":"Number"})
            Sector_df["Percent (%)"] = (Sector_df["Number"]*100/sum(Sector_df["Number"])).round(2)
            st.write(Sector_df)
            
            st.subheader('Average Revenue of Borrowers')
            Annual_Revenue = format(round(df['Annual_revenue_of_borrower'].mean(), 0), ',')
            st.metric('Average Revenue (UGX)',Annual_Revenue)
            
            st.subheader('Average Number of Employees')
            employees = round(df['Number_of_employees'].mean(), 0)
            st.metric('Average number of employees:', employees)