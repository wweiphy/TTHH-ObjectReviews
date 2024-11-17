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


	return df[['N_Jets','N_BTagsM','Electron_Pt[0]','Electron_Eta_Supercluster[0]','check_ElectronTrigger']]

def get_efficiency(df, selection, isdata, pt_edges, eta_edges):

	n_x_bins = len(pt_edges) - 1
	n_y_bins = len(eta_edges) - 1

	ROOT.gStyle.SetOptStat(0)

	hist1 = ROOT.TH2D("notrigger", "Trigger Efficiency;Electron Pt; Electron Eta",n_x_bins, array('d', pt_edges), n_y_bins, array('d', eta_edges))

	hist2 = ROOT.TH2D("trigger", "Trigger Efficiency;Electron Pt; Electron Eta", n_x_bins, array('d', pt_edges), n_y_bins, array('d', eta_edges))

	
	hist3 = ROOT.TH1D("notrigger", "Trigger Efficiency;Electron Pt;Efficiency",n_x_bins, array('d', pt_edges))

	hist33 = ROOT.TH1D("trigger", "Trigger Efficiency;Electron Pt;Efficiency", n_x_bins, array('d', pt_edges))

	hist4 = ROOT.TH1D("notrigger", "Trigger Efficiency;Electron Eta;Efficiency", n_y_bins, array('d', eta_edges))

	hist44 = ROOT.TH1D("trigger", "Trigger Efficiency;Electron Eta;Efficiency", n_y_bins, array('d', eta_edges))


	pt_list = df['Electron_Pt[0]'].to_list()
	eta_list = df['Electron_Eta_Supercluster[0]'].to_list()

	df_pass = df[df['check_ElectronTrigger']==1]

	pt2_list = df_pass['Electron_Pt[0]'].to_list()
	eta2_list = df_pass['Electron_Eta_Supercluster[0]'].to_list()



	for i in range(len(pt_list)):

		hist1.Fill(pt_list[i], eta_list[i])
		hist3.Fill(pt_list[i])
		hist4.Fill(eta_list[i])

	for i in range(len(pt2_list)):
		hist2.Fill(pt2_list[i], eta2_list[i])
		hist33.Fill(pt2_list[i])
		hist44.Fill(eta2_list[i])


	hist1.Sumw2()
	hist2.Sumw2()
	hist3.Sumw2()
	hist4.Sumw2()
	hist33.Sumw2()
	hist44.Sumw2()

	ratio_hist = hist2.Clone("Trigger Efficiency")
	ratio_hist.SetTitle(selection+" Trigger Efficiency;Electron Pt;Electron Eta")
	ratio_hist.Divide(hist1)


	pt_ratio = hist33.Clone('Trigger Efficiency')
	pt_ratio.SetTitle(selection +" Trigger Efficiency;Electron Pt;Efficiency")
	pt_ratio.Divide(hist3)
	pt_ratio.GetYaxis().SetRangeUser(0, 1)

	eta_ratio = hist44.Clone('Trigger Efficiency')
	eta_ratio.SetTitle(selection +" Trigger Efficiency;Electron Eta;Efficiency")
	eta_ratio.Divide(hist4)
	eta_ratio.GetYaxis().SetRangeUser(0, 1)

	return ratio_hist, pt_ratio, eta_ratio




