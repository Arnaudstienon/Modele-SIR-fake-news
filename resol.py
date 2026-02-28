import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def modele_fake_news(y, t, beta, alpha, gamma1, gamma2):
    S, I, R, V = y

    dS_dt = -beta * S * I
    dI_dt = beta * S * I * alpha - gamma2 * I
    dR_dt = beta * S * I * (1 - alpha) - gamma1 * R + I * gamma2 
    dV_dt = R * gamma1
    
    return [dS_dt, 
 dI_dt, dR_dt, dV_dt]

beta = 50
alpha = 0.0005
gamma1 = 0.05
gamma2 = 0.2

I0 = 50000 / 12000000
S0 = 1 - I0
R0 = 0
V0 = 0
y0 = [S0, I0, R0, V0]

t = np.linspace(0, 100, 1000)

solution = odeint(modele_fake_news, y0, t, args=(beta, alpha, gamma1, gamma2))

S_res = solution[:, 0]
I_res = solution[:, 1]
R_res = solution[:, 2]
V_res = solution[:, 3]

plt.plot(t, S_res, label='Ignorants (S)')
plt.plot(t, I_res, label='Propagateurs (I)')
plt.plot(t, R_res, label='Muets (R)')
plt.plot(t, V_res, label='Savants (V)')
plt.plot(t, I_res + R_res, label='Muets (R) + propagateurs (I)')
plt.xlabel('Temps')
plt.ylabel('Proportion de la population')
plt.title('Propagation d\'une Fake News au cours du temps')
plt.legend()
plt.grid()
plt.show()