# 15400Project
This project dedicates to implement local graph clustering algorithm for existing graph convolution framework, namely, the GraphSAGE algorithm. The goal of this project is to test different local graph clustering techniques when applying to GraphSAGE. One can immigrant the implementation to larger system, such as PinSAGE.

Part I: implement the raw capacity releasing diffusion algorithm, then integrate it into GraphSAGE. In this version, we will use networkx for graph data structure, and numpy for matrix operation, which is supposed to be slower than pytorch or tensorflow.
