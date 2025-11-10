from setuptools import setup, find_packages

setup(
    name="personal-assistant",
    version="1.0.0",
    description="Персональний помічник для управління контактами та нотатками",
    author="Student",
    author_email="student@example.com",
    packages=find_packages(),
    install_requires=[
        "colorama",
        "difflib",
    ],
    entry_points={
        'console_scripts': [
            'personal-assistant=main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)