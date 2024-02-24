from pathlib import Path

import basedosdados as bd
import pandas as pd


def load_last_five_days_data_chamados(
    project_id: str, dir_to_save: str = None, ref_date: str = "2024-02-01"
) -> pd.DataFrame:

    path_to_save = Path(dir_to_save)
    query = f"""
    SELECT DATE(t1.data_inicio) as data_inicio,
           COUNT(*) as qtd_chamados
    FROM `datario.administracao_servicos_publicos.chamado_1746` t1
    AND DATE(t1.data_inicio) BETWEEN DATE_SUB(DATE '{ref_date}',INTERVAL 5 DAY)
    AND DATE '{ref_date}'
    GROUP BY 1
    ORDER BY 1 DESC;
    """
    df = bd.read_sql(query, billing_project_id=project_id)

    # CONVERT DATE COLUMNS TO DATETIME

    date_cols = df.select_dtypes(include="dbdate")
    for col in date_cols.columns:
        df[col] = pd.to_datetime(date_cols[col], format="%Y-%m-%d")


    if path_to_save:
        if path_to_save.is_dir():
            df.to_csv(
                f"{path_to_save}/dataset_last_five_days_chamado1746_{ref_date}.csv",
                
            )
        else:
            path_to_save.mkdir(parents=True)
            df.to_csv(
                f"{path_to_save}/dataset_last_five_days_chamado1746_{ref_date}.csv",
                
            )

    else:
        return df


if __name__ == "__main__":
    PROJ_ID = "teste-cientista-dados-jr-rj"
    REF_DATE = "2023-01-12"
    load_last_five_days_data_chamados(
        project_id=PROJ_ID, ref_date=REF_DATE, dir_to_save="../../datasets/raw"
    )
