import streamlit as st
import zlibrary
import asyncio
import pandas as pd

# ZLIB_DOMAIN = '<ADD YOUR PERSONAL DOMAIN HERE>'

async def search_book(query, email, password):
    lib = zlibrary.AsyncZlib()
    await lib.login(email, password)
    paginator = await lib.search(q=query, count=10)
    result_set = await paginator.next()
    return result_set

async def fetch_book_details(book):
    await book.fetch()
    book_info = book.__dict__
    return book_info

def display_table(result_set):
    data = []
    for result in result_set:
        book_name = result['name']
        author_name = result['authors'][0]['author']
        data.append([book_name, author_name])
    
    df = pd.DataFrame(data, columns=['Book Name', 'Author Name'])
    st.table(df)


def main():
    st.title("zLibrary")
    st.sidebar.image("https://lib-adx6glm3iku7ovjtugrh2i7u.1lib.me/img/logo.zlibrary.png", width=200)
    #add a line dash
    st.sidebar.markdown("---")
    st.sidebar.header("1. Search and download books from zLibrary")
    st.sidebar.header("2. Enter your zLibrary credentials to search and download books")
    email = st.text_input("Enter your email")
    password = st.text_input("Enter your password", type="password")
    query = st.text_input("Enter Book Name")
    if query and email and password:
        result_set = asyncio.run(search_book(query, email, password))
        display_table(result_set)
        selected_book_index = st.selectbox("Select a book", [i for i in range(len(result_set))])
        if st.button("Get Book Details"):
            selected_book = asyncio.run(fetch_book_details(result_set[selected_book_index]))
            book_info = selected_book['parsed']
            columns = ["Name", "Language", "Extension", "Size", "Rating", "Download URL"]
            data = [[book_info["name"], book_info["language"], book_info["extension"], book_info["size"], book_info["rating"], book_info["download_url"]]]
            df_book_info = pd.DataFrame(data=data, columns=columns)
            st.table(df_book_info)
            st.markdown(f"[Download Book]({book_info['download_url']})")

if __name__ == '__main__':
    main()
