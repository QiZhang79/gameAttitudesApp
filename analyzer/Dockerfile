FROM fokkodriesprong/docker-pyspark:latest

## make a local directory
RUN mkdir /analyzer

# set "Twitter-Analysis" as the working directory from which CMD, RUN, ADD references
WORKDIR /analyzer

# now copy all the files in this directory to /analyzer
ADD . .

# pip install the local requirements.txt
RUN pip install -r requirements.txt

# Define our command to be run when launching the container
CMD python main/analyzer.py
