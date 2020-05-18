from setuptools import setup, find_packages

# see details in https://github.com/pypa/sampleproject/blob/master/setup.py

setup(
    name="datalize",
    description="No Frills, No Deps, Dataclass serialization",
    url="https://gitlab.com/Spindel/datalize",
    author="D. Spindel Ljungmark",
    author_email="spider@skuggor.se",
    keywords="dataclass json serialize",
    python_requires=">=3.8",
    # automatic version handling from git
    setup_requires=["setuptools_scm"],
    # Paths and packaging data
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    use_scm_version=True,
)
