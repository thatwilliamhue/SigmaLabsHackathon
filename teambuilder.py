import streamlit as st
import pandas as pd
import random

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
    dfplayers['Price'] = dfplayers['price']
    dfplayers['Media Focus'] = dfplayers['focus'].apply(lambda val: str(val) + ' tweets')
    dfplayers['Sport Name'] = dfplayers['sport']
    dfplayers['Sport Category'] = dfplayers['category']
    dfplayers = dfplayers.set_index('ID', drop=False)
    return dfplayers

dfplayers = load_and_prep_players()

cols = ['ID','Name','Age','Gender','Height','Weight','Nationality','Medals','Olympics Games Participated','Price','Media Focus','Sport Name', 'Sport Category',]

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
        color = 'lightcyan'
    elif str(val) <= '1000' and str(val) >= '0' :
        color = 'lightblue'
    else:
        color = 'blue'
    return 'background-color: %s' % color


heading_properties = [('font-size', '16px'), ('text-align', 'center'),
                      ('color', 'gray'), ('font-weight', 'bold'),
                      ('background', 'gold'), ('border', '1.2px solid')]

cell_properties = [('font-size', '16px'), ('text-align', 'center'), ('color', 'black')]

dfstyle = [{"selector": "th", "props": heading_properties},
           {"selector": "td", "props": cell_properties}]

# Expander Styling

st.markdown(
    """
<style>
.streamlit-expanderHeader {
 #   font-weight: bold;
    background: gold;
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

tab_selection, tab_lookup, tab_instructions, tab_credits = st.tabs(["Player/Team Selection", "Player/Team Lookup", "Instructions", "Credits"])

col1, col2, col3 = st.sidebar.columns([1, 8, 1])
with col1:
    st.write("")
with col2:
    st.image('data/logo.svg.webp', use_column_width=True)
with col3:
    st.write("")

st.sidebar.markdown(" ## About Olympic Fantasy League")
st.sidebar.markdown(
    "  \n Welcome to Olympic Fantasy League!  \n It's time to build your 2024 Paris Olympics dream team.  \n 5 Athletes 🏃‍♂️ 🏊‍♀️ 🚴‍♂️ 🏋️‍♀️ 🤺  \n 2 teams ⚽ 🏀  \n 1000 Coin Budget 🪙")
st.sidebar.info("Read more about the app and see the code on our [Github](https://github.com/thatwilliamhue/SigmaLabsHackathon).", icon="ℹ️")
st.sidebar.markdown("")
st.sidebar.image('data/HSBC_Logo.png', use_column_width=True)
########################################### Selection Tab ###########################################

def check_selection():
    # for i in range(0, 6):
        # a = []
        # a += dfplayers._get_value(players_selected[i], 'Category')
    if len(players_selected) == 7:
        return "true"
    else:
        return "false"

def update_budget_on_change(players_selected):
    if check_selection() == "true":
        budget = 1000
        cost = 0
        for i in range(0,6):
            cost += int(dfplayers._get_value(players_selected[i], 'Price'))
        money_left = budget - cost

        if money_left < 0:
            return "Oops, you've gone over budget."
        else:
            return money_left
    else:
        return "Selection not valid, please choose 5 individual sports and 2 team sports."

with tab_selection:
    budget = 1000

    st.write(f'''
         ##### <div style="text-align: center"> Time to select your 5 individual players and 2 teams. You have <span style="color:gold"> {budget} </span>  coins to spend. </div>
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

    st.button("Reset", type="primary")
    if st.button("Check budget"):
        st.write(update_budget_on_change(players_selected))
    else:
        st.write("Budget: 1000")

    st.success('''**Tips & Hints:**
    Try to spend all your coins to maximise your chances''')

########################################### Player/Team Tab ###########################################
#player lookup and review stats
with tab_lookup:
    st.write(f'''
         ##### <div style="text-align: center"> Filter and explore players. </div>
         ''', unsafe_allow_html=True)

    query = st.text_input("E.g. Football, Canada")
    if query:
        mask = dfplayers.applymap(lambda x: query in str(x).lower()).any(axis=1)
        dfplayers = dfplayers[mask]
    st.data_editor(
        dfplayers,
        hide_index=True,
        column_order=('ID','Name','Age','Gender','Height','Weight','Nationality','Medals','Olympics Games Participated','Price','Media Focus','Sport Name', 'Sport Category')
    )


########################################### Credits Tab ###########################################
with tab_credits:

    st.write(f'''
         ##### <div style="text-align: center"> HSBC SigmaLabs Hackathon Team <br><br> Aleksandr Agadzhanov <br> Christian Albertalli <br> James Attwood <br> Sarah Howard <br> Viktoriya Savchyn <br> Will Zhang <br><br> <span style="color:blue"> {'Thank you for your support!'} </span></div>
         ''', unsafe_allow_html=True)

with tab_instructions:
    st.markdown(" ### Instructions🔎 ")

    ########## 
    expand_faq1 = st.expander('''How to Play''')
    with expand_faq1:

        st.write(
            '''You can choose 5 individual athletes and 2 teams.  \n You have a budget of 1000 coins - player cost will vary depending on experience so choose your team wisely!  \n Follow along with live Olympic events and gain points as your players do.  \n Compare and compete with friends and immerse yourselves in the Paris Olympics.''',
            unsafe_allow_html=True)

    ##########

    expand_faq2 = st.expander('''Easter Egg Game''')
    with expand_faq2:

        ###Easter Egg by James###
        # Function to check if any player has won
        # Function to generate a random number between 1 and 100
        def generate_random_number():
            return random.randint(1, 100)


        # Function to check if the guess is correct
        def check_guess(secret_number, guess):
            if guess < secret_number:
                return "Too low! Try again."
            elif guess > secret_number:
                return "Too high! Try again."
            else:
                return "Congratulations! You guessed it right!"


        # Streamlit app
        def main():
            st.title("Number Guessing Game")
            st.write("I have chosen a number between 1 and 10. Try to guess it!")

            # Generate a random number
            secret_number = generate_random_number()

            # Game loop
            guess = st.number_input("Enter your guess:", min_value=1, max_value=10, step=1)
            message = ""
            if st.button("Check"):
                message = check_guess(secret_number, guess)
                st.write(message)
                if message.startswith("Congratulations"):
                    st.write("The secret number was:", secret_number)
                    st.warning("Game over! Please refresh the page to play again.")


        # Run the app
        if __name__ == "__main__":
            main()

