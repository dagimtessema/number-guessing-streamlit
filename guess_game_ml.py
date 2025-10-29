import streamlit as st
import random
import pandas as pd
import numpy as np
from collections import defaultdict

class SmartNumberGame:
    def __init__(self):
        self.reset_game()
    
    def reset_game(self):
        self.attempts = 0
        self.game_over = False
        self.guess_history = []
        self.player_pattern = []
        
    
    
    def make_guess(self, guess, target_number):
        self.attempts += 1
        self.guess_history.append(guess)
        
        if guess < target_number:
            feedback = "low"
            self.player_pattern.append((guess, "low"))
        elif guess > target_number:
            feedback = "high"
            self.player_pattern.append((guess, "high"))
        else:
            feedback = "correct"
            self.game_over = True
            
        return feedback
    
    def analyze_pattern(self, target_number):
        """Simple analysis of player's guessing pattern"""
        if len(self.guess_history) < 2:
            return "Keep guessing to see pattern analysis!"
        
        # Calculate average guess
        avg_guess = np.mean(self.guess_history)
        
        # Check if player is improving
        improvements = []
        for i in range(1, len(self.guess_history)):
            prev_diff = abs(self.guess_history[i-1] - target_number)
            curr_diff = abs(self.guess_history[i] - target_number)
            improvements.append(curr_diff < prev_diff)
        
        improvement_rate = sum(improvements) / len(improvements) if improvements else 0
        
        analysis = f"""
        **Pattern Analysis:**
        - Average guess: {avg_guess:.1f}
        - Improvement rate: {improvement_rate:.0%}
        - Total guesses: {self.attempts}
        """
        
        if improvement_rate > 0.6:
            analysis += "\n🎯 Great strategy! You're consistently getting closer!"
        elif improvement_rate < 0.3:
            analysis += "\n💡 Try adjusting your guesses more strategically!"
        
        return analysis

def main():
    st.set_page_config(page_title="Smart Number Game", page_icon="🎯")
    
    st.title("🤖 Smart Number Guessing Game")
  
    st.write("Select difficulty level")
    # Initialize game
    if 'game' not in st.session_state:
        st.session_state.game = SmartNumberGame()
    
    game = st.session_state.game
    
    # Sidebar with stats
    with st.sidebar:
        st.header("📊 Game Statistics")
        st.metric("Attempts", game.attempts)
        st.metric("Target Number", "???" if not game.game_over else st.session_state.target_number)
        
        if game.guess_history:
            st.subheader("Guess History")
            for i, guess in enumerate(game.guess_history, 1):
                st.write(f"Attempt {i}: {guess}")
   
    
    # Main game area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if not game.game_over:
            def difficulty_selector_fixed():
    
                # Initialize a session state variable for difficulty if it doesn't exist
                if 'difficulty' not in st.session_state:
                    st.session_state.difficulty = "None"
    
                
                    st.write("### Select a difficulty level:")
    
                col1, col2, col3 = st.columns(3)
    
                with col1:
                     if st.button("Easy", use_container_width=True):
                        st.session_state.difficulty = "Easy"
                        target_number_level=random.randint(1,50)
                        st.session_state.target_number= target_number_level
                with col2:
                     if st.button("Medium", use_container_width=True):
                        st.session_state.difficulty = "Medium"
                        target_number_level=random.randint(1,100)
                        st.session_state.target_number= target_number_level
                with col3:
                     if st.button("Hard", use_container_width=True):
                        st.session_state.difficulty = "Hard"
                        target_number_level=random.randint(1,200)
                        st.session_state.target_number= target_number_level
                if st.session_state.difficulty == "Easy":
                     st.write("Guess a number between 1 and 50. I'll analyze your strategy!")
                     guess_level = st.number_input("Enter your guess:", min_value=1, max_value=50, step=1)
                     
                     st.session_state.guess = guess_level
                     
        
                elif st.session_state.difficulty == "Medium":
                     st.write("Guess a number between 1 and 100. I'll analyze your strategy!")
                    
                     guess_level = st.number_input("Enter your guess:", min_value=1, max_value=100, step=1)
                     
                     st.session_state.guess = guess_level
                     

                elif st.session_state.difficulty == "Hard":
                     st.write("Guess a number between 1 and 200. I'll analyze your strategy!")
                     guess_level = st.number_input("Enter your guess:", min_value=1, max_value=200, step=1)
                     
                     st.session_state.guess = guess_level
                     
                else:
                    # This will only show on the first load before a button is clicked
                     st.write("Please select a difficulty level to continue.")
                     st.session_state.guess = None
                     st.session_state.target_number= None

                return st.session_state.guess, st.session_state.target_number

                 
            guess, target_number = difficulty_selector_fixed()

                 
                
            if st.button("🎯 Submit Guess", use_container_width=True):
                             
                feedback = game.make_guess(guess, target_number)
                
                if feedback == "correct":
                   st.success(f"🎉 Perfect! You found it in {game.attempts} attempts!")
                   st.balloons()
                    
                        # Show analysis
                   with st.expander("View Strategy Analysis"):
                         st.write(game.analyze_pattern(target_number))
                else:
                   st.error(f"Too {feedback}! Try again.")
                    
                        # Show hint after 3 attempts
                   if game.attempts >= 3:
                      with st.expander("💡 Hint"):
                           if feedback == "low":
                              st.write(f"The number is higher than {guess}. Try guessing in the upper range.")
                           else:
                              st.write(f"The number is lower than {guess}. Try guessing in the lower range.")
    
    with col2:
        st.subheader("Game Tips")
        st.info("""
        - Start with 50 (middle)
        - Use binary search strategy
        - Pay attention to the pattern analysis
        - Try to beat your personal best!
        """)
        
        if game.attempts > 0 and not game.game_over:
            with st.expander("Current Analysis"):
                st.write(game.analyze_pattern(target_number))
    
    # Reset button
    if game.game_over:
        st.divider()
        if st.button("🔄 Play Again", use_container_width=True):
            game.reset_game()
            st.session_state.difficulty = "None"
            st.rerun()
            

if __name__ == "__main__":
    main()
