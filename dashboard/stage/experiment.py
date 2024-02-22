import streamlit as st

from dashboard.types import *

import networkx as nx
import plotly.graph_objects as go
from streamlit_echarts import st_echarts, JsCode

import random

class Experimental(Stage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def activate(self) -> None:
        # Create a Streamlit app
        st.title('Person and Mental Features Graph')

        # Create an empty graph
        G = nx.Graph()

        # Add central node (person's name)
        G.add_node("John Doe", level=0)

        # Define mental features
        features = [
            {"name": "Intelligence", "level": 1},
            {"name": "Creativity", "level": 1},
            {"name": "Empathy", "level": 1},
            {"name": "Resilience", "level": 1},
            {"name": "Curiosity", "level": 1},
            {"name": "Optimism", "level": 1},
            {"name": "Adaptability", "level": 1}
        ]

        # Add mental feature nodes and edges
        for feature in features:
            G.add_node(feature["name"], level=feature["level"])
            G.add_edge("John Doe", feature["name"])

        # Create node positions using a layout algorithm
        pos = nx.spring_layout(G)

        # Create edge positions
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        # Create node trace
        node_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=False,
                colorscale='YlGnBu',
                reversescale=True,
                color=[],
                size=20,
                colorbar=dict(
                    thickness=15,
                    title='Feature Level',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2))

        # Populate node trace
        for node in G.nodes():
            x, y = pos[node]
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])
            node_trace['text'] += tuple([node])
            node_trace['marker']['color'] += tuple([G.nodes[node]['level']])

        # Create edge trace
        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=1, color='lightblue'),
            hoverinfo='none',
            mode='lines')

        # Create figure
        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title='Person and Mental Features',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

        # Display the graph using Streamlit
        st.plotly_chart(fig)

        st.divider()

        options = {
            "title": {
                "text": "Depression Level",
                "subtext": "From ExcelHome",
                "sublink": "http://e.weibo.com/1341556070/Aj1J2x5a5",
            },
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"},
                "formatter": JsCode(
                    "function(params){var tar;if(params[1].value!=='-'){tar=params[1]}else{tar=params[0]}return tar.name+'<br/>'+tar.seriesName+' : '+tar.value}"
                ).js_code,
            },
            "legend": {"data": ["Normal", "Depression"]},
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            "xAxis": {
                "type": "category",
                "splitLine": {"show": False},
                "data": [f"Day {i}" for i in range(1, 12)],
            },
            "yAxis": {"type": "value"},
            "series": [
                {
                    "name": "Auxiliary",
                    "type": "bar",
                    "stack": "Total",
                    "itemStyle": {
                        "barBorderColor": "rgba(0,0,0,0)",
                        "color": "rgba(0,0,0,0)",
                    },
                    "emphasis": {
                        "itemStyle": {
                            "barBorderColor": "rgba(0,0,0,0)",
                            "color": "rgba(0,0,0,0)",
                        }
                    },
                    "data": [0, 900, 1245, 1530, 1376, 1376, 1511, 1689, 1856, 1495, 1292],
                },
                {
                    "name": "Depression",
                    "type": "bar",
                    "stack": "Total",
                    "label": {"show": True, "position": "top"},
                    "data": [900, 345, 393, "-", "-", 135, 178, 286, "-", "-", "-"],
                },
                {
                    "name": "Normal",
                    "type": "bar",
                    "stack": "Total",
                    "label": {"show": True, "position": "bottom"},
                    "data": ["-", "-", "-", 108, 154, "-", "-", "-", 119, 361, 203],
                },
            ],
        }

        st_echarts(options=options, height="500px")

        st.divider()

        option = {
            "title": {"text": "Personality Aspects Radar Chart"},
            "legend": {"data": ["Saleh", "Pouya"]},
            "backgroundColor": "rgba(0, 0, 0, 0)",  # Translucent background
            "radar": {
                "indicator": [
                    {"name": "Intelligence", "max": 100},
                    {"name": "Creativity", "max": 100},
                    {"name": "Empathy", "max": 100},
                    {"name": "Resilience", "max": 100},
                    {"name": "Curiosity", "max": 100},
                    {"name": "Optimism", "max": 100},
                    {"name": "Adaptability", "max": 100},
                ],
                "shape": "circle",  # Shape of the radar chart
                "splitArea": {"areaStyle": {"color": ["rgba(255, 255, 255, 0)", "rgba(255, 255, 255, 0)"]}},
                # Translucent split area
                "splitLine": {"lineStyle": {"color": "rgba(255, 255, 255, 0.5)"}},  # Translucent split line
            },
            "series": [
                {
                    "name": "Personality Aspects",
                    "type": "radar",
                    "data": [
                        {
                            "value": [80, 70, 90, 75, 85, 80, 95],
                            "name": "Saleh",
                        },
                        {
                            "value": [90, 85, 80, 70, 90, 75, 80],
                            "name": "Pouya",
                        },
                    ],
                }
            ],
        }
        st_echarts(option, height="500px")

        st.divider()

        person_name = "John Doe"

        person_aspect = {"name": person_name, "symbolSize": 20, "category": 0}

        person_aspects = [
            person_aspect,
            {"name": "Intelligence", "symbolSize": 10, "category": 1, "value": 80},
            {"name": "Creativity", "symbolSize": 10, "category": 1, "value": 75},
            {"name": "Empathy", "symbolSize": 10, "category": 1, "value": 90},
            {"name": "Resilience", "symbolSize": 10, "category": 1, "value": 85},
            {"name": "Curiosity", "symbolSize": 10, "category": 1, "value": 80},
            {"name": "Optimism", "symbolSize": 10, "category": 1, "value": 70},
            {"name": "Adaptability", "symbolSize": 10, "category": 1, "value": 95},
        ]

        links = [
            {"source": person_name, "target": aspect["name"]} for aspect in person_aspects[1:]
        ]

        categories = [
            {"name": "Person", "symbol": "circle"},
            {"name": "Aspect", "symbol": "circle"},
        ]

        option = {
            "title": {
                "text": f"Personality Aspects of {person_name}",
                "subtext": "Default layout",
                "top": "bottom",
                "left": "right",
            },
            "tooltip": {},
            "legend": [{"data": [category["name"] for category in categories]}],
            "series": [
                {
                    "name": "Personality",
                    "type": "graph",
                    "layout": "force",
                    "data": person_aspects,
                    "links": links,
                    "categories": categories,
                    "roam": True,
                    "label": {
                        "position": "right",
                        "formatter": "{b}: {c}",  # Display the aspect name and value
                    },
                    "draggable": True,
                    "force": {"repulsion": 100},
                }
            ],
        }

        st_echarts(option, height="500px")

        st.divider()

        persons = [
            {
                "name": "John Doe",
                "aspects": [
                    {"name": "Intelligence", "value": 80},
                    {"name": "Creativity", "value": 75},
                    {"name": "Empathy", "value": 90},
                    {"name": "Resilience", "value": 85},
                    {"name": "Curiosity", "value": 80},
                    {"name": "Optimism", "value": 70},
                    {"name": "Adaptability", "value": 95},
                ],
            },
            {
                "name": "Pouya",
                "aspects": [
                    {"name": "Intelligence", "value": 70},
                    {"name": "Creativity", "value": 85},
                    {"name": "Empathy", "value": 75},
                    {"name": "Resilience", "value": 80},
                    {"name": "Curiosity", "value": 90},
                    {"name": "Optimism", "value": 85},
                    {"name": "Adaptability", "value": 80},
                ],
            },
            {
                "name": "Saleh",
                "aspects": [
                    {"name": "Intelligence", "value": 85},
                    {"name": "Creativity", "value": 85},
                    {"name": "Empathy", "value": 95},
                    {"name": "Resilience", "value": 80},
                    {"name": "Curiosity", "value": 69},
                    {"name": "Optimism", "value": 78},
                    {"name": "Adaptability", "value": 80},
                ],
            },
        ]

        data = {
            "name": "Users",
            "children": [],
        }

        for person in persons:
            person_aspect = {"name": person["name"], "value": 100, "children": person["aspects"]}
            data["children"].append(person_aspect)

        # Assign values to each node
        def assign_values(node):
            if "value" not in node:
                node["value"] = 0
            for child in node.get("children", []):
                assign_values(child)

        assign_values(data)

        option = {
            "tooltip": {"trigger": "item", "triggerOn": "mousemove"},
            "series": [
                {
                    "type": "tree",
                    "data": [data],
                    "top": "1%",
                    "left": "7%",
                    "bottom": "1%",
                    "right": "20%",
                    "symbolSize": 7,
                    "label": {
                        "position": "left",
                        "verticalAlign": "middle",
                        "align": "right",
                        "fontSize": 9,
                    },
                    "leaves": {
                        "label": {
                            "position": "right",
                            "verticalAlign": "middle",
                            "align": "left",
                        }
                    },
                    "emphasis": {"focus": "descendant"},
                    "expandAndCollapse": True,
                    "animationDuration": 550,
                    "animationDurationUpdate": 750,
                }
            ],
        }

        st_echarts(option, height="500px")

        st.divider()

        schema = [
            {"name": "date", "index": 0, "text": "start point"},
            {"name": "Intelligence", "index": 1, "text": "智力"},
            {"name": "Creativity", "index": 2, "text": "创造力"},
            {"name": "Empathy", "index": 3, "text": "移情能力"},
            {"name": "Resilience", "index": 4, "text": "韧性"},
            {"name": "Curiosity", "index": 5, "text": "好奇心"},
            {"name": "Optimism", "index": 6, "text": "乐观主义"},
            {"name": "Adaptability", "index": 7, "text": "适应能力"},
        ]

        dataPerson1 = [
            [1, 80, 75, 90, 85, 80, 70, 95],
            [2, 75, 85, 75, 80, 90, 85, 80],
            [3, 1, 12, 8, 32, 11, 7, 2],
            # Add more data points for Person 1
        ]

        dataPerson2 = [
            [1, 5, 80, 7, 80, 11, 70, 90],
            [2, 8, 55, 8, 95, 78, 16, 29],
            [3, 7, 80, 15, 10, 85, 80, 87],
            # Add more data points for Person 2
        ]

        dataPerson3 = [
            [1, 70, 75, 80, 85, 80, 75, 80],
            [2, 75, 80, 85, 80, 75, 80, 85],
            [3, 80, 85, 90, 85, 80, 85, 80],
            # Add more data points for Person 3
        ]

        lineStyle = {"normal": {"width": 1, "opacity": 0.5}}
        option = {
            "backgroundColor": "#333",
            "legend": {
                "bottom": 30,
                "data": ["Person 1", "Person 2", "Person 3"],
                "itemGap": 20,
                "textStyle": {"color": "#fff", "fontSize": 14},
            },
            "tooltip": {
                "padding": 10,
                "backgroundColor": "#222",
                "borderColor": "#777",
                "borderWidth": 1,
            },
            "parallelAxis": [
                {
                    "dim": 0,
                    "name": schema[0]["text"],
                    "inverse": True,
                    "max": 3,
                    "nameLocation": "start",
                },
                {"dim": 1, "name": schema[1]["name"]},
                {"dim": 2, "name": schema[2]["name"]},
                {"dim": 3, "name": schema[3]["name"]},
                {"dim": 4, "name": schema[4]["name"]},
                {"dim": 5, "name": schema[5]["name"]},
                {"dim": 6, "name": schema[6]["name"]},
                {"dim": 7, "name": schema[7]["name"]},
            ],
            "visualMap": {
                "show": True,
                "min": 0,
                "max": 100,
                "dimension": 2,
                "inRange": {"color": ["#50a3ba", "#eac736", "#d94e5d"], },
            },
            "parallel": {
                "left": "5%",
                "right": "18%",
                "bottom": 100,
                "parallelAxisDefault": {
                    "type": "value",
                    "nameLocation": "end",
                    "nameGap": 20,
                    "nameTextStyle": {"color": "#fff", "fontSize": 12},
                    "axisLine": {"lineStyle": {"color": "#aaa"}},
                    "axisTick": {"lineStyle": {"color": "#777"}},
                    "splitLine": {"show": False},
                    "axisLabel": {"color": "#fff"},
                },
            },
            "series": [
                {"name": "John", "type": "parallel", "lineStyle": lineStyle, "data": dataPerson1},
                {"name": "Pouya", "type": "parallel", "lineStyle": lineStyle, "data": dataPerson2},
                {"name": "Saleh", "type": "parallel", "lineStyle": lineStyle, "data": dataPerson3},
            ],
        }

        st_echarts(option, height="500px")

        st.divider()

        option = {
            "title": {"text": "Personality Funnel", "subtext": "Data Visualization"},
            "tooltip": {"trigger": "item", "formatter": "{a} <br/>{b} : {c}%"},
            "toolbox": {
                "feature": {
                    "dataView": {"readOnly": False},
                    "restore": {},
                    "saveAsImage": {},
                }
            },
            "legend": {"data": ["Intelligence", "Creativity", "Empathy", "Resilience", "Curiosity"]},
            "series": [
                {
                    "name": "Expected",
                    "type": "funnel",
                    "left": "10%",
                    "width": "80%",
                    "label": {"formatter": "{b} (Expected)"},
                    "labelLine": {"show": False},
                    "itemStyle": {"opacity": 0.7},
                    "emphasis": {
                        "label": {"position": "inside", "formatter": "{b} (Expected): {c}%"}
                    },
                    "data": [
                        {"value": 60, "name": "Intelligence"},
                        {"value": 40, "name": "Creativity"},
                        {"value": 20, "name": "Empathy"},
                        {"value": 80, "name": "Resilience"},
                        {"value": 100, "name": "Curiosity"},
                    ],
                },
                {
                    "name": "Actual",
                    "type": "funnel",
                    "left": "10%",
                    "width": "80%",
                    "maxSize": "80%",
                    "label": {"position": "inside", "formatter": "{c}%", "color": "#fff"},
                    "itemStyle": {"opacity": 0.5, "borderColor": "#fff", "borderWidth": 2},
                    "emphasis": {
                        "label": {"position": "inside", "formatter": "{b} (Actual): {c}%"}
                    },
                    "data": [
                        {"value": 30, "name": "Intelligence"},
                        {"value": 10, "name": "Creativity"},
                        {"value": 5, "name": "Empathy"},
                        {"value": 50, "name": "Resilience"},
                        {"value": 80, "name": "Curiosity"},
                    ],
                    "z": 100,
                },
            ],
        }
        st_echarts(option, height="500px")

        st.divider()

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
                    "axisLine": {"lineStyle": {"width": 40}},
                    "splitLine": {"show": False, "distance": 0, "length": 10},
                    "axisTick": {"show": False},
                    "axisLabel": {"show": False, "distance": 50},
                    "data": [
                        {
                            "value": random.randint(1, 99),
                            "name": "Intelligence",
                            "title": {"offsetCenter": ["0%", "-30%"]},
                            "detail": {"offsetCenter": ["0%", "-20%"]},
                        },
                        {
                            "value": random.randint(1, 99),
                            "name": "Creativity",
                            "title": {"offsetCenter": ["0%", "0%"]},
                            "detail": {"offsetCenter": ["0%", "10%"]},
                        },
                        {
                            "value": random.randint(1, 99),
                            "name": "Empathy",
                            "title": {"offsetCenter": ["0%", "30%"]},
                            "detail": {"offsetCenter": ["0%", "40%"]},
                        },
                    ],
                    "title": {"fontSize": 14},
                    "detail": {
                        "width": 50,
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

        st_echarts(option, height="500px", key="echarts")

        st.divider()

        data = [
            {"name": "awesome", "value": 100},
            {"name": "cool", "value": 90},
            {"name": "amazing", "value": 80},
            {"name": "fun", "value": 70},
            {"name": "fantastic", "value": 60},
            {"name": "great", "value": 50},
            {"name": "nice", "value": 40},
            {"name": "sweet", "value": 30},
            {"name": "excellent", "value": 20},
            {"name": "wonderful", "value": 10},
            {"name": "awesome", "value": 5},
            {"name": "lovely", "value": 3},
            {"name": "good", "value": 2},
            {"name": "toxic", "value": 1},
            {"name": "hate", "value": 1},
            {"name": "disgusting", "value": 1},
            {"name": "mean", "value": 1},
            {"name": "rude", "value": 1},
            {"name": "nasty", "value": 1},
            {"name": "awful", "value": 1},
            {"name": "horrible", "value": 1},
            {"name": "terrible", "value": 1},
            {"name": "bad", "value": 1},
            {"name": "negative", "value": 1},
            {"name": "toxicity", "value": 1},
            {"name": "offensive", "value": 1},
            {"name": "abusive", "value": 1},
            {"name": "vulgar", "value": 1},
            {"name": "insulting", "value": 1},
            {"name": "obnoxious", "value": 1},
            {"name": "harmful", "value": 1},
            {"name": "hateful", "value": 1},
            {"name": "cruel", "value": 1},
            {"name": "mean-spirited", "value": 1},
            {"name": "toxic behavior", "value": 1},
            {"name": "toxic comments", "value": 1},
            {"name": "toxic culture", "value": 1},
            {"name": "toxic environment", "value": 1},
            {"name": "toxic relationship", "value": 1},
            {"name": "toxic people", "value": 1},
            {"name": "toxicity", "value": 1},
            {"name": "toxic community", "value": 1},
            {"name": "toxic language", "value": 1},
            {"name": "toxic mindset", "value": 1},
            {"name": "toxic influence", "value": 1},
            {"name": "toxic atmosphere", "value": 1},
            {"name": "toxic interactions", "value": 1},
            {"name": "toxic behavior", "value": 1},
            {"name": "toxicity", "value": 1},
            {"name": "toxic people", "value": 1},
            {"name": "toxicity", "value": 1},
            {"name": "toxic environment", "value": 1},
            {"name": "toxic culture", "value": 1},
            {"name": "toxic comments", "value": 1},
            {"name": "toxic relationship", "value": 1},
            {"name": "toxic language", "value": 1},
            {"name": "toxicity", "value": 1},
            {"name": "toxic community", "value": 1},
            {"name": "toxic mindset", "value": 1},
            {"name": "toxic influence", "value": 1},
            {"name": "toxic atmosphere", "value": 1},
            {"name": "toxic interactions", "value": 1},
            {"name": "toxic behavior", "value": 1},
            {"name": "toxicity", "value": 1},
            {"name": "toxic people", "value": 1},
            {"name": "toxicity", "value": 1},
            {"name": "toxic environment", "value": 1},
            {"name": "toxic culture", "value": 1},
            {"name": "toxic comments", "value": 1},
            {"name": "shit", "value": 6}
        ]

        wordcloud_option = {"series": [{"type": "wordCloud", "data": data}]}
        st_echarts(wordcloud_option)

        st.divider()

    def dump(self):
        pass

    def __call__(self, *args, **kwargs):
        pass