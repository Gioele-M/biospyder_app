# BioSpyder Sequence Analysis Tool
This is a fast tool for preliminary gene analysis which offers an interface for visualising descriptive metrics about the genes

*This is the* [deployed](https://biospyder-app.herokuapp.com) *version* 

*This is the* [link](https://github.com/Gioele-M/biospyder_app) *to the repo*


# Installation and usage
In order to run the app locally, you will need to have [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) installed.

### Installation
Once the directory is been downloaded or cloned locally, you will need to create a conda environment:
`conda env create -f environment.yml`

You can check for the successful creation of the environment using:
`conda BlastPTree_env list`

Once the environment is created, using the terminal:
- Move into the directory
`cd biospyder_app`
- Activate the conda environment
`conda activate spyder_app`
- Run the app
`python app.py`

The local host [server](http://localhost:8000/) will run on port 8000


### Usage
_Once the server is running, or the heroku server has responded, you will find yourself in the landing page, where you can upload a .fasta or .csv file containing genomic sequences._
![landing page](/assets/landing.png)




_After uploading a file in the correct format, you will be prompted with the number of sequences loaded, as well as a dropdown menu indicating to select one of the sequences for further details._
![upload page](/assets/uploaded.png)





_Once one of the sequences is chosen, the app will present you with metrics about the selected sequence, including length, base distribution and 10bp sequence with highest GC content._
![results page](/assets/results.png)


# Technologies
The app is based on Dash, but implements the use of pandas for data handling, pytest for testing and gunicorn for deploying.

# Future features
Future features include:
- Blasting the sequence against the NCBI database
- Local alignment of sequences
- Sequence translation and inference of 3D structure
