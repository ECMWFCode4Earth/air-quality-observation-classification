#!/usr/bin/env python
# coding: utf-8

# In[1]:



import numpy as np
c = np.array([['b','a','c'],['c','c','a'],['c','b','c'],['a','a','b'],['a','b','c']])


# In[3]:


print(c)


# In[4]:


import giddy
m = giddy.markov.Markov(c)


# In[5]:


print(m)


# In[6]:


m = giddy.markov.Markov(c, summary=False)
print(m.classes)


# In[7]:


print(len(m.classes))


# In[8]:


print(m.transitions)


# In[9]:


print(m.p)


# In[10]:


m.steady_state  # steady state distribution


# In[11]:


import libpysal
f = libpysal.io.open(libpysal.examples.get_path("usjoin.csv"))
pci = np.array([f.by_col[str(y)] for y in range(1929,2010)])
print(pci.shape)


# In[12]:


print(f)


# In[13]:


print(pci[0, :])


# In[14]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
years = range(1929,2010)
names = np.array(f.by_col("Name"))
order1929 = np.argsort(pci[0,:])
order2009 = np.argsort(pci[-1,:])
names1929 = names[order1929[::-1]]
names2009 = names[order2009[::-1]]
first_last = np.vstack((names1929,names2009))
from pylab import rcParams
rcParams['figure.figsize'] = 15,10
plt.plot(years,pci)
for i in range(48):
    plt.text(1915,54530-(i*1159), first_last[0][i],fontsize=12)
    plt.text(2010.5,54530-(i*1159), first_last[1][i],fontsize=12)
plt.xlim((years[0], years[-1]))
plt.ylim((0, 54530))
plt.ylabel(r"$y_{i,t}$",fontsize=14)
plt.xlabel('Years',fontsize=12)
plt.title('Absolute Dynamics',fontsize=18)


# In[15]:


years = range(1929,2010)
rpci= (pci.T / pci.mean(axis=1)).T
names = np.array(f.by_col("Name"))
order1929 = np.argsort(rpci[0,:])
order2009 = np.argsort(rpci[-1,:])
names1929 = names[order1929[::-1]]
names2009 = names[order2009[::-1]]
first_last = np.vstack((names1929,names2009))
from pylab import rcParams
rcParams['figure.figsize'] = 15,10
plt.plot(years,rpci)
for i in range(48):
    plt.text(1915,1.91-(i*0.041), first_last[0][i],fontsize=12)
    plt.text(2010.5,1.91-(i*0.041), first_last[1][i],fontsize=12)
plt.xlim((years[0], years[-1]))
plt.ylim((0, 1.94))
plt.ylabel(r"$y_{i,t}/\bar{y}_t$",fontsize=14)
plt.xlabel('Years',fontsize=12)
plt.title('Relative Dynamics',fontsize=18)


# In[16]:


import mapclassify as mc
q5 = np.array([mc.Quantiles(y,k=5).yb for y in pci]).transpose()
print(q5[:, 0])


# In[17]:


print(f.by_col("Name"))


# In[18]:


print(q5[4, :])


# In[19]:


m5 = giddy.markov.Markov(q5)


# In[20]:


print(m5.transitions)


# In[21]:


print(m5.p)


# In[22]:


print(m5.steady_state)


# In[23]:


print(giddy.ergodic.fmpt(m5.p))


# In[24]:


import geopandas as gpd
import pandas as pd


# In[25]:


geo_table = gpd.read_file(libpysal.examples.get_path('us48.shp'))
income_table = pd.read_csv(libpysal.examples.get_path("usjoin.csv"))
complete_table = geo_table.merge(income_table,left_on='STATE_NAME',right_on='Name')
complete_table.head()


# In[26]:


