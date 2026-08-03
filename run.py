from app import create_app

app = create_app()

if __name__ == "__main__":

    print("\n=== ROUTES ===")

    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint:30} -> {rule}")

    app.run(debug=True)