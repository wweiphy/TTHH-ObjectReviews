import pandas as pd
import matplotlib
import numpy as np
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv

def get_ratio(input_path):

	with pd.HDFStore(input_path, mode="r") as store:

		df = store.select("data")
        samp = int(df.shape[0]*1.0)
        df = df.head(samp)

	df = df[(df['N_Jets'] >= 4)]

	pre_weight = df["total_preweight"].values
	total_weight = df['total_weight'].values
	n_jets = df['N_Jets'].values

	# ratio = len(df) / sum(df["Weight_CSV_UL"].values)
	# df = df[df['N_Jets'] >= 5]
	# print(df['N_Jets'].head(10))
	# ratio = sum(df["total_preweight"].values)/sum(df["total_weight"].values)
	# df['test'] = df['Weight_CSV_UL']*df['sf_weight']*df['xs_weight']
	# df['test2'] = df['sf_weight']*df['xs_weight']
	# print(df.shape[0]/sum(df['Weight_CSV_UL'].values))
	# print(sum(df['test2'].values/df.shape[0]))

	# sum(df["total_preweight"].values)/sum(df["total_weight"].values)

	# sum(df3["total_preweight"].values)/sum(df3["total_weight"].values)


	return pre_weight, total_weight, n_jets


def get_ratio_for_btag(input_path, syst):

	with pd.HDFStore(input_path, mode="r") as store:

		df = store.select("data")
        samp = int(df.shape[0]*1.0)
        df = df.head(samp)

	df = df[(df['N_Jets'] >= 4)]


	df.loc[:, 'total_weight_btag_nocorrection'] = df['total_preweight'] * df['Weight_CSV_UL_'+syst]

	pre_weight = df["total_preweight"].values
	total_weight = df['total_weight_btag_nocorrection'].values
	n_jets = df['N_Jets'].values


	return pre_weight, total_weight, n_jets



if __name__ == "__main__":

	file_path = "/uscms/home/wwei/nobackup/SM_TTHH/Summer20UL/CMSSW_11_1_2/src/TTHHRun2UL_DNN/workdir"

	# folder_name = "/BTag_0308_UL_3_"
	folder_name = "/BTag_16pre_UL_"
	# folder_name = "/BTag_16post_UL_"
	# folder_name = "/BTag_0119_UL_"

	events = ['ttHH','ttSL','ttDL','ttbbSL','ttbbDL','ttZH','ttZ','ttHSL','ttHDL','ttZZ','tt4b']
	# events = ['ttHH','ttSL','ttDL','ttbbDL','ttZH','ttZ','ttHSL','ttHDL','ttZZ','tt4b']
	# events = ['ttSL','ttDL']
	systs = ['JES','JER']
	btags = ['hf','lf','lfstats1','lfstats2','hfstats1','hfstats2','cferr1','cferr2']
	# systs = []

	outfile_path = "btag-correction-2016pre-by-bin.csv"
	fields = ["sample","syst", "bin","ratio"]

	with open(outfile_path, mode='w') as file:
    	
		writer = csv.writer(file)

	    # Write column headers
		writer.writerow(fields)


		for event in events:

			print(event)

			input_file1 = file_path+folder_name+"nominal/"+event+"_dnn.h5"
			pre_weight, total_weight, n_jets = get_ratio(input_file1)

			min_val = min(n_jets)
			max_val = max(n_jets)
			bins = np.linspace(min_val, max_val+1, max_val - min_val + 2)
			# print("done1")

			hist1, _ = np.histogram(n_jets, bins=bins, weights=pre_weight)
			hist2, _ = np.histogram(n_jets, bins=bins, weights=total_weight)
			# print("done2")

			hist2 = np.where(hist2 == 0, 1, hist2)

			weights_map = hist1 / hist2

			# print(max_val)
			# print(event)
			# print(bins)
			# print(weights_map)

			for i in range(min_val, max_val+1):
				row = [event,'nominal']
				row.append(i)
				row.append(weights_map[i-min_val]) 
				writer.writerow(row)
	        	
			# print("done3")

			for btag in btags:

				btagup = "up"+btag
				btagdown = "down"+btag

				pre_weight_bup, total_weight_bup, n_jets_bup = get_ratio_for_btag(input_file1, btagup)

				pre_weight_bdown, total_weight_bdown, n_jets_bdown = get_ratio_for_btag(input_file1, btagdown)


				hist1_bup, _ = np.histogram(n_jets_bup, bins=bins, weights=pre_weight_bup)
				hist2_bup, _ = np.histogram(n_jets_bup, bins=bins, weights=total_weight_bup)
				# print("done2")

				hist2_bup = np.where(hist2_bup == 0, 1, hist2_bup)

				weights_map_bup = hist1_bup / hist2_bup


				hist1_bdown, _ = np.histogram(n_jets_bdown, bins=bins, weights=pre_weight_bdown)
				hist2_bdown, _ = np.histogram(n_jets_bdown, bins=bins, weights=total_weight_bdown)
				# print("done2")

				hist2_bdown = np.where(hist2_bdown == 0, 1, hist2_bdown)

				weights_map_bdown = hist1_bdown / hist2_bdown


				for i in range(min_val, max_val+1):
					row = [event,btagup]
					row.append(i)
					row.append(weights_map_bup[i-min_val]) 
					writer.writerow(row)

				for i in range(min_val, max_val+1):
					row = [event,btagdown]
					row.append(i)
					row.append(weights_map_bdown[i-min_val]) 
					writer.writerow(row)



			for syst in systs:


				systup = syst + "up"
				systdown = syst + 'down'

				input_file2 = file_path+folder_name + systup + "/"+event+"_dnn.h5" 
				input_file3 = file_path+folder_name + systdown + "/"+event+"_dnn.h5" 

				pre_weight_up, total_weight_up, n_jets_up = get_ratio(input_file2)
				pre_weight_down, total_weight_down, n_jets_down = get_ratio(input_file3)


				min_val_up = min(n_jets_up)
				max_val_up = max(n_jets_up)
				bins_up = np.linspace(min_val_up, max_val_up+1, max_val_up - min_val_up + 2)
				hist1_up, _ = np.histogram(n_jets_up, bins=bins_up, weights=pre_weight_up)
				hist2_up, _ = np.histogram(n_jets_up, bins=bins_up, weights=total_weight_up)
				hist2_up = np.where(hist2_up == 0, 1, hist2_up)
				weights_map_up = hist1_up / hist2_up


				min_val_down = min(n_jets_down)
				max_val_down = max(n_jets_down)
				bins_down = np.linspace(min_val_down, max_val_down+1, max_val_down - min_val_down + 2)
				hist1_down, _ = np.histogram(n_jets_down, bins=bins_down, weights=pre_weight_down)
				hist2_down, _ = np.histogram(n_jets_down, bins=bins_down, weights=total_weight_down)

				hist2_down = np.where(hist2_down == 0, 1, hist2_down)

				weights_map_down = hist1_down / hist2_down


				for i in range(min_val_up, max_val_up+1):
					row = [event,syst+"up"]
					row.append(i)
					row.append(weights_map_up[i-min_val_up]) 
					writer.writerow(row)

				for i in range(min_val_down, max_val_down+1):
					row = [event,syst+"down"]
					row.append(i)
					row.append(weights_map_down[i-min_val_down]) 
					writer.writerow(row)

	        

	print('finished writing csv file')	




		
