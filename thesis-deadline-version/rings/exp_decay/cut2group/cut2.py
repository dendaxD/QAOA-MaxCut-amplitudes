def amplitude(n):
	amplitude = ''
	for x in range(1,n):
		amplitude += f'(I Sin[x])^{x} Cos[x]^{n-x} + '
	return amplitude[:-3]

with open('cut2.nb', 'w') as f:
	for n in range(4,20,2):
		f.write(f'a{n}[x_] := {n}*Abs[{amplitude(n)}]/Sqrt[2^{n}];\n')

	for n in range(4,20,2):
		f.write(f'Print[{amplitude(n)}//ComplexExpand]\n')

	for n in range(4,20,2):
		f.write(f'NMaximize[{{a{n}[x], 0 <= x <= Pi}}, x]\n')