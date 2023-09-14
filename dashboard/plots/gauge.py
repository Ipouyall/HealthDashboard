from streamlit_echarts import st_echarts, JsCode
from dashboard.model.mood import MoodModel
import streamlit as st


def emotion_gauge(text, model: MoodModel, ph):
    vs = model.predict(text)

    option = {
        "series": [
            {
                "type": "gauge",
                "startAngle": 90,
                "endAngle": -270,
                "pointer": {"show": False},
                "progress": {
                    "show": True,
                    "overlap": False,
                    "roundCap": True,
                    "clip": False,
                    "itemStyle": {"borderWidth": 1, "borderColor": "#464646"},
                },
                "axisLine": {"lineStyle": {"width": 15}},
                "splitLine": {"show": False, "distance": 0, "length": 10},
                "axisTick": {"show": False},
                "axisLabel": {"show": False, "distance": 50},
                "data": [
                    {
                        "value": round(vs.angry, 2),
                        "name": "Anger",
                        "title": {"offsetCenter": ["0%", "-55%"]},
                        "detail": {"offsetCenter": ["0%", "-35%"]},
                    },
                    {
                        "value": round(vs.happy, 2),
                        "name": "Happiness",
                        "title": {"offsetCenter": ["0%", "-15%"]},
                        "detail": {"offsetCenter": ["0%", "5%"]},
                    },
                    {
                        "value": round(vs.sad, 2),
                        "name": "Sadness",
                        "title": {"offsetCenter": ["0%", "25%"]},
                        "detail": {"offsetCenter": ["0%", "45%"]},
                    },
                ],
                "title": {"fontSize": 14},
                "detail": {
                    "width": 40,
                    "height": 14,
                    "fontSize": 14,
                    "color": "auto",
                    "borderColor": "auto",
                    "borderRadius": 20,
                    "borderWidth": 1,
                    "formatter": "{value}%",
                },
            }
        ]
    }

    with ph:
        st.markdown("<div style='text-align: center;'>Emotions Aggregated</div>", unsafe_allow_html=True)
        st_echarts(option, height="300px", key="echarts")
