import json

with open("af.json", "r", encoding="utf-8") as f:
    af = json.load(f)


# -----
# definição do Autómato Finito 
V = set(af["V"])
Q = set(af["Q"])
delta =	af["delta"]	
q0 = af["q0"]
F = set(af["F"]) 

# especificação da função para avaliar se uma dada 
# palavra é reconhecida no Autómato AF
def reconhece( palavra: str ) -> bool:
	estado_atual: str = q0  # começar pelo estado inicial!
	tam: int = len(palavra) # tamanho da palavra a reconhecer
	i: int = 0 			   
	while (i < tam ) and (estado_atual != "erro"):
		simbolo_atual = palavra[i]
		if  (simbolo_atual in delta[estado_atual]):  
			estado_atual = delta[ estado_atual ][ simbolo_atual ]
		else:
			estado_atual = "erro"
		# --- end if
		i = i + 1
	# --- end while
	return (estado_atual in F) # and (i==tam)

# testar a função reconhece
for exemplo in ["ab", "aba", "abb", "a", "aa", "ba"]:
	print(f"'{exemplo}'   {reconhece(exemplo)}")

# utilização 
# python3 aula10_rec.py
# 'ab'   True
# 'aba'  True
# 'abb'  True
# 'a'    False
# 'aa'   False
# 'ba'   False
	
	
	
	