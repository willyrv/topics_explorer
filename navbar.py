import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate


from app import app,view

def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Overview",href="/")),
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                id='topic-id',
                label="Topic",
                children=[
                    dbc.DropdownMenuItem(children="Topic "+ str(id),href='/topic') for id in range(view.model.number_topics)
                ]
             
            )
        ],
        brand="Topics explorer",
        brand_href="/",
        color="primary",
        dark=True
    )
    return navbar