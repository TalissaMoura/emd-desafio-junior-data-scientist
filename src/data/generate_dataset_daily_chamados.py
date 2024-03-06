import configparser
from pathlib import Path

import basedosdados as bd
import pandas as pd
import streamlit as st
from google.oauth2 import service_account


def load_daily_data_chamados(
    project_id: str,gcp_credentials: dict, dir_to_save: str = None, ref_date: str = "2024-02-01"
) -> pd.DataFrame:
    """
    Load the data from chamados_1746 table at a ref_date with additional geolocation information from bairros table.
    Args:
        project_id (str): name of the project on your account in GCP.
        gcp_credentials (dict): the dict of a service_account in GCP. See https://cloud.google.com/iam/docs/service-account-overview
        dir_to_save (str, optional): Path of the directory to save the dataset. If dosen't exist, create one. Defaults to None.
        ref_date (str, optional): Reference date to filter the data from chamados_1746 table. Defaults to "2024-02-01".

    Returns:
        pd.DataFrame: A pandas dataframe with all the data in the ref_date.
    """
    if dir_to_save:
        path_to_save = Path(dir_to_save)
    else:
        path_to_save = dir_to_save
    query = f"""
    SELECT t1.id_chamado,
       t1.data_inicio,
       t1.id_bairro,
       t2.nome as nome_bairro,
       t2.subprefeitura,
       t2.geometry as geometry_bairro,
       t1.categoria,
       t1.id_tipo,
       t1.tipo,
       t1.id_subtipo,
       t1.subtipo,
       t1.status,
       t1.situacao,
       t1.tipo_situacao,
       t1.latitude,
       t1.longitude,
       t1.geometry as geometry_chamado
    FROM `datario.administracao_servicos_publicos.chamado_1746` t1
    LEFT JOIN `datario.dados_mestres.bairro` t2
    ON t1.id_bairro = t2.id_bairro 
    WHERE t1.data_particao = DATE_TRUNC(DATE '{ref_date}', MONTH)
    AND DATE(t1.data_inicio) = '{ref_date}' 
    """
    df = pd.read_gbq(query=query, project_id=project_id,credentials=service_account.Credentials.from_service_account_info(gcp_credentials),progress_bar_type="tqdm")
    # CONVERT DATE COLUMNS TO DATETIME

    date_cols = df.select_dtypes(include="dbdate")
    for col in date_cols.columns:
        df[col] = pd.to_datetime(date_cols[col], format="%Y-%m-%d")

    if path_to_save:
        if path_to_save.is_dir():
            df.to_parquet(
                f"{path_to_save}/dataset_daily_chamado1746_{ref_date}.parquet.gzip",
                compression="gzip",
            )
        else:
            path_to_save.mkdir(parents=True)
            df.to_parquet(
                f"{path_to_save}/dataset_chamado1746_{ref_date}.parquet.gzip",
                compression="gzip",
            )

    else:
        return df


if __name__ == "__main__":
    cfg = configparser.ConfigParser()
    cfg.read_file(open("../../secrets.toml","r"))
    PROJ_ID = cfg["ENV"]["project_id"]
    REF_DATE = "2023-04-01"
    load_daily_data_chamados(
        project_id=PROJ_ID,gcp_credentials=cfg["GCP_CREDENTIALS"], ref_date=REF_DATE, dir_to_save="../../datasets/raw"
    )
