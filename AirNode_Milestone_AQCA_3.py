#!/usr/bin/env python
# coding: utf-8

# In[2]:


import libpysal as ps
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import pandas as pd
import geopandas as gpd


# In[ ]:


from giddy.markov import FullRank_Markov


# In[ ]:


income_table = pd.read_csv(ps.examples.get_path("usjoin.csv"))
income_table.head()


# In[ ]:


pci = income_table[list(map(str,range(1929,2010)))].values
pci


# In[ ]:


m = FullRank_Markov(pci)
m.ranks


# In[ ]:


m.transitions


# In[ ]:


m.p


# In[ ]:


m.fmpt


# In[ ]:


m.sojourn_time


# In[ ]:


df_fullrank = pd.DataFrame(np.c_[m.p.diagonal(),m.sojourn_time], columns=["Staying Probability","Sojourn Time"], index = np.arange(m.p.shape[0])+1)
df_fullrank.head()


# In[ ]:


df_fullrank.plot(subplots=True, layout=(1,2), figsize=(15,5))


# In[ ]:


sns.distplot(m.fmpt.flatten(),kde=False)


# In[ ]:


from giddy.markov import GeoRank_Markov, Markov, sojourn_time
gm = GeoRank_Markov(pci)


# In[ ]:


gm.transitions


# In[ ]:


gm.p


# In[ ]:


gm.sojourn_time[:10]


# In[ ]:


gm.sojourn_time


# In[ ]:


gm.fmpt


# In[ ]:


income_table["geo_sojourn_time"] = gm.sojourn_time
i = 0
for state in income_table["Name"]:
    income_table["geo_fmpt_to_" + state] = gm.fmpt[:,i]
    income_table["geo_fmpt_from_" + state] = gm.fmpt[i,:]
    i = i + 1
income_table.head()


# In[ ]:


geo_table = gpd.read_file(ps.examples.get_path('us48.shp'))
# income_table = pd.read_csv(libpysal.examples.get_path("usjoin.csv"))
complete_table = geo_table.merge(income_table,left_on='STATE_NAME',right_on='Name')
complete_table.head()


# In[ ]:


complete_table.columns


# In[ ]:


fig, axes = plt.subplots(nrows=2, ncols=2,figsize = (15,7))
target_states = ["California","Mississippi"]
directions = ["from","to"]
for i, direction in enumerate(directions):
    for j, target in enumerate(target_states):
        ax = axes[i,j]
        col = direction+"_"+target
        complete_table.plot(ax=ax,column = "geo_fmpt_"+ col,cmap='OrRd',
                    scheme='quantiles', legend=True)
        ax.set_title("First Mean Passage Time "+direction+" "+target)
        ax.axis('off')
        leg = ax.get_legend()
        leg.set_bbox_to_anchor((0.8, 0.15, 0.16, 0.2))
plt.tight_layout()


# In[ ]:


fig, axes = plt.subplots(nrows=1, ncols=2,figsize = (15,7))
schemes = ["Quantiles","Equal_Interval"]
for i, scheme in enumerate(schemes):
    ax = axes[i]
    complete_table.plot(ax=ax,column = "geo_sojourn_time",cmap='OrRd',
                scheme=scheme, legend=True)
    ax.set_title("Rank Sojourn Time ("+scheme+")")
    ax.axis('off')
    leg = ax.get_legend()
    leg.set_bbox_to_anchor((0.8, 0.15, 0.16, 0.2))
plt.tight_layout()


# In[ ]:





# In[ ]:




