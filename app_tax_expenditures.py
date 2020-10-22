"""
app00.py illustrates use of TPRU-India taxcalc release 2.0.0
USAGE: python app00.py > app00.res
CHECK: Use your favorite Windows diff utility to confirm that app00.res is
       the same as the app00.out file that is in the repository.
"""
import pandas as pd
import matplotlib.pyplot as plt
from taxcalc import *

# create Records object containing pit.csv and pit_weights.csv input data
recs = Records()

grecs = GSTRecords()

# create CorpRecords object using cross-section data
crecs1 = CorpRecords(data='cit_poland.csv', weights='cit_weights_poland.csv')
# Note: weights argument is optional
assert isinstance(crecs1, CorpRecords)
assert crecs1.current_year == 2017

# create Policy object containing current-law policy
pol = Policy()

# specify Calculator objects for current-law policy
calc1 = Calculator(policy=pol, records=recs, corprecords=crecs1,
                   gstrecords=grecs, verbose=False)

# NOTE: calc1 now contains a PRIVATE COPY of pol and a PRIVATE COPY of recs,
#       so we can continue to use pol and recs in this script without any
#       concern about side effects from Calculator method calls on calc1.

assert isinstance(calc1, Calculator)
assert calc1.current_year == 2017

np.seterr(divide='ignore', invalid='ignore')

# Produce DataFrame of results using cross-section
calc1.calc_all()
#sector=calc1.carray('sector')
weight = calc1.carray('weight')

dump_vars = ['CIT_ID_NO', 'legal_form', 'sector', 'province', 'small_business', 
             'revenue', 'expenditure', 'income', 'tax_base_before_deductions', 
             'deductions_from_tax_base',
             'income_tax_base_after_deductions', 'citax']
dumpdf = calc1.dataframe_cit(dump_vars)
#create the weight variable
dumpdf['weight']= weight
dumpdf['weighted_citax']= dumpdf['weight']*dumpdf['citax']
dumpdf['ID_NO']= "A"+ dumpdf['CIT_ID_NO'].astype('str') 
#print(dumpdf)
dumpdf.to_csv('tax_expenditures_current_law.csv', index=False, float_format='%.0f')

pol2 = Policy()
#reform = Calculator.read_json_param_objects('tax_incentives_benchmark.json', None)
reform = Calculator.read_json_param_objects('tax_incentives_benchmark.json', None)

#reform = Calculator.read_json_param_objects('app01_reform.json', None)

with open('taxcalc/current_law_policy_poland.json') as f:
    current_law_policy = json.load(f)
ref_dict = reform['policy']
var_list = []
tax_expediture_list = []
tax_expediture_list_polish = []
for pkey, sdict in ref_dict.items():
        #print(f'pkey: {pkey}')
        #print(f'sdict: {sdict}')
        for k, s in sdict.items():
            reform.pop("policy")
            mydict={}
            mydict[k]=s
            mydict0={}
            mydict0[pkey]=mydict
            reform['policy']=mydict0
            #print('reform:', reform)
            #var_list= k
            #print(f'k: {k}')
            #print(f's: {s}')
            pol2.implement_reform(reform['policy'])
            
            calc2 = Calculator(policy=pol2, records=recs, corprecords=crecs1,
                               gstrecords=grecs, verbose=False)
            
            
            calc2.calc_all()
            dump_vars = ['CIT_ID_NO', 'citax']
            dumpdf_2 = calc2.dataframe_cit(dump_vars)
            dumpdf_2['ID_NO']= "A"+ dumpdf_2['CIT_ID_NO'].astype('int').astype('str')
            dumpdf_2.drop('CIT_ID_NO', axis=1, inplace=True)
            #print(dumpdf_2)
            dumpdf_2 = dumpdf_2.rename(columns={'citax':"tax_collected_under_policy"+ k})
            dumpdf = pd.merge(dumpdf, dumpdf_2, how="inner", on="ID_NO")
            #create the weight variable
            dumpdf['weighted_tax_collected_under_policy'+ k]= dumpdf['weight']*dumpdf['tax_collected_under_policy'+ k]
            #calculating expenditure

            dumpdf[current_law_policy[k]['description']]= (dumpdf["weighted_tax_collected_under_policy"+ k]- dumpdf["weighted_citax"])/10**6
            dumpdf[current_law_policy[k]['long_name']]= (dumpdf["weighted_tax_collected_under_policy"+ k]- dumpdf["weighted_citax"])/10**6            
            var_list = var_list + [k]
            tax_expediture_list = tax_expediture_list + [current_law_policy[k]['description']]
            tax_expediture_list_polish = tax_expediture_list_polish + [current_law_policy[k]['long_name']]            
            #print(var_list)
            #var_list= [var_list]+[k]
            #print(var_list)
            #dumpdf[var_list]= dumpdf[var_list] + dumpdf[k]
            #print(dumpdf)
            
dumpdf.to_csv('tax_expenditures_poland.csv', index=False, float_format='%.0f')
            
#Summarize here
tax_expenditure_df = dumpdf[tax_expediture_list].sum(axis = 0)
tax_expenditure_df= tax_expenditure_df.reset_index()
tax_expenditure_df.columns = ['Tax Expenditure', 'Million Zlotys']
tax_expenditure_df.to_csv('tax_expenditures_sum.csv',index=False, float_format='%.0f')
print(tax_expenditure_df)
tax_expenditure_df = dumpdf[tax_expediture_list_polish].sum(axis = 0)
tax_expenditure_df= tax_expenditure_df.reset_index()
tax_expenditure_df.columns = ['Wydatki Podatkowe', 'Milion Zlotys']
tax_expenditure_df.to_csv('tax_expenditures_sum_polish.csv', encoding='utf-8', index=False, float_format='%.0f')
tax_expenditure_df.to_csv('tax_expenditures_sum_polish.txt', encoding='utf-8', sep=',', index=False)