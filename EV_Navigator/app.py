from flask import Flask, render_template, request, redirect, url_for
from graph_algo import battery_dijkstra
from map_generator import generate_map

app = Flask(__name__)

MAX_BATTERY_PERCENT = 100
MILEAGE_PER_PERCENT = 0.5

last_path_data = {"path": None, "distance": 0, "battery": 0}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        source = int(request.form["source"])
        destination = int(request.form["destination"])
        battery = int(request.form["battery"])

        path, total_distance, remaining_battery = battery_dijkstra(
            source, destination, battery, MILEAGE_PER_PERCENT, MAX_BATTERY_PERCENT
        )

        if path is None:
            return render_template("index.html", message="🚫 Cannot reach destination with current battery!", redirect_to_map=False)

        last_path_data["path"] = path
        last_path_data["distance"] = total_distance
        last_path_data["battery"] = remaining_battery

        generate_map(path)

        success_msg = f"✅ Path found! Total distance: {round(total_distance, 2)} km, Remaining battery: {round(remaining_battery, 2)}% : Please wait, Page is loading"
        return render_template("index.html", message=success_msg, redirect_to_map=True)

    return render_template("index.html")

@app.route("/map")
def show_map():
    if last_path_data["path"] is None:
        return redirect(url_for("index"))
    return render_template("map.html", distance=round(last_path_data["distance"], 2), battery=round(last_path_data["battery"], 2))

@app.route("/about")
def about():
    return render_template("about.html")

# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
