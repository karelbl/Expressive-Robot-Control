import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import transforms3d.euler as euler
import os
import importlib

def open_file(file_path): #open .dat data and convert to list
    data = pd.read_csv(file_path,sep=',',header=None)
    data_list = data.values.tolist()
    for i in range(len(data)):
        data_list[i] = data_list[i][0]
        data_list[i] = data_list[i].split('\t')
        for j in range(len(data_list[i])):
            data_list[i][j] = float(data_list[i][j])
    return data_list


#def compute_angles(data):
def conversion_matrix2angle(data): #data pour une partie du corps
    res=[]
    if len(data[0])==13:
        for i in range(1,len(data)):
            matrix_0 = [data[0][j] for j in range(4,len(data[0]))]
            matrix_0 = np.array(matrix_0).reshape(3,3)
            time = data[i][0]
            pos = np.array([data[i][1],data[i][2],data[i][3]])
            matrix = [data[i][j] for j in range(4,len(data[i]))]
            matrix = np.array(matrix).reshape(3,3)
            matrix = np.dot(matrix_0,matrix)
            angle = np.array(euler.mat2euler(matrix,axes = "sxyz"))
            res.append([time,pos,angle])
    if len(data[0])==10:
        for i in range(1,len(data)):
            matrix_0 = [data[0][j] for j in range(1,len(data[0]))]
            matrix_0 = np.array(matrix_0).reshape(3,3)
            time = data[i][0]
            matrix = [data[i][j] for j in range(1,len(data[i]))]
            matrix = np.array(matrix).reshape(3,3)
            matrix = np.dot(matrix_0,matrix)
            angle = np.array(euler.mat2euler(matrix,axes = "sxyz"))
            res.append([time,angle])
    if len(data[0])==2:
        for i in range(1,len(data)):
            angle_0 = data[0][1]
            angle = data[i][1]
            angle = angle - angle_0
            time = data[i][0]
            res.append([time,angle])
    return res



def time_derivative(data): #il faut insérer la liste data[1]
    dt = data[1][0] - data[0][0]
    res = []
    for i in range(1,len(data)):
        q_point = []
        for j in range(1,len(data[0])):
           value = (data[i][j]-data[i-1][j])/dt
           if isinstance(value,np.ndarray):
               value = value.tolist()
           q_point.append(value)
        res.append(q_point)
    return res

def q_point_column(data): #xelect data among the captors (for example, body, head, ...), here q_point are requested
    q_point = []
    for i in range(len(data[0][1])): #sur les temps
        res=[]
        for j in range(len(data)): #sur les parties du corps
            for k in range(len(data[j][1][i])):
                res+=data[j][1][i][k]
        q_point.append(res)
    return q_point

def auto_correl_matrix(q_point_col, T):
    q_point_col = np.array(q_point_col)
    new_q = []
    for i in range(len(q_point_col)):
        new_q.append(q_point_col[i].reshape(12,1))
    print(new_q[50])
    print(q_point_col[50])
    res = np.zeros([len(q_point_col[0]), len(q_point_col[0])])
    for i in range(1, len(q_point_col)):
        res += np.dot(new_q[i], new_q[i-1].T)
    res = 1/T * res

    return res.reshape(-1,1)
    
#def compute_matrix(q_point):

def auto_correl_matrix_from_beginning(file_path):
    data = []
    for nom_fichier in os.listdir(file_path):
        chemin_fichier = os.path.join(file_path, nom_fichier)
        # Vérifiez si c'est un fichier (et pas un dossier)
        if os.path.isfile(chemin_fichier):
            print(f'Trouvé fichier: {chemin_fichier}')
            # Faites quelque chose avec le fichier
            data.append([nom_fichier,open_file(chemin_fichier)])
    T = data[0][1][len(data[0][1])-1][0]

    new_data = []
    for i in range(len(data)):
        new_data.append([data[i][0],conversion_matrix2angle(data[i][1])])

    q_point = []
    for i in range(len(new_data)):
        q_point.append([new_data[i][0],time_derivative(new_data[i][1])])
    selected_data=[q_point[0],q_point[1],q_point[14]]


    q_point_col = q_point_column(selected_data)
    auto_correl = auto_correl_matrix(q_point_col,T)
    return auto_correl





        
