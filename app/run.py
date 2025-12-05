from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)


# for use in unit testing or running actual db