import streamlit as st

def sidebar(user, nav_items, nav_choice):
    # Показывать sidebar только для залогиненного пользователя
    if user:
        st.sidebar.markdown(f"👋 Hello, **{user}**!")
        for item in nav_items:
            if st.sidebar.button(item, key=f"nav_{item}", use_container_width=True):
                st.session_state['nav_choice'] = item
        st.sidebar.markdown("---")
        if st.sidebar.button("🔴 Logout", key="logout_btn", use_container_width=True):
            st.session_state["user"] = None
            st.session_state["user_id"] = None
            st.session_state['page'] = 'home'
            st.success("You have logged out.")
            st.rerun() 