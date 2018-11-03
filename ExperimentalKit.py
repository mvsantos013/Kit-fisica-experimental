# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
from uncertainties import ufloat
from sympy import Symbol, diff, latex, sqrt, Abs, sin, cos, tan, cot, sec, csc, sinc, asin, acos, atan, acot, asec, acsc, \
atan2, sinh, cosh, tanh, coth, sech, csch, asinh, acosh, atanh, acoth, asech, exp, log
from sympy.parsing.sympy_parser import parse_expr

error_1 = "A função em deve ser dada em forma de string. Ex: \"x+2*y\""
error_2 = "As medidas devem estar dentro de uma lista. Ex: [[medida1], [medida2], [medida3], ...]."
error_3 = "As medidas devem estar dentro de uma lista na forma de [[valor, erro, 'símbolo'], ...]. Ex: [[3, 1, 'y'], [7, 2, 'z']]"
error_4 = "O valor da medida deve ser um número."
error_5 = "O erro da medida deve ser um número."
error_6 = "O simbolo da medida deve ser alfabetico e dado em forma de string."
error_7 = "A variável definida na função não está contida nas medidas."
error_8 = "O simbolo da medida não está definido na função."
error_9 = "O valor da medida deve ser expresso na forma de tuple. Ex: (13, 1); function((13,1))"
error_10 = "O algarismo significativo deve ser um inteiro positivo."
error_11 = "Divisão por zero na equação."
error_12 = "Equação com sintaxe errada. Ex: Errado: 2x, Certo: 2*x"
error_13 = "savefigure aceita apenas boolean (True ou False)."
error_14 = "O tamanho da fonte deve ser um inteiro positivo."
error_15 = "Nome do arquivo deve ser dado em forma de string. Ex: \"my_file\""
error_16 = "Os dados devem estar dentro de uma lista na forma de [[dados1], [dados2], ...]. Ex: Ex: [[(3,1), (4,1), (5,2)], [(7,1), (3,2), (2,2)], ...]"
error_17 = "O valor de entrada deve ser um número, uma tuple ou uma lista conforme o exemplo. Ex: 2; (6.7, 0.1); [(3,2), (5,2), (3,1), ...]"
error_18 = "O valor do expoente deve ser um inteiro."
error_19 = "Os titulos das colunas devem estar dentro de uma lista na forma de [[titulo1], [titulo2], ...]"
error_20 = "Os dados devem estar dentro de uma lista na forma de [[dados1], [dados2], ...]." \
           " Ex: [[(3,1), (4,1), (5,2)], [(7,1), (3,2), (2,2)], ...] ou [[1, 2, 3, 4, 5], [7, 8, 9], ...]"


def calculateAndPropagate(function, measures):
    if type(function) != str:
        raise Exception(error_1)
    if isinstance(measures, list):
        for measure in measures:
            if isinstance(measure, list) and len(measure) == 3:
                if isinstance(measure[0], int) or isinstance(measure[0], float):
                    if isinstance(measure[1], int) or isinstance(measure[1], float):
                        if type(measure[2]) != str or not (u"%s"%measure[2]).isalpha():
                            raise Exception(error_6)
                    else:
                        raise Exception(error_5)
                else:
                    raise Exception(error_4)
            else:
                raise Exception(error_3)
    else:
        raise Exception(error_2)
    try:
        parse_expr(function)
    except Exception:
        raise Exception(error_12) from None
    variables = list(function)
    for i in range(len(variables)):
        if not (u"%s" % variables[i]).isalpha():
            variables[i] = " "
    variables = "".join(variables).split()
    simbolos = []
    for i in range(len(variables)):
        for j in range(len(measures)):
            simbolos.append(measures[j][2])
        if variables[i] not in simbolos:
            raise Exception(error_7 + " Variável: " + variables[i])
    for s in simbolos:
        if s not in variables:
            raise Exception(error_8 + " Símbolo: " + s)
    #calculateAndPropagate
    f, values, error = parse_expr(function), [], 0
    for v in range(len(measures)):
        variable = Symbol(measures[v][2])
        partials = diff(f, variable)
        error += (partials.subs(variable, measures[v][0])*measures[v][1])**2
        values.append((variable, measures[v][0]))
    value, error = float(f.subs(values)), sqrt(float(error.subs(values)))
    return value, error


