# -*- coding: utf-8 -*-
"""
Created on Tue Jan 09 12:41:50 2018

@author: dany
"""

import pandas as pd
import numpy as np

datos = pd.read_csv("resultados_media")

datos_std = pd.read_csv("resultados_desviacion")

datos["Jaccard"] = datos["Jaccard"] / datos["Flooding"]
datos["Dice"] = datos["Dice"] / datos["Flooding"]
datos["Sokal"] = datos["Sokal"] / datos["Flooding"]
datos["New"] = datos["New"] / datos["Flooding"]
datos["Flooding"] = datos["Flooding"] / datos["Flooding"]
datos["Folkes"] = datos["Folkes"] / datos["Flooding"]

datos["improvement"] = ((datos["New"] - datos["Sokal"]) / datos["Sokal"]) * 100  
datos["imp_eu"] = ((datos["New"] - datos["Euclidean"]) / datos["Euclidean"]) * 100  

datos_std["Jaccard"] = ((datos_std["Jaccard"] / datos_std["Flooding"]) * 1.96) / np.sqrt(20)
datos_std["Dice"] = ((datos_std["Dice"] / datos_std["Flooding"]) * 1.96) / np.sqrt(20)
datos_std["Sokal"] = ((datos_std["Sokal"] / datos_std["Flooding"]) * 1.96) / np.sqrt(20)
datos_std["New"] = ((datos_std["New"] / datos_std["Flooding"]) * 1.96) / np.sqrt(20)
datos_std["Flooding"] = ((datos_std["Flooding"] / datos_std["Flooding"]) * 1.96) / np.sqrt(20)
datos_std["Folkes"] = ((datos_std["Folkes"] / datos_std["Flooding"]) * 1.96) / np.sqrt(20)


del(datos["Unnamed: 0"])
del(datos_std["Unnamed: 0"])
x= np.array([100, 120, 140, 160, 180, 200])

ax = datos.plot(x, kind="bar",  yerr = datos_std, edgecolor='black', width=0.8, grid=True, ylim=(0.2,1.1), error_kw=dict(ecolor='black',elinewidth=0.5))
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax.set_xlabel("Number of Vehicles")
ax.set_ylabel("Normalized Re")
