import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="HSBC SigmaLabs", page_icon="🏅",initial_sidebar_state="expanded")
########################################### Load Data ###########################################
@st.cache
def load_and_prep_players():
    dfplayers = pd.read_csv('data/data.csv')
    dfplayers['ID'] = dfplayers['id']
    dfplayers['Name'] = dfplayers['name']
    dfplayers['Age'] = dfplayers['age']
    dfplayers['Gender'] = dfplayers['gender']
    dfplayers['Height'] = dfplayers['height'].apply(lambda val: str(val) + ' cm')
    dfplayers['Weight'] = dfplayers['weight'].apply(lambda val: str(val) + ' kg')
    dfplayers['Nationality'] = dfplayers['nationality']
    dfplayers['Medals'] = dfplayers['medals']
    dfplayers['Olympics Games Participated'] = dfplayers['games']
    dfplayers['Biography'] = dfplayers['biography']
    dfplayers['Price'] = dfplayers['price'].apply(lambda val: str(val) + ' coins')
    dfplayers['Media Focus'] = dfplayers['focus'].apply(lambda val: str(val) + ' tweets')
    dfplayers['Sport Name'] = dfplayers['sport']
    dfplayers['Sport Category'] = dfplayers['category']
    dfplayers = dfplayers.set_index('ID', drop=False)
    return dfplayers

dfplayers = load_and_prep_players()

cols = ['ID','Name','Age','Gender','Height','Weight','Nationality','Medals','Olympics Games Participated','Biography','Price','Media Focus','Sport Name', 'Sport Category',]

########################################### Style ###########################################

# CSS for tables

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>   """

center_heading_text = """
    <style>
        .col_heading   {text-align: center !important}
    </style>          """

center_row_text = """
    <style>
        td  {text-align: center !important}
    </style>      """

# Inject CSS with Markdown

st.markdown(hide_table_row_index, unsafe_allow_html=True)
st.markdown(center_heading_text, unsafe_allow_html=True)
st.markdown(center_row_text, unsafe_allow_html=True)

# More Table Styling

def color_focus(val):
    if str(val) == '0':
        color = 'azure'
    elif str(val) <= '1000' and str(val) >= '0' :
        color = 'lightgreen'
    else:
        color = 'green'
    return 'background-color: %s' % color


heading_properties = [('font-size', '16px'), ('text-align', 'center'),
                      ('color', 'black'), ('font-weight', 'bold'),
                      ('background', 'mediumturquoise'), ('border', '1.2px solid')]

cell_properties = [('font-size', '16px'), ('text-align', 'center'), ('color', 'black')]

dfstyle = [{"selector": "th", "props": heading_properties},
           {"selector": "td", "props": cell_properties}]

# Expander Styling

st.markdown(
    """
<style>
.streamlit-expanderHeader {
 #   font-weight: bold;
    background: aliceblue;
    font-size: 18px;
}
</style>
""",
    unsafe_allow_html=True,
)

########################################### Title, Tabs and Sidebar ###########################################

st.title("Olympic Fantasy League")
st.markdown('''##### <span style="color:gray">Build your Olympics dream team</span>
            ''', unsafe_allow_html=True)

tab_selection, tab_lookup, tab_credits = st.tabs(["Player/Team Selection", "Player/Team Lookup", "Credits"])

col1, col2, col3 = st.sidebar.columns([1, 8, 1])
with col1:
    st.write("")
with col2:
    st.image('data/logo.svg.webp', use_column_width=True)
with col3:
    st.write("")

st.sidebar.markdown(" ## About Olympic Fantasy League")
st.sidebar.markdown(
    "Welcome to Olympic Fantasy League!  \n You have 500 coins to build your 2024 Paris Olympics team.  \n Choose 5 athletes from individual sports and 2 teams.  \n Follow along with live Olympic events and gain points as your players do.  \n Compare and compete with friends and immerse yourselves in the Paris Olympics.")


########################################### Selection Tab ###########################################

with tab_selection:

    budget = 500

    st.write(f'''
         ##### <div style="text-align: center"> You need to select 5 individual sports and 2 team sports. You have <span style="color:blue"> {budget} </span>  coins to spend. </div>
         ''', unsafe_allow_html=True)

    player = st.selectbox("Player lookup (just start typing):", dfplayers.Name, index=None)

    styler_player = (dfplayers[dfplayers.Name == player][cols]
                     .style.set_properties(**{'background': 'azure', 'border': '1.2px solid'})
                     .hide(axis='index')
                     .set_table_styles(dfstyle)
                     .applymap(color_focus, subset=pd.IndexSlice[:, ['Media Focus']]))
    st.table(styler_player)


    players_selected = st.multiselect(
        "Choose 5 individual sports and 2 team sports",
        dfplayers.ID,default=None, key=None, help=None, on_change=None, args=None, max_selections=7, placeholder="Choose an option", disabled=False, label_visibility="visible"
    )

    st.write("You selected:",str(players_selected)[1:-1])

######### Update the budget

st.success('''**Tips & Hints:**
Try to spend all your coins to maximise your chances''')

########################################### Player/Team Tab ###########################################
#player lookup and review stats
with tab_lookup:
    st.write(f'''
         ##### <div style="text-align: center"> text. </div>
         ''', unsafe_allow_html=True)



########################################### Credits Tab ###########################################
