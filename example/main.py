from pipeline import (
	Pipeline, 
	Extractor, 
	Transformer, 
	Loader, 
	cache_factory,
	artefact_factory
)
import pandas as pd


class AuthorExtractor(Extractor):
	"""
	AuthorExtractor retries author first name and last name, based on the post author id field
	"""

	def __init__(self, base_url: str, **params)-> None:
		super().__init__(**params)
		
		self.base_url = base_url

	@cache_factory("./cache", "authors", 10)
	def extract(self, author_id: int)-> dict:
		return self._get_from_url(self.base_url + "/authors/" + str(author_id))


class PostExtractor(Extractor):
	"""
	PostExtractor retries posts from the demo API
	"""

	def __init__(self, author_extractor: AuthorExtractor, base_url: str, **params)-> None:
		super().__init__(**params)

		self.author_extractor = author_extractor
		self.base_url = base_url

	# @cache_factory("./cache", "posts", 10)
	def extract(self)-> dict:
		body = self._get_from_url(self.base_url + "/posts")

		return [
			{
				"id": post["id"],
				"title": post["title"],
				"author": self.author_extractor.extract(author_id = post["author_id"])
			} for post in body
		]


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
	# pipe.run_schedule("* * * * *")