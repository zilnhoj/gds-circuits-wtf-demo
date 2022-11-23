from flask import Flask
from flask_compress import Compress
from flask_talisman import Talisman
from jinja2 import ChoiceLoader, PackageLoader, PrefixLoader

app = Flask(__name__, static_url_path="/assets")

app.jinja_loader = ChoiceLoader(
    [
        PackageLoader("app"),
        PrefixLoader({"govuk_frontend_jinja": PackageLoader("govuk_frontend_jinja")}),
    ]
)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

csp = {
        "default-src": "'self'",
        "style-src": ["'self'",
                      "'unsafe-inline'",
                      'https://cdn.bokeh.org/bokeh/release/bokeh-2.4.3.min.js',
                      ],
        "script-src": [
                    "'self'",
                    "'unsafe-inline'",
                    'https://cdn.bokeh.org/bokeh/release/bokeh-tables-2.4.3.min.js',
                     ],
        'img-src': ['*', 'self', 'data: https:']
    }

Compress(app)
Talisman(app, content_security_policy=csp)

from app import routes  # noqa: E402, F401
# from app.src.set_circuits import
