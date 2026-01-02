from typing import Any
from flask import render_template, current_app

"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views on create_app Flask factory::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""

"""
    Application wide 404 error handler
"""


@current_app.errorhandler(404)
def page_not_found(e: Any) -> tuple[str, int]:
    return (
        render_template(
            "404.html",
            base_template=current_app.appbuilder.base_template,
            appbuilder=current_app.appbuilder,
        ),
        404,
    )