fig, axes = plt.subplots(nrows=2, ncols=3,figsize = (15,7))
for i in range(2):
    for j in range(3):
        ax = axes[i,j]
        complete_table.plot(ax=ax, column=str(index_year[i*3+j]), cmap='OrRd', scheme='quantiles', legend=True)
        ax.set_title('Per Capita Income %s Quintiles'%str(index_year[i*3+j]))
        ax.axis('off')
        leg = ax.get_legend()
        leg.set_bbox_to_anchor((0.8, 0.15, 0.16, 0.2))
plt.tight_layout()


# In[27]:


from esda.moran import Moran
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
w = libpysal.io.open(libpysal.examples.get_path("states48.gal")).read()
w.transform = 'R'
mits = [Moran(cs, w) for cs in pci]
res = np.array([(mi.I, mi.EI, mi.seI_norm, mi.sim[974]) for mi in mits])
years = np.arange(1929,2010)
fig, ax = plt.subplots(nrows=1, ncols=1,figsize = (10,5) )
ax.plot(years, res[:,0], label='Moran\'s I')
#plot(years, res[:,1], label='E[I]')
ax.plot(years, res[:,1]+1.96*res[:,2], label='Upper bound',linestyle='dashed')
ax.plot(years, res[:,1]-1.96*res[:,2], label='Lower bound',linestyle='dashed')
ax.set_title("Global spatial autocorrelation for annual US per capita incomes",fontdict={'fontsize':15})
ax.set_xlim([1929,2009])
ax.legend()


# In[28]:


get_ipython().run_line_magic('pinfo', 'giddy.markov.Spatial_Markov')


# In[29]:


sm = giddy.markov.Spatial_Markov(rpci.T, w, fixed = True, k = 5,m=5) # spatial_markov instance o


# In[30]:


print(sm.p)


# In[31]:


sm.summary()


# In[32]:


#we use seaborn to create a heatmap (`pip install seaborn` to install seaborn if you do not have it)
import seaborn as sns
sns.set()

fig, ax = plt.subplots(figsize = (5,4))
im = sns.heatmap(sm.p, annot=True, linewidths=.5, ax=ax, cbar=True, vmin=0, vmax=1,
                          square=True,  cmap="YlGn",fmt='.3f')


# In[33]:


fig, axes = plt.subplots(2,3,figsize = (15,8))

for i in range(2):
    for j in range(3):
        ax = axes[i,j]
        if i==1 and j==2:
            ax.axis('off')
            continue
        p_temp = sm.P[i*3+j]
        im = sns.heatmap(p_temp, annot=True, linewidths=.5, ax=ax, cbar=True, vmin=0, vmax=1,
                          square=True, cmap="YlGn",fmt='.3f')
        ax.set_title("Spatial Lag %d"%(i*3+j),fontsize=13)


# In[34]:


fig, axes = plt.subplots(2,3,figsize = (15,8))

for i in range(2):
    for j in range(3):
        ax = axes[i,j]
        if i==0 and j==0:
            im = sns.heatmap(sm.p, annot=True, linewidths=.5, ax=ax, cbar=True, vmin=0, vmax=1,
                          square=True, cmap="YlGn",fmt='.3f')
            ax.set_title("Global",fontsize=13)
        else:
            p_temp = sm.P[i*3+j-1]
            im = sns.heatmap(p_temp, annot=True, linewidths=.5, ax=ax, cbar=True, vmin=0, vmax=1,
                          square=True, cmap="YlGn",fmt='.3f')
            ax.set_title("Spatial Lag %d"%(i*3+j),fontsize=13)


# In[35]:


print(sm.S)


# In[36]:


print(sm.F)


# In[37]:


giddy.markov.Homogeneity_Results(sm.T).summary()


# In[38]:


print(giddy.markov.kullback(sm.T))


# In[39]:


lm = giddy.markov.LISA_Markov(pci.T, w)
print(lm.classes)


# In[40]:


print(lm.transitions)


# In[41]:


print(lm.p)


# In[42]:


print(lm.steady_state)


# In[43]:


print(giddy.ergodic.fmpt(lm.p))


# In[44]:


print(lm.chi_2)


# In[ ]:




