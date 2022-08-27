from pipeline import (
	Pipeline, 
	Extractor, 
	Transformer, 
	Loader, 
	cache_factory,
	artefact_factory
)
import pandas as pd


class PostExtractor(Extractor):
	"""
	PostExtractor retries posts from the demo API
	"""

	def __init__(self, **params)-> None:
		super().__init__(**params)
		if "author_extractor" not in params:
			raise Exception("author_extractor not supplied")

		if "base_url" not in params:
			raise Exception("base_url not supplied")

		self.author_extractor : AuthorExtractor = params["author_extractor"]
		self.base_url = params["base_url"]

	@cache_factory("./cache", "posts", 10)
	def extract(self)-> dict:
		body = self._get_from_url(self.base_url + "/posts")

		return [
			{
				"id": post["id"],
				"title": post["title"],
				"author": self.author_extractor.extract(author_id = post["author_id"])
			} for post in body
		]


class AuthorExtractor(Extractor):
	"""
	AuthorExtractor retries author first name and last name, based on the post author id field
	"""

	def __init__(self, **params)-> None:
		super().__init__(**params)

		if "base_url" not in params:
			raise Exception("base_url not supplied")
		
		self.base_url = params["base_url"]

	def extract(self, **params)-> dict:
		if "author_id" not in params:
			raise Exception("author_id not supplied")

		return self._get_from_url(self.base_url + "/authors/" + str(params["author_id"]))


class PostTransformer(Transformer):
	
	def __init__(self) -> None:
		super().__init__()

	@artefact_factory("./artefacts", "posts", True)
	def transform(self, data: dict)-> pd.DataFrame:
		trans_data = [
			[
				post["id"], 
				post["title"], 
				post["author"]["first_name"], 
				post["author"]["last_name"] 
			] for post in data
		]
		return pd.DataFrame(data=trans_data, columns=[
			"id", "title", "author_first_name", "author_last_name"
		])


class PrintLoader(Loader):

	def __init__(self) -> None:
		super().__init__()

	def load(self, data: pd.DataFrame)-> None:
		print(data)


if __name__ == "__main__":
	author_extractor = AuthorExtractor(base_url = "http://localhost:3000")
	pipe = Pipeline(
		PostExtractor(
			base_url = "http://localhost:3000", 
			author_extractor = author_extractor),
		PostTransformer(),
		PrintLoader()
	)

	pipe.run_once()