from launcher.launcher import Launcher

launcher = Launcher()

while True:

    app = input("\nOpen : ")

    if app == "exit":
        break

    if launcher.launch(app):

        print("Opened successfully.")

    else:

        print("Application not found.")