##### Read the scenario file #############
### Input: Scenario.tcl, number of nodes and duration
### Output: X e Y node positions --> node_x and node_y


def read_tcl_function(scenario_tcl,node_number,duration):
        
    f0=open (scenario_tcl,'r')
    f0.seek(0)    
    h=0
        
    node_x=[]
    node_y=[]
   
    for j in range(node_number):
        f0.seek(0) 
        i=0 
        last_time=0 
        last_elemento_x=0
        last_elemento_y=0
        z=0
        primer_elemento=0
        node_one_x=[]
        node_one_y=[]
        for line in f0:
            linea_un = line.split(' ')
               
            if len(linea_un)>3 and linea_un[3]=='"$node_('+str(j)+')'  and float(linea_un[2])<=duration:
                if (i==0):
                    primer_elemento=int(float(linea_un[2]))
        
                node_one_x.insert(int(float(linea_un[2])),float(linea_un[5]))
                node_one_y.insert(int(float(linea_un[2])),float(linea_un[6]))
                z+=1
                                
                if float(linea_un[2])!=float(last_time)+1 and i!=0:
                    
                    for x in range(int(float(linea_un[2]))-int(last_time)-1):
                        node_one_x.insert(len(node_one_x)+x,last_elemento_x)
                        node_one_y.insert(len(node_one_y)+x,last_elemento_y)
                last_time=(float(linea_un[2]))    
                last_elemento_x=float(linea_un[5])
                last_elemento_y=float(linea_un[6])             
                i+=1
                
        if len(node_one_x)==0:
            for h in range(duration):
                node_one_x.insert(h,"None")
                node_one_y.insert(h,"None")
        else: 
            if len(node_one_x)< duration:
                for g in range(duration-int(last_time)-1):
                    node_one_x.insert(len(node_one_x)+g,last_elemento_x)
                    node_one_y.insert(len(node_one_y)+g,last_elemento_y)

            if primer_elemento!=0:
                for h in range(primer_elemento):
                    node_one_x.insert(h,"None")
                    node_one_y.insert(h,"None")
       
        node_x.append(node_one_x)
        node_y.append(node_one_y)
        node_one_x=[]
        node_one_y=[]

    return node_x,node_y


#node_positions=[]   #X Y positions n nodes t seconds
#node_positions=read_tcl_function("Seville_2x2_100_1.tcl",100,1)


##node_positions[0]--> coord X
##node_positions[1]--> coord Y
##########################################

#node_positions[0][0]--> Coord X, node 0, from t=0 to t=simulation_time
#node_positions[0][49]--> Coord X, node 50, from t=0 to t=simulation_time

#node_positions[1][0]--> Coord Y, node 0, from t=0 to t=simulation_time
#node_positions[1][49]--> Coord Y, node 50, from t=0 to t=simulation_time

