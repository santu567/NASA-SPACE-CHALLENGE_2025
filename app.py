# app.py
import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import Draw
import json, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import shape, Point, Polygon

st.set_page_config(layout="wide", page_title="City Impact Prototype")

st.title("City Growth Impact — Prototype (Draw area and compare)")

col1, col2 = st.columns([2,1])

with col1:
    st.markdown("**Map** — draw a polygon (Draw tool) to select an area to evaluate.")
    m = folium.Map(location=[28.6139, 77.2090], zoom_start=12)  # default: New Delhi (changeable)
    draw = Draw(export=True)
    draw.add_to(m)
    st_map = st_folium(m, width=700, height=550)

# read geojson if user drew something
geojson = st_map.get("last_active_drawing") or st_map.get("all_drawings")
polygon_geom = None
if geojson:
    # st_folium returns the whole set; try to extract the last polygon
    try:
        if isinstance(geojson, dict) and "geometry" in geojson:
            polygon_geom = geojson["geometry"]
        elif isinstance(geojson, dict) and "features" in geojson:
            polygon_geom = geojson["features"][-1]["geometry"]
    except Exception:
        polygon_geom = None

with col2:
    st.markdown("## Controls & Output")
    st.write("Pick a city baseline (for demo we use simple default values).")
    city = st.selectbox("City (demo)", ["New Delhi", "San Francisco", "Nairobi", "Your city"], index=0)

    # baseline (mock) satellite-derived averages for a selected city
    baselines = {
        "New Delhi": {"NDVI": 0.25, "LST_C": 33.0, "AOD": 0.6},
        "San Francisco": {"NDVI": 0.35, "LST_C": 20.0, "AOD": 0.1},
        "Nairobi": {"NDVI": 0.45, "LST_C": 27.0, "AOD": 0.2},
        "Your city": {"NDVI": 0.30, "LST_C": 28.0, "AOD": 0.25},
    }
    base = baselines[city]

    st.markdown("### Selected area stats (mocked for demo)")
    if polygon_geom:
        st.success("Polygon detected ✅")
        # mock: area size by polygon bounding box (approx)
        poly = Polygon(polygon_geom["coordinates"][0])
        area_km2 = poly.area  # not geographic area; fine for demo
        st.write(f"Approx. area (map coordinates units): {area_km2:.4f}")

        # For prototype, compute the area's current average NDVI / LST by slightly varying baseline
        # We'll use centroid to create deterministic variation so different areas get different numbers
        c = poly.centroid
        seed = (c.x + c.y) % 1
        current_ndvi = max(0, min(1, base["NDVI"] + (seed - 0.5) * 0.2))
        current_lst = base["LST_C"] + (seed - 0.5) * 4
        current_aod = max(0, base["AOD"] + (seed - 0.5) * 0.2)

        st.write(f"Current NDVI (veg index): **{current_ndvi:.2f}**")
        st.write(f"Current Land Surface Temp (°C): **{current_lst:.1f}°C**")
        st.write(f"Current AOD (air particulates proxy): **{current_aod:.2f}**")
    else:
        st.info("Draw a polygon on the map to evaluate an area.")
        current_ndvi = base["NDVI"]
        current_lst = base["LST_C"]
        current_aod = base["AOD"]

    # scenario parameters (simple rule-based changes)
    st.markdown("---")
    st.markdown("### Scenario presets (simple rules)")
    st.write("Scenario effects are *rules* you can show to judges to be transparent.")
    st.write("Examples (editable):")
    develop_ndvi_delta = st.number_input("Develop: ΔNDVI (e.g. -0.30)", value=-0.30, step=0.05)
    develop_lst_delta = st.number_input("Develop: ΔLST (°C, e.g. +3.0)", value=3.0, step=0.5)
    develop_aod_delta = st.number_input("Develop: ΔAOD (e.g. +0.10)", value=0.10, step=0.05)

    park_ndvi_delta = st.number_input("Park: ΔNDVI (e.g. +0.25)", value=0.25, step=0.05)
    park_lst_delta = st.number_input("Park: ΔLST (°C, e.g. -2.0)", value=-2.0, step=0.5)
    park_aod_delta = st.number_input("Park: ΔAOD (e.g. -0.05)", value=-0.05, step=0.01)

    # simple impact score — lower is better (0..100)
    def compute_score(ndvi, lst, aod):
        # normalize metrics to 0..1 using plausible ranges
        ndvi_norm = 1 - (ndvi)  # higher NDVI is better so invert
        lst_norm = (lst - 10) / 40.0  # assume 10-50°C range
        aod_norm = aod / 2.0  # assume 0-2 range
        # weights
        w_ndvi, w_lst, w_aod = 0.4, 0.4, 0.2
        raw = w_ndvi * ndvi_norm + w_lst * lst_norm + w_aod * aod_norm
        score = max(0, min(100, raw * 100))
        return score

    # compute scenario results if polygon exists
    if polygon_geom:
        dev_ndvi = current_ndvi + develop_ndvi_delta
        dev_lst = current_lst + develop_lst_delta
        dev_aod = current_aod + develop_aod_delta

        park_ndvi = current_ndvi + park_ndvi_delta
        park_lst = current_lst + park_lst_delta
        park_aod = current_aod + park_aod_delta

        dev_score = compute_score(dev_ndvi, dev_lst, dev_aod)
        park_score = compute_score(park_ndvi, park_lst, park_aod)
    else:
        dev_ndvi = park_ndvi = current_ndvi
        dev_lst = park_lst = current_lst
        dev_aod = park_aod = current_aod
        dev_score = park_score = compute_score(current_ndvi, current_lst, current_aod)

    st.markdown("---")
    st.subheader("Impact Score (lower is better)")
    st.metric("Develop scenario score", f"{dev_score:.1f}")
    st.metric("Park scenario score", f"{park_score:.1f}")

    # show numeric deltas
    df = pd.DataFrame({
        "metric": ["NDVI", "LST (°C)", "AOD"],
        "current": [current_ndvi, current_lst, current_aod],
        "develop": [dev_ndvi, dev_lst, dev_aod],
        "park": [park_ndvi, park_lst, park_aod]
    })
    st.table(df.set_index("metric"))

    # small bar chart comparing scores
    fig, ax = plt.subplots()
    ax.bar(["Develop","Park"], [dev_score, park_score])
    ax.set_ylabel("Impact score (lower better)")
    st.pyplot(fig)

    # export GeoJSON button
    if polygon_geom:
        export_geojson = {
            "type": "Feature",
            "properties": {
                "city": city,
                "current_ndvi": round(current_ndvi,3),
                "current_lst": round(current_lst,2),
                "develop_score": round(dev_score,1),
                "park_score": round(park_score,1)
            },
            "geometry": polygon_geom
        }
        if st.button("Export GeoJSON of selection"):
            st.download_button("Download GeoJSON", json.dumps(export_geojson), file_name="selection.geojson", mime="application/json")

st.markdown("---")
st.caption("Prototype uses simple, transparent rules. Replace rule-based numbers with GEE or NASA data for a production-ready tool.")
