import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

st.title("Lissajous Figure Explorer")

# --- UI controls ---
fx = st.slider("Frequency fx", 0.1, 5.0, 1.0, 0.1)
fy = st.slider("Frequency fy", 0.1, 5.0, 2.0, 0.1)

phix = st.slider("Phase φx (rad)", 0.0, 2 * np.pi, 0.0, 0.1)
phiy = st.slider("Phase φy (rad)", 0.0, 2 * np.pi, 0.0, 0.1)

# --- Cached time grid ---
@st.cache_data
def make_t():
    return np.linspace(0, 2 * np.pi, 2000)

t = make_t()

# --- Session state ---
if "animate" not in st.session_state:
    st.session_state.animate = False

# --- Buttons ---
col1, col2 = st.columns(2)

with col1:
    if st.button("Animate frequency sweep"):
        st.session_state.animate = True

with col2:
    if st.button("Stop"):
        st.session_state.animate = False

# --- Plot placeholder ---
placeholder = st.empty()

# --- Figure builder ---
def make_figure(x, y, title):
    fig = go.Figure(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            line=dict(width=2)
        )
    )
    fig.update_layout(
        title=title,
        xaxis_title="x(t)",
        yaxis_title="y(t)",
        template="plotly_white",
        hovermode=False
    )
    fig.update_xaxes(
        scaleanchor="y",
        scaleratio=1,
        showgrid=True,
        range=[-1.1, 1.1]
    )
    fig.update_yaxes(
        showgrid=True,
        range=[-1.1, 1.1]
    )
    return fig

# --- Static plot ---
def plot_static(fx, fy, phix, phiy):
    x = np.sin(fx * t + phix)
    y = np.sin(fy * t + phiy)
    fig = make_figure(
        x, y,
        f"Lissajous: fx={fx:.2f}, fy={fy:.2f}, φx={phix:.2f}, φy={phiy:.2f}"
    )
    placeholder.plotly_chart(fig, use_container_width=True)

# --- Animation ---
def animate():
    for f in np.linspace(0.5, 5.0, 80):
        if not st.session_state.animate:
            break

        x = np.sin(f * t + phix)
        y = np.sin((f + 1) * t + phiy)

        fig = make_figure(
            x, y,
            f"Lissajous sweep: fx={f:.2f}, fy={f+1:.2f}"
        )
        placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.06)

# --- Main logic ---
if st.session_state.animate:
    animate()
else:
    plot_static(fx, fy, phix, phiy)
