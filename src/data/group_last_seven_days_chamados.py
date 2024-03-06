import configparser
from pathlib import Path

import basedosdados as bd
import pandas as pd
from google.oauth2 import service_account


def load_last_seven_days_data_chamados(
    project_id: str, gcp_credentials:dict, dir_to_save: str = None, ref_date: str = "2024-02-01"
) -> pd.DataFrame:
    if dir_to_save:
        path_to_save = Path(dir_to_save)
    else:
        path_to_save = dir_to_save
    query = f"""
    SELECT DATE(t1.data_inicio) as data_inicio,
           COUNT(*) as qtd_chamados
    FROM `datario.administracao_servicos_publicos.chamado_1746` t1
    WHERE DATE(t1.data_inicio) BETWEEN DATE_SUB(DATE '{ref_date}',INTERVAL 6 DAY)
    AND DATE '{ref_date}'
    GROUP BY 1
    ORDER BY 1 DESC;
    """
    df = pd.read_gbq(query=query, project_id=project_id,credentials=service_account.Credentials.from_service_account_info(gcp_credentials),progress_bar_type="tqdm_gui")

    # CONVERT DATE COLUMNS TO DATETIME

    date_cols = df.select_dtypes(include="dbdate")
    for col in date_cols.columns:
        df[col] = pd.to_datetime(date_cols[col], format="%Y-%m-%d")

    if path_to_save:
        if path_to_save.is_dir():
            df.to_csv(
                f"{path_to_save}/dataset_last_seven_days_chamado1746_{ref_date}.csv",
            )
        else:
            path_to_save.mkdir(parents=True)
            df.to_csv(
                f"{path_to_save}/dataset_last_seven_days_chamado1746_{ref_date}.csv",
            )

    else:
        return df


if __name__ == "__main__":
    cfg = configparser.ConfigParser()
    cfg.read_file(open("../../secrets.toml","r"))
    PROJ_ID = cfg["ENV"]["project_id"]
    REF_DATE = "2023-01-12"
    load_last_seven_days_data_chamados(
        project_id=PROJ_ID,gcp_credentials=cfg["GCP_CREDENTIALS"], ref_date=REF_DATE, dir_to_save="../../datasets/raw"
    )
