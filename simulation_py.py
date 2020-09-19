# -*- coding: utf-8 -*-
"""simulation.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19xrmxkwv6TQ_cv4lZErk9klJO_jeLEEt
"""

import matplotlib.pyplot as plt
import numpy as np

class epid:
  def __init__(self, population=1, k=0,beta = 0.2, gamma=1/14, alpha=1/5, lamb=0., mu=0.):
    '''
    #Creation of a model.
    #PARAMETERS >>         population : redundant.
    #                      k          : (in SEIRs models) relation between infected and susceptible people.
    #                      beta       : 
    #                      gamma      : inverse of 2 weeks in days
    #                      alpha      : 
    #                      lamb       : birth rate.
    #                      mu         : death rate
    #                      days       : number of days to analyze.
    #
    #INTERNAL VARIABLES >> dt  : a day divided in hours.
    #                      kdt : number of hours in a day.
    #                      N   : total population.
    #                      S   : susceptible people (in SIR models can be infected. In SEIR models they can't, they are going to expose itself to the disease).
    #                      E   : exposed people (only valid in SEIR models. Represent infectable people).
    #                      I   : infected people (they can infect other people).
    #                      R   : recovered people.
    #
    #CALL EXAMPLE >>       mdl : epid(300000, 4, .2, .07, .2, .005, .001)
    '''

    self.days       = 365
    self.dt         = 1/24
    self.kdt        = 24
    self.beta       = beta
    self.gamma      = gamma
    self.alpha      = alpha
    self.lamb       = lamb
    self.mu         = mu
    self.population = population
    self.k          = k

    self.S = np.zeros(self.days)
    self.I = np.zeros(self.days)
    self.R = np.zeros(self.days)
    self.N = np.zeros(self.days)
    self.E = np.zeros(self.days)



    self.N[0] = self.population
    self.I[0] = inf0
    self.R[0] = 0.
    self.E[0] = self.k*self.I[0]
    self.S[0] = self.N[0] - self.E[0] - self.I[0]
    return(self.N[0],)


  def exec(self,method,model,*args):
    '''
    #CALL EXAMPLE >> mdl1.exec(mdl1.rk4,mdl1.sir_mod, mdl1.S, mdl1.I, mdl1.R)
    '''

    self.integration(method,model,*args)
    self.graph(model,method)
    strings=['susceptible','infected','recovered','exposed']
    arrays=[self.S,self.E,self.I,self.R]
    for i in range(4):
      if i!=3:
        self.max(arrays[i],strings[i])
      if i == 3:
        self.max(arrays[i],strings[i])
    return


  def integration(self, method, model, *args):
    '''
    #PARAMETERS >> method : integration method euler or rk4;
    #              model  : epidemiological desease model sir_mod or seir_mod; 
    #              days   : receives an integer wich indicates the amount of days to evaluate
    #              *args  : receive multiple list as posicional parameters S,I,R or S,E,I,R;
    #
    #CALL EXAMPLE >> integration(euler, sir_mod, S, I, R)
    '''
    
    for i in range(self.days-1): ##-- corregido, no pide argumento. Toma el valor de self.days.
      array = []
      counter = 0
      for arg in args:
        array.append(arg[i])
      for arg in args:
        arg[i+1] = method(model, array)[counter]
        counter += 1
      self.N[i+1]= sum(array)
    
    return ()


  def euler(self,model, array, kdt=24): 
    '''
    #integration by eulers method
    #PARAMETERS >>      model : epidemiological desease model sir_mod or seir_mod 
    #                   array : receives the current elements of a list
    #                   kdt   : number of integrations in one day
    '''

    flag = 0
    array2 = np.zeros(len(array))
    for i in range(kdt):
      array2 = model(array, flag)
      array = array2

    return np.array(array)


  def rk4(self,model,xold): 
    '''
    #Runge-Kutta's 4th orden integration method** revision pendiente
    # PARAMETERS >> model : epidemiological desease model sir_mod or seir_mod;
    #               xold  : receives the last element in a list
    '''

    flag = 1
    dx1 = model( xold, flag )
    dx2 = model( xold + 0.5 * dx1, flag )
    dx3 = model( xold + 0.5 * dx2, flag )
    dx4 = model( xold + dx3, flag )
    xnew= xold +  ( dx1 + 2.0 * (dx2 + dx3) + dx4 ) / 6.0    
    return np.array(xnew)


  def sir_mod(self,array, flag = 0):
    '''
    #The SIR model for epidemic diseases-
    # PARAMETERS >> array
    #               flag = 
    '''

    global N0
    S0, I0, R0 = array[0], array[1], array[2]
    N0 = self.population   
    if flag == 0:
      S1 = S0 - self.beta*(S0*I0/N0)*self.dt
      I1 = I0 + (self.beta*(S0*I0/N0) - self.gamma*I0)*self.dt
      R1 = R0 + (self.gamma*I0)*self.dt
    elif flag == 1:
      S1 = - self.beta*(S0*I0/N0)
      I1 = self.beta*(S0*I0/N0) - self.gamma*I0
      R1 = self.gamma*I0
    else:
      print("Flag error: expected 0/1, recibed:", flag)
    return np.array([S1, I1, R1])


  def seir_mod(self,array, flag = 0):
    '''
    #PARAMETERS >>   array = 
    #                flag =
    #CALL EXAMPLE >> seir_mod(data, 1)
    '''

    global N0
    S0, E0, I0, R0 = array[0], array[1], array[2], array[3]
    N0 = self.population
    if flag == 0:
      S1 = S0 + (self.lamb*N0 - self.mu*S0 - self.beta*(S0*I0/N0)) * self.dt
      E1 = E0 + (self.beta*(S0*I0/N0) - (self.mu + self.alpha)*E0) * self.dt
      I1 = I0 + (self.alpha*E0 - (self.gamma + self.mu)*I0) * self.dt
      R1 = R0 + (self.gamma*I0 - self.mu*R0)*self.dt
    elif flag == 1:
      S1 = self.lamb*N0 - self.mu*S0 - self.beta*(S0*I0/N0)
      E1 = self.beta*(S0*I0/N0) - (self.mu + self.alpha)*E0
      I1 = self.alpha*E0 - (self.gamma + self.mu)*I0
      R1 = self.gamma*I0 - self.mu*R0
    else:
      print ("Flag error: expected 0/1, recibed:", flag)
    return np.array([S1, E1, I1, R1])


  def graph(self,mod,method):
    '''
    '''
    t = np.arange(self.days)
    plt.figure(figsize=[10,7])
    plt.grid()
    plt.plot(t,self.S,'b', lw=3, label='Susceptible')
    if self.E[1] != 0:
      plt.plot(t,self.E,'orange', lw=3, label='Exposed')
    plt.plot(t,self.I,'r', lw=3, label='Infected')
    plt.plot(t,self.R,'g', lw=3, label='Recovered')
    plt.xlabel("Time (Days)")
    plt.ylabel("Population")
    #plt.title(mod,"model by ", method,"'s method")
    plt.legend()

    #a = np.arange(max(N)*.8,max(N)*1.2,  (max(N) - max(N)*.1 ) / 3 ) #Utilizado para ajustar la escala del eje las ordenadas
    b  = self.population
    a = np.arange(b-5,b+5,  1 )
    plt.figure(figsize=[10,7])
    plt.grid()
    plt.plot(t,self.N,'b', lw=3, label='Poblacion total')
    plt.yticks(a)
    plt.legend()  
    return


  def max (self, array, string):
    print ("The peak of", string, "people occurs in day", int(np.argmax(array)),)
    return





  def listar(self, N):
    for i in N:
      print (i)

mdl1 = epid(300000)
mdl1.exec(mdl1.euler,mdl1.seir_mod, mdl1.S, mdl1.E, mdl1.I, mdl1.R)