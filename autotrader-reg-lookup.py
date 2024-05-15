import streamlit as st
import pandas as pd
import numpy as np
from urllib.error import URLError
import pyodbc

#@st.cache_data
def get_autotrader_data(n=1000):
    cnxn = pyodbc.connect("Driver=SQL Server;Server=MP-SQL;Database=AutoTrader;UID=" + st.secrets["DB_USERNAME"] + ";PWD=" + st.secrets["DB_PASSWORD"])
    sql = "select top " + str(n) + " * from [AutoTrader].[dbo].[Vehicles] (nolock) aut"
    df = pd.read_sql(sql,cnxn)
    return df.set_index("Registration")
    
    
try:
    df_at = get_autotrader_data(10000)
    makes = st.selectbox(
        "Choose registration", list(df_at.index)
    )
    if not makes:
        st.error("Please select at least one reg.")
    else:
        data_at = df_at.loc[makes]
        st.write("### Autotrader Registration")
        st.dataframe(data_at.sort_index(), use_container_width=True)

except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )
