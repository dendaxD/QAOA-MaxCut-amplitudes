import subprocess
from os import system, remove, chdir
from tabulate import tabulate


# the set of edges in a complete graph given by the number of the vertices
# An $\mathcal{O}(n^2)$ function which generates the set of edges in n-vertex CG.
def edges(n):
    return [(x + 1, y + 1) for x in range(n) for y in range(n) if x < y]


# This one takes $\mathcal{O}(n)$.
def hamming_distance(string1, string2):
    diff = 0
    for c1, c2 in zip(string1, string2):
        if c1 != c2:
            diff += 1
    return diff


# $\mathcal{O}(1)$
def cut(l, n):
    l = int(l)
    return n * (n - 1) / 2 - 2 * l * (n - l)


# $\mathcal{O}(n)$
def label(state):
    return str(min(state.count("1"), state.count("0")))


# $\mathcal{O}(2^n\cdot n)$
def create_label_to_states_dict(n):
    label_to_states_dict = {}
    # iterate through all the states that start with 0
    # the rest is included by 'not_s'
    for i in range(2 ** (n - 1)):
        # Each computational basis state is a binary representation
        # of some i (e.g. '01001' is binary form of 9).
        s = str(bin(i))[2:]
        s = (n - len(s)) * "0" + s
        # It takes $\mathcal{O}(n)$ to obtain 'not_s'.
        not_s = ""
        for symbol in s:
            not_s += "0" if symbol == "1" else "1"
        l = label(s)  # $\mathcal{O}(n)$
        c = cut(l, n)
        # A look-up to a dictionary takes, on average, only $\mathcal{O}(1)$.
        # In the worst case $\mathcal{O}(n)$.
        if l in label_to_states_dict:
            label_to_states_dict[l].extend([s, not_s])
        else:
            label_to_states_dict[l] = [s, not_s]
    return label_to_states_dict

# $\mathcal{O}(n^2\cdot2^n)$
def create_ampl_info(n, representant, label_to_states, labels):
    ampl_info = {}  # cut to {hamming_distance to coefficients}
    for l in labels:
        if cut(l, n) not in ampl_info:
            ampl_info[cut(l, n)] = {}
        # $\mathcal{O}(n\cdot2^n)$ - This bound could be improved as it will never
        # happen for all states to have the same label.
        for state in label_to_states[l]:
            ham = hamming_distance(representant, state)  # $\mathcal{O}(n)$
            if ham in ampl_info[cut(l, n)]:
                ampl_info[cut(l, n)][ham] += 1
            else:
                ampl_info[cut(l, n)][ham] = 1
    return ampl_info

# $\mathcal{O}(n^3)$
def create_amplitude(n, ampl_info):
    ampl = ""  # ampl for amplitude
    for c in ampl_info: #c for cut
        ampl += f"Exp[{-c} I y] ("
        # $\mathcal{O}(n)$
        for ham, coef in ampl_info[c].items():
            if coef != 1:
                ampl += f"{coef} "
            if ham == n:
                ampl += f"(I Sin[x])^{n}"
            elif ham == 0:
                ampl += f"Cos[x]^{n}"
            else:
                ampl += f"(I Sin[x])^{ham} Cos[x]^{n - ham}"
            ampl += " + "
        ampl = ampl[:-3] + ") + "
        # '[:-3]' to remove the additional ' + '
    return f"{ampl[:-3]}" #it is not normalized

# $\mathcal{O}(n^3\cdot 2^n)$
def create_label_to_amplitude_dict(n, label_to_states):
    label_to_amplitude_dict = {}
    labels = label_to_states.keys()
    # $\mathcal{O}(n^3\cdot 2^n)$
    for label in labels:  # number of labels = round up n/2
        representant = label_to_states[label][0]
        # $\mathcal{O}(n^2\cdot2^n)$
        ampl_info = create_ampl_info(n, representant, label_to_states, labels)
        label_to_amplitude_dict[label] = create_amplitude(n, ampl_info)
    return label_to_amplitude_dict


