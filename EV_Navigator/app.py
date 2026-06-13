from flask import Flask, render_template, request, redirect, url_for

from graph_algo import find_ev_route
from map_generator import generate_map

app = Flask(__name__)

MAX_BATTERY_PERCENT = 100
MILEAGE_PER_PERCENT = 0.5

last_path_data = {
    "path": None,
    "distance": 0,
    "battery": 0,
    "status": "",
    "charging_station": None
}


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        try:

            source = int(request.form["source"])
            destination = int(request.form["destination"])
            battery = int(request.form["battery"])

            result = find_ev_route(
                source,
                destination,
                battery,
                MILEAGE_PER_PERCENT,
                MAX_BATTERY_PERCENT
            )

            # -------------------------
            # CASE 3
            # -------------------------
            if result["status"] == "NO_ROUTE":

                return render_template(
                    "index.html",
                    message="🚫 No feasible route found even through charging stations!",
                    redirect_to_map=False
                )

            # Save route information
            last_path_data["path"] = result["path"]
            last_path_data["distance"] = result["distance"]
            last_path_data["battery"] = result["battery"]
            last_path_data["status"] = result["status"]
            last_path_data["charging_station"] = result.get(
                "charging_station"
            )

            # Generate gmplot map
            generate_map(result["path"])

            # -------------------------
            # CASE 1
            # -------------------------
            if result["status"] == "DIRECT":

                success_msg = (
                    f"✅ Direct path found! "
                    f"Total Distance: {round(result['distance'], 2)} km | "
                    f"Remaining Battery: {round(result['battery'], 2)}% "
                    f"| Redirecting to map..."
                )

            # -------------------------
            # CASE 2
            # -------------------------
            else:

                success_msg = (
                    f"⚡ Charging Required at Station "
                    f"{result['charging_station']}! "
                    f"Total Distance: {round(result['distance'], 2)} km | "
                    f"Remaining Battery: {round(result['battery'], 2)}% "
                    f"| Redirecting to map..."
                )

            return render_template(
                "index.html",
                message=success_msg,
                redirect_to_map=True
            )

        except Exception as e:

            return render_template(
                "index.html",
                message=f"Error: {str(e)}",
                redirect_to_map=False
            )

    return render_template("index.html")


@app.route("/map")
def show_map():

    if last_path_data["path"] is None:
        return redirect(url_for("index"))

    return render_template(
        "map.html",
        distance=round(last_path_data["distance"], 2),
        battery=round(last_path_data["battery"], 2),
        status=last_path_data["status"],
        charging_station=last_path_data["charging_station"]
    )


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000,
        debug=True
    )