from obspy import read
import streamlit as st
import pandas as pd
import numpy as np
from bokeh.plotting import figure


sidebar_expander = st.sidebar.beta_expander("Seismic Viewer!")

rawData = None

with sidebar_expander:
    rawData = st.file_uploader('Upload data', type=['sgy'])
    buttomOk = st.button('Display Data')

    if rawData is not None:
      dataSGY = read(rawData)
      nTrace = len(dataSGY)
      nLength = len(dataSGY[0].data)

      axisXData = np.zeros((nLength, nTrace))
      axisYData = np.zeros((nLength, nTrace))

      maxTime = dataSGY[0].stats.npts
      time = np.cumsum([dataSGY[0].stats.delta for i in range(maxTime)])

      for i in range(len(dataSGY)):
        axisXData[:,i] = dataSGY[i].data
        axisYData[:,i] = time
      
      # print(np.shape(rawData))
      # print(np.shape(timeAxis))

# if axisXData is not None:
seisFig = figure(title="seismic viewer")
x = np.linspace(0, 4*np.pi, 100)
y = np.sin(x)
seisFig.line(x, y, line_width=0.2, color='black')
# for i in range(nTrace):
#   x = np.array(axisXData[:,i])
#   y = time
#   print(np.shape(x), np.shape(y))
#   seisFig.line(x, y, line_width=0.2, color='black')

st.bokeh_chart(seisFig, use_container_width=True)

# if dataSGY is not None:
#   fig, ax = plt.subplots()
#   for i in range(24):
#       x = (dataSGY[i].data / np.linalg.norm(dataSGY[i].data))*3 + i
#       ax.plot(x, time, color= 'black', linewidth=0.5)
#       ax.fill_betweenx(time, i, x, where=(x > i), color='black')
#   ax.invert_yaxis()

#   for i in range(24):
#     chart_data[i] = pd.DataFrame((dataSGY[i].data / np.linalg.norm(dataSGY[i].data))*3 + i)

#   # st.line_chart(chart_data, color='black')
#   st.pyplot(fig)



