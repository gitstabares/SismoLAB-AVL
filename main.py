import streamlit as st
import src.model as m

tree = m.Node(10)
tree.add_nodes([5,15,1,23,7,5,9,5,4,8,6,2,13,45])

st.badge('Esto es una etiqueta',color='violet')
st.graphviz_chart(tree.get_tree_graph())
tree.get_node(10)._Node__rotate_left()
st.graphviz_chart(tree.get_tree_graph())