import streamlit as st
st.set_page_config(layout='wide', page_title='Seismic Viewer')
import pandas as pd
import numpy as np
from obspy import read
import plotly.graph_objects as go

# event handling
from plotly.callbacks import Points, InputDeviceState

# local module
from load import loadData

def click_fn(trace, points, state):
    inds = points.point_inds
    print(inds)

def volumePlot():
  X, Y, Z = np.mgrid[-1:1:30j, -1:1:30j, -1:1:30j]
  values =    np.sin(np.pi*X) * np.cos(np.pi*Z) * np.sin(np.pi*Y)

  fig = go.Figure(data=go.Volume(
      x=X.flatten(),
      y=Y.flatten(),
      z=Z.flatten(),
      value=values.flatten(),
      isomin=-0.1,
      isomax=0.8,
      opacity=0.1, # needs to be small to see through all surfaces
      surface_count=21, # needs to be a large number for good volume rendering
      colorscale='RdBu',
      ))

  fig.update_layout(autosize=False,
                        height= 800,
                        width= 800,
                        margin=dict(
                          l=0,
                          r=0,
                          b=0,
                          t=0,
                          pad=0),
                          showlegend=False)

  return fig

# @st.cache
def seisPlot(rawData, axisYData, ampGain, timeScaling):
  if rawData is not None:
    st.sidebar.success('Data terupload')
    # Add histogram data
    fig = go.Figure()
    for i in range(1, 24):
      x = (rawData[:,i] / np.linalg.norm(rawData[:,i]))*ampGain + i+1
      y = axisYData[:,i]
      fig.add_trace(go.Scatter(x=x, 
                              y=y, 
                              mode='lines', 
                              line= dict(color='white', width=0.5),
                              fill='tozeroy'))

      fig.update_yaxes(autorange='reversed')
      fig.update_layout(autosize=False,
                        height= timeScaling,
                        xaxis_title = 'Number of Traces',
                        yaxis_title='Time (ms)',
                        margin=dict(
                          l=0,
                          r=0,
                          b=0,
                          t=0,
                          pad=0),
                          showlegend=False)
    # Plot!
    st.header(f'Source data: {uploadedFile.name}')
    st.plotly_chart(fig, use_container_width=True)

# Sidebar option & File uploader
st.sidebar.header('SEIRA 2.0 PRO')
processSelect = st.sidebar.selectbox('Process', ['Home',
                                                 'Seismic Viewer', 
                                                 'Dispersion Curve', 
                                                 '1D VS30 Inversion', 
                                                 '2D VS30'], )

if processSelect == 'Home':
  st.header('GEOPHYSICAL ENGINEERING \n INSTITUT TEKNOLOGI SUMATERA')

if processSelect == 'Seismic Viewer':
  rawData = None
  uploadedFile = st.sidebar.file_uploader('Seismic data', type=['.sgy'])
  
  rawData, axisYData = loadData(uploadedFile)

  # EXPANDER PARAMETERS
  paramOption = st.sidebar.beta_expander('ADJUST PARAMETERS')
  ampGain = paramOption.slider('Amplitude Gain', min_value=1, max_value=20)
  timeScaling = paramOption.slider('Time Scale', min_value=480, max_value=1080)

  paramOption.write('Bandpass Filter')
  minFrequency = paramOption.number_input('Min Freq (Hz)', min_value=0, max_value=200)
  maxFrequency = paramOption.number_input('Max Freq (Hz)', min_value=0, max_value=200)
  applyBandpass = paramOption.checkbox('Apply filter')

  confirmSaveData = paramOption.button('Save to SGY File')

  # EXPANDER PICKING FB
  expanderPick = st.sidebar.beta_expander('PICKING FB')

  # CALLBACK PROCESS
  seisPlot(rawData, axisYData, ampGain, timeScaling)

if processSelect == 'Dispersion Curve':
  points, state = Points(), InputDeviceState()
  datax = np.array(10)
  datay = np.array(10)
  f = go.Scatter(x=datax, y=datay)
  f.on_click(click_fn)
  st.plotly_chart(f)

if processSelect == '1D VS30 Inversion':
  pass

if processSelect == '2D VS30':
  pass