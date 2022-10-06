import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode


########################################################################################################################
######################################### INTERACTIVE TABLE ############################################################
def interactive_table():
    query_df = pd.read_csv(st.session_state['uploaded_file'] )
    st.header("📊 Explore")
    def aggrid_interactive_table(df: pd.DataFrame):
        """Creates an st-aggrid interactive table based on a dataframe.
        Args:
            df (pd.DataFrame]): Source dataframe
        Returns:
            dict: The selected row
        """
        options = GridOptionsBuilder.from_dataframe(
            df, enableRowGroup=True, enableValue=True, enablePivot=True
        )

        options.configure_side_bar()
        options.configure_selection("single")
        selection = AgGrid(
            df,
            enable_enterprise_modules=True,
            gridOptions=options.build(),
<<<<<<< HEAD
=======
            theme="streamlit",
>>>>>>> b6efcdf76e45223210b663a919d6821a0e4f2a89
            height=800,
            update_mode=GridUpdateMode.MODEL_CHANGED,
            allow_unsafe_jscode=True,
        )

        return selection  # return the selected row


    selection = aggrid_interactive_table(df=query_df)  # create the table


if __name__ == "__main__":
    interactive_table()