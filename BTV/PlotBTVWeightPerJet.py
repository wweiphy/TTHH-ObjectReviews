import pandas as pd
import matplotlib
import numpy as np
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def get_df(event, input_path, btagfile, systs):

	with pd.HDFStore(input_path, mode="r") as store:

		df = store.select("data")
        samp = int(df.shape[0]*1.0)
        df = df.head(samp)

	df = df[(df['N_Jets'] >= 4)]

	this_btag = btagfile[(btagfile['sample'] == event) & (btagfile['syst'] == "nominal")]
	bin_range = this_btag['bin'].values
	df.loc[:,'N_Jets_for_bTag'] = np.clip(df['N_Jets'].values, min(bin_range),max(bin_range))
	df_combine = pd.merge(df, this_btag, left_on='N_Jets_for_bTag', right_on='bin', how='left')
	df.loc[:, 'btagfactor'] = df_combine['ratio'].values

	for syst in systs:


		this_btag2 = btagfile[(btagfile['sample'] == event) & (btagfile['syst'] == "up"+syst)]
		bin_range2 = this_btag2['bin'].values
		df.loc[:,'N_Jets_for_bTag_up'+syst] = np.clip(df['N_Jets'].values, min(bin_range2),max(bin_range2))
		df_combine2 = pd.merge(df, this_btag2, left_on='N_Jets_for_bTag_up'+syst, right_on='bin', how='left')
		df.loc[:, 'btagfactor_up'+syst] = df_combine2['ratio'].values


		this_btag3 = btagfile[(btagfile['sample'] == event) & (btagfile['syst'] == "down"+syst)]
		bin_range3 = this_btag3['bin'].values
		df.loc[:,'N_Jets_for_bTag_down'+syst] = np.clip(df['N_Jets'].values, min(bin_range3),max(bin_range3))
		df_combine3 = pd.merge(df, this_btag3, left_on='N_Jets_for_bTag_down'+syst, right_on='bin', how='left')
		df.loc[:, 'btagfactor_down'+syst] = df_combine3['ratio'].values


	return df

def get_df_JESJER(event, input_path, btagfile, syst):

	with pd.HDFStore(input_path, mode="r") as store:

		df = store.select("data")
        samp = int(df.shape[0]*1.0)
        df = df.head(samp)

	df = df[(df['N_Jets'] >= 4)]

	this_btag = btagfile[(btagfile['sample'] == event) & (btagfile['syst'] == syst)]
	bin_range = this_btag['bin'].values
	df.loc[:,'N_Jets_for_bTag'] = np.clip(df['N_Jets'].values, min(bin_range),max(bin_range))
	df_combine = pd.merge(df, this_btag, left_on='N_Jets_for_bTag', right_on='bin', how='left')
	df.loc[:, 'btagfactor'] = df_combine['ratio'].values


	return df


def make_histograms_btags(df, syst,event, variable, btagsyst = False):

	fig = plt.figure()

	binrange = [4, 15]
	bins = binrange[1] - binrange[0]

	if btagsyst == False:

		if syst == 'nominal':
			df.loc[:, 'total_weight_btag'] = df['btagfactor'] * df['total_weight']
		elif syst == "JESUp" or syst == "JERUp" or syst == "JESDown" or syst == "JERDown":
			df.loc[:, 'total_weight_btag'] = df['btagfactor'] * df['total_weight']
		else:
			
			df.loc[:, 'total_weight_btag_nocorrection'] = df['total_preweight'] * df['Weight_CSV_UL_'+syst]

			df.loc[:, 'total_weight_'+syst] = df['btagfactor'] * df['total_preweight'] * df['Weight_CSV_UL_'+syst]
	else:
	# syst == "uplf" or syst == "downlf":

		df.loc[:, 'total_weight_btag_nocorrection'] = df['total_preweight'] * df['Weight_CSV_UL_'+syst]

		df.loc[:, 'total_weight_'+syst] = df['btagfactor_'+syst] * df['total_preweight'] * df['Weight_CSV_UL_'+syst]

	

	# binrange = [0.4, 2]
	plt.hist(df[variable].values,label='No btag SF', bins = bins, range = binrange, histtype='step', weights = df["total_preweight"].values)
	

	if syst == "nominal" or syst == "JESUp" or syst == "JESDown" or syst == "JERUp" or syst == "JERDown":

		plt.hist(df[variable].values, label="btag SF for "+syst, bins = bins, range = binrange,histtype='step', weights = df['total_weight'].values)

		plt.hist(df[variable].values,label = 'btag SF + Correction', bins = bins, range = binrange,histtype='step', weights = df['total_weight_btag'].values)
		

	else:

		plt.hist(df[variable].values, label="btag SF for "+syst, bins = bins, range = binrange,histtype='step', weights = df['total_weight_btag_nocorrection'].values)

		plt.hist(df[variable].values,label = 'btag SF + Correction', bins = bins, range = binrange,histtype='step', weights = df['total_weight_'+syst].values)

		



	title = event+ " comparison for "+syst
	xlabel = syst

	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel('Events')
	plt.legend()
	plt.savefig(event+"_"+syst+'.png')
	plt.close()



