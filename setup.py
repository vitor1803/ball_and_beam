from setuptools import setup, find_packages

setup(
    name="ball_and_beam",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "pyserial",
    ],
    entry_points={
        "console_scripts": [
            "ui_arduino_ball_and_beam=main:main",
        ],
    },
    description="Uma aplicação Python para comunicação serial com Arduino.",
    author="Vitor Freitas",
    author_email="vsouza.eng@gmail.com",
)
