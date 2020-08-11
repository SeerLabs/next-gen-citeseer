from distutils.core import setup

setup(name="Modules",
      version="0.1",
      description="Next Gen Seer Modules",
      author="Sai Raghav Keesara",
      packages=['ingestion', 'models', 'routers', 'services', 'utils'],
      requires=[])
