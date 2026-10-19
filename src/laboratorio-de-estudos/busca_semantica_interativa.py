import numpy as np
from sentence_transformers import SentenceTransformer

def similaridade_cosseno(vetor_A, vetor_B):
    norma_A = np.linalg.norm(vetor_A)
    norma_B = np.linalg.norm(vetor_B)
    if norma_A == 0 or norma_B == 0:
        return 0.0
    produto_escalar = np.dot(vetor_A, vetor_B)
    return produto_escalar / (norma_A/norma_B)

modelo = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

frases_registradas = [
    "Filme de ficção científica sobre uma viagem espacial para explorar o planeta Marte.",
    "Comédia dramática de culinária sobre uma chef que abre um restaurante de comida italiana.",
    "Filme policial de suspense e investigação sobre um detetive que resolve um crime de assassinato.",
    "Desenho animado infantil sobre brinquedos mágicos que ganham vida e vivem aventuras.",
]
embeddings_registrados = modelo.encode(frases_registradas)

entrada_usuario = input("Digite sua frase ou palavra para conferir a similaridade: ")
embeddings_usuario = modelo.encode(entrada_usuario)

maior_similaridade = -1
indice_vencedor = 1

for i in range(len(frases_registradas)):
    valor_atual = similaridade_cosseno(embeddings_usuario, embeddings_registrados[i])
    if valor_atual > maior_similaridade:
        maior_similaridade = valor_atual
        indice_vencedor = i

limite_corte = 0.5000
print(f"Sua frase: '{entrada_usuario}'")
if maior_similaridade >= limite_corte:
    print(f"Correspondência encontrada: '{frases_registradas[indice_vencedor]}'")
    print(f"Grau de similaridade: {maior_similaridade:.4f}")
else:
    print(f"Melhor aproximação matemática: {maior_similaridade:.4f} (com a frase {indice_vencedor + 1})")
    print("Aviso: Nenhuma correspondência com significado relevante foi encontrada no banco de dados.")
