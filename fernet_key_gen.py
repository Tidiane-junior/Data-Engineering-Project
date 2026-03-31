#%% Generer une cle de chiffrement Fernet pour Airflow
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
# %%
