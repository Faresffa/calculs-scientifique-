import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error

# Fonction pour résoudre les équations de Lotka-Volterra avec la méthode d'Euler
def lotka_volterra(alpha, beta, delta, gamma, step, iterations):
    time = [0]
    lapin = [1]  # Population initiale de lapins (normalisée)
    renard = [2]  # Population initiale de renards (normalisée)

    for _ in range(iterations):
        new_value_time = time[-1] + step
        new_value_lapin = lapin[-1] + (lapin[-1] * (alpha - beta * renard[-1])) * step
        new_value_renard = renard[-1] + (renard[-1] * (delta * lapin[-1] - gamma)) * step

        time.append(new_value_time)
        lapin.append(new_value_lapin)
        renard.append(new_value_renard)

    # Re-multiplier pour revenir à l'échelle des données réelles
    lapin = np.array(lapin) * 1000
    renard = np.array(renard) * 1000
    return time, lapin, renard

# Fonction pour calculer l'erreur quadratique moyenne (MSE)
def calculate_mse(pred_lapin, pred_renard, real_lapin, real_renard):
    mse_lapin = mean_squared_error(real_lapin, pred_lapin)
    mse_renard = mean_squared_error(real_renard, pred_renard)
    return mse_lapin + mse_renard  # La somme des deux erreurs

# Lecture des données réelles depuis le fichier CSV
real_data = pd.read_csv("E:/projects hetic/dev back/calculs-scientifique-/populations_lapins_renards.csv")
real_lapins = real_data['lapin']  # Colonne 'lapin'
real_renards = real_data['renard']  # Colonne 'renard'
real_time = real_data['date'] 

# Paramètres à tester dans le grid search
alpha_values = [1/3, 2/3, 1, 4/3]
beta_values = [1/3, 2/3, 1, 4/3]
delta_values = [1/3, 2/3, 1, 4/3]
gamma_values = [1/3, 2/3, 1, 4/3]

# Grid search pour trouver les meilleurs paramètres
best_mse = float('inf')
best_params = None
best_pred_lapin = None
best_pred_renard = None

# Test toutes les combinaisons possibles de paramètres
for alpha in alpha_values:
    for beta in beta_values:
        for delta in delta_values:
            for gamma in gamma_values:
                # Résolution des équations avec les paramètres actuels
                _, lapin, renard = lotka_volterra(alpha, beta, delta, gamma, 0.001, 1000)
                
                # Calcul de l'erreur (MSE)
                mse = calculate_mse(lapin[:len(real_lapins)], renard[:len(real_renards)], real_lapins, real_renards)
                
                # Si l'erreur est plus petite que la meilleure erreur trouvée, on met à jour
                if mse < best_mse:
                    best_mse = mse
                    best_params = (alpha, beta, delta, gamma)
                    best_pred_lapin = lapin[:len(real_lapins)]
                    best_pred_renard = renard[:len(real_renards)]

# Afficher les meilleurs paramètres trouvés et les courbes correspondantes
print(f"Meilleurs paramètres: alpha={best_params[0]}, beta={best_params[1]}, delta={best_params[2]}, gamma={best_params[3]}")
print(f"Erreur quadratique moyenne: {best_mse}")

# Tracé des courbes des meilleures prédictions avec le temps réel comme axe des x
plt.figure(figsize=(15, 6))

# Utilisation de real_time comme axe des abscisses (temps réel)
plt.plot(real_time, best_pred_lapin, "b-", label="Lapins (prédiction)")
plt.plot(real_time, best_pred_renard, "r-", label="Renards (prédiction)")

# Affichage des populations réelles avec real_time
plt.scatter(real_time, real_lapins, color="blue", label="Lapins (réel)", alpha=0.5)
plt.scatter(real_time, real_renards, color="green", label="Renards (réel)", alpha=0.5)

plt.xlabel("Temps [Mois]")
plt.ylabel("Population")
plt.title("Dynamique des populations de Lapins et Renards avec meilleurs paramètres")
plt.legend()

plt.grid(False)

plt.show()
