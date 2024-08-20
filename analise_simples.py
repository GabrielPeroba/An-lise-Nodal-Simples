# -*- coding: utf-8 -*-

import numpy as np



def main(arquivo_netlist):



    ArqNetlist = []     #Lista com nomes e valores dos componentes
    
    with open(arquivo_netlist, "r") as arquivo:     #Leitura do arquivo

        for linha in arquivo:
 
            palavras = linha.strip().split()

            tupla = tuple(palavras)
            ArqNetlist.append(tupla)




    no_maior=0
   
    i = 0  # Variavel i (indice do loop)
    
    while i < len(ArqNetlist):  #loop para determinar ordem dos nos para resistores
        termo = ArqNetlist[i]  

        if termo[0][0] == 'R':
            
            no_a = int(termo[1])
            no_b = int(termo[2])
            
            if max(no_a, no_b) > no_maior:
                
                no_maior = max(no_a, no_b) 

        elif termo[0][0] == 'I':  #loop para determinar ordem dos nos para correntes independentes
            
            no_a = int(termo[1])
            no_b = int(termo[2])
            
            if max(no_a, no_b) > no_maior:
                
                no_maior = max(no_a, no_b)

        elif termo[0][0] == 'G':  #loop para determinar ordem dos nos para correntes independentes
            
            no_a = int(termo[1])
            no_b = int(termo[2])
            no_c = int(termo[3])
            no_d = int(termo[4])
            
            if max(no_a, no_b, no_c, no_d) > no_maior:
                
                no_maior = max(no_a, no_b, no_c, no_d)

        i += 1  

    no_maior += 1 
    A = np.zeros((no_maior, no_maior), dtype=float) #matriz de transcondutancia
    B = np.zeros(no_maior)  #vetor de correntes
    
    i = 0  # loops para preencher as matrizes com os termos
    while i < len(ArqNetlist):
        termo = ArqNetlist[i]

        if termo[0][0] == 'R':      #estampa do resistor
            
            Resistor = float(termo[3])
            no_a = int(termo[1])
            no_b = int(termo[2])
            
            A[no_a, no_a] = A[no_a, no_a] + 1 / Resistor
            A[no_a, no_b] = A[no_a, no_b] - 1 / Resistor
            A[no_b, no_a] = A[no_b, no_a] - 1 / Resistor
            A[no_b, no_b] = A[no_b, no_b] + 1 / Resistor

        elif termo[0][0] == 'I':    #estampa da fonte de corrente independente
            
            fonte_I = float(termo[4])
            no_a = int(termo[1])
            no_b = int(termo[2])
            
            B[no_a] = B[no_a] - fonte_I
            B[no_b] = B[no_b] + fonte_I

        elif termo[0][0] == 'G':    #estampa da fonte de corrente dependente
            
            no_a = int(termo[1])
            no_b = int(termo[2])
            no_c = int(termo[3])
            no_d = int(termo[4])
            fonte_Idep = float(termo[5])
            
            A[no_a, no_c] = A[no_a, no_c] + fonte_Idep
            A[no_a, no_d] = A[no_a, no_d] - fonte_Idep
            A[no_b, no_c] = A[no_b, no_c] - fonte_Idep
            A[no_b, no_d] = A[no_b, no_d] + fonte_Idep

        i += 1  

    A = A[1:, 1:]
    B = B[1:]
    
    resposta =  np.linalg.solve(A, B) #Resolver as equacoes


    i = 0
    while i < len(resposta):
    
        #Resposta em forma de texto
        print(f"e{i + 1} = {resposta[i]} V")

        i += 1

    print("")
    return resposta





if __name__ == "__main__":
    arquivo_netlist = "C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\trab_CE2\\netlist3.txt" #Trocar este endereco por onde o arquivo da netlist esta localizado
    tensao_nodal = main(arquivo_netlist)
