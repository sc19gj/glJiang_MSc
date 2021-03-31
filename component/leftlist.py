# from main import ehr
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State, ALL


#layout of left list for UI
leftlist_index = dbc.ButtonGroup(
    [
        dbc.Button("Upload File", className="text-white border border-dark", href="/index", external_link=True),
        dbc.Button("Filtering", className="text-white border border-dark", href="/row1", external_link=True),
        dbc.Button("Comparison", className="text-white border border-dark", href="/row3", external_link=True),
        dbc.Button("WholeDataset", className="text-white border border-dark", href="/row4", external_link=True),
    ],
    vertical=True,
    className="mt-2",
    style={
        "width":"90%"
    }
)


#generate buttons on the left list
def leftlist():
    leftlist = dbc.Row(
        leftlist_index,
        id="leftlist",
        justify="center",
    )
    return leftlist
