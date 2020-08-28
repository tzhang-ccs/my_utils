import pandas as pd
import numpy as np

def styling_specific_cell(x,Pvals_df,siglevel):
	"""
	this function is used to style some speicifc cells in correlation table based on corresponding pvalues
	created by Yi Qin on Aug 28, 2020
	
	input:
	x: correlation dataframe 
	Pvals_df: pvalue dataframe
	siglevel: significant levels. generally set it as 0.05
	
	output: 
	colored correlation dataframe

	usage:
	Axis set to None to work on entire dataframe
	Cors_df.style.apply(styling_specific_cell, Pvals_df=Pvals_df, siglevel = 0.05, axis = None)
	if we want to ouput the final table into excel, please add: 
	.to_excel('./figure/styled.xlsx',engine='openpyxl') 

	notion:
	if you'd like to ouput excel, you need to have install openpyxl in your environment.
	"""
    # Step1: change all pvalues greater than siglevel as nan
    Pvals_df[Pvals_df>siglevel] = np.nan
    # Step2: get index and columns not nan
    input_ind = list(Pvals_df[Pvals_df.notnull()].stack().index)

    # Step3: styling specific cells 
    df_styler = pd.DataFrame('', index=x.index, columns=x.columns)
    for i,j in input_ind:
        print('in function',i,j)
#         color = 'background-color: white; color: deepskyblue'
        color = 'color: blue'
        df_styler.loc[i, j] = color
    return df_styler