if __name__ == "__main__":

	file_path = "/uscms/home/wwei/nobackup/SM_TTHH/Summer20UL/EL8/CMSSW_12_4_3/src/TTHHRun2UL_DNN/workdir"

	# folders = ["/Eval_0515_UL_3_","/Eval_0523_UL_3_"]
	# folders = ["/Eval_0308_UL_4_"]
	mc_folder = "/Trigger_0308_UL_3_nominal"
	data_folder = '/Trigger_0308_UL_data'

	mc_file = file_path+mc_folder+"/ttDL_dnn.h5"
	data_file = file_path+data_folder+"/singlemuon_dnn.h5"

	df_mc = get_df(mc_file)
	df_mc_5j4b = df_mc[(df_mc['N_Jets'] >= 5)]

	df_data = get_df(data_file)
	df_data_5j4b = df_data[(df_data['N_Jets'] >= 5)]


	pt_edges = [34,50,75,100,150,250,500]
	eta_edges = [-2.5, -1.5660, -1.4442, 0, 1.4442,1.5660,2.5]

	ratio_hist, pt_ratio, eta_ratio= get_efficiency(df_mc, selection='4j', isdata=False, pt_edges=pt_edges, eta_edges=eta_edges)
	ratio_hist2, pt_ratio2, eta_ratio2 = get_efficiency(df_mc_5j4b, selection='5j', isdata=False, pt_edges=pt_edges, eta_edges=eta_edges)

	ratio_hist3, pt_ratio3, eta_ratio3= get_efficiency(df_data, selection='4j', isdata=True, pt_edges=pt_edges, eta_edges=eta_edges)
	ratio_hist4,pt_ratio4, eta_ratio4 = get_efficiency(df_data_5j4b, selection='5j', isdata=True, pt_edges=pt_edges, eta_edges=eta_edges)


	# Set up the canvas
	canvas = ROOT.TCanvas("canvas", "Trigger Efficiency 4j", 1400, 1200)
	canvas.SetRightMargin(0.15)

	canvas.cd()

	# Draw the ratio histogram with color palette
	pt_ratio.SetLineColor(ROOT.kRed)
	pt_ratio3.SetLineColor(ROOT.kBlue)
	pt_ratio.SetMarkerColor(ROOT.kRed)
	pt_ratio3.SetMarkerColor(ROOT.kBlue)

	ratio = ROOT.TRatioPlot(pt_ratio3, pt_ratio, "divsym")
	ratio.SetH1DrawOpt("e")
	ratio.SetH2DrawOpt("e")
	ratio.Draw()

	ROOT.gPad.Modified()
	ROOT.gPad.Update() #  make sure it’s really (re)drawn
	# pad = ROOT.TPad("pad1", "This is pad1", 0.1, 0.1, 0.9, 0.9)
	pad = ratio.GetUpperPad()


	legend = ROOT.TLegend(0.6, 0.5, 0.9, 0.7)
	legend.AddEntry(pt_ratio, "ttDL", "ep")  # "l" means line style
	legend.AddEntry(pt_ratio3, "Data", "ep")

	# Draw the legend
	legend.Draw()
	pad.Modified()
	pad.Update()

	# Update the canvas to show the plot
	canvas.Update()

	# Save the plot to a file
	canvas.SaveAs("pt_ratio-4j.png")
	canvas.Close()


		# Set up the canvas
	canvas = ROOT.TCanvas("canvas", "Trigger Efficiency 4j", 1400, 1200)
	canvas.SetRightMargin(0.15)
	canvas.cd()

	# Draw the ratio histogram with color palette
	eta_ratio.SetLineColor(ROOT.kRed)
	eta_ratio3.SetLineColor(ROOT.kBlue)
	eta_ratio.SetMarkerColor(ROOT.kRed)
	eta_ratio3.SetMarkerColor(ROOT.kBlue)

	ratio = ROOT.TRatioPlot(eta_ratio3, eta_ratio, "divsym")
	ratio.SetH1DrawOpt("e")
	ratio.SetH2DrawOpt("e")
	ratio.Draw()

	ROOT.gPad.Modified()
	ROOT.gPad.Update() #  make sure it’s really (re)drawn
	# pad = ROOT.TPad("pad1", "This is pad1", 0.1, 0.1, 0.9, 0.9)
	pad = ratio.GetUpperPad()

	legend = ROOT.TLegend(0.6, 0.5, 0.9, 0.7)
	legend.AddEntry(eta_ratio, "ttDL", "ep")  # "l" means line style
	legend.AddEntry(eta_ratio3, "Data", "ep")

	# Draw the legend
	legend.Draw()
	pad.Modified()
	pad.Update()

	# Update the canvas to show the plot
	canvas.Update()

	# Save the plot to a file
	canvas.SaveAs("eta_ratio-4j.png")
	canvas.Close()


		# Set up the canvas
	canvas = ROOT.TCanvas("canvas", "Trigger Efficiency 5j4b", 1400, 1200)
	canvas.SetRightMargin(0.15)
	canvas.cd()

	# Draw the ratio histogram with color palette
	pt_ratio2.SetLineColor(ROOT.kRed)
	pt_ratio4.SetLineColor(ROOT.kBlue)
	pt_ratio2.SetMarkerColor(ROOT.kRed)
	pt_ratio4.SetMarkerColor(ROOT.kBlue)


	ratio = ROOT.TRatioPlot(pt_ratio4, pt_ratio2, "divsym")
	ratio.SetH1DrawOpt("e")
	ratio.SetH2DrawOpt("e")
	ratio.Draw()

	ROOT.gPad.Modified()
	ROOT.gPad.Update() #  make sure it’s really (re)drawn
	# pad = ROOT.TPad("pad1", "This is pad1", 0.1, 0.1, 0.9, 0.9)
	pad = ratio.GetUpperPad()


	legend = ROOT.TLegend(0.6, 0.5, 0.9, 0.7)
	legend.AddEntry(pt_ratio2, "ttDL", "ep")  # "l" means line style
	legend.AddEntry(pt_ratio4, "Data", "ep")

	# Draw the legend
	legend.Draw()
	pad.Modified()
	pad.Update()


	# Update the canvas to show the plot
	canvas.Update()

	# Save the plot to a file
	canvas.SaveAs("pt_ratio-5j.png")
	canvas.Close()


		# Set up the canvas
	canvas = ROOT.TCanvas("canvas", "Trigger Efficiency 5j4b", 1400, 1200)
	canvas.SetRightMargin(0.15)


	# Draw the ratio histogram with color palette
	eta_ratio2.SetLineColor(ROOT.kRed)
	eta_ratio4.SetLineColor(ROOT.kBlue)
	eta_ratio2.SetMarkerColor(ROOT.kRed)
	eta_ratio4.SetMarkerColor(ROOT.kBlue)

	ratio = ROOT.TRatioPlot(eta_ratio4, eta_ratio2, "divsym")
	ratio.SetH1DrawOpt("e")
	ratio.SetH2DrawOpt("e")
	ratio.Draw()

	ROOT.gPad.Modified()
	ROOT.gPad.Update() #  make sure it’s really (re)drawn
	# pad = ROOT.TPad("pad1", "This is pad1", 0.1, 0.1, 0.9, 0.9)
	pad = ratio.GetUpperPad()

	legend = ROOT.TLegend(0.6, 0.5, 0.9, 0.7)
	legend.AddEntry(eta_ratio2, "ttDL", "ep")  # "l" means line style
	legend.AddEntry(eta_ratio4, "Data", "ep")

	# Draw the legend
	legend.Draw()
	pad.Modified()
	pad.Update()

	# Update the canvas to show the plot
	canvas.Update()

	# Save the plot to a file
	canvas.SaveAs("eta_ratio-5j.png")
	canvas.Close()



	# Set up the canvas
	canvas = ROOT.TCanvas("canvas", "Trigger Efficiency", 1400, 1200)
	canvas.SetRightMargin(0.15)

	# Draw the ratio histogram with color palette
	ratio_hist.Draw("col")

	# text_objects = []
	# Annotate each bin with the ratio value
	for i in range(1, ratio_hist.GetNbinsX() + 1):
		for j in range(1, ratio_hist.GetNbinsY() + 1):
			bin_value = ratio_hist.GetBinContent(i, j)
			bin_error = ratio_hist.GetBinError(i, j)
			# if hist2.GetBinContent(i, j) > 0:  # Avoid showing text for empty bins in hist2
				# print(i)
				# print(j)
				# print(ratio_value)
			x = ratio_hist.GetXaxis().GetBinCenter(i)
			y = ratio_hist.GetYaxis().GetBinCenter(j)
			# text = ROOT.TText(x, y, f"{ratio_value:.2f} ")

			text = f"#splitline{{{bin_value:.2f}}}{{#pm {bin_error:.2f}}}"

			label = ROOT.TLatex()
			label.SetTextSize(0.02)
			label.SetTextAlign(22) # Center alignment
			label.DrawLatex(x, y, text)
			
			# text.SetTextSize(0.02)
			# text.SetTextAlign(22)  # Center alignment
			# text.Draw()
			# text_objects.append(text) 
				# canvas.Update()

	# Update the canvas to show the plot
	canvas.Update()

	# Save the plot to a file
	canvas.SaveAs("MC_trigger.png")
	canvas.Close()


	# Set up the canvas
	canvas2 = ROOT.TCanvas("canvas2", "Trigger Efficiency", 1400, 1200)
	canvas2.SetRightMargin(0.15)

	# Draw the ratio histogram with color palette
	ratio_hist2.Draw("col")

	# text_objects2 = []
	# Annotate each bin with the ratio value
	for i in range(1, ratio_hist2.GetNbinsX() + 1):
		for j in range(1, ratio_hist2.GetNbinsY() + 1):
			bin_value = ratio_hist2.GetBinContent(i, j)
			bin_error = ratio_hist2.GetBinError(i, j)
			# if hist2.GetBinContent(i, j) > 0:  # Avoid showing text for empty bins in hist2
				# print(i)
				# print(j)
				# print(ratio_value)
			x = ratio_hist2.GetXaxis().GetBinCenter(i)
			y = ratio_hist2.GetYaxis().GetBinCenter(j)

			text = f"#splitline{{{bin_value:.2f}}}{{#pm {bin_error:.2f}}}"

			label = ROOT.TLatex()
			label.SetTextSize(0.02)
			label.SetTextAlign(22) # Center alignment
			label.DrawLatex(x, y, text)


			# text = ROOT.TText(x, y, f"{ratio_value:.2f}")
			# text.SetTextSize(0.02)
			# text.SetTextAlign(22)  # Center alignment
			# text.Draw()
			# text_objects2.append(text) 
				# canvas.Update()

	# Update the canvas to show the plot
	canvas2.Update()

	# Save the plot to a file
	canvas2.SaveAs("MC2_trigger.png")
	canvas2.Close()


		# Set up the canvas
	canvas = ROOT.TCanvas("canvas", "Trigger Efficiency", 1400, 1200)
	canvas.SetRightMargin(0.15)

	# Draw the ratio histogram with color palette
	ratio_hist3.Draw("col")

	# text_objects = []
	# Annotate each bin with the ratio value
	for i in range(1, ratio_hist3.GetNbinsX() + 1):
		for j in range(1, ratio_hist3.GetNbinsY() + 1):
			bin_value = ratio_hist3.GetBinContent(i, j)
			bin_error = ratio_hist3.GetBinError(i, j)
			# if hist2.GetBinContent(i, j) > 0:  # Avoid showing text for empty bins in hist2
				# print(i)
				# print(j)
				# print(ratio_value)
			x = ratio_hist3.GetXaxis().GetBinCenter(i)
			y = ratio_hist3.GetYaxis().GetBinCenter(j)

			text = f"#splitline{{{bin_value:.2f}}}{{#pm {bin_error:.2f}}}"

			label = ROOT.TLatex()
			label.SetTextSize(0.02)
			label.SetTextAlign(22) # Center alignment
			label.DrawLatex(x, y, text)


			# text = ROOT.TText(x, y, f"{ratio_value:.2f}")
			# text.SetTextSize(0.02)
			# text.SetTextAlign(22)  # Center alignment
			# text.Draw()
			# text_objects.append(text) 
				# canvas.Update()

	# Update the canvas to show the plot
	canvas.Update()

	# Save the plot to a file
	canvas.SaveAs("Data_trigger.png")
	canvas.Close()


		# Set up the canvas
	canvas = ROOT.TCanvas("canvas", "Trigger Efficiency", 1400, 1200)
	canvas.SetRightMargin(0.15)

	# Draw the ratio histogram with color palette
	ratio_hist4.Draw("col")

	# text_objects = []
	# Annotate each bin with the ratio value
	for i in range(1, ratio_hist4.GetNbinsX() + 1):
		for j in range(1, ratio_hist4.GetNbinsY() + 1):
			bin_value = ratio_hist4.GetBinContent(i, j)
			bin_error = ratio_hist4.GetBinError(i, j)
			# if hist2.GetBinContent(i, j) > 0:  # Avoid showing text for empty bins in hist2
				# print(i)
				# print(j)
				# print(ratio_value)
			x = ratio_hist4.GetXaxis().GetBinCenter(i)
			y = ratio_hist4.GetYaxis().GetBinCenter(j)

			text = f"#splitline{{{bin_value:.2f}}}{{#pm {bin_error:.2f}}}"

			label = ROOT.TLatex()
			label.SetTextSize(0.02)
			label.SetTextAlign(22) # Center alignment
			label.DrawLatex(x, y, text)

			# text = ROOT.TText(x, y, f"{ratio_value:.2f}")
			# text.SetTextSize(0.02)
			# text.SetTextAlign(22)  # Center alignment
			# text.Draw()
			# text_objects.append(text) 
				# canvas.Update()

	# Update the canvas to show the plot
	canvas.Update()

	# Save the plot to a file
	canvas.SaveAs("Data_trigger2.png")
	canvas.Close()






	ratio_to_ratio = ratio_hist3.Clone("SF")
	ratio_to_ratio.SetTitle("SF 4j;Electron Pt;Electron Eta")
	ratio_to_ratio.Divide(ratio_hist)

	# Set up the canvas
	canvas3 = ROOT.TCanvas("canvas3", "SF", 1400, 1200)
	canvas3.SetRightMargin(0.15)

	# Draw the ratio histogram with color palette
	ratio_to_ratio.Draw("col")

	# text_objects3 = []
	# Annotate each bin with the ratio value
	for i in range(1, ratio_to_ratio.GetNbinsX() + 1):
		for j in range(1, ratio_to_ratio.GetNbinsY() + 1):
			bin_value = ratio_to_ratio.GetBinContent(i, j)
			bin_error = ratio_to_ratio.GetBinError(i, j)
			# if hist2.GetBinContent(i, j) > 0:  # Avoid showing text for empty bins in hist2
				# print(i)
				# print(j)
				# print(ratio_value)
			x = ratio_to_ratio.GetXaxis().GetBinCenter(i)
			y = ratio_to_ratio.GetYaxis().GetBinCenter(j)

			text = f"#splitline{{{bin_value:.2f}}}{{#pm {bin_error:.2f}}}"

			label = ROOT.TLatex()
			label.SetTextSize(0.02)
			label.SetTextAlign(22) # Center alignment
			label.DrawLatex(x, y, text)

			# text = ROOT.TText(x, y, f"{ratio_value:.2f}")
			# text.SetTextSize(0.02)
			# text.SetTextAlign(22)  # Center alignment
			# text.Draw()
			# text_objects3.append(text) 
				# canvas.Update()

	# Update the canvas to show the plot
	canvas3.Update()

	# Save the plot to a file
	canvas3.SaveAs("SF_trigger_4j.png")
	canvas3.Close()


	ratio_to_ratio = ratio_hist4.Clone("SF")
	ratio_to_ratio.SetTitle("SF 5j;Electron Pt;Electron Eta")
	ratio_to_ratio.Divide(ratio_hist2)


	# Set up the canvas
	canvas3 = ROOT.TCanvas("canvas3", "SF", 1400, 1200)
	canvas3.SetRightMargin(0.15)

	# Draw the ratio histogram with color palette
	ratio_to_ratio.Draw("col")

	# text_objects3 = []
	# Annotate each bin with the ratio value
	for i in range(1, ratio_to_ratio.GetNbinsX() + 1):
		for j in range(1, ratio_to_ratio.GetNbinsY() + 1):
			bin_value = ratio_to_ratio.GetBinContent(i, j)
			bin_error = ratio_to_ratio.GetBinError(i, j)
			# if hist2.GetBinContent(i, j) > 0:  # Avoid showing text for empty bins in hist2
				# print(i)
				# print(j)
				# print(ratio_value)
			x = ratio_to_ratio.GetXaxis().GetBinCenter(i)
			y = ratio_to_ratio.GetYaxis().GetBinCenter(j)

			text = f"#splitline{{{bin_value:.2f}}}{{#pm {bin_error:.2f}}}"


			label = ROOT.TLatex()
			label.SetTextSize(0.02)
			label.SetTextAlign(22) # Center alignment
			label.DrawLatex(x, y, text)
			

			# text = ROOT.TText(x, y, f"{ratio_value:.2f}")
			# text.SetTextSize(0.02)
			# text.SetTextAlign(22)  # Center alignment
			# text.Draw()
			# text_objects3.append(text) 
				# canvas.Update()

	# Update the canvas to show the plot
	canvas3.Update()

	# Save the plot to a file
	canvas3.SaveAs("SF_trigger_5j.png")
	canvas3.Close()

				







