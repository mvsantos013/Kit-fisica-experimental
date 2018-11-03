import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter
import math

class Tools:
    
    def ajustarReta(self, x, y, y_error):
        if (len(x) != len(y)):
            return "x dim must be == y dim"

        #transform arrays elements into float
        for i in range(len(x)):
            x[i] = 1.0*x[i]
            y[i] = 1.0*y[i]
            y_error[i] = 1.0*y_error[i]

        P, Q, R, S, T = 0, 0, 0, 0, 0

        for n in range(len(x)):
            P += (x[n]*x[n])/(y_error[n]*y_error[n])
            Q += 1/(y_error[n]*y_error[n])
            R += x[n]/(y_error[n]*y_error[n])
            S += (x[n]*y[n])/(y_error[n]*y_error[n])
            T += y[n]/(y_error[n]*y_error[n])

        A = (Q*S - R*T)/(P*Q - R*R)
        A_error = math.sqrt(Q/(P*Q - R*R))
        B = (P*T - R*S)/(P*Q - R*R)
        B_error = math.sqrt(P/(P*Q - R*R))
        
        chi_square = 0
        for n in range(len(x)):
            chi_square += math.pow((B + A*x[n] - y[n])/y_error[n],2)
        chi_square_dof = chi_square/(len(x) - 2) 

        return (A, A_error, B, B_error, chi_square_dof)


    def notacaoCientifica(self, x, pref_expoent):
        x_nominal = str(x)
        x_expoent = 0
        
        #select expoent
        if (str(x).find("e") != -1):
            x_expoent = int(str(x)[str(x).find("e")+1:])
            x_nominal = str(x)[:str(x).find("e")]

        #treatment decimals
        if (pref_expoent > x_expoent):
            m = - abs(abs(pref_expoent) - abs(x_expoent))
            x_expoent = pref_expoent
        else:
            m = abs(abs(pref_expoent) - abs(x_expoent))
            x_expoent = pref_expoent

        if (m <= 0):
            str_x = x_nominal
            for i in range(abs(m)):
                str_x = "0" + str_x
                point_index = str_x.index(".")
                prev_number = str_x[point_index - 1]
                str_x = list(str_x)
                str_x[point_index] = prev_number
                str_x[point_index - 1] = "."
                str_x = "".join(str_x)
                x_nominal = str_x
            if (int(x_nominal[:x_nominal.index(".")]) == 0):
                x_nominal = "0" + x_nominal[x_nominal.index("."):]
            else:
                x_nominal_int = int(x_nominal[:x_nominal.index(".")])
                x_nominal = str(x_nominal_int) + x_nominal[x_nominal.index("."):]

        else:
            str_x = x_nominal
            for i in range(abs(m)):
                str_x = str_x + "0"
                point_index = str_x.index(".")
                prev_number = str_x[point_index + 1]
                str_x = list(str_x)
                str_x[point_index] = prev_number
                str_x[point_index + 1] = "."
                str_x = "".join(str_x)
                x_nominal = str_x
                
        return x_nominal


    def algarismoSignificativo(self, x, x_error):
        x_int = x[:x.index(".")]
        x_decimal = x[x.index(".")+1:] + "0000000000000000000"
        x_error_int = x_error[:x_error.index(".")]
        x_error_decimal = x_error[x_error.index(".")+1:] + "0"

        if(int(x_error_int) != 0):
            return x_int, x_error_int
        else:
            for n in range(len(x_error_decimal)):
                if (int(x_error_decimal[n]) != 0):
                    first_nonzero = str(round(
                        int(x_error_decimal[n]+x_error_decimal[n+1]),-1))[0]
                    if (n>0):
                        x_error_decimal = x_error_decimal[:n]+first_nonzero
                    else:
                        x_error_decimal = first_nonzero
                    x_error = x_error_int + "." + x_error_decimal

                    last_number = str(round(
                        int(x_decimal[n]+x_decimal[n+1]),-1))[0]
                    if (n>0):
                        x_decimal = x_decimal[:n]+last_number
                    else:
                        x_decimal = last_number
                    x = x_int + "." + x_decimal
                    
                    return x, x_error
        return "x"
    

    def exportarParaExcel(self, file_name, list_data, data_names, list_other=[], other_names=[]):
        workbook = xlsxwriter.Workbook(file_name + ".xlsx")
        worksheet = workbook.add_worksheet()

        row = 0
        col = 0
        for j in range(len(list_data)):
            for i in range(len(list_data[j])):
                worksheet.write(row+1+i, col+j, list_data[j][i])
        for j in range(len(data_names)):
            worksheet.write(row, col+j, data_names[j])

        for j in range(len(list_other)):
             worksheet.write(row+1, col+j+len(list_data), list_other[j])
        for j in range(len(other_names)):
            worksheet.write(row, col+j+len(list_data), other_names[j])
        
        workbook.close()
        

    def exportarGrafico(self, file_name, title, xlabel, ylabel, x, y, y_error=[], dataAdjust=[]):
        plt.figure(figsize=(20, 10))

        def function_adjust(x, alfa, beta):
            return alfa*x + beta
        x_adjust = np.arange(x[0] - 0.2*x[0], x[-1] + 0.2*x[0], 0.001)
        y_adjust = function_adjust(x_adjust, dataAdjust[0], dataAdjust[2])
        plt.plot(x_adjust, y_adjust, 'b-')

        if (y != []):
            plt.errorbar(x, y, xerr = 0, yerr = y_error, color = 'k', linestyle='None', marker='.')
        else:
            plt.plot(x, y, 'k. ')

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig(file_name + ".png")
        plt.show()        





















    
