from pathlib import Path

import basedosdados as bd
import pandas as pd
import streamlit as st


def load_data_chamados_for_subtype(
    project_id: str,
    id_subtype: str,
    dir_to_save: str = None,
    first_ref_date: str = "2022-01-01",
    sec_ref_date: str = "2022-02-01",
) -> pd.DataFrame:
    """
    Load the data from chamados_1746 from a specific id_subtype from a time range from first_ref_date and sec_ref_date.

    Args:
        project_id (str): name of the project on your account in GCP.
        id_subtype (str): it's the id_subtipo of the specific occurrence.
        dir_to_save (str, optional):  Path of the directory to save the dataset. If dosen't exist, create one. Defaults to None.
        first_ref_date (str, optional): Initial date of reference. Defaults to "2022-01-01".
        sec_ref_date (str, optional): End data of reference. Defaults to "2022-02-01".

    Returns:
        pd.DataFrame: A pandas dataframe with all data from specific subtype in a time range from first_ref_date and sec_ref_date.
    """
    if dir_to_save:
        path_to_save = Path(dir_to_save)
    else:
        path_to_save = dir_to_save
    query = f"""
    SELECT t1.*
    FROM `datario.administracao_servicos_publicos.chamado_1746` t1
    WHERE data_particao BETWEEN "{first_ref_date}" AND "{sec_ref_date}"
    AND t1.id_subtipo = "{id_subtype}"
    """
    df = pd.read_gbq(query=query, project_id=project_id,credentials=st.secrets["GCP_CREDENTIALS"],progress_bar_type="tqdm")

    # CONVERT DATE COLUMNS TO DATETIME

    date_cols = df.select_dtypes(include="dbdate")
    for col in date_cols.columns:
        df[col] = pd.to_datetime(date_cols[col], format="%Y-%m-%d")

    if path_to_save:
        if path_to_save.is_dir():
            df.to_parquet(
                f"{path_to_save}/dataset_chamado_1746_idsub-{id_subtype}_{first_ref_date}-{sec_ref_date}.parquet.gzip",
                compression="gzip",
            )
        else:
            path_to_save.mkdir(parents=True)
            df.to_parquet(
                f"{path_to_save}/dataset_chamado_1746_idsub-{id_subtype}_{first_ref_date}-{sec_ref_date}.parquet.gzip",
                compression="gzip",
            )

    else:
        return df


if __name__ == "__main__":
    PROJ_ID = st.secrets["ENV"]["project_id"]
    FIRST_REF_DATE = "2022-01-01"
    SEC_REF_DATE = "2023-12-01"
    load_data_chamados_for_subtype(
        project_id=PROJ_ID,
        id_subtype="5071",
        first_ref_date=FIRST_REF_DATE,
        sec_ref_date=SEC_REF_DATE,
        dir_to_save="../../datasets/raw",
    )