if __name__ == "__main__":

	file_path = "/uscms/home/wwei/nobackup/SM_TTHH/Summer20UL/CMSSW_11_1_2/src/TTHHRun2UL_DNN/workdir"

	# folder_name = "/BTag_0308_UL_3_"
	folder_name = "/BTag_16pre_UL_"
	# folder_name = "/BTag_16post_UL_"
	# folder_name = "/BTag_0119_UL_"

	events = ['ttHH','ttSL','ttDL','ttbbSL','ttbbDL','ttZH','ttZ','ttHSL','ttHDL','ttZZ','tt4b']
	# events = ['ttHH','ttSL','ttDL','ttbbDL','ttZH','ttZ','ttHSL','ttHDL','ttZZ','tt4b']

	systs = ['JES','JER']

	# btags = []

	btags = ['hf','lf','lfstats1','lfstats2','hfstats1','hfstats2','cferr1','cferr2']

	variables = ['N_Jets']

	filedir = "/uscms/home/wwei/nobackup/SM_TTHH/Summer20UL/EL8/CMSSW_12_4_3/src/TTHHRun2UL_DNN/preprocessing/BTagCorrection"



	# if folder_name == "BTag_0308_UL_3_":
	btagcorrection = pd.read_csv(filedir+"/btag-correction-2016pre-by-bin.csv")
	# elif folder_name == "/BTag_0119_UL_":
	# btagcorrection = pd.read_csv(filedir+"/btag-correction-2017-by-bin.csv")
	# elif folder_name == "/BTag_16post_UL_":
	# btagcorrection = pd.read_csv(filedir+"/btag-correction-2016post-by-bin.csv")
	# elif folder_name == "/BTag_16pre_UL_":

	# btagcorrection = pd.read_csv(filedir+"/btag-correction-2016pre-by-bin.csv")



	for event in events:

		print("do process "+event)

		input_file = file_path+folder_name+"nominal/"+event+"_dnn.h5"
		df = get_df(event, input_file, btagcorrection, btags)

		# for syst in systs:
		for variable in variables:

			# print("Do variable "+variable)

			make_histograms_btags(df,"nominal",event, variable)

			# print("Do plot for nominal")

			for btag in btags:

				# print("Do plot for btag "+btag)

				btagup = "up"+btag
				btagdown = "down"+btag

				make_histograms_btags(df,btagup,event, variable, btagsyst=True)
				make_histograms_btags(df,btagdown,event, variable, btagsyst=True)


			for syst in systs:

				print("Do plot for "+syst)

				input_file_up = file_path+folder_name+syst+"up/"+event+"_dnn.h5"
				df_up = get_df_JESJER(event, input_file_up, btagcorrection, syst+"up")

				input_file_down = file_path+folder_name+syst+"down/"+event+"_dnn.h5"
				df_down = get_df_JESJER(event, input_file_down, btagcorrection, syst+"down")

				make_histograms_btags(df_up,syst+"Up",event, variable)
				make_histograms_btags(df_down,syst+"Down",event, variable)

			


	print("Done with plotting")



