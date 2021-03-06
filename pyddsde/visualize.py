import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mtick
import seaborn as sns
import statsmodels.graphics
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pyddsde.metrics import metrics


class visualize(metrics):
	"""
	Module to visualize and plot analysed data

	:meta private:
	"""
	def __init__(self, op_x, op_y, op, autocorrelation_time, **kwargs):
		self.op_x = op_x
		self.op_y = op_y
		self.op = op
		self.autocorrelation_time = int(autocorrelation_time)
		self.__dict__.update(kwargs)
		metrics.__init__(self)

		self._c_pallet = sns.color_palette("colorblind", as_cmap=True)

		return None

	def _stylize_axes(self,
					 ax,
					 x_label=None,
					 y_label=None,
					 title=None,
					 tick_size=20,
					 title_size=20,
					 label_size=20,
					 label_pad=12):
		"""
		Beautify the plot axis
		"""

		# Hide the top and right spines of the axis
		ax.spines['top'].set_visible(False)
		ax.spines['right'].set_visible(False)

		ax.set_title(title, fontsize=title_size)

		ax.set_xlabel(x_label, fontsize=label_size, labelpad=label_pad)
		ax.set_ylabel(y_label, fontsize=label_size, labelpad=label_pad)
		ax.tick_params(axis='both', which='major', labelsize=tick_size)

		return None

	def _plot_summary(self,
					  data,
					  vector=True,
					  kde=False,
					  tick_size=12,
					  title_size=15,
					  label_size=15,
					  label_pad=8,
					  n_ticks=3,
					  timeseries_start=0,
					  timeseries_end=1000,
					  **plot_text):
		"""
		Plots the summary chart
		"""
		text = {
			'timeseries_title' : 'Time Series',
			'timeseries_xlabel' : 'Time Index',
			'timeseries_ylabel' : 'M',
			'hist_title' : '',
			'hist_xlabel' : 'M',
			'hist_ylabel' : 'Frequency',
			'drift_title' : 'Drift',
			'drift_xlabel' : 'm',
			'drift_ylabel' : 'F',
			'diffusion_title' : 'Diffusion',
			'diffusion_xlabel' : 'm',
			'diffusion_ylabel' : '$G^{2}$',

			'timeseries1_title' : 'Time Series',
			'timeseries1_ylabel' : '$M_{x}, M_{y}$',
			'timeseries1_xlabel' : '',
			'timeseries1_legend1' : '$M_{x}$',
			'timeseries1_legend2' : '$M_{y}$',
			'timeseries2_title' : '',
			'timeseries2_xlabel' : 'Time Index',
			'timeseries2_ylabel' : '|M|',
			
			'2dhist1_title' : '',
			'2dhist1_xlabel' : '$M_{x}$',
			'2dhist1_ylabel' : 'Frequency',
			
			'2dhist2_title' : '',
			'2dhist2_xlabel' : '$M_{y}$',
			'2dhist2_ylabel' : 'Frequency',
			
			'2dhist3_title' : '',
			'2dhist3_xlabel' : '|M|',
			'2dhist3_ylabel' : 'Frequency',
			
			'3dhist_title' : '',
			'3dhist_xlabel' : '$M_{x}$',
			'3dhist_ylabel' : '$M_{y}$',
			'3dhist_zlabel' : 'Frequency',
			
			'driftx_title' : 'Drift X',
			'driftx_xlabel' : '$m_{x}$',
			'driftx_ylabel' : '$m_{y}$',
			'driftx_zlabel' : '$A_{1}$',
			
			'drifty_title' : 'Drift Y',
			'drifty_xlabel' : '$m_{x}$',
			'drifty_ylabel' : '$m_{y}$',
			'drifty_zlabel' : '$A_{2}$',
			
			'diffusionx_title' : 'Diffusion X',
			'diffusionx_xlabel' : '$m_{x}$',
			'diffusionx_ylabel' : '$m_{y}$',
			'diffusionx_zlabel' : '$B_{11}$',
			
			'diffusiony_title' : 'Diffusion Y',
			'diffusiony_xlabel' : '$m_{x}$',
			'diffusiony_ylabel' : '$m_{y}$',
			'diffusiony_zlabel' : '$B_{22}$'
		}
		for k in plot_text.keys():
			if k not in text.keys():
				print("{} not a valid plot text key".format(k))
		text.update(plot_text)
		if vector:
			Mx, My, driftX, driftY, diffX, diffY = data
			M = np.sqrt(Mx**2 + My**2)
			#fig, axs = plt.subplots(nrows=3, ncols=4,figsize=(15,12), dpi=150)
			#plt.subplots_adjust(wspace= 0.5, hspace= 0.5)
			fig = plt.figure(constrained_layout=True, figsize=(15,12), dpi=100)

			#gs = axs[0, 0].get_gridspec()
			gs = gridspec.GridSpec(nrows=3, ncols=4,wspace=0.5, hspace=0.5,figure=fig)
			#fig.set_constrained_layout_pads(w_pad=1, h_pad=5)
			# remove the underlying axes
			#for ax in axs.flatten():
			#    ax.remove()

			Mx_axis = fig.add_subplot(gs[0,0:2])
			Mx_axis.plot(range(timeseries_start, timeseries_end), Mx[timeseries_start:timeseries_end], label=text['timeseries1_legend1'])
			Mx_axis.plot(range(timeseries_start, timeseries_end), My[timeseries_start:timeseries_end], color='red', label=text['timeseries1_legend2'])
			#Mx_axis.set_xticks([])
			Mx_axis.set_yticks(np.linspace(min(min(Mx), min(My)), max(max(Mx), max(My)), n_ticks).round(2))
			self._stylize_axes(Mx_axis,
				  x_label=text['timeseries1_xlabel'],#'',
				  y_label=text['timeseries1_ylabel'],#'$M_{x}, M_{y}$',
				  title=text['timeseries1_title'],#'Time Series',
				  tick_size=tick_size,
				  title_size=title_size,
				  label_size=label_size,
				  label_pad=label_pad)
			Mx_axis.minorticks_on()
			Mx_axis.legend(loc="best")
			Mx_axis.grid("on")

			My_axis = fig.add_subplot(gs[1,0:2])
			My_axis.plot(range(timeseries_start, timeseries_end), M[timeseries_start:timeseries_end])
			My_axis.set_yticks(np.linspace(min(M), max(M), n_ticks).round(2))
			self._stylize_axes(My_axis,
				  x_label=text['timeseries2_xlabel'],#'Time Index',
				  y_label=text['timeseries2_ylabel'],#'$|M|$',
				  title=text['timeseries2_title'],#'',
				  tick_size=tick_size,
				  title_size=title_size,
				  label_size=label_size,
				  label_pad=label_pad)
			My_axis.minorticks_on()
			My_axis.grid("on")

			driftX_axis = fig.add_subplot(gs[2,0], projection='3d')
			_, driftX_axis = self._plot_data(driftX,
										 ax=driftX_axis,
										 title=text['driftx_title'],#"Drift X",
										 x_label=text['driftx_xlabel'],#'$m_{x}$',
										 y_label=text['driftx_ylabel'],#'$m_{y}$',
										 z_label=text['driftx_zlabel'],#'$A_{1}$',
										 tick_size=tick_size,
										 title_size=title_size,
										 label_size=label_size,
										 label_pad=label_pad)




			driftY_axis = fig.add_subplot(gs[2,1], projection='3d')
			_, driftY_axis = self._plot_data(driftY,
										 ax=driftY_axis,
										 title=text['drifty_title'],#"Drift Y",
										 x_label=text['drifty_xlabel'],#'$m_{x}$',
										 y_label=text['drifty_ylabel'],#'$m_{y}$',
										 z_label=text['drifty_zlabel'],#'$A_{2}$',
										 tick_size=tick_size,
										 title_size=title_size,
										 label_size=label_size,
										 label_pad=label_pad)			





			diffX_axis = fig.add_subplot(gs[2,2], projection='3d')
			_, driffX_axis = self._plot_data(diffX,
										 ax=diffX_axis,
										 title=text['diffusionx_title'],#"Diffusion X",
										 x_label=text['diffusionx_xlabel'],#'$m_{x}$',
										 y_label=text['diffusionx_ylabel'],#'$m_{y}$',
										 z_label=text['diffusionx_zlabel'],#'$B_{11}$',
										 tick_size=tick_size,
										 title_size=title_size,
										 label_size=label_size,
										 label_pad=label_pad)

			diffY_axis = fig.add_subplot(gs[2,3], projection='3d')
			_, diffY_axis = self._plot_data(diffY,
										 ax=diffY_axis,
										 title=text['diffusiony_title'],#"Diffusion Y",
										 x_label=text['diffusiony_xlabel'],#'$m_{x}$',
										 y_label=text['diffusiony_ylabel'],#'$m_{y}$',
										 z_label=text['diffusiony_zlabel'],#'$B_{22}$',
										 tick_size=tick_size,
										 title_size=title_size,
										 label_size=label_size,
										 label_pad=label_pad)

			distMx_axis = fig.add_subplot(gs[0,2])
			distMx_axis = sns.distplot(Mx, kde=kde, ax=distMx_axis)
			ticks = [str(i)+"K" for i in (np.array(distMx_axis.get_yticks())/1000).round(1)]
			distMx_axis.set_yticklabels(ticks)
			self._stylize_axes(distMx_axis,
							  x_label=text['2dhist1_xlabel'],#'$M_{x}$',
							  y_label=text['2dhist1_ylabel'],#'Frequency',
							  title=text['2dhist1_title'],#'',
							  tick_size=tick_size,
							  title_size=title_size,
							  label_size=label_size,
							  label_pad=label_pad)

			distMy_axis = fig.add_subplot(gs[0,3])
			distMy_axis = sns.distplot(My, kde=kde, ax=distMy_axis)
			ticks = [str(i)+"K" for i in (np.array(distMy_axis.get_yticks())/1000).round(1)]
			distMy_axis.set_yticklabels(ticks)
			self._stylize_axes(distMy_axis,
							  x_label=text['2dhist2_xlabel'],#'$M_{y}$',
							  y_label=text['2dhist2_ylabel'],#'Frequency',
							  title=text['2dhist2_title'],#'',
							  tick_size=tick_size,
							  title_size=title_size,
							  label_size=label_size,
							  label_pad=label_pad)


			distM_axis = fig.add_subplot(gs[1, 2])
			distM_axis = sns.distplot(np.sqrt(Mx**2 + My**2), kde=kde, ax=distM_axis)
			ticks = [str(i)+"K" for i in (np.array(distM_axis.get_yticks())/1000).round(1)]
			distM_axis.set_yticklabels(ticks)
			self._stylize_axes(distM_axis,
							  x_label=text['2dhist3_xlabel'],#'|M|',
							  y_label=text['2dhist3_ylabel'],#'Frequency',
							  title=text['2dhist3_title'],#'',
							  tick_size=tick_size,
							  title_size=title_size,
							  label_size=label_size,
							  label_pad=label_pad)

			pdf_axis = fig.add_subplot(gs[1,3], projection='3d')
			pdf_axis = self._plot_3d_hisogram(Mx, My, ax=pdf_axis, title='', title_size=title_size, tick_size=tick_size,label_size=label_size, label_pad=label_pad)

			"""
			fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(15, 12))
			#TimeSeries
			if timeseries_end > len(Mx):
				timeseries_end = len(Mx)

			ax[0][0].plot(range(timeseries_start, timeseries_end),
						  M[timeseries_start:timeseries_end])
			ax[0][0].set_ylim(0, 1)
			self._stylize_axes(ax[0][0],
							  x_label='Time Index',
							  y_label='|M|',
							  title='Time Series',
							  tick_size=tick_size,
							  title_size=title_size,
							  label_size=label_size,
							  label_pad=label_pad)

			#Dist Mx, My
			ax[1][0].remove()
			ax[1][0] = fig.add_subplot(2,3,4, projection='3d')
			ax[1][0] = self._plot_3d_hisogram(Mx, My, ax=ax[1][0], title='Mx,My distrubition', title_size=title_size, tick_size=tick_size,label_size=label_size, label_pad=label_pad)

			#sns.distplot(M, kde=kde, ax=ax[1][0])
			#self._stylize_axes(ax[1][0],
			#				  x_label='op',
			#				  y_label='freq',
			#				  title='Dist |M|',
			#				  tick_size=tick_size,
			#				  title_size=title_size,
			#				  label_size=label_size,
			#				  label_pad=label_pad)

			#Drift X
			ax[0][1].remove()
			ax[0][1] = fig.add_subplot(2, 3, 2, projection='3d')
			_, ax[0][1] = self._plot_data(driftX,
										 ax=ax[0][1],
										 title="Drift X",
										 x_label='$m_{x}$',
										 y_label='$m_{y}$',
										 z_label='$A_{1}$',
										 tick_size=tick_size,
										 title_size=title_size,
										 label_size=label_size,
										 label_pad=label_pad)

			#Drift Y
			ax[0][2].remove()
			ax[0][2] = fig.add_subplot(2, 3, 3, projection='3d')
			_, ax[0][2] = self._plot_data(driftY,
										 ax=ax[0][2],
										 title="Drift Y",
										 x_label='$m_{x}$',
										 y_label='$m_{y}$',
										 z_label='$A_{2}$',
										 tick_size=tick_size,
										 title_size=title_size,
										 label_size=label_size,
										 label_pad=label_pad)

			#Diffusion X
			ax[1][1].remove()
			ax[1][1] = fig.add_subplot(2, 3, 5, projection='3d')
			_, ax[1][1] = self._plot_data(diffX,
										 ax=ax[1][1],
										 title="Diffusion X",
										 x_label='$m_{x}$',
										 y_label='$m_{y}$',
										 z_label='$B_{11}$',
										 tick_size=tick_size,
										 title_size=title_size,
										 label_size=label_size,
										 label_pad=label_pad)

			#Diffusion Y
			ax[1][2].remove()
			ax[1][2] = fig.add_subplot(2, 3, 6, projection='3d')
			_, ax[1][2] = self._plot_data(diffY,
										 ax=ax[1][2],
										 title="Diffusion Y",
										 x_label='$m_{x}$',
										 y_label='$m_{y}$',
										 z_label='$B_{22}$',
										 tick_size=tick_size,
										 title_size=title_size,
										 label_size=label_size,
										 label_pad=label_pad)
			 """

		else:
			#Time Series
			M, drift, diff, drift_ebar, diff_ebar = data
			if timeseries_end > len(M):
				timeseries_end = len(M)
			fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(12, 12))
			M_ = M[timeseries_start:timeseries_end]
			ax[0][0].plot(range(timeseries_start, timeseries_end),  M_)
			ax[0][0].set_ylim(min(M_), max(M_))
			self._stylize_axes(ax[0][0],
							  x_label=text['timeseries_xlabel'],#'Time Index',
							  y_label=text['timeseries_ylabel'],#'|M|',
							  title=text['timeseries_title'],#'Time Series',
							  tick_size=tick_size,
							  title_size=title_size,
							  label_size=label_size,
							  label_pad=label_pad)

			#Dist |M|
			sns.distplot(M, kde=kde, ax=ax[1][0])
			ax[1][0].set_xticks(np.linspace(min(M), max(M), 5))
			self._stylize_axes(ax[1][0],
							  x_label=text['hist_xlabel'],#'M',
							  y_label=text['hist_ylabel'],#'Frequency',
							  title=text['hist_title'],#'',
							  tick_size=tick_size,
							  title_size=title_size,
							  label_size=label_size,
							  label_pad=label_pad)

			#Drift
			#p_drift, _ = self._fit_poly(self.op, drift, drift_order)
			#ax[0][1].scatter(self.op, drift, marker='.', label='drift')
			ax[0][1].errorbar(self.op, drift, yerr=drift_ebar,fmt='o', label='drift')
			"""
			ax[0][1].plot(self.op,
							 p_drift(self.op),
							 #marker='.',
							 alpha=0.3,
							 color='black',
							 label='poly_fit')
			"""
			ax[0][1].set_xticks(np.linspace(min(self.op), max(self.op), 5))
			ax[0][1].set_yticks(np.linspace(min(drift), max(drift), 5))
			self._stylize_axes(ax[0][1],
							  x_label=text['drift_xlabel'],#'m',
							  y_label=text['drift_ylabel'],#'F',
							  title=text['drift_title'],#'Drift',
							  tick_size=tick_size,
							  title_size=title_size,
							  label_size=label_size,
							  label_pad=label_pad)
			#ax[0][1].legend(loc=1, frameon=False, fontsize=tick_size)
			#Diffusion
			#p_diff, _ = self._fit_poly(self.op, diff, diff_order)
			#ax[1][1].scatter(self.op, diff, marker='.', label='diffusion')
			ax[1][1].errorbar(self.op, diff, yerr=diff_ebar, fmt='o', label='diffusion')
			"""
			ax[1][1].plot(self.op,
							 p_diff(self.op),
							 #marker='.',
							 alpha=0.3,
							 color='black',
							 label='poly_fit')
			"""
			ax[1][1].set_xticks(np.linspace(min(self.op), max(self.op), 5))
			ax[1][1].set_yticks(np.linspace(min(diff), max(diff), 5))
			self._stylize_axes(ax[1][1],
							  x_label=text['diffusion_xlabel'],#'m',
							  y_label=text['diffusion_ylabel'],#'$G^{2}$',
							  title=text['diffusion_title'],#'Diffusion',
							  tick_size=tick_size,
							  title_size=title_size,
							  label_size=label_size,
							  label_pad=label_pad)
			#ax[1][1].legend(loc=1, frameon=False, fontsize=tick_size)

		#plt.tight_layout()
		#plt.subplots_adjust(bottom=0.3)
		#fig.add_axes([0,0,1,1]).axis("off")
		plt.tight_layout()
		return fig

	def _plot_timeseries(self,
						 timeseries,
						 vector,
						 start=0,
						 stop=1000,
						 n_ticks=3,
						 dpi=150,
						 tick_size=12,
						 title_size=14,
						 label_size=14,
						 label_pad=0,
						 **plot_text):
		"""
		Plots timeseries figure
		"""
		text = {
			'timeseries_title' : 'Time Series',
			'timeseries_xlabel' : 'Time Index',
			'timeseries_ylabel' : 'M',

			'timeseries1_title' : 'Time Series',
			'timeseries1_xlabel' : '',
			'timeseries1_ylabel' : '$M_{x}$',

			'timeseries2_title' : '',
			'timeseries2_xlabel' : '',
			'timeseries2_ylabel' : '$M_{y}$',

			'timeseries3_title' : '',
			'timeseries3_xlabel' : '',
			'timeseries3_ylabel' : '|M|'
		}
		for k in plot_text.keys():
			if k not in text.keys():
				print("{} not a valid plot text key".format(k))
		text.update(plot_text)
		if vector:
			Mx, My = timeseries
			if stop > len(Mx):
				stop = len(Mx)
			fig, ax = plt.subplots(nrows=3, ncols=1, dpi=150, figsize=(8,6))
			ax[0].plot(range(start, stop),Mx[start:stop], linewidth=1)
			ax[0].set_xticks([])
			ax[0].set_yticks(np.linspace(min(Mx), max(Mx), n_ticks).round(2))
			self._stylize_axes(ax[0],x_label=text['timeseries1_xlabel'], y_label=text['timeseries1_ylabel'], title=text['timeseries1_title'], label_size=label_size, title_size=title_size, tick_size=tick_size)


			ax[1].plot(range(start, stop),My[start:stop], linewidth=1)
			ax[1].set_xticks([])
			ax[1].set_yticks(np.linspace(min(My), max(My), n_ticks).round(2))
			self._stylize_axes(ax[1],x_label=text['timeseries2_xlabel'], y_label=text['timeseries2_ylabel'], title=text['timeseries2_title'],label_size=label_size, tick_size=tick_size)


			M = np.sqrt(Mx**2 + My**2)
			ax[2].plot(range(start, stop),M[start:stop], linewidth=1)
			ax[2].set_yticks(np.linspace(min(M), max(M), n_ticks).round(2))
			self._stylize_axes(ax[2],x_label=text['timeseries3_xlabel'], y_label=text['timeseries3_ylabel'], title=text['timeseries3_title'], label_size=label_size, tick_size=tick_size)


		else:
			Mx = timeseries[0]
			if stop > len(Mx):
				stop = len(Mx)
			fig, ax = plt.subplots(dpi=150, figsize=(6,3))
			ax.plot(range(start, stop),Mx[start:stop], linewidth=1)
			self._stylize_axes(ax,x_label=text['timeseries_xlabel'], y_label=text['timeseries_ylabel'], title=text['timeseries_title'],tick_size=tick_size, label_size=label_size, title_size=title_size)
			ax.set_yticks(np.linspace(min(Mx), max(Mx), n_ticks).round(2))

		plt.tight_layout()
		return fig

	def _plot_histograms(self,
						 timeseries,
						 vector,
						 dpi=150,
						 kde=False,
						 title_size=14,
						 label_size=15,
						 tick_size=12,
						 label_pad=8,
						 **plot_text):
		"""
		Plot histogram figures
		"""

		text = {
			'hist_title' : '',
			'hist_xlabel' : 'M',
			'hist_ylabel' : 'Frequency',


			'hist1_title' : '',
			'hist1_xlabel' : '$M_{x}$',
			'hist1_ylabel' : 'Frequency',

			'hist2_title' : '',
			'hist2_xlabel' : '$M_{y}$',
			'hist2_ylabel' : 'Frequency',	

			'hist3_title' : '',
			'hist3_xlabel' : '$|M|$',
			'hist3_ylabel' : 'Frequency',

			'hist4_title' : '',
			'hist4_xlabel' : '$M_{x}$',
			'hist4_ylabel' : '$M_{y}$',
			'hist4_zlabel' : 'Frequency'		
		}
		for k in plot_text.keys():
			if k not in text.keys():
				print("{} not a valid plot text key".format(k))
		text.update(plot_text)
		if vector:
			Mx, My = timeseries
			M = np.sqrt(Mx**2 + My**2)
			fig, ax = plt.subplots(nrows=2, ncols=2, dpi=150, figsize=(8,8))
			plt.subplots_adjust(wspace= 0.4, hspace= 0.4)
			ax[0][0] = sns.distplot(Mx, kde=kde, ax=ax[0][0])
			if not kde:
				ticks = [str(i)+"K" for i in (np.array(ax[0][0].get_yticks())/1000).round(1)]
				ax[0][0].set_yticklabels(ticks)
			self._stylize_axes(ax[0][0],	x_label=text['hist1_xlabel'], y_label=text['hist1_ylabel'], title=text['hist1_title'], tick_size=tick_size, label_size=label_size, title_size=title_size, label_pad=label_pad)

			ax[0][1] = sns.distplot(My, kde=kde, ax=ax[0][1])
			if not kde:
				ticks = [str(i)+"K" for i in (np.array(ax[0][1].get_yticks())/1000).round(1)]
				ax[0][1].set_yticklabels(ticks)
			self._stylize_axes(ax[0][1],	x_label=text['hist2_xlabel'], y_label=text['hist2_ylabel'], title=text['hist2_title'], tick_size=tick_size, label_size=label_size, title_size=title_size, label_pad=label_pad)

			ax[1][0] = sns.distplot(M, kde=kde, ax=ax[1][0])
			if not kde:
				ticks = [str(i)+"K" for i in (np.array(ax[1][0].get_yticks())/1000).round(1)]
				ax[1][0].set_yticklabels(ticks)
			self._stylize_axes(ax[1][0],	x_label=text['hist3_xlabel'], y_label=text['hist3_ylabel'], title=text['hist3_title'], tick_size=tick_size, label_size=label_size, title_size=title_size, label_pad=label_pad)

			ax[1][1].remove()
			ax[1][1] = fig.add_subplot(2,2,4, projection='3d')
			ax[1][1].set_title('3d Histogram')
			ax[1][1] = self._plot_3d_hisogram(Mx, My, ax=ax[1][1], title=text['hist4_title'], title_size=title_size, label_size=label_size, tick_size=tick_size, label_pad=label_pad)

		else:
			M = timeseries[0]
			fig, ax = plt.subplots(nrows=1, ncols=2, dpi=150, figsize=(8,4))
			ax[0] = sns.distplot(M, kde=kde, ax=ax[0])
			self._stylize_axes(ax[0], x_label=text['hist_xlabel'], y_label=text['hist_ylabel'], title=text['hist_title'],tick_size=tick_size, label_size=label_size, title_size=title_size, label_pad=label_pad)
			ticks = [str(i)+"K" for i in (np.array(ax[0].get_yticks())/1000).round(1)]
			ax[0].set_yticklabels(ticks)

			ax[1] = sns.distplot(np.sqrt(M**2), kde=kde, ax=ax[1])
			self._stylize_axes(ax[1], x_label="|{}|".format(text['hist_xlabel']), y_label=text['hist_ylabel'], title=text['hist_title'], tick_size=tick_size, label_size=label_size, title_size=title_size, label_pad=label_pad)
			ticks = [str(i)+"K" for i in (np.array(ax[1].get_yticks())/1000).round(1)]
			ax[1].set_yticklabels(ticks)

		plt.tight_layout()
		return fig

	def _plot_noise_characterstics(self, 
									data, 
									dpi=150, 
									kde=True, 
									title_size=14, 
									tick_size=15, 
									label_size=15,
									label_pad=8):
		"""
		Plot noise charactersitic figure
		"""

		noise, kl_dist, X1, h_lim, k, l_lim, f, noise_correlation = data

		fig, ax = plt.subplots(nrows=2, ncols=2, dpi=150, figsize=(10,8))

		ax[0][0].plot(noise[0:1000])
		self._stylize_axes(ax[0][0],	
						x_label='', 
						y_label='Noise', 
						title="Residuals", 
						tick_size=tick_size, 
						label_size=label_size, 
						title_size=title_size, 
						label_pad=label_pad)

		lags = 50
		if len(noise) < lags + 1:
			lags = len(noise) - 1
		statsmodels.graphics.tsaplots.plot_acf(noise, lags=lags, ax=ax[1][0], missing='conservative')
		#ax[1][0].plot(noise_correlation[0], noise_correlation[1])
		self._stylize_axes(ax[1][0],	
						x_label='lags', 
						y_label='ACF(Noise)', 
						title="Noise Autocorrelation", 
						tick_size=tick_size, 
						label_size=label_size, 
						title_size=title_size, 
						label_pad=label_pad)

		ax[0][1] = sns.distplot(noise, kde=kde, ax=ax[0][1])
		self._stylize_axes(ax[0][1],	
						x_label='', 
						y_label='Density', 
						title="Noise Distribution", 
						tick_size=tick_size, 
						label_size=label_size, 
						title_size=title_size, 
						label_pad=label_pad)

		ax[1][1] = sns.distplot(kl_dist, kde=kde, ax=ax[1][1])
		start, stop = ax[1][1].get_ylim()
		ax[1][1].plot(np.ones(len(X1)) * l_lim,
		 np.linspace(start, stop, len(X1)), 'r', label='2.5%')
		ax[1][1].plot(np.ones(len(X1)) * k,
		 np.linspace(start, stop, len(X1)), 'g', label='Test Statistics')
		ax[1][1].plot(np.ones(len(X1)) * h_lim,
		 np.linspace(start, stop, len(X1)), 'r', label='97.5%'.format(h_lim))
		self._stylize_axes(ax[1][1],	
				x_label='', 
				y_label='', 
				title="Hypothesis Testing", 
				tick_size=tick_size, 
				label_size=label_size, 
				title_size=title_size, 
				label_pad=label_pad)
		ax[1][1].legend(prop={'size':6})
		"""
		ax[0][0] = sns.distplot(noise, kde=kde, ax=ax[0][0])
		self._stylize_axes(ax[0][0],	
						x_label='', 
						y_label='Density', 
						title="Noise Distrubution", 
						tick_size=tick_size, 
						label_size=label_size, 
						title_size=title_size, 
						label_pad=label_pad)

		ax[0][1].plot(noise_correlation[0], noise_correlation[1])
		self._stylize_axes(ax[0][1],	
						x_label='', 
						y_label='Correlation coeff', 
						title="Noise Correlation", 
						tick_size=tick_size, 
						label_size=label_size, 
						title_size=title_size, 
						label_pad=label_pad)

		ax[1][0] = sns.distplot(kl_dist, kde=kde, ax=ax[1][0])
		start, stop = ax[1][0].get_ylim()
		ax[1][0].plot(np.ones(len(X1)) * l_lim,
		 np.linspace(start, stop, len(X1)), 'r', label='lower_cl')
		ax[1][0].plot(np.ones(len(X1)) * k,
		 np.linspace(start, stop, len(X1)), 'g', label='Test Statistics')
		ax[1][0].plot(np.ones(len(X1)) * h_lim,
		 np.linspace(start, stop, len(X1)), 'r', label='upper_cl')
		self._stylize_axes(ax[1][0],	
				x_label='', 
				y_label='', 
				title="Null hypothesis", 
				tick_size=tick_size, 
				label_size=label_size, 
				title_size=title_size, 
				label_pad=label_pad)
		ax[1][0].legend(prop={'size':6})

		
		ax[1][1].plot(X1[1:], f)
		ax[1][1].plot(np.ones(len(X1[1:])) * l_lim, f, 'r', label='lower_cl')
		ax[1][1].plot(np.ones(len(X1[1:])) * h_lim, f, 'r', label='upper_cl')
		ax[1][1].plot(np.ones(len(X1[1:])) * k, f, 'g', label='Test Stat')
		self._stylize_axes(ax[1][1],	
				x_label='', 
				y_label='', 
				title="CDF", 
				tick_size=tick_size, 
				label_size=label_size, 
				title_size=title_size, 
				label_pad=label_pad)
		ax[1][1].legend(loc=1, prop={'size':6})
		"""
		plt.tight_layout()
		return fig


	def _remove_nans(self, Mx, My):
		"""
		Remove nan's from data
		"""
		nan_idx = (np.where(np.isnan(Mx)) and np.where(np.isnan(My)))
		return np.array([np.delete(Mx, nan_idx), np.delete(My, nan_idx)])

	def _plot_3d_hisogram(self, Mx, My, ax=None, title="PDF",xlabel="$M_{x}$", ylabel="$M_{y}$",zlabel="Frequency", tick_size=12, title_size=14, label_size=10, label_pad=12, r_fig=False, dpi=150):
		"""
		Plot 3d bar plot
		"""
		if ax is None:
			fig = plt.figure(dpi=dpi)
			ax = fig.add_subplot(projection="3d")


		H, edges, X, Y, Z, dx, dy, dz = self._histogram3d(self._remove_nans(Mx, My))
		colors = plt.cm.coolwarm(dz.flatten() / float(dz.max()))
		hist3d = ax.bar3d(X,Y,Z,dx,dy,dz,alpha=0.6,cmap=plt.cm.coolwarm,color=colors)
		ax.set_xlabel(xlabel, fontsize=label_size, labelpad=label_pad)
		ax.set_ylabel(ylabel, fontsize=label_size, labelpad=label_pad)
		ax.zaxis.set_rotate_label(False)
		ax.set_zlabel(zlabel, fontsize=label_size, labelpad=label_pad, rotation=90)
		ax = self._set_zaxis_to_left(ax)

		# make the panes transparent
		ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
		ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
		ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

		# make the grid lines transparent
		ax.xaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
		ax.yaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
		ax.zaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
		#Set ticks lable and its fontsize
		ax.set_xticks(np.linspace(round(min(Mx),2), round(max(Mx),2), 3))
		ax.set_yticks(np.linspace(round(min(My),2), round(max(My),2), 3))
		ax.set_title(title, fontsize=title_size)
		ticks = [str(i)+"K" for i in (np.array(ax.get_zticks())/1000).round(1)]
		ax.set_zticklabels(ticks)
		ax.tick_params(axis='both', which='major', labelsize=tick_size, pad=5)
		if r_fig:
			return fig, ax
		return ax

	def _slider_3d(self, slider_data, init_pos=0, prefix='dt', order=None, **plot_text):
		"""
		Get slider for analysed vector data.
		"""
		slider_texts = {
		'dt':{
			'title1' : 'Drift X',
			'x_label1' : 'mx',
			'y_label1' : 'my',
			'z_label1' : 'A1',

			'title2' : 'Drift Y',
			'x_label2' : 'mx',
			'y_label2' : 'my',
			'z_label2' : 'A2' 	},

		'Dt' :{
			'title1' : 'Diffusion X',
			'x_label1' : 'mx',
			'y_label1' : 'my',
			'z_label1' : 'B11',

			'title2' : 'Diffusion Y',
			'x_label2' : 'mx',
			'y_label2' : 'my',
			'z_label2' : 'B22' 	},

		'c_dt': {
			'title1' : 'Diffusion XY',
			'x_label1' : 'mx',
			'y_label1' : 'my',
			'z_label1' : 'B12',

			'title2' : 'Diffusion YX',
			'x_label2' : 'mx',
			'y_label2' : 'my',
			'z_label2' : 'B21' 	}
		}

		text = slider_texts[prefix]
		text.update(plot_text)

		dt_s = list(slider_data.keys())
		opt_step = dt_s[init_pos]
		if prefix == 'Dt':
			t = 'Drift'
			t_tex = "\Delta t"
			sub_titles = (text['title1'], text['title2'])
			scene1 = dict(
				xaxis=dict(showbackground=True),
				yaxis=dict(showbackground=True),
				zaxis=dict(showbackground=True, ),
				xaxis_title=text['x_label1'],
				yaxis_title=text['y_label1'],
				zaxis_title=text['z_label1'],
			)
			scene2 = dict(
				xaxis=dict(showbackground=True),
				yaxis=dict(showbackground=True),
				zaxis=dict(showbackground=True, ),
				xaxis_title=text['x_label2'],
				yaxis_title=text['y_label2'],
				zaxis_title=text['z_label2'],
			)
		elif prefix == 'dt':
			t = 'Diffusion'
			t_tex = "\delta t"
			sub_titles = (text['title1'], text['title2'])
			scene1 = dict(
				xaxis=dict(showbackground=True),
				yaxis=dict(showbackground=True),
				zaxis=dict(showbackground=True, ),
				xaxis_title=text['x_label1'],
				yaxis_title=text['y_label1'],
				zaxis_title=text['z_label1'],
			)
			scene2 = dict(
				xaxis=dict(showbackground=True),
				yaxis=dict(showbackground=True),
				zaxis=dict(showbackground=True, ),
				xaxis_title=text['x_label2'],
				yaxis_title=text['y_label2'],
				zaxis_title=text['z_label2'],
			)
		else:
			prefix = 'dt'
			t = 'Cross Correaltion'
			t_tex = "\delta t"
			sub_titles = (text['title1'], text['title2'])
			scene1 = dict(
				xaxis=dict(showbackground=True),
				yaxis=dict(showbackground=True),
				zaxis=dict(showbackground=True, ),
				xaxis_title=text['x_label1'],
				yaxis_title=text['y_label1'],
				zaxis_title=text['z_label1'],
			)
			scene2 = dict(
				xaxis=dict(showbackground=True),
				yaxis=dict(showbackground=True),
				zaxis=dict(showbackground=True, ),
				xaxis_title=text['x_label2'],
				yaxis_title=text['y_label2'],
				zaxis_title=text['z_label2'],
			)
		nrows, ncols = 1, 2
		title_template = r"$\text{{ {0} |  Autocorrelation time (Mx, My, |M^2|) : ({4}, {5}, {1}) }} | \text{{ Slider switched to }}{2}= {3}$"
		fig = make_subplots(
			rows=nrows,
			cols=ncols,
			specs=[
				[{
					'type': 'scene'
				}, {
					'type': 'scene'
				}],
			],
			print_grid=False,
			subplot_titles=sub_titles,
			horizontal_spacing=0.1,
		)

		x, y = np.meshgrid(self.op_x, self.op_y)
		n = list(sub_titles)
		for dt in slider_data:
			data = slider_data[dt]
			visible = 'legendonly'
			if dt == opt_step:
				visible = True
			k = 0
			for r in range(1, nrows + 1):
				for c in range(1, ncols + 1):
					#marker_colour = 'blue'
					#if k % 2: marker_colour = 'red'
					marker_colour = self._c_pallet[dt_s.index(dt)%len(self._c_pallet)]
					if k % 2 : marker_colour = self._c_pallet[dt_s.index(dt)%len(self._c_pallet)]
					fig.append_trace(
						go.Scatter3d(x=(x.flatten()),
									 y=(y.flatten()),
									 z=(data[k].flatten()),
									 opacity=1,
									 mode='markers',
									 #marker=dict(size=3, color=marker_colour),
									 marker=dict(
										color=marker_colour,
										size=3,
										line=dict(
											color='black',
											width=0
										)
									),
									 name="{}, {}".format(n[k], dt),
									 visible=visible),
						row=r,
						col=c,
					)
					if isinstance(order, int):
						x, y = np.meshgrid(self.op_x, self.op_y)
						c_s = []
						for _ in range(len(x.flatten())):
							c_s.append([1, 'rgb(1, 0, 0)'])
						try:
							plane = self._fit_plane(x=x, y=y, z=data[k], order=order)
						except:
							print('Unable to fit plane')
							order =None
							k = k + 1
							continue
						fig.append_trace(
							go.Surface(
								x=x,
								y=y,
								z=plane(x,y),
								opacity=0.3,
								name='fit',
								visible=visible,
								showscale=False,
								colorscale=c_s,
								surfacecolor=c_s,
								),
							row=r,
							col=c,
							)
					k = k + 1
		fig.update_layout(
			autosize=True,
			scene1_aspectmode='cube',
			scene2_aspectmode='cube',
			scene1=scene1,
			scene2=scene2,
			#scene3 = scene,
			#scene4 = scene,
			title_text=title_template.format(t, self.autocorrelation_time,
											 t_tex,
											 dt_s[init_pos], self._act_mx, self._act_my),
			height=600,
			width=900,
			#updatemenus=[
			#	dict(
			#		type="buttons",
			#		direction="left",
			#		buttons=list([
			#			dict(
			#				args=[{
			#					"type": ["scatter3d", "scatter3d"]
			#				}],
			#				#{'traces': [0, 1]}],
			#				label="3D",
			#				method="restyle"),
			#			dict(
			#				args=[{
			#					"type": ["heatmap", "heatmap"]
			#				}],
			#				#{'traces': [0, 1]}],
			#				label="Heatmap",
			#				method="restyle")
			#		]),
			#		pad={
			#			"r": 10,
			#			"t": 10
			#		},
			#		showactive=True,
			#		x=0.11,
			#		xanchor="left",
			#		y=1.1,
			#		yanchor="top"),
			#]
			)

		steps = []
		step_n = 2
		if isinstance(order, int):
			step_n = 4
		for i in range(len(slider_data)):
			step = dict(
				method='update',
				args=[{
					"visible": ['legendonly'] * len(fig.data)
				}, {
					"title":
					title_template.format(t, self.autocorrelation_time, t_tex,
										  str(dt_s[i]), self._act_mx, self._act_my),
				}],  # layout attribute
				label='{} {}'.format(prefix,
									 list(slider_data.keys())[i]))
			#step['args'][0][i*4:i*4+4] = [True for j in range(4)]
			#step['args'][0]['visible'][i * 2:i * 2 + 2] = [True for j in range(2)]
			step['args'][0]['visible'][i * step_n:i * step_n + step_n] = [True for j in range(step_n)]

			steps.append(step)

		sliders = [
			dict(
				currentvalue={"prefix": "{} : ".format(prefix)},
				active = init_pos,
				steps=steps,
			)
		]

		fig.layout.sliders = sliders
		fig.layout.template = 'plotly_white'
		#fig.layout.template = 'plotly'


		return fig

	def _slider_2d(self, slider_data, init_pos=0, prefix='Dt', polynomial_order=None, **plot_text):
		"""
		Get slider for analysed scalar data
		"""
		slider_texts = {
		'Dt': {
			'x_label':'m',
			'y_label':'A1'
			},
		'dt': {
			'x_label':'m',
			'y_label':'A2'
			}
		}
		text = slider_texts[prefix]
		text.update(plot_text)
		data = slider_data
		title_template = r"$\text{{ {0} |  Auto correlation time : {1} }} | \text{{ Slider switched to }}{2}= {3}$"
		if prefix == 'Dt':
			t = 'Drift'
			t_tex = "\Delta t"
		else:
			t = 'Diffusion'
			t_tex = "\delta t"
			
		# Create figure
		fig = go.Figure()
		# Add traces, one for each slider step
		dt_s = list(data.keys())
		opt_step = dt_s[init_pos]
		for step in sorted(data.keys()):
			visible = 'legendonly'
			if step == opt_step:
				visible = True
			marker_colour = "red"
			marker_colour = self._c_pallet[dt_s.index(step)%len(self._c_pallet)]
			fig.add_trace(
				go.Scatter(
					visible=visible,
					mode='markers',
					marker=dict(
						color=marker_colour,
						size=10,
						opacity=1,
						line=dict(
							color='black',
							width=1
						)
					),
					#line=dict(color=marker_colour, width=6),
					name="{} = {}".format(prefix, str(step)),
					x=data[step][-1],
					y=data[step][0]))
			if isinstance(polynomial_order, int):
				poly, op = self._fit_poly(data[step][-1], data[step][0], polynomial_order)

				fig.add_trace(
					go.Scatter(
						visible=visible,
						#mode='markers',
						opacity=0.3,
						line=dict(color=marker_colour, width=6),
						name="poly_fit = " + str(step),
						x=op,
						y=poly(op)))

		fig.update_layout(
			autosize=True,
			scene_aspectmode='cube',
			title_text=title_template.format(t, self.autocorrelation_time,
											 t_tex,
											 dt_s[init_pos]),
			height=850,
			width=850,
			)
		fig.update_xaxes(title=dict(text=text['x_label']))
		fig.update_yaxes(title=dict(text=text['y_label']))

		# Create and add slider
		steps = []
		step_n = 1
		if isinstance(polynomial_order, int):
			step_n = 2
		for i in range(len(dt_s)):
			step = dict(
				method="update",
				args=[{"visible": ['legendonly'] * len(fig.data)},
					  {"title": title_template.format(t, self.autocorrelation_time, t_tex,  str(dt_s[i]))}],  # layout attribute
				label='{} {}'.format(prefix,
						 list(data.keys())[i]))
			
			#step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
			step['args'][0]['visible'][i * step_n:i * step_n + step_n] = [True for j in range(step_n)]
			steps.append(step)

		sliders = [dict(
			active=init_pos,
			currentvalue={"prefix": "{}: ".format(prefix)},
			#pad={"t": 50},
			steps=steps
		)]



		fig.layout.sliders = sliders
		fig.layout.template = 'plotly_white'

		return fig

	def _thrace_pane(self, data):
		"""
		Thrace an arbetery surface that covers the data points.

		Notes
		-----
		To be used only to get a better visual of the shape of the surface.
		"""
		op_x = self.op_x.copy()
		op_y = self.op_y.copy()
		plane1 = []
		plane2 = []
		for y in data:
			nan_idx = np.where(np.isnan(y))
			try:
				p, x = self._fit_poly(op_x, y, deg=6)
				d = p(op_x)
			except Exception as e:
				d = np.zeros(y.shape)
			d[nan_idx] = np.nan
			plane1.append(d)

		for y in data.T:
			nan_idx = np.where(np.isnan(y))
			try:
				p, x = self._fit_poly(op_x, y, deg=6)
				d = p(op_x)
			except:
				d = np.zeros(y.shape)
			d[nan_idx] = np.nan
			plane2.append(d)

		plane1 = np.array(plane1)
		plane2 = np.array(plane2)
		err_1 = np.nanmean(np.sqrt(np.square(plane1 - data)))
		err_2 = np.nanmean(np.sqrt(np.square(plane2 - data.T)))
		if err_1 < err_2:
			return 0, plane1
		return 1, plane2

	def _set_zaxis_to_left(self, ax):
		"""
		Sets the z-axis of 3d figure to left
		"""
		default_planes = (
		(0, 3, 7, 4), (1, 2, 6, 5),     # yz planes
		(0, 1, 5, 4), (3, 2, 6, 7),     # xz planes
		(0, 1, 2, 3), (4, 5, 6, 7),     # xy planes
			)
		tmp_planes = ax.zaxis._PLANES
		if tmp_planes == default_planes:
			ax.zaxis._PLANES = (tmp_planes[2], tmp_planes[3],
				 tmp_planes[0], tmp_planes[1],
				 tmp_planes[4], tmp_planes[5])
		return ax

	def _plot_data(self,
				  data_in,
				  title='title',
				  x_label='$m_x$',
				  y_label='$m_y$',
				  z_label='z',
				  ax=None,
				  clear=True,
				  legend=False,
				  plot_plane=False,
				  tick_size=12,
				  title_size=16,
				  label_size=14,
				  label_pad=12,
				  label=None,
				  order=3,
				  m=False,
				  m_th=2,
				  dpi=150,
				  heatmap=False):
		"""
		Plot data on a 3d axis
		"""

		fig = None
		if heatmap:
			return self._plot_heatmap(data_in, title=title)
		if ax is None:
			fig = plt.figure(dpi=dpi)
			ax = fig.add_subplot(projection="3d")

		#ax = self._set_zaxis_to_left(ax)

		data = data_in.copy()
		mask = np.where(((data > m_th * np.nanstd(data)) |
						 (data < -m_th * np.nanstd(data))))
		if m:
			#print(mask)
			data[mask] = np.nan
		if clear:
			ax.cla()
		op_x = self.op_x.copy()
		op_y = self.op_y.copy()

		plane = []
		if plot_plane:
			plane_id, plane = self._thrace_pane(data)

		x, y = np.meshgrid(op_x, op_y)
		z = data.copy()
		ax.set_title(title, fontsize=title_size)

		ax.scatter3D(x, y, z.ravel(), label=label, marker='.')
		if plot_plane:
			if plane_id:
				#print('Plane 2')
				ax.plot_surface(
					y,
					x,
					plane,
					rstride=1,
					cstride=1,
					alpha=0.5,
				)
			else:
				#print('Plane 1')
				ax.plot_surface(
					x,
					y,
					plane,
					rstride=1,
					cstride=1,
					alpha=0.5,
				)
		ax.set_xlabel(x_label, fontsize=label_size, labelpad=label_pad)
		ax.set_ylabel(y_label, fontsize=label_size, labelpad=label_pad)
		ax.zaxis.set_rotate_label(False)
		ax.set_zlabel(z_label, fontsize=label_size, labelpad=label_pad, rotation=90)
		ax = self._set_zaxis_to_left(ax)

		# make the panes transparent
		ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
		ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
		ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
		# make the grid lines transparent
		ax.xaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
		ax.yaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
		ax.zaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
		#Set ticks lable and its fontsize
		ax.set_xlim3d(round(op_x[0], 2), round(op_x[-1], 2))
		ax.set_ylim3d(round(op_x[0], 2), round(op_x[-1], 2))
		ax.set_xticks(np.linspace(round(op_x[0],2), round(op_x[-1],2), 3))
		ax.set_yticks(np.linspace(round(op_y[0],2), round(op_y[-1],2), 3))
		#ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
		ax.ticklabel_format(style='sci',axis='x',scilimits=(0,0), useMathText=True)
		ax.ticklabel_format(style='sci',axis='y',scilimits=(0,0), useMathText=True)

		ax.tick_params(axis='both', which='major', labelsize=tick_size)
		#ax.xaxis._axinfo['label']['space_factor'] = 2.0
		#ax.yaxis._axinfo['label']['space_factor'] = 2.0
		#ax.zaxis._axinfo['label']['space_factor'] = 2.0
		#plt.tight_layout()
		if legend:
			#plt.legend(prop={'size': 14})
			ax.legend()
		return fig, ax

	def _plot_heatmap(self, data, title='title', num_ticks=5):
		"""
		Plots heatmap of data
		"""
		fig = plt.figure()
		plt.suptitle(title, verticalalignment='center', ha='right')
		ticks = self.op_x.copy()
		ticks_loc = np.linspace(0, len(ticks), num_ticks)
		ticks = np.linspace(min(ticks), max(ticks), num_ticks).round(2)
		ax = sns.heatmap(data,
						 xticklabels=ticks[::-1],
						 yticklabels=ticks,
						 cmap=plt.cm.coolwarm,
						 center=0)
		ax.set_xlabel('$m_x$', fontsize=16, labelpad=10)
		ax.set_ylabel('$m_y$', fontsize=16, labelpad=10)
		ax.set_xticks(ticks_loc)
		ax.set_yticks(ticks_loc)
		ax.tick_params(axis='both', which='major', labelsize=14)
		plt.tight_layout()
		return fig, ax

	def _histogram3d(self,
					 x,
					 bins=20,
					 normed=False,
					 color='blue',
					 alpha=1,
					 hold=False,
					 plot_hist=False):
		"""
		Plotting a 3D histogram

		Parameters
		----------

		sample : array_like.		
			The data to be histogrammed. It must be an (N,2) array or data 
			that can be converted to such. The rows of the resulting array 
			are the coordinates of points in a 2 dimensional polytope.

		bins : sequence or int, optional, default: 10.
			The bin specification:
			
			* A sequence of arrays describing the bin edges along each dimension.
			* The number of bins for each dimension (bins =[binx,biny])
			* The number of bins for all dimensions (bins = bins).

		normed : bool, optional, default: False.
			If False, returns the number of samples in each bin. 
			If True, returns the bin density bin_count / sample_count / bin_volume.

		color: string, matplotlib color arg, default = 'blue'

		alpha: float, optional, default: 1.
			0.0 transparent through 1.0 opaque

		hold: boolean, optional, default: False

		Returns   
		--------
		H : ndarray.
			The bidimensional histogram of sample x.

		edges : list.
			A list of 2 arrays describing the bin edges for each dimension.
			
		Examples
		--------
		>>> r = np.random.randn(1000,2)
		>>> H, edges = np._histogram3d(r,bins=[10,15])
		"""

		if np.size(bins) == 1:
			bins = [bins, bins]

		if (len(x) == 2):
			x = x.T

		H, edges = np.histogramdd(x, bins, normed=normed)

		H = H.T
		X = np.array(
			list(np.linspace(min(edges[0]), max(edges[0]), bins[0])) * bins[1])
		Y = np.sort(
			list(np.linspace(min(edges[1]), max(edges[1]), bins[1])) * bins[0])

		dz = np.array([])

		for i in range(bins[1]):
			for j in range(bins[0]):
				dz = np.append(dz, H[i][j])

		Z = np.zeros(bins[0] * bins[1])

		dx = X[1] - X[0]
		dy = Y[bins[0]] - Y[0]

		if plot_hist:
			if (not hold):
				fig = plt.figure(dpi=300)
				ax = fig.add_subplot(111, projection='3d')
				colors = plt.cm.jet(dz.flatten() / float(dz.max()))
				ax.bar3d(X, Y, Z, dx, dy, dz, alpha=alpha, color=colors)
			else:
				try:
					ax = plt.gca()
					colors = plt.cm.jet(dz.flatten() / float(dz.max()))
					ax.bar3d(X, Y, Z, dx, dy, dz, alpha=alpha, color=colors)
				except:
					plt.close(plt.get_fignums()[-1])
					fig = plt.figure()
					ax = fig.add_subplot(111, projection='3d')
					colors = plt.cm.jet(dz.flatten() / float(dz.max()))
					ax.bar3d(X, Y, Z, dx, dy, dz, alpha=alpha, color=colors)

			plt.xlabel('X')
			plt.ylabel('Y')
		edges = [X, Y]
		H = dz.reshape(bins[0], bins[1])

		#return H, edges;
		return H, edges, X, Y, Z, dx, dy, dz
