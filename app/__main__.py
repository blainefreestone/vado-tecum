from app.app import App
import yaml

config = yaml.safe_load(open("config.yaml"))

if __name__ == "__main__":
    if App.load("app.pickle"):
        app = App.load(config["app_save_path"])
    else:
        app = App()
        app.add_text_files(config['texts_path'])

    app.run()

    app.save(config["app_save_path"])