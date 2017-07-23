from flask import render_template
from flask_cors import cross_origin
from exts.graphs import setup as graphs


def setup(app):
    """
    Setup routes on app obj.
    :param app:
    :return:
    """
    @app.route('/')
    @app.route('/index')
    @app.route('/index/')
    @app.route('/index.html')
    @app.route('/index.html/')
    @cross_origin()
    def index():
        """

        :return:
        """

        return render_template(
            'index.html',
            title=app.title,
            section=app.__name__,
            navitems=[])

    @app.route('/home')
    @app.route('/home/')
    @app.route('/home.html')
    @app.route('/home.html/')
    @cross_origin()
    def home():
        """

        :return:
        """

        return render_template('default.html',
                               title=app.title,
                               html=f"""
                               Test
                               """
                               )

    @app.route('/routes')
    @app.route('/routes/')
    @cross_origin()
    def routes():
        """

        :return:
        """
        items = []
        views = sorted(set(list(app.view_functions)))
        for view in views:
            items.append(f'<div id="route_row_{view}" style="display:table-row; width: 1450px; padding-top:25px">')
            items.append(f'    <div id="route_row_{view}__name" style="display: table-cell; width: 1450px;">')
            items.append(f'        - {view}')
            items.append(f'    </div>')
            items.append(f'</div>')
        items_out = '\n'.join(items)
        return render_template(
            'default.html',
            html=f"""  {items_out}  """
        )

    @app.errorhandler(403)
    @cross_origin()
    def errors__403(error):
        """
        scripts/errors/403

        :return:
        """

        return render_template('errors/403.html', title=app.title), 403

    @app.errorhandler(404)
    @cross_origin()
    def errors__404(error):
        """
        scripts/errors/404

        :return:
        """

        return render_template('errors/404.html', title=app.title), 404

    @app.errorhandler(410)
    @cross_origin()
    def errors__410(error):
        """
        scripts/errors/410

        :return:
        """

        return render_template('errors/410.html', title=app.title), 410

    @app.errorhandler(500)
    @cross_origin()
    def errors__500(error):
        """
        scripts/errors/500

        :return:
        """

        return render_template('errors/500.html', title=app.title), 500

    app = graphs(app)

    return app
