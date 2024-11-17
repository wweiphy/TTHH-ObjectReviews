import pandas as pd
import matplotlib
import numpy as np
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def get_df(event, input_path):

	with pd.HDFStore(input_path, mode="r") as store:

		df = store.select("data")
        samp = int(df.shape[0]*1.0)
        df = df.head(samp)

	# df = df[(df['N_Jets'] >= 6) & (df['N_BTagsM'] >= 4) & (df['sf_weight'] > 0.) & df['Weight_GEN_nom'] < 0]

	df = df[(df['N_Jets'] >= 5) & (df['N_BTagsM'] >= 4)]

	# print("event yield for "+event+" is ", df.shape[0])


	return df


def make_histograms(df, syst,name_in_weight, event, bins = 50):

	fig = plt.figure()

	systup = syst+"_up"
	systdown = syst+"_down"
	nominal = 'Weight_GEN_nom'

	# binrange = [-0.3, 2]
	if event == 'ttH':
		binrange = [-0.25,1]
	elif event == 'ttcc' or event == 'ttlf':
		binrange = [-100,1000]
	elif event == 'ttmb':
		binrange = [-30,100]

	# x_max = max(df[systup].max()*df[nominal].max(),df[nominal].max(), df[systdown].max()*df[nominal].max())
	# x_min = min(df[systup].min()*df[nominal].min(),df[nominal].min(), df[systdown].min()*df[nominal].min())
	# binrange = [x_min,x_max]
 
	plt.hist(df[systup]*df[nominal],label=name_in_weight+'up', bins = bins, range = binrange, histtype='step')
	plt.hist(df[nominal], label="GenWeight", bins = bins, range = binrange,histtype='step')
	# plt.hist(df["total_weight"], label="nominal", bins = bins, range = binrange,histtype='step')
	plt.hist(df[systdown]*df[nominal],label = name_in_weight+'down', bins = bins, range = binrange,histtype='step')

	# plt.hist(df[systup]*df[nominal],label=name_in_weight+'up', bins = bins, histtype='step')
	# plt.hist(df[nominal], label="GenWeight", bins = bins, histtype='step')
	# # plt.hist(df["total_weight"], label="nominal", bins = bins, range = binrange,histtype='step')
	# plt.hist(df[systdown]*df[nominal],label = name_in_weight+'down', bins = bins, histtype='step')


	title = event+ " weight for "+name_in_weight
	xlabel = name_in_weight

	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel('Events')
	plt.legend()
	plt.savefig(event+"_"+name_in_weight+'_WeightOnly.png')
	plt.close()



	# fig = plt.figure()

	# systup = "total_weight_up"+name_in_weight
	# systdown = 'total_weight_down'+name_in_weight


	# # print(max(df[systup].max(),df[systdown].max()))
	# binrange = [min(df[systup].min(),df[systdown].min()), max(df[systup].max(),df[systdown].max())/3]
	# # binrange = [0.4, 2]
	# plt.hist(df[systup],label=name_in_weight+'up', bins = bins, range = binrange, histtype='step')
	# # plt.hist(df["Weight_CSV_UL"], label="nominal", bins = bins, range = binrange,histtype='step')
	# plt.hist(df["total_weight"], label="nominal", bins = bins, range = binrange,histtype='step')
	# plt.hist(df[systdown],label = name_in_weight+'down', bins = bins, range = binrange,histtype='step')
	# # plt.yscale("log")

	# title = event+ " weight for "+name_in_weight
	# xlabel = syst

	# plt.title(title)
	# plt.xlabel(xlabel)
	# plt.ylabel('Events')
	# plt.legend()
	# plt.savefig(event+"_"+name_in_weight+'_totalweight.png')
	# plt.close()


	print("Histograms saved as PNG files for "+event+" in "+name_in_weight+ ' for '+xlabel)


if __name__ == "__main__":

	file_path = "/work/SM_TTHH/Summer20UL/CMSSW_11_1_2/src/TTHHRun2UL_DNN/workdir"

	# folder_name = "/Eval_0308_UL_4_"
	# folder_name = "/Eval_0119_UL_4_"
	# folder_name = "/Eval_0515_UL_4_" 
	folder_name = "/Eval_0523_UL_4_"

	systs = ['GenWeight_isr_Def','GenWeight_fsr_Def']

	# events = ['ttHH','ttH','ttZ','ttZH','ttZZ','ttlf','ttcc','ttmb','ttnb']
	events = ['ttH','ttlf','ttcc','ttmb']

	bins = 50


	for event in events:

		input_file = file_path+folder_name+"nominal/"+event+"_dnn.h5"
		df = get_df(event, input_file)

		for syst in systs:
				
			make_histograms(df, syst, syst, event, bins)


	print("Done with plotting")



