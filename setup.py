import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="snip",
    version="0.1",
    author="Fabrizio Destro",
    author_email="destro.fabrizio@gmail.com",
    description="A small snippet manager.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dexpota/snip",
    packages=setuptools.find_packages(),
)