def main():
    start = 4
    end = 10


    with open('result.txt', 'w') as f:#to delete any content
        pass
    with open('amplitudes.txt', 'w') as f:#to create the file
        pass


    for number_of_qubits in range(start, end+1):
        label_to_states = create_label_to_states_dict(number_of_qubits)  # $\mathcal{O}(2^n\cdot n)$

        for l, amplitude in create_label_to_amplitude_dict(number_of_qubits, label_to_states).items():
            number_of_qubits = str(number_of_qubits)
            print(number_of_qubits, "v", l)


            #here we are creating mathematica file (for information gain) so that we could subsequently run it
            with open(number_of_qubits+ "v" + l + ".nb", "w") as file, open("templates/results.nb", "r") as template:
                                                
                file.write    ( "nqubits = " + number_of_qubits + ";\n" + 
                                "label = \"" + number_of_qubits + "v" + l + "\";\n" +
                                "nstates = " + str(len(label_to_states[l])) + ";\n"

                                "amplitude[x_, y_] := (" + amplitude + ")/Sqrt[2^nqubits];\n" +
                                "amplitude2[x_, y_] := (" + amplitude + ");\n" + 
                                 probability[x_, y_] := Abs[amplitude[x, y]]^2;\n\n"
                            )

                for line in template:
                    file.write(line)

                file.write("\nExport[\"images/plots/" + number_of_qubits+ "v" + l + ".jpg\", Plot3D[f, {c, 0, n/2},{d, 0, n}, PlotRange -> All]];\n")
                file.write("Export[\"images/contour-plots/" + number_of_qubits+ "v" + l + " c.jpg\", ContourPlot[probability[x, y], {x, -n, n}, {y, -n, n}, PlotLegends -> Automatic, Contours -> 30, PlotPoints -> 100, FrameLabel -> {\[Beta],\[Gamma]}, FrameTicks ->{Range[-Pi, Pi, Pi/2],Range[-Pi, Pi, Pi/2]}]];\n")

            #Here we run the mathematica file. Then we remove it.
            subprocess.run(["math", "-script", number_of_qubits + "v" + l + ".nb"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            remove(number_of_qubits+ "v" + l + ".nb")

            #here we are creating useful mathematica file - sth to play with later
            with open("mathematica-files/" + number_of_qubits+ "v" + l + ".nb", "w") as file, open("templates/useful.nb", "r") as template:

                file.write    ( "nqubits = " + number_of_qubits + ";\n" + 
                                "label = \"" + number_of_qubits + "v" + l + "\";\n" +
                                "nstates = " + str(len(label_to_states[l])) + ";\n\n"

                                "amplitude[x_,y_] := (" + amplitude + ")/Sqrt[2^nqubits];\n" +
                                "amplitude2[x_,y_] := (" + amplitude + ");\n" + 
                                "probability[x_, y_] := Abs[amplitude[x, y]]^2;\n\n"
                )

                for line in template:
                    file.write(line)

                file.write("\nPlot3D[f, {c, 0, n/2}, {d, -n, n}, PlotRange -> All]\n")
                file.write("ContourPlot[probability[x, y], {x, 0, n/2}, {y, 0, n}, PlotLegends -> Automatic, Contours -> 30]\n")


    #here we are creating the result.txt file: [type <-> Pmax <-> beta <-> gamma] table
    with open('result.txt', 'r') as file:
        x = file.readlines()

    results = []
    for line in x:
        line = line.replace("\"","").split()
        results.append(line)

    with open('result.txt', 'w') as f:
        f.write(tabulate(results, headers=['Name', 'Max Probability', "beta (X)", "gamma (ZZ)"]))


    #create the amplitudes.pdf file
    with open("templates/amplitudes.tex", "r") as template, open("amplitudes/amplitudes.tex", "w") as file, open("amplitudes.txt", "r") as data:

        for line in template:
            file.write(line)

        for line in data:
            line = line.replace("\"","").replace("\\\\","\\").replace("\\\n", "")
            file.write(line) 
        file.write("\\end{document}")


    chdir('./amplitudes')
    system('make')
    system('make cleanaux')
    chdir('../')
    remove('amplitudes.txt')


if __name__ == "__main__":
    main()