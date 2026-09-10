from pydoc import text

import streamlit as st
import src.model as m

tree = m.Node(6)
tree.add_nodes([5,4,3,2,1])

st.title('Arbol sin balancear',text_alignment='center')
st.graphviz_chart(tree.get_tree_graph())
tree.balance_tree()
st.title('Arbol balanceado',text_alignment='center')
st.graphviz_chart(tree.get_tree_graph())