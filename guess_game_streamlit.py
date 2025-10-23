import streamlit as st
import random

def main():
    st.title("🎯 Number Guessing Game")
    st.write("I'm thinking of a number between 1 and 100. Can you guess it?")
    
    # Initialize game state
    if 'target_number' not in st.session_state:
        st.session_state.target_number = random.randint(1, 100)
        st.session_state.attempts = 0
        st.session_state.game_over = False
    
    # Display game info
    st.sidebar.header("Game Stats")
    st.sidebar.write(f"Attempts: {st.session_state.attempts}")
    
    if not st.session_state.game_over:
        # Get user input
        guess = st.number_input("Enter your guess:", min_value=1, max_value=100, step=1)
        
        if st.button("Submit Guess"):
            st.session_state.attempts += 1
            
            if guess < st.session_state.target_number:
                st.error("Too low! Try again.")
                st.balloons()  # Fun effect
            elif guess > st.session_state.target_number:
                st.error("Too high! Try again.")
                st.snow()  # Fun effect
            else:
                st.success(f"🎉 Congratulations! You guessed it in {st.session_state.attempts} attempts!")
                st.session_state.game_over = True
                
                # Show celebration
                st.balloons()
                st.snow()
    
    # Reset game
    if st.session_state.game_over:
        if st.button("Play Again"):
            st.session_state.target_number = random.randint(1, 100)
            st.session_state.attempts = 0
            st.session_state.game_over = False
            st.rerun()

if __name__ == "__main__":
    main()