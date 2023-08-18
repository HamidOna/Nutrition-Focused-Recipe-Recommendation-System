#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from PIL import Image
import requests
import pandas as pd
from IPython.display import Markdown, display


# In[ ]:


def calculate_recommendations(dataframe):
    """
    Calculate recommendations based on user inputs.

    Parameters:
    dataframe (pd.DataFrame): The DataFrame containing recipe data.

    Returns:
    pd.DataFrame: Filtered and recommended DataFrame with selected columns.
    """
    weight_kg = float(input("Enter your weight in kg: "))
    height_cm = float(input("Enter your height in cm: "))
    age_years = int(input("Enter your age in years: "))
    gender = input("Enter your gender (male/female): ")
    body_goal = input("Enter your body goal (cutting/bulking/maintenance): ")
    selected_tags = input("Enter selected tags (comma-separated) e.g healthy, vegan, halal: ").split(',')

    # Calculate BMR
    if gender == 'male':
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age_years)
    else:
        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age_years)
    
    # Calculate recommended calories based on body goal
    if body_goal == 'cutting':
        recommended_calories = bmr * 0.8
    elif body_goal == 'bulking':
        recommended_calories = bmr * 1.2
    else:
        recommended_calories = bmr * 1.0  # Maintenance
    
    # Filter recipes based on body goal
    if body_goal == 'cutting':
        filtered_df = dataframe[dataframe['calories'] <= 10]  # Example calorie threshold for cutting
    elif body_goal == 'bulking':
        filtered_df = dataframe[dataframe['calories'] >= 400]  # Example calorie threshold for bulking
    else:
        filtered_df = dataframe  # No filtering for maintenance
        
    # Filter recipes by selected tags
    for tag in selected_tags:
        filtered_df = filtered_df[filtered_df['tag'].str.contains(tag, case=False, na=False)]
    
    def display_recipe_details(row):
        display(Markdown(f"### Recipe: {row['recipe_name']}"))
        display(Markdown(f"**Cook Time:** {row['cook_time']}"))
        display(Markdown(f"**Directions:** {row['directions']}"))
        display(Markdown(f"**Image:**"))
        display(row['image_url'])
        display(Markdown("---"))
    
    # Load the image URLs and return the selected columns
    filtered_df['image_url'] = filtered_df['image_url'].apply(lambda url: Image.open(requests.get(url, stream=True).raw))
    selected_columns = ['recipe_name', 'image_url', 'cook_time', 'directions']
    recommended_recipes = filtered_df[selected_columns].head()

    # Display recipe details
    for index, row in recommended_recipes.iterrows():
        display_recipe_details(row)

