from pydoc import text

import streamlit as st
import src.model as m

root = m.Node(6)
for i in range(5,0,-1):
    root.add_node(m.Node(i))
st.title('Arbol sin balancear',text_alignment='center')
st.graphviz_chart(root.get_tree_graph())
root.balance_tree()
st.title('Arbol balanceado',text_alignment='center')
st.graphviz_chart(root.get_tree_graph())