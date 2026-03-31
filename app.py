import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='PhonePe Pulse', layout='wide', page_icon='📱')

st.title('📱 PhonePe Pulse - Transaction Insights Dashboard')
st.markdown('**Real Data Visualization using Different Chart Types**')

df = pd.read_csv('aggregated_transaction.csv')
df['State'] = df['State'].str.title()

# Filters
st.sidebar.header('🔍 Filters')
selected_year = st.sidebar.selectbox('Select Year', sorted(df['Year'].unique()), index=len(df['Year'].unique())-1)
selected_states = st.sidebar.multiselect('Select States', sorted(df['State'].unique()), 
                                        default=['Tamil Nadu', 'Karnataka', 'Maharashtra'])

filtered_df = df[(df['Year'] == selected_year) & (df['State'].isin(selected_states))]

tab1, tab2, tab3, tab4, tab5 = st.tabs(['State Performance', 'Payment Patterns', 'Distribution & Correlation', 'Growth Trends', 'Business Insights'])

with tab1:
    st.subheader('State Performance')
    c1, c2 = st.columns(2)
    with c1:
        fig1 = px.bar(filtered_df.groupby('State')['Transaction_amount'].sum().reset_index(), 
                      x='State', y='Transaction_amount', title='Total Transaction Value by State')
        st.plotly_chart(fig1, use_container_width=True)
        
        fig2 = px.bar(filtered_df.groupby('State')['Transaction_count'].sum().reset_index(), 
                      x='State', y='Transaction_count', title='Total Number of Transactions by State')
        st.plotly_chart(fig2, use_container_width=True)
    with c2:
        fig3 = px.pie(filtered_df, names='Transaction_type', values='Transaction_count', title='Payment Method Distribution')
        st.plotly_chart(fig3, use_container_width=True)
        
        fig4 = px.pie(filtered_df.groupby('Transaction_type')['Transaction_amount'].sum().reset_index(), 
                      names='Transaction_type', values='Transaction_amount', hole=0.6, title='Revenue Share by Payment Type')
        st.plotly_chart(fig4, use_container_width=True)

with tab2:
    st.subheader('Payment Patterns & Hierarchy')
    c1, c2 = st.columns(2)
    with c1:
        fig5 = px.sunburst(filtered_df, path=['State', 'Transaction_type'], values='Transaction_amount', 
                           title='State-wise Payment Type Breakdown (Sunburst)')
        st.plotly_chart(fig5, use_container_width=True)
        
        fig6 = px.treemap(filtered_df, path=['State', 'Transaction_type'], values='Transaction_amount', 
                          title='Hierarchical View of Transaction Value (Treemap)')
        st.plotly_chart(fig6, use_container_width=True)
    with c2:
        bubble = filtered_df.groupby('State').agg({'Transaction_amount':'sum', 'Transaction_count':'sum'}).reset_index()
        fig7 = px.scatter(bubble, x='Transaction_count', y='Transaction_amount', size='Transaction_amount', 
                          color='State', title='State Performance Bubble Chart')
        st.plotly_chart(fig7, use_container_width=True)

with tab3:
    st.subheader('Distribution & Correlation')
    c1, c2 = st.columns(2)
    with c1:
        # Heatmap
        pivot = filtered_df.pivot_table(values='Transaction_amount', index='State', columns='Transaction_type', aggfunc='sum').fillna(0)
        fig8 = px.imshow(pivot, text_auto=True, aspect='auto', color_continuous_scale='Viridis', 
                         title='Heatmap - Amount by State & Payment Type')
        st.plotly_chart(fig8, use_container_width=True)
        
        # Scatter Plot
        fig9 = px.scatter(filtered_df, x='Transaction_count', y='Transaction_amount', color='Transaction_type', 
                          size='Transaction_amount', title='Transaction Count vs Value (Scatter Plot)')
        st.plotly_chart(fig9, use_container_width=True)
    with c2:
        # Stacked Bar
        fig10 = px.bar(filtered_df, x='State', y='Transaction_amount', color='Transaction_type', 
                       barmode='stack', title='Stacked Payment Type Contribution by State')
        st.plotly_chart(fig10, use_container_width=True)

with tab4:
    st.subheader('Growth Trends Over Time')
    trend = df.groupby(['Year', 'Transaction_type'])['Transaction_amount'].sum().reset_index()
    
    fig11 = px.line(trend, x='Year', y='Transaction_amount', color='Transaction_type', markers=True, 
                    title='Year-wise Growth Trend by Payment Type (Line Chart)')
    st.plotly_chart(fig11, use_container_width=True)
    
    fig12 = px.area(trend, x='Year', y='Transaction_amount', color='Transaction_type', 
                    title='Cumulative Growth (Area Chart)')
    st.plotly_chart(fig12, use_container_width=True)

with tab5:
    st.subheader('Business Insights')
    st.markdown('''
    ### Key PhonePe Insights:
    - **Tamil Nadu, Karnataka & Maharashtra** consistently lead in transaction value.
    - **UPI and Merchant Payments** are the dominant categories.
    - Strong year-on-year growth is visible across states.

    ### Business Use Cases:
    • Customer Segmentation using Scatter & Bubble Charts  
    • Regional Strategy using Heatmap  
    • Payment Pattern Analysis using Sunburst & Treemap  
    • Growth Forecasting using Line & Area Charts
    ''')

st.sidebar.success('Diverse Chart Types Used')
st.caption('PhonePe Transaction Insights Project')
