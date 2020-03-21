import pandas as pd
import os
import re

url = "https://pt.wikipedia.org/wiki/Lista_de_concelhos_por_NUTS,_distritos_e_ilhas"


def clear_brackets(name: str) -> str:
    """ Clears brackets for example [2] from the provided string """
    return re.sub(r"\[.*\]", "", name)


locations = pd.read_html(url)
pt_continental_df = locations[1][["Distrito", "Concelhos"]].applymap(clear_brackets)
acores_df = locations[2][["Ilha", "Concelhos"]].applymap(clear_brackets)
madeira_df = locations[3][["Ilha", "Concelhos"]].applymap(clear_brackets)

acores_df.columns = pt_continental_df.columns
madeira_df.columns = pt_continental_df.columns

output_path = "data"
pt_continental_df.to_csv(os.path.join(output_path, "pt.csv"), index=False)
acores_df.to_csv(os.path.join(output_path, "acores.csv"), index=False)
madeira_df.to_csv(os.path.join(output_path, "madeira.csv"), index=False)
