from setuptools import find_packages
from setuptools import setup


def read_requirements(filename: str) -> list[str]:
	try:
		with open(filename, "r") as file_handle:
			return file_handle.read().splitlines()
	except FileNotFoundError:
		print("File not found. Requirements default to an empty list.")
		return [""]


setup(name="Pydantic Examples", version="0.0.1", packages=find_packages(), install_requires=read_requirements("requirements.txt"))
