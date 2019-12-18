FROM victorhcm/opencv
ADD amazesolver.py ./
#ADD readamazeimage.py ./
CMD ["python","amazesolver.py"]
#CMD ["python","readamazeimage.py"]
