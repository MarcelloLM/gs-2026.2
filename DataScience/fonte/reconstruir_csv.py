"""Reconstrói o painel a partir dos quatro CSVs oficiais do SP156."""
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlretrieve
import hashlib
import pandas as pd

FONTES = [('https://dados.prefeitura.sp.gov.br/dataset/0aecfa2b-aa3a-40d4-8183-0d4351b7fd0a/resource/7c5aeb58-2cad-40ba-9e9e-af1c17cc5070/download/arquivo-final-1-trim-25.csv', 'f9d02a8bf358f019a5851e0d3d05daa236f803f5b22f254b66fd7b69f63e5170'),
    ('https://dados.prefeitura.sp.gov.br/dataset/0aecfa2b-aa3a-40d4-8183-0d4351b7fd0a/resource/f5df7f4a-d614-4f85-b4a0-263ec9370cd9/download/arquivo-final-2-trim-25.csv', '66fc96cf4c4bed437b9f560f23aeb8d93c33d2ff7212fd0bc240742681bedc1e'),
    ('https://dados.prefeitura.sp.gov.br/dataset/0aecfa2b-aa3a-40d4-8183-0d4351b7fd0a/resource/3b1d2648-d586-40c8-819c-24fbb8005343/download/arquivo-final-3-trim-25.csv', '6b5c382dbc409074db3a3dbdb577c4c2abc76c8009757a457a2a418956e22c2d'),
    ('https://dados.prefeitura.sp.gov.br/dataset/0aecfa2b-aa3a-40d4-8183-0d4351b7fd0a/resource/d3a98097-8128-45d4-b8fe-21874b81c971/download/arquivo-final-4-trim-25.csv', '0a19e3451e30f33f1a8c2581608e1cc92d036915d0594737f0a2ceb0e05929cc')]
SERVICO = "Fazer reclamação de falta de varrição"
DESTINO = Path(__file__).resolve().parents[1] / "varricao_sp156.csv"

def reconstruir():
    blocos = []
    with TemporaryDirectory() as pasta:
        for i, (url, esperado) in enumerate(FONTES, 1):
            arquivo = Path(pasta) / f"trimestre_{i}.csv"
            urlretrieve(url, arquivo)
            with arquivo.open("rb") as entrada:
                assinatura = hashlib.file_digest(entrada, "sha256").hexdigest()
            if assinatura != esperado:
                raise ValueError(f"Fonte do trimestre {i} foi alterada. Confira a versão publicada.")
            for parte in pd.read_csv(arquivo, encoding="latin1", sep=";", dtype="string",
                                     usecols=["Data de Abertura", "Distrito", "Serviço"], chunksize=100000):
                linhas = parte.loc[parte["Serviço"].str.strip().eq(SERVICO),
                                   ["Data de Abertura", "Distrito"]].dropna().copy()
                linhas["distrito"] = linhas.pop("Distrito").str.strip().str.upper()
                datas = pd.to_datetime(linhas.pop("Data de Abertura"), format="%d/%m/%Y")
                linhas["semana"] = datas - pd.to_timedelta(datas.dt.weekday, unit="D")
                blocos.append(linhas.loc[datas.between("2025-01-06", "2025-12-28")])
    dados = pd.concat(blocos)
    semanas = pd.date_range("2025-01-06", "2025-12-22", freq="W-MON")
    indice = pd.MultiIndex.from_product([sorted(dados.distrito.unique()), semanas],
                                        names=["distrito", "semana"])
    painel = dados.groupby(["distrito", "semana"]).size().reindex(indice, fill_value=0)
    painel.rename("pedidos").reset_index().to_csv(DESTINO, index=False)

if __name__ == "__main__":
    reconstruir()
