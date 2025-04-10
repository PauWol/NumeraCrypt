from setuptools import setup, find_packages

setup(
    name="numeracrypt",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["base91", "typer"],
    entry_points={
        "console_scripts": [
            "numcrypt=numcrypt.cli:main"
        ]
    },
    author="Your Name",
    description="NumeraCrypt CLI Tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
