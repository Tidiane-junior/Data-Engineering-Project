#%% Generer une cle de chiffrement Fernet
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
# %%
