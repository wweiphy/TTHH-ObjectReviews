import pandas as pd
import matplotlib
import numpy as np
import ROOT
from array import array
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def get_df(input_path):

	with pd.HDFStore(input_path, mode="r") as store:

		df = store.select("data")
		samp = int(df.shape[0]*1.0)
		df = df.head(samp)


	df = df[(df['N_Jets']>=5) & (df['N_BTagsM'] >=4) & (df['N_TightMuons'] == 0) & (df['N_LooseMuons']==0)]
	return df[['N_TightElectrons','N_LooseElectrons','N_TightMuons','N_LooseMuons','check_ElectronTrigger', 'N_promptElectrons','N_passesIDElectrons','N_prompt_passesID_Electrons',"N_promptLooseElectrons","N_passesIDLooseElectrons","N_prompt_passesID_LooseElectrons", "N_promptElectronsDL","N_passesIDElectronsDL","N_prompt_passesID_ElectronsDL"]]


if __name__ == "__main__":

	file_path = "/uscms/home/wwei/nobackup/SM_TTHH/Summer20UL/EL8/CMSSW_12_4_3/src/TTHHRun2UL_DNN/workdir"

	# folders = ["/Eval_0515_UL_3_","/Eval_0523_UL_3_"]
	# folders = ["/Eval_0308_UL_4_"]
	mc_folder = "/EleID_0308_UL_nominal_4"
	# data_folder = '/Trigger_0308_UL_data'

	mc_file = file_path+mc_folder+"/ttSL_dnn.h5"
	# data_file = file_path+data_folder+"/singlemuon_dnn.h5"

	df = get_df(mc_file)

	# Electron ID efficiency for prompt electrons


	# num = df[(df['check_ElectronTrigger']==1)&(df['N_TightElectrons']==1)&(df['N_LooseElectrons']==1)&(df['Electron_isMatched[0]'] == 1.)&(df['Electron_passesID[0]'] == 1.) & (df['Electron_isPrompt[0]'] == 1.)&(df['LooseElectron_isMatched[0]'] == 1.)&(df['LooseElectron_passesID[0]'] == 1.) & (df['LooseElectron_isPrompt[0]'] == 1.)]
	
	# den = df[(df['check_ElectronTrigger']==1)&(df['N_TightElectrons']==1) & (df['N_LooseElectrons']==1)& (df['Electron_isMatched[0]'] == 1.)& (df['Electron_isPrompt[0]'] == 1.)& (df['LooseElectron_isMatched[0]'] == 1.)& (df['LooseElectron_isPrompt[0]'] == 1.)]

	# print('Number of prompt electrons passes tight ID: ',num.shape[0])
	# print('NUmber of prompt electrons: ', den.shape[0])
	# print('ratio: ', float(num.shape[0])/float(den.shape[0]))

	# num3 = df[(df['check_ElectronTrigger']==1)&(df['N_TightElectrons']==1)]['N_Prompt_PassesID'].sum()
	# den3 = df[(df['check_ElectronTrigger']==1)&(df['N_TightElectrons']==1)]['N_promptElectrons'].sum()
	# print(df.shape[0])
	# print(df['N_LooseElectrons'].sum())

	num3 = df["N_prompt_passesID_ElectronsDL"].sum()
	den3 = df["N_promptElectronsDL"].sum()
	# den3 = df[(df['check_ElectronTrigger']==1)&(df['N_TightElectrons']==1)]

	print('Number of prompt electrons passes tight ID: ',num3)
	print('NUmber of prompt electrons: ', den3)
	print('ratio: ', float(num3)/float(den3))


	# Veto efficiency for prompt electrons

	num2 = df[(df['check_ElectronTrigger']==1)&(df['N_passesIDLooseElectrons']==1)&(df['N_passesIDElectrons']==1)&(df['N_promptElectrons']==2)]

	den2 = df[(df['check_ElectronTrigger']==1)&(df['N_passesIDElectrons']==1)&(df['N_promptElectrons'] == 2)]

	print('Number of prompt electrons with veto: ',num2.shape[0])
	print('NUmber of prompt electrons: ', den2.shape[0])
	print('ratio2: ', float(num2.shape[0])/float(den2.shape[0]))


	# num = df[(df['N_LooseElectrons']==1) & (df['N_TightElectrons']==1) & (df['LooseElectron_isPrompt[0]'] == 1.) & (df['LooseElectron_isPrompt[0]'] == 1.)&(df['LooseElectron_isMatched[0]'] == 1.)& (df['Electron_isMatched[0]'] == 1.)&(df['LooseElectron_passesID[0]'] == 1.)&(df['Electron_lassesID[0]'] == 1.)]

	


	