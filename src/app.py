import streamlit as st
import prepocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer") 

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue() 
    data = bytes_data.decode("utf-8")
    df = prepocessor.preprocess(data)
    user_list = df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show Analysis wrt" , user_list)
    
    if st.sidebar.button("Show Analysis"):

        st.title('Top Statistics')

        num_messages,num_words,num_media,num_links = helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(num_words)

        with col3:
            st.header("Total Images")
            st.title(num_media)

        with col4:
            st.header("Total Links")
            st.title(num_links)

        #Timeline
        st.title('Monthy Timeline')
        timeline = helper.monthly_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'] , timeline['message'], color = 'green')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        st.title('Daily Timeline')
        daily_timelin = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.figure(figsize=(4,4))
        ax.plot(daily_timelin['only_date'], daily_timelin['message'], color='black')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


    #finding the busiest users in the group
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x,newdf = helper.most_busy_users(df)
            fig,ax = plt.subplots()
            col1, col2 = st.columns(2) 

            with col1:
                ax.bar(x.index , x.values, color = "red")
                plt.xticks(rotation=90)
                st.pyplot(fig)
            with col2:
                st.dataframe(newdf)    

        #WordCLoud  
        st.title('Word Cloud')
        df_wc = helper.create_worldcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)     
        st.pyplot(fig) 
        #Most common words
        st.title('Most Common Words')
        x = helper.common_words(selected_user, df)
        fig,ax = plt.subplots()
        ax.bar(x[0], x[1], color = 'blue')
        plt.xticks(rotation=90)
        st.pyplot(fig)
        #Most commom emoji
        st.title('Most Common Emoji')
        df_emoji = helper.count_emoji(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(df_emoji)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(df_emoji[1].head(), labels = df_emoji[0].head(),autopct="%0.2f")
            st.pyplot(fig)    