def getFancyValue(value_error, significantDigits=1):
    if not isinstance(value_error, tuple):
        raise Exception(error_9)
    if len(value_error) != 2:
        raise Exception(error_9)
    if not isinstance(value_error[0], int) and not isinstance(value_error[0], float):
        raise Exception(error_4)
    if not isinstance(value_error[1], int) and not isinstance(value_error[1], float):
        raise Exception(error_5)
    if not isinstance(significantDigits, int):
        raise Exception(error_10)
    if significantDigits < 0:
        raise Exception(error_10)
    #getFancyValue
    form = '{:.%su}' % significantDigits
    v = form.format(ufloat(float(value_error[0]), float(value_error[1])))
    str_v, x_value, x_error, exp, form = str(v), 0, 0, 0, 0
    if "e" in str_v:
        x_value = str_v[str_v.index("(")+1:str_v.index("+")]
        x_error = str_v[str_v.index("-")+1:str_v.index(")")]
        exp = str_v[str_v.index("e")+1:]
    else:
        x_value = str_v[:str_v.index("+")]
        x_error = str_v[str_v.index("-")+1:]
        exp = "0"
    return x_value, x_error, exp


def getLaTexValue(value_error, significantDigits=1):
    if not isinstance(value_error, tuple):
        raise Exception(error_9)
    if len(value_error) != 2:
        raise Exception(error_9)
    if not isinstance(value_error[0], int) and not isinstance(value_error[0], float):
        raise Exception(error_4)
    if not isinstance(value_error[1], int) and not isinstance(value_error[1], float):
        raise Exception(error_5)
    if not isinstance(significantDigits, int):
        raise Exception(error_10)
    if significantDigits < 0:
        raise Exception(error_10)
    #getLaTexValue
    x_value, x_error, exp = getFancyValue((value_error[0], value_error[1]), significantDigits)
    form = ""
    if exp != "0":
        form = "$(" + x_value + " \\pm " + x_error + ") \\times 10^{" + exp + "}$"
    else:
        form = "$" + x_value + " \\pm " + x_error + "$"
    return form


def getLaTexPropagationEq(equation):
    if type(equation) != str:
        raise Exception(error_1)
    try:
        parse_expr(equation)
    except Exception:
        raise Exception(error_12) from None
    eq, error = parse_expr(equation), 0
    if "zoo" in str(eq):
        raise Exception(error_11)
    #getLaTexPropagationEq
    variables = list(equation)
    for i in range(len(variables)):
        if not (u"%s" % variables[i]).isalpha():
            variables[i] = " "
    variables = "".join(variables).split()
    for v in variables:
        v = (Symbol('%s'%v), Symbol('ddd'+'%s'%v))
        partials = diff(eq, v[0])
        error += (partials*v[1])**2
    for v in variables:
        exec(v + " = (Symbol('%s'))" % v)
        exec("ddd" + v + " = (Symbol('ddd%s'))" % v)
    eq = latex(eval(str(eq)))
    error = latex(eval(str(sqrt(error)))).replace("ddd", "\\sigma_")
    sigmas, sigmaPos = [], 0
    for i in range(error.count("sigma_")):
        sigmaPos = error.index("sigma", sigmaPos + 1)
        varquadPos = error.index("^", sigmaPos)
        variable = error[sigmaPos + 6:varquadPos]
        toReplace = error[sigmaPos:varquadPos]
        byReplace = "sigma_{" + variable + "}"
        sigmas.append(byReplace)
        error = error.replace(toReplace, byReplace)
    return eq, error


def getStringPropagationEq(equation):
    if type(equation) != str:
        raise Exception(error_1)
    try:
        parse_expr(equation)
    except Exception:
        raise Exception(error_12) from None
    eq, error = parse_expr(equation), 0
    if "zoo" in str(eq):
        raise Exception(error_11)
    #getStringPropagationEq
    variables = list(equation)
    for i in range(len(variables)):
        if not (u"%s" % variables[i]).isalpha():
            variables[i] = " "
    variables = "".join(variables).split()
    for v in variables:
        v = (Symbol('%s'%v), Symbol('ddd'+'%s'%v))
        partials = diff(eq, v[0])
        error += (partials*v[1])**2
    for v in variables:
        exec(v + " = (Symbol('%s'))" % v)
        exec("ddd" + v + " = (Symbol('ddd%s'))" % v)
    eq = str(eq)
    error = str(sqrt(error)).replace("ddd", "d")
    return eq, error


def stringToLaTex(string):
    if type(string) != str:
        raise Exception(error_1)
    try:
        parse_expr(string)
    except Exception:
        raise Exception(error_12) from None
    #stringToLaTex
    strL = list(string)
    for i in range(len(strL)):
        if not (u"%s" % (strL[i])).isalpha():
            strL[i] = " "
    strL = "".join(strL).split()
    for v in strL:
        exec(v + " = Symbol('%s')" % v)
    eq = str(latex(eval(string)))
    return eq


