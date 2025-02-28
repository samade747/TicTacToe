import streamlit as st
import numpy as np

# Function to initialize an empty 3x3 board
def initialize_board():
    return [[' ' for _ in range(3)] for _ in range(3)]

# Function to check if a player has won the game
def check_winner(board, player):
    # Check rows for a win
    for row in board:
        if row.count(player) == 3:
            return True
    # Check columns for a win
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # Check diagonals for a win
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True
    return False

# Function to check if the board is full (draw condition)
def is_full(board):
    return all(cell != ' ' for row in board for cell in row)

# Main function to run the Tic-Tac-Toe game
def tic_tac_toe():
    # Set up Streamlit page configuration
    st.set_page_config(page_title="Tic-Tac-Toe", layout="wide", page_icon="🎮")
    st.markdown("""
        <style>
            .main { background-color: #1E1E1E; }
            h1, h2, h3, h4, h5, h6 { color: white; text-align: center; }
            .stButton>button { height: 80px; width: 80px; font-size: 24px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("✨ Tic-Tac-Toe Game ✨")
    st.markdown("<h3 style='text-align: center; color: #FFFFFF; background-color: #4CAF50; padding: 10px;'>Enjoy Your Game!</h3>", unsafe_allow_html=True)
    
    # Initialize game state variables in Streamlit session state
    if 'board' not in st.session_state or st.session_state.get('reset', False):
        st.session_state.board = initialize_board()
        st.session_state.current_player = 'X'
        st.session_state.players = {'X': 'Player 1', 'O': 'Player 2'}
        st.session_state.winner = None
        st.session_state.reset = False
    
    # Get player names from user input
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.player1 = st.text_input("Enter Player 1 Name:", "Player 1")
    with col2:
        st.session_state.player2 = st.text_input("Enter Player 2 Name:", "Player 2")
    
    st.session_state.players = {'X': st.session_state.player1, 'O': st.session_state.player2}
    
    # Display the current player's turn
    st.markdown(f"<h3 style='text-align: center; color: black;'>🎲 {st.session_state.players[st.session_state.current_player]}'s Turn ({st.session_state.current_player})</h3>", unsafe_allow_html=True)
    
    # Create a 3x3 button grid for the game board with improved UI
    board_container = st.container()
    with board_container:
        cols = st.columns(3)
        for row in range(3):
            for col in range(3):
                btn_label = st.session_state.board[row][col]
                btn_style = "background-color: #333; color: white; border-radius: 10px;"
                if cols[col].button(btn_label if btn_label != ' ' else ' ', key=f"{row}-{col}", help="Click to mark"):
                    if st.session_state.board[row][col] == ' ' and st.session_state.winner is None:
                        st.session_state.board[row][col] = st.session_state.current_player
                        if check_winner(st.session_state.board, st.session_state.current_player):
                            st.session_state.winner = st.session_state.current_player
                            st.success(f"🏆 {st.session_state.players[st.session_state.winner]} wins!")
                        elif is_full(st.session_state.board):
                            st.warning("🤝 It's a draw!")
                        else:
                            st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'
                        st.rerun()
    
    # If a player has won or it's a draw, provide a restart button
    if st.session_state.winner or is_full(st.session_state.board):
        if st.button("🔄 Restart Game", key="restart_button", help="Click to restart the game"):
            st.session_state.board = initialize_board()
            st.session_state.current_player = 'X'
            st.session_state.winner = None
            st.session_state.reset = True
            st.rerun()

# Run the Tic-Tac-Toe game
tic_tac_toe()
