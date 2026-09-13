from pydoc import text

import streamlit as st
import src.model as m

tree = m.Tree()
for i in range(6,0,-2):
    tree.add_node(i)
for i in range(7,0,-2):
    tree.add_node(i)
st.graphviz_chart(tree.get_tree_graph())
tree.balance_tree()
st.graphviz_chart(tree.get_tree_graph())
print(tree.get_weight())