import streamlit as st
import altair as alt


def raw_table(df):
    """"""
    st.table(df)


def bar_chart(df):
    """"""
    df.reset_index(inplace=True)
    c = alt.Chart(df[:1000]).mark_bar().encode(
        x='1', 
        y=alt.Y(
            'index', sort=alt.EncodingSortField(field="1", order='descending')
        )
    )
    st.altair_chart(c, use_container_width=True)