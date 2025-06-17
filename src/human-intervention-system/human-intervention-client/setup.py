from setuptools import setup, find_packages

setup(
    name="session_client_lib",
    version="0.1.0",
    description="Client library for session management with messaging and validation",
    author="Narasimha Prasanna HN",
    author_email="prasanna@opencyberspace.org",
    url="",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "nats-py>=2.0.0",
        "asyncio; python_version<'3.7'"
    ],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
