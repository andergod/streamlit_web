import streamlit as st
from src.model import train_model
from src.data_loader import load_data

st.title("🤖 Model Training")

df = load_data("data/sample.csv")
accuracy = train_model(df)

st.success(f"Model trained with accuracy: {accuracy:.2f}")
