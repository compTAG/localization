# TDA based localization
* TODO: Include a descriptive over view paragraph of our project here

## Prerequisits
* TODO: Add a list of `prereqs` to run this program

## Installing
* TODO: Add a step by step guide for `installing` the necessary tooling along side the project itself (possibly a video? does the compTag group have a channel we could upload it to for reference?)

## Running the Code with test.las

To get started, run main.py. You will then be prompted for the number of one dimensional partitions for your pointcloud which should be entered as an integer value. If two is chosen,  eight sections will be created. 

Next, when prompted for the filename, enter ‘test’ and press enter. 

After this, you will be prompted with options for point cloud data to localize which can be manually selected from the sections or randomly chosen. 

When prompted for the number of results desired, enter an integer value for the number of cell identifiers with the lowest bottleneck distances to the cell being searched for. The code will then evaluate the bottleneck distance between this chosen section and every other section and will return the desired number of distances.


## Running tests 

- #### What you will need
    - TODO: Add the data/format required to run our tests on.

- #### Examples
    - TODO: Provide examples of us running our tests with provided example data.

## Build with
- Anaconda
- Dionysus
- jsonpickle

## Authors
- George Engel
- Clare DuVal
- Luke Askew

## Acknowledgments
- David Millman
- Binhai Zhu
- Brittany Fasy