def exportLaTexMeasureTable(filename, dataList, headList=[]):
    if type(filename) != str:
        raise Exception(error_15)
    if type(dataList) != list:
        raise Exception(error_16)
    else:
        for elem in dataList:
            if type(elem) != list:
                raise Exception(error_20)
    if type(headList) != list:
        raise Exception(error_19)
    #exportLaTexMeasureTable
    fileWriter = open(filename+".txt", 'w')
    if headList != []:
        for i in range(len(headList)):
            fileWriter.write(headList[i])
            if i != len(headList)-1:
                fileWriter.write(" & ")
            else:
                fileWriter.write(" \\\\ \n\n")
    n = []
    for i in range(len(dataList)):
        n.append(len(dataList[i]))
    n = max(n)
    for i in range(n):
        for j in range(len(dataList)):

            if len(dataList[j]) < i+1:
                fileWriter.write(" ")
            else:
                fileWriter.write(str(dataList[j][i]))
            if j != len(dataList)-1:
                fileWriter.write(" & ")
        fileWriter.write(" \\\\\n")
    fileWriter.close()


def exportGraph(filename, xValues, yValues, title="", xlabel="", ylabel="", figuresize=(10,6), show=True):
    plt.figure(figsize=figuresize)
    x, y, y_error = [], [], []
    for i in range(len(xValues)):
        x.append(xValues[i][0])
        y.append(yValues[i][0])
        y_error.append(yValues[i][1])
    if y_error != []:
        plt.errorbar(x, y, xerr=0, yerr=y_error, color='k', linestyle='None', marker='.')
    else:
        plt.plot(x, y, 'k.')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(filename + ".png")
    if show:
        plt.show()


def conversion(xValues, exp):
    if type(xValues) != list:
        if type(xValues) != tuple:
            if type(xValues) != int and type(xValues) != float:
                raise Exception(error_17)
        else:
            if len(xValues) != 2:
                raise Exception(error_17)
            if type(xValues[0]) != int and type(xValues[0]) != float:
                raise Exception(error_4)
            if type(xValues[1]) != int and type(xValues[1]) != float:
                raise Exception(error_5)
    else:
        for elem in xValues:
            if type(elem) != tuple:
                raise Exception(error_17)
            if len(elem) != 2:
                raise Exception(error_17)
            if type(elem[0]) != int and type(elem[0]) != float:
                raise Exception(error_4)
            if type(elem[1]) != int and type(elem[1]) != float:
                raise Exception(error_5)
    if type(exp) != int:
        raise Exception(error_18)
    #conversion
    if type(xValues) == int or type(xValues) == float:
        return xValues*10**(exp)
    if isinstance(xValues, tuple):
        x = (xValues[0]*10**(exp), xValues[1]*10**(exp))
        return x
    if isinstance(xValues, list):
        x = []
        for i in range(len(xValues)):
            x.append((xValues[i][0]*10**(exp), xValues[i][1]*10**(exp)))
        return x


def showLaTex(stringLaTex, savefigure=False, fontsize=32):
    if type(stringLaTex) != str and type(stringLaTex) != tuple:
        raise Exception(error_1)
    if not isinstance(savefigure, bool):
        raise Exception(error_13)
    if not isinstance(fontsize, int):
        raise Exception(error_14)
    if fontsize < 0:
        raise Exception(error_14)
    #showLaTex
    fig = plt.figure(num="showLaTex")
    ax = plt.axes([0, 0, 1, 1])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.format_coord = lambda x, y: ''
    text, text2 = "", ""
    if isinstance(stringLaTex, tuple):
        if type(stringLaTex[0]) != str or type(stringLaTex[1]) != str:
            raise Exception(error_1)
        else:
            text, textf = r'$%s$' % stringLaTex[0], r'$f:$'
            plt.text(0.5, 0.7, text, size=fontsize, horizontalalignment='center')
            plt.text(0.05, 0.7, textf, size=fontsize-10, horizontalalignment='center')
            text2, text2df = r'$%s$' % stringLaTex[1], r'$\sigma f:$'
            plt.text(0.5, 0.3, text2, size=fontsize, horizontalalignment='center')
            plt.text(0.01, 0.3, text2df, size=fontsize-10, horizontalalignment='left')
    else:
            text = r'$%s$' % stringLaTex
            plt.text(0.5, 0.5, text, size=fontsize, horizontalalignment='center')
    if savefigure:
        plt.savefig("LaTexFig.png")
    plt.show()

# ajuste
# entradas do export graph


#bugs theta
#double bar
#tamanho letras latex
































