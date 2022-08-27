from pipeline import Extractor, Transformer, Loader


class Pipeline:

	def __init__(self, extractor: Extractor, transformer: Transformer, loader: Loader)-> None:
		self.extractor = extractor
		self.transformer = transformer
		self.loader = loader

	def run_once(self)-> None:
		self.loader.load(
			self.transformer.transform(
				self.extractor.extract()
			)
		)

	def run_schedule(self, schedule: str)-> None:
		pass