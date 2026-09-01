#!/usr/bin/env python3
"""
Roteiro 2 - Gera o dataset individual da sua dupla a partir do pool do CICIDS2017.

    python meu_dataset.py --dupla "Nome Sobrenome; Nome Sobrenome"

Saída: dados/R2_<codigo>.csv.gz  (~110 mil fluxos, 83 colunas)  e a CLASSE DIFÍCIL da dupla.
O código da dupla e a amostra são determinísticos: rodar de novo gera o mesmo arquivo.
Use SEMPRE o seu próprio arquivo — os números do relatório são conferidos contra ele.
"""
import argparse
import os
import re
import unicodedata
import zlib

import numpy as np
import pandas as pd

POOL = "pool/cicids2017_pool.csv"
N_ALVO = 110_000
CLASSES_DIFICEIS = [
    ("Bot", ["Bot"]),
    ("Web Attack (separar XSS de Brute Force)", ["Web Attack - Brute Force", "Web Attack - XSS", "Web Attack - Sql Injection"]),
    ("DoS lento (slowloris + Slowhttptest)", ["DoS slowloris", "DoS Slowhttptest"]),
    ("DoS Hulk (por que cai no split temporal?)", ["DoS Hulk"]),
    ("Infiltration + Heartbleed", ["Infiltration", "Heartbleed"]),
]

def codigo_dupla(nomes: str) -> tuple[str, int]:
    partes = [unicodedata.normalize("NFKD", p).encode("ascii", "ignore").decode().lower()
              for p in re.split(r"[;,/]", nomes)]
    partes = sorted(re.sub(r"[^a-z]", "", p) for p in partes if p.strip())
    chave = "|".join(partes)
    seed = zlib.crc32(chave.encode()) & 0xFFFFFFFF
    return f"{seed:08x}"[:6], seed

def gerar(nomes: str, pool_path: str = POOL, saida_dir: str = "dados"):
    cod, seed = codigo_dupla(nomes)
    rng = np.random.default_rng(seed)
    if not os.path.exists(pool_path) and os.path.exists(f"{pool_path}.gz"):
        pool_path = f"{pool_path}.gz"
    pool = pd.read_csv(pool_path, encoding="latin-1", low_memory=False)
    lab = " Label"
    partes = []
    frac = N_ALVO / len(pool)
    for cls, g in pool.groupby(lab):
        n = len(g) if len(g) < 3000 else int(len(g) * frac)
        partes.append(g.sample(n, random_state=int(rng.integers(0, 2**31))))
    df = pd.concat(partes).sample(frac=1, random_state=seed).reset_index(drop=True)
    dif_nome, dif_labels = CLASSES_DIFICEIS[seed % len(CLASSES_DIFICEIS)]
    os.makedirs(saida_dir, exist_ok=True)
    arq = os.path.join(saida_dir, f"R2_{cod}.csv.gz")
    df.to_csv(arq, index=False, encoding="latin-1", compression="gzip")
    return cod, seed, arq, df, dif_nome, dif_labels

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dupla", required=True, help='ex.: "Ana Lima; Bruno Souza"')
    a = ap.parse_args()
    cod, seed, arq, df, dif_nome, dif_labels = gerar(a.dupla)
    print(f"Código da dupla : {cod}")
    print(f"random_state    : {seed}   <- use este valor em TODO train_test_split / modelo")
    print(f"Arquivo         : {arq}  ({df.shape[0]} fluxos x {df.shape[1]} colunas)")
    print(f"Classe difícil  : {dif_nome}   -> rótulos {dif_labels}")
    print("\nDistribuição de rótulos:")
    print(df[" Label"].value_counts().to_string())
