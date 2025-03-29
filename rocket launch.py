import math as m
import numpy as np
import matplotlib.pyplot as plt

#=============================================================================
#                   TRADUCTION DES DIFFÉRENTES LOIS EN PYTHON
#=============================================================================

#=============================================================================
#                  LOIS RÉGISSANT LA PROPULSION DE LA FUSÉE
#=============================================================================

def resistance_air(rho, Cx, S, V):
    return (1/2) * rho * Cx * S * (V**2)

# densité de l'air rho en kg/m^3
# Vitesse V en m.s-1
# Surface S en m2
# Coefficient de pénétration dans l’air Cx (sans dimension)

def force_de_poussée(P, S):
    return 2 * P * S

# Pression de l'air P en Pascal (Pa)
# Surface S en m2

#=============================================================================
#                  LOIS RÉGISSANT LE VOL DE LA FUSÉE
#=============================================================================

def acceleration(F, M):
    return F / M

# Résultante des forces F en Newton
# Masse totale de la fusée M en Kg

def Vlimite(M, g, p, Cx, S):
    return m.sqrt((2 * M * g) / (p * Cx * S))

# Pesanteur g = 9,81 m.s-2.
# Masse totale de la fusée M en Kg
# Surface S en m2
# Coefficient de pénétration dans l’air Cx (sans dimension)
# Pression de l'air p en Pascal (Pa)

#=============================================================================
#                LOIS RÉGISSANT LA STABILITÉ DE LA FUSÉE
#=============================================================================

def Force(M,g,R):
    return (M*g)-R

# Pesanteur g = 9,81 m.s-2.
# Masse totale de la fusée M en Kg
# Résistance R en Newton (N)

#-----------------------------------------------------------------------

def centre_gravité(Mv, Xv, Me, X1, X2):
    
    # Calcul de Xe
    Xe = X1 + X2
    
    # Calcul de Mg (masse totale de la fusée en charge)
    Mg = Mv + Me
    
    # Calcul de Xg (distance du CdG de la fusée en charge par rapport au sommet du cône)
    Xg = (Mv * Xv + Me * Xe) / Mg
    
    return Xg

# Mg×Xg=Mv×Xv+Me×Xe

# Mg la masse totale de la fusée en charge (fusée + eau).
# Xg la distance du CdG de la fusée en charge par rapport au sommet du cône.
# Mv la masse de la fusée à vide.
# Xv la distance du CdG de la fusée à vide par rapport au sommet du cône.
# Me est la masse d'eau
# Xe la distance du CdG de la masse d'eau par rapport au sommet du cône.


#=============================================================================
#               PROGRAMME DE SIMULATION D'UNE PHASE DE VOL
#=============================================================================


#----------------------------------------------------------------------------
#DONNÉES VIA DOCUMENTATION SUR LE FICHIER PDF

g = 9.81                    # accélération due à la gravité en m/s^2
rho = 1.225                 # densité de l'air en kg/m^3
Cx = 0.5                    # coefficient de traînée (à ajuster selon la forme de la fusée)
S = 0.0001                  # surface d'éjection en m^2
Pi = 80000                 # pression initiale en Pa
masse_bouteille = 0.2       # masse de la bouteille vide en kg
masse_eau_initiale = 0.5    # masse initiale de l'eau en kg

#----------------------------------------------------------------------------
#CONDITIONS INITIALES

masse_totale = masse_bouteille + masse_eau_initiale
vitesse = 0
altitude = 0
pas_de_temps = 0.01         # intervalle de temps en secondes
temps = 0
duree_poussee = 1           # durée de la poussée en secondes (à ajuster)

# Listes pour stocker les résultats
temps_liste = []
altitudes = []
vitesses = []

#----------------------------------------------------------------------------

#=============================================================================
#                    SIMULATION DE LA PHASE DE PROPULSION
#=============================================================================

while temps < duree_poussee:
    
    F_poussée = force_de_poussée(Pi, S)                 # poussée en N
    Poids = masse_totale*g                              # poids en N
    Résistance = resistance_air(rho,Cx,S,vitesse)       # résistance de l'air en N
    force_nette = F_poussée-Poids-Résistance            # force nette en N
    a = acceleration(force_nette, masse_totale)         # accélération en m/s^2
    
#----------------------------------------------------------------------------
    # Mise à jour des paramètres
    
    vitesse += a*pas_de_temps
    altitude += vitesse * pas_de_temps
    masse_totale -= masse_eau_initiale/duree_poussee*pas_de_temps  # diminution de la masse de l'eau

#----------------------------------------------------------------------------
    # Stockage des résultats
    
    temps_liste.append(temps)
    altitudes.append(altitude)
    vitesses.append(vitesse)
    
#----------------------------------------------------------------------------
    # Mise à jour du temps
    temps += pas_de_temps
    
#=============================================================================
#            SIMULATION DE LA PHASE DE PROPULSION ET DE DESCENTE
#=============================================================================

while altitude > 0:
    Poids = masse_totale*g                              # poids en N
    Résistance = resistance_air(rho,Cx,S,vitesse)       # résistance de l'air en N
    force_nette = -Poids-Résistance                     # force nette en N (poussée nulle)
    a = acceleration(force_nette,masse_totale)          # accélération en m/s^2
    
#----------------------------------------------------------------------------
    # Mise à jour des paramètres
    
    vitesse += a*pas_de_temps
    altitude += vitesse*pas_de_temps
    
#----------------------------------------------------------------------------
    # Stockage des résultats
    
    temps_liste.append(temps)
    altitudes.append(altitude)
    vitesses.append(vitesse)
    
#----------------------------------------------------------------------------
    # Mise à jour du temps
    
    temps += pas_de_temps


#=============================================================================
#                      AFFICHAGE DES RÉSULTATS
#=============================================================================

plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(temps_liste, altitudes)
plt.xlabel('Temps (s)')
plt.ylabel('Altitude (m)')
plt.title('Altitude en fonction du temps')

plt.subplot(2, 1, 2)
plt.plot(temps_liste, vitesses)
plt.xlabel('Temps (s)')
plt.ylabel('Vitesse (m/s)')
plt.title('Vitesse en fonction du temps')

plt.tight_layout()
plt.show()