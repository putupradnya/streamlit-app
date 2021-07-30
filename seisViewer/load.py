from obspy import read
import numpy as np

def loadData(uploadedFile):
  if uploadedFile is not None:
    try:
      dataSGY = read(uploadedFile)
      nTrace = len(dataSGY)
      nLength = len(dataSGY[0].data)

      rawData = np.zeros((nLength, nTrace))
      axisYData = np.zeros((nLength, nTrace))

      maxTime = dataSGY[0].stats.npts
      time = np.cumsum([dataSGY[0].stats.delta for i in range(maxTime)])

      for i in range(len(dataSGY)):
        rawData[:,i] = dataSGY[i].data
        axisYData[:,i] = time

    except UnicodeDecodeError as e:
      statError = (f'error loading sgy data: {e}')
      return statError
  else:
    rawData = None
    axisYData = None

  return rawData, axisYData