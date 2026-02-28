import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize
import matplotlib.pyplot as plt


beta, alpha, gamma1, gamma2 = 300, 0.003, 0.12, 0.06
gamma_max, k1 = 0.5, 3
c1, c2 = 500, 100
B_max = 10

t_delay = 7 

y0 = [1 - 1e-7, 1e-7, 0, 0] 
t = np.linspace(0, 100, 1000)


def simuler(u):
    u1, u2 = u
    
    def modele(y, t):
        S, I, R, V = y
        if t < t_delay:
            gamma1_actuel = gamma1
            gamma2_actuel = gamma2
        else:
            gamma1_actuel = gamma1 + gamma_max * (1 - np.exp(-k1 * u1))
            gamma2_actuel = gamma2 + u2 
            
        beta_actuel = beta 

        dS_dt = -beta_actuel * S * I
        dI_dt = alpha * beta_actuel * S * I - gamma2_actuel * I
        dR_dt = beta_actuel * S * I * (1 - alpha) - gamma1_actuel * R + gamma2_actuel * I
        dV_dt = gamma1_actuel * R
        
        return [dS_dt, dI_dt, dR_dt, dV_dt]
        
    return odeint(modele, y0, t, rtol=1e-10, atol=1e-10)


def calcul_pic(u):
    solution = simuler(u)
    return np.max(solution[:, 1] + 
 solution[:, 2])

def contrainte_budget(u):
    u1, u2 = u
    return B_max - (c1 * u1**2 + c2 * u2)


bounds = [(0, 1), (0, 1)]
constraints = {'type': 'ineq', 'fun': contrainte_budget}
u0 = [0.0, 0.0]

resultat = minimize(calcul_pic, u0, method='SLSQP', bounds=bounds,
                    constraints=constraints, options={'eps': 1e-3, 'disp': True})
u1_opt, u2_opt = resultat.x
print("u1 optimal : ", u1_opt)
print("u2 optimal : ", u2_opt)

sol_base = simuler([0, 0])
courbe_base = sol_base[:, 1] + sol_base[:, 2]

sol_opt = simuler(resultat.x)
courbe_opt = sol_opt[:, 1] + sol_opt[:, 2]

plt.figure(figsize=(10, 6))
plt.plot(t, courbe_base, 'r--', label='Sans intervention (Baseline)')
plt.plot(t, courbe_opt, 
 'g', linewidth=2,
      label=f'Strategie optimale post-delai (u1={u1_opt:.2f}, u2={u2_opt:.2f})')
    
plt.axvline(x=t_delay, color='gray', linestyle=':', label=f'Debut intervention (t={t_delay}j)')

plt.title("Impact de la contre-ingerence avec retard de reaction")
plt.xlabel('Temps (jours)')
plt.ylabel('Proportion de la population atteinte (I+R)')
plt.ylim(0, 1)
plt.legend()
plt.grid(True)
plt.savefig('comparaison_optimisation_delay.png', dpi=300)
plt.show()