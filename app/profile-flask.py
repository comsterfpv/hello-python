from main import app

app.config["PROFILE"] = True
app.config["DEBUG"] = True
app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.run(use_debugger = True)