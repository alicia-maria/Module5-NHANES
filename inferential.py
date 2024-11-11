import pandas as pd
from scipy.stats import chi2_contingency
import numpy as np

demo = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2021-2022/DEMO_L.XPT', format='xport')
bp = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2021-2022/BPXO_L.XPT', format='xport')
body = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2021-2022/BMX_L.XPT', format='xport')
chol_total = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2021-2022/TCHOL_L.XPT', format='xport')
glycohemo = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2021-2022/GHB_L.XPT', format='xport')
crp = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2021-2022/HSCRP_L.XPT', format='xport')
dm = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2021-2022/DIQ_L.XPT', format='xport')
phy = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2021-2022/PAQ_L.XPT', format='xport')
whd = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2021-2022/WHQ_L.XPT', format='xport')

demographics = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2021-2022/DEMO_L.XPT', format='xport')
demographics.DMDMARTZ

nhanes_data = demo.merge(bp, on='SEQN', how='left')\
                  .merge(body, on='SEQN', how='left')\
                  .merge(chol_total, on='SEQN', how='left')\
                  .merge(glycohemo, on='SEQN', how='left')\
                  .merge(crp, on='SEQN', how='left')\
                  .merge(dm, on='SEQN', how='left')\
                  .merge(phy, on='SEQN', how='left')\
                  .merge(whd, on='SEQN', how='left')

print(nhanes_data)

nhanes_data['DMDMARTZ'] = nhanes_data['DMDMARTZ'].apply(lambda x: 1 if x == 1 else 0)
nhanes_data['DMDEDUC2'] = nhanes_data['DMDEDUC2'].apply(lambda x: 1 if x in [4, 5] else 0)
nhanes_data['PAD680'].replace([7777, 9999], np.nan, inplace=True)
nhanes_data['WHD020'].replace([7777, 9999], np.nan, inplace=True)

##Is there an association between marital status and education level?

from scipy.stats import chi2_contingency
contingency_table = pd.crosstab(nhanes_data['DMDMARTZ'], nhanes_data['DMDEDUC2'])
chi2, p, dof, ex = chi2_contingency(contingency_table)
print(f"Chi2 Statistic: {chi2}, p-value: {p}")

##Based on the following statistics, there is no correlation between marital status and education level

##Is there a difference in the mean sedentary behavior time between those who are married and those who are not married?

from scipy.stats import ttest_ind
married = nhanes_data[nhanes_data['DMDMARTZ'] == 1]['PAD680'].dropna()
not_married = nhanes_data[nhanes_data['DMDMARTZ'] == 0]['PAD680'].dropna()
t_stat, p_val = ttest_ind(married, not_married)
print(f"T-Statistic: {t_stat}, p-value: {p_val}")

##Based on this statistics there is a mean difference between sedentary behavior time to those are are married or not married 

##How do age and marital status affect systolic blood pressure?

import statsmodels.api as sm
from statsmodels.formula.api import ols
model = ols('BPXOSY3 ~ RIDAGEYR + C(DMDMARTZ)', data=nhanes_data).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)
# I was a little unsure  if age and marital status does actuallu affect systolic blood pressure. 




## Is there a correlation between self-reported weight and minutes of sedentary behavior?
subset_data = nhanes_data[['WHD020', 'PAD680']].dropna()
from scipy.stats import pearsonr
correlation, p_value = pearsonr(subset_data['WHD020'], subset_data['PAD680'])
print(f"Correlation: {correlation}, p-value: {p_value}")

## Based on this statistic, we can see that there is a positive correction between weight that is self reported and sedentary minute behavior.
