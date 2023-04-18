import streamlit as st
from Zlibrary import Zlibrary

st.title("zLibrary")
st.sidebar.image("https://lib-adx6glm3iku7ovjtugrh2i7u.1lib.me/img/logo.zlibrary.png", width=200)
    #add a line dash
st.sidebar.markdown("---")
st.sidebar.header("1. Search and download books from zLibrary")
st.sidebar.header("2. Enter your zLibrary credentials to search and download books")



# Create Zlibrary object and login
@st.cache_data
def login(email, password):
    return Zlibrary(email=email, password=password)

email = st.text_input("Enter email:")
password = st.text_input("Enter password:", type="password")

if email and password:
    Z = login(email, password)

    # Search for books
    book_name = st.text_input("Enter book name:")
    if book_name:
        results = Z.search(message=book_name)

        # Create dropdown select box to select a book
        book_options = {}
        for book in results["books"]:
            book_options[book["title"] + " by " + book["author"] + " | Language: " + book["language"] + " | Format: " + book["extension"]] = book
        selected_book = st.selectbox("Select a book:", list(book_options.keys()))

        # Download selected book
        if st.button("Confirm selection"):
            book = book_options[selected_book]
            filename, content = Z.downloadBook(book)
            st.download_button(label="Download " + filename, data=content, file_name=filename)
