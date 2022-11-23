import pandas as pd
from set-circuits import get_circuit
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import Range1d, ColumnDataSource, DataTable, DateFormatter, TableColumn


def circuit_table():
    df = get_circuit
    circuits_src = ColumnDataSource(df)
    columns = [
        TableColumn(field="Circuit", title="Circuit"),
        TableColumn(field="Work", title="Work"),
        TableColumn(field="Rest", title="Rest")
    ]
    circuits_dt = DataTable(source=circuits_src, columns=columns, width=400, height=280)
    script, div = components(circuits_dt)

    return scritp, div


