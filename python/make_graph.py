"""
An example using Graph as a weighted network.
"""

import matplotlib.pyplot as plt
import networkx as nx
import pickle

links = pickle.load(open("links.pickle", "rb"))

G=nx.Graph()

for link in links:
    G.add_edge(link["source"], link["target"], length=link["value"])
#
# elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >0.5]
# esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <=0.5]

pos=nx.spring_layout(G) # positions for all nodes

# nodes
nx.draw_networkx_nodes(G,pos,node_size=400)

# edges
nx.draw_networkx_edges(G,pos, width=1)
# nx.draw_networkx_edges(G,pos,edgelist=esmall,
#                     width=6,alpha=0.5,edge_color='b',style='dashed')

# labels
nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')

plt.axis('off')
plt.savefig("weighted_graph.png") # save as png
plt.show() # display
