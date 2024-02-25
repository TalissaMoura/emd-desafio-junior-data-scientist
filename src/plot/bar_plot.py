from typing import Any, Dict, Optional

import altair as alt
import matplotlib.pyplot as plt
import pandas as pd


def bar_plot(
    dataframe: pd.DataFrame,
    x: Optional[str | alt.X],
    y: Optional[str | alt.Y],
    encode_kw: Optional[None | Dict[str, Any]] = None,
    mark_bar_kw: Optional[Dict[str, Any] | None] = None,
    config_xaxis: Optional[None | Dict[str, Any]] = None,
    config_yaxis: Optional[None | Dict[str, Any]] = None,
):

    if encode_kw:
        base_bar = alt.Chart(dataframe).encode(x=x, y=y, **encode_kw)
    else:
        base_bar = alt.Chart(dataframe).encode(
            x=x,
            y=y,
        )

    if config_xaxis:
        base_bar = base_bar.configure_axisX(**config_xaxis)
    elif config_yaxis:
        base_bar = base_bar.configure_axisY(**config_yaxis)

    if mark_bar_kw:
        return base_bar.mark_bar(**mark_bar_kw)
    else:
        return base_bar.mark_bar()
