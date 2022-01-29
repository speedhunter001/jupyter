from vowpalwabbit import pyvw
from datetime import datetime
import tensorboardX as tx


class DFtoVWtoTensorboard:
	"""This class provides capability for learning possible on DFtoVW object, provides capability to 
	print metrics (average_loss, since_last, label, prediction, num_features) and also provides support 
	to log these metrics for Tensorboard Visualization"""

	def __init__(self, df_to_vw, vw):
		"""Construct a DFtoVWtoTensorboard object

		Parameters
		----------

		df_to_vw : A DFtoVW object
					This would be used to construct examples 
		vw		 : A vowpalwabbit object
 					This would be used for learning using the algorithm specified in the object, and also to compute a few metrics

		Returns
		-------

		self : DFtoVWtoTensorboard
		"""
		self.vw = vw
		self.vw_formatted_data = df_to_vw.convert_df()


	#------------------------------------------------------------------------------------------------		
	def _calculate_average_loss(self, sum_loss, weighted_examples):
		"""Calculate average loss

		Parameters
		----------

		sum_loss			: float
								This is the sum loss which is used to calculate average_loss
		weighted_examples   : float
								This is the weighted_example which is used to calculate average_loss

		Returns
		-------

		average_loss      : float
								average_loss calculated by sum_loss and weigted_examples or if ZeroDivisionError is encountered then 0. is returned 
		""" 
		try:
			return sum_loss / weighted_examples

		except ZeroDivisionError:
			return 0.


	#------------------------------------------------------------------------------------------------		
	def _calculate_since_last(self, sum_loss_since_last, weighted_examples_since_last):
		"""Calculate since last 

		Parameters
		----------

		sum_loss_since_last          : float
										This is the difference between current iteration's sum_loss and previous iteration's sum_loss which is used to calculate since_last
		weighted_examples_since_last : float
										This is the difference between current iteration's weighted_examples and previous iteration's weighted_examples which is used to calculate since_last

		Returns
		-------

		since_last      : float
							since_last calculated using sum_loss_since_last and weighted_examples_since_last or if ZeroDivisionError is encountered then 0. is returned 
		""" 
		try:
			return sum_loss_since_last / weighted_examples_since_last

		except ZeroDivisionError:
			return 0.


	#------------------------------------------------------------------------------------------------		
	def _print_metrics(self, average_loss, since_last, label, prediction, num_features):
		"""This method prints metrics

		Parameters
		----------

		average_loss : float
						This is the average_loss value
		since_last   : float
						This is the since_last value
		label        : integer
						This is the actual label of current example
		prediction   : integer
						This is the predicted label of current example
		num_features : integer
						This is the num_features value

		Returns
		-------

		None
		"""
		print( 'average_loss:{:.6f}'.format(average_loss) , end='\t')
		print('since_last:{:.6f}'.format(since_last), end='\t')
		print('label:', label, end='\t')    
		print('prediction:', prediction, end='\t')    
		print('num_features:', num_features) 


	#------------------------------------------------------------------------------------------------		
	def get_label(self, example, label_type):
		"""Similar to pyvw.get_prediction implementation this method gets the label for current example

		Parameters
		----------

		example    : example object
						Methods of this example object are used to get the appropiate label
		label_type : integer
						This is the integer for representing a specific type of label in vw
						- 0: lDEFAULT
						- 1: lBINARY
						- 2: lMULTICLASS
						- 3: lCOST_SENSITIVE
						- 4: lCONTEXTUAL_BANDIT
						- 5: lMAX
						- 6: lCONDITIONAL_CONTEXTUAL_BANDIT
						- 7: lSLATES
						- 8: lCONTINUOUS

		Returns
		-------

		label  : integer
					Actual label of the current example object
		"""
		switch_label_type = {
			pyvw.vw.lDefault: None,
			pyvw.vw.lBinary: example.get_simplelabel_label,
			pyvw.vw.lMulticlass: example.get_multiclass_label,
			pyvw.vw.lCostSensitive: example.get_costsensitive_class,
			pyvw.vw.lContextualBandit: example.get_cbandits_class,
	#         pyvw.vw.lConditionalContextualBandit: None,
	#         pyvw.vw.lSlates: None,
	#         pyvw.vw.lContinuous: None
		}
		return switch_label_type[label_type]()	


	#------------------------------------------------------------------------------------------------		
	def fit(self, df, tensorboard=True):
		"""Learns on the relevant examples and can also log metrics for tensorboard visualization

		Parameters
		----------

		df           : Pandas Dataframe object
						This is used for vw to learn from the corresponding examples of the records in this Pandas Dataframe object
		tensorboard  : boolean
						Default value is True, this parameter is used to control the logging of metrics for Tensorboard visualization
						If value is True : metrics are logged for Tensorboard visualization
						If value is False : metrics are not logged for Tensorboard visualization

		Returns
		-------

		None
		"""
		if tensorboard:
			logdir = "logs/scalars/" + datetime.now().strftime("%Y%m%d-%H%M%S")  # logs directory
			file_writer = tx.SummaryWriter(logdir + "/iris")   # creating file writer
		
		sum_loss = 0.
		weighted_examples = 0.

		for iteration, vw_format in enumerate(self.vw_formatted_data):
			# vw_format = self.vw_formatted_data[ind]   # get the string format of specific example
			example = self.vw.parse(vw_format)       # parse the string format, it returns an example object
			self.vw.learn(example)                  # learn on example

			label = self.get_label(example, self.vw.get_label_type())    
			prediction = pyvw.get_prediction(example, self.vw.get_prediction_type())
			num_features = example.get_feature_number()    

			self.vw.finish_example(example)  # Any use of vw object should be done after this and use of example before this 

			sum_loss_since_last = self.vw.get_sum_loss() - sum_loss  # vw.get_sum_loss() return current sum loss, sum_loss variable right now holds sum loss of previous iteration
			weighted_examples_since_last = self.vw.get_weighted_examples() - weighted_examples  # vw.get_weighted_examples() return current weighted examples(sum),  weighted_examples variable right now holds weighted examples of previous iteration		        
		
			sum_loss= self.vw.get_sum_loss()  # Now sum_loss no longer hold previous iteration's sum_loss
			weighted_examples = self.vw.get_weighted_examples()  # Now weighted_examples no longer hold previous iteration's weighted examples
		
			average_loss = self._calculate_average_loss(sum_loss, weighted_examples)
			since_last = self._calculate_since_last(sum_loss_since_last, weighted_examples_since_last)
		
			self._print_metrics(average_loss, since_last, label, prediction, num_features)

			if tensorboard:
				file_writer.add_scalar('average_loss', average_loss, iteration)  # logging average_loss on each iteration
				file_writer.add_scalar('since_last', since_last, iteration)   # logging since_last on each iteration
			#     file_writer.add_scalar('label' , label, iteration)
			#     file_writer.add_scalar('prediction', prediction, iteration)
			#     file_writer.add_histogram('label-prediction', [label, prediction], iteration)
			#     file_writer.add_histogram('label', label, iteration)
			#     file_writer.add_histogram('prediction', prediction, iteration)
				file_writer.add_scalar('num_features', num_features, iteration)