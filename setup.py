from setuptools import setup
from pathlib import Path

HERE = Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
	name="python_etl_pipeline",
	keywords="python etl pipeline date date-science data-engineer",
	packages=["pipeline"],
	version="0.0.2",
	description="Python ETL data science pipeline",
	long_description=README,
	long_description_content_type="text/markdown",
	url="https://github.com/MihaiBlebea/etl_pipeline",
	author="Mihai Blebea",
	author_email="mihaiserban.blebea@gmail.com",
	license="MIT",
	install_requires=["requests", "cron-converter", "openpyxl", "pandas"],
	setup_requires=["pytest-runner"],
	tests_require=["pytest==4.4.1"],
	test_suite="tests",
)