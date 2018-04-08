FROM python:3.6-slim

## make a local directory
RUN mkdir /collector

# set "Twitter-Analysis" as the working directory from which CMD, RUN, ADD references
WORKDIR /collector

# now copy all the files in this directory to /collector
ADD . .

# pip install the local requirements.txt
RUN pip install -r requirements.txt

# Listen to port 5000 at runtime
EXPOSE 5555

# Define our command to be run when launching the container
CMD python main/stream.py
