class matrix_class:

    def matrix_checker(self, x, file_path):
        unknowns = []
        result = []
        dct = {}
        flag = None

        with open(file_path) as file:
            for line in file:
                line = line.split()
                if len(line) == x + 1: #Checks for 'answer' values in equation. (Checks columns)
                    line = [float(i) for i in line]
                    unknowns.append(line)
                else:
                    flag = False

            if len(unknowns) != x: #Checks for no. of rows
                flag = False

        for a in unknowns:
            result.append(a[x])
            #del a[-1]

        if flag == False:
            return False
        else:
            dct.update(unknowns=unknowns)
            dct.update(results=result)
            return dct


    def gaussian_solver(self, x, dct):
        unknowns = dct['unknowns']
        results = dct['results']

        """
        print "Original unknowns: "
        print unknowns

        print "Original results"
        print results
        """
        l = 0
        k = 1
        value = 0

        while l < x - 1:
            while k < x:
                for i in range(l, x+1, 1):
                    if i == l:
                        sign = 1.0
                        if unknowns[l][i] * unknowns[k][i] > 0:
                            sign = -1.0
                        value = sign * unknowns[k][i] / unknowns[l][i]
                    unknowns[k][i] = unknowns[k][i] + (value * unknowns[l][i])
                k += 1
            l += 1
            k = l + 1

        results = []

        for a in unknowns:
            results.append(a[-1])
            del a[-1]

        for i in range(x-1, -1, -1):
            for j in range(x-1, i - 1, -1):
                if i == j:
                    results[i] = results[i] / unknowns[i][j]
                    break
                else:
                    results[i] = results[i] - (unknowns[i][j] * results[j])

        return "Unknowns: " + str(unknowns) + " Results: " + str(results)

        """
        print "Changed unknowns"
        print unknowns

        print "Changed results"
        print results
        """