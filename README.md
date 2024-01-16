# QAOA-MaxCut-amplitudes

Documentation: Appendix B in https://dendaxd.github.io/documents/DendasDiplomaThesis.pdf

### Short description

In the project, we numericaly simulate QAOA (The quantum approximate optimization algorithm \[[1411.4028](https://arxiv.org/abs/1411.4028)\]) for
[MaxCut](https://en.wikipedia.org/wiki/Maximum_cut) on rings, lines and complete graphs. However, we don't aim for the approximation of the maximal cut value, but rather we focus on the QAOA ansatz state $|\vec{\gamma},\vec{\beta}\rangle$ (the created quantum state right before the measurement) in hope to increase our understanding of QAOA potential. We ask, more broadly, what computational basis states (they include the optimal solution) can be reached in shallow QAOA circuits (depth one and two).

For each graph type, using a python script, we generate Mathematica files (one for each computational basis state) that we use to:
- calculate the maximal probability of obtaining the state using shallow QAOA,
- generate contour plot graph showing how the probability depends on QAOA parameters.
