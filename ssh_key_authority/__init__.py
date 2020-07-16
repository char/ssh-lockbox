from quart import Quart, render_template

app = Quart(__name__, static_folder="../static/", template_folder="../templates/")


@app.route("/")
async def index_page():
    return await render_template("index.html.j2")


@app.route("/login", methods=["POST"])
async def log_in():
    # TODO: Sign in a user by username and password, and set a session cookie.
    # Always redirect to the main page; if login fails, we can show a flash to the user.
    pass


@app.route("/create", methods=["POST"])
async def create_key_entry():
    # TODO: Parse the request form and create a key entry for the authenticated user.
    # Authentication should be possible via Bearer token or session cookies.
    pass


@app.route("/keys/<user>")
async def fetch_keys(user):
    # TODO: Return a text/plain response containing this user's SSH keys.
    # If a valid authentication token is provided, include the SSH keys' comment fields.
    pass
