import pandas as pd
import basedosdados as bd
from datetime import datetime
from pathlib import Path

def load_data_chamados_with_geolocation(project_id: str,dir_to_save: str = None,ref_date: str="2024-02-01") -> pd.DataFrame:
    path_to_save = Path(dir_to_save)
    query = f"""
      SELECT t1.*,
       t2.nome as nome_bairro,
       t2.subprefeitura as subprefeitura_bairro,
       t2.area as area_bairro,
       t2.perimetro as perimetro_bairro,
       t2.geometry as geometry_bairro
    FROM `datario.administracao_servicos_publicos.chamado_1746` t1
    LEFT JOIN `datario.dados_mestres.bairro` t2
    ON t1.id_bairro = t2.id_bairro
    WHERE data_particao='{ref_date}'
    """
    df = bd.read_sql(query,billing_project_id=project_id)

    # CONVERT DATE COLUMNS TO DATETIME

    date_cols = df.select_dtypes(include="dbdate")
    for col in date_cols.columns:
        df[col] = pd.to_datetime(date_cols[col],format="%Y-%m-%d")

    if path_to_save:
        if path_to_save.is_dir():
            df.to_parquet(f"{path_to_save}/dataset_chamado_1746_with_geoloc_{ref_date}.parquet.gzip",compression="gzip")
        else:
            path_to_save.mkdir(parents=True)
            df.to_parquet(f"{path_to_save}/dataset_chamado_1746_with_geoloc_{ref_date}.parquet.gzip",compression="gzip")
    
    else:
        return df

if __name__ == "__main__":
    PROJ_ID = "teste-cientista-dados-jr-rj"
    REF_DATE = "2023-04-01"
    load_data_chamados_with_geolocation(project_id=PROJ_ID,
                                        ref_date=REF_DATE,
                                        dir_to_save="../../datasets/raw")
    