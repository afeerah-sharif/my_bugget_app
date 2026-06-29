"""
Smart Budget Advisor & Expense Analyzer
A complete Streamlit web application for personal budget management.
Run this file with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------------------------
# 1. PAGE CONFIGURATION (Must be the first Streamlit command)
# -----------------------------------------------
st.set_page_config(
    page_title="Smart Budget Advisor",
    page_icon=":money bag:",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------
# 2. CUSTOM CSS FOR ENHANCED UI/UX
# -----------------------------------------------
st.markdown("""
    <style>
        /* Main container styling */
        .main {
            padding: 2rem 1rem;
        }
        
        /* Card-like containers */
        .stExpander {
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* Custom button styling */
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.5rem 2rem;
            border: none;
            transition: all 0.3s ease;
            width: 100%;
        }
        .stButton > button:hover {
            background-color: #45a049;
            transform: scale(1.02);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        /* Success/Info/Warning boxes */
        .success-box {
            padding: 1rem;
            border-radius: 10px;
            background-color: #d4edda;
            border-left: 6px solid #28a745;
            color: #155724;
            margin: 1rem 0;
        }
        .info-box {
            padding: 1rem;
            border-radius: 10px;
            background-color: #fff3cd;
            border-left: 6px solid #ffc107;
            color: #856404;
            margin: 1rem 0;
        }
        .warning-box {
            padding: 1rem;
            border-radius: 10px;
            background-color: #f8d7da;
            border-left: 6px solid #dc3545;
            color: #721c24;
            margin: 1rem 0;
        }
        
        /* Metric styling */
        .metric-container {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        /* Title styling */
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------
# 3. APPLICATION TITLE AND DESCRIPTION
# -----------------------------------------------
st.title("Smart Budget Advisor & Expense Analyzer")
st.markdown("### Take control of your finances with intelligent insights")
st.markdown("---")

# -----------------------------------------------
# 4. USER INPUT SECTION
# -----------------------------------------------
with st.container():
    st.subheader("Enter Your Monthly Financial Data")
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Total Monthly Income
        total_income = st.number_input(
            "Total Monthly Income",
            min_value=0.0,
            value=5000.0,
            step=100.0,
            help="Enter your total monthly income after taxes"
        )
        
        # Utility Bills
        utility_bills = st.number_input(
            "Utility Bills (Electricity, Water, Gas)",
            min_value=0.0,
            value=500.0,
            step=50.0,
            help="Include electricity, water, gas, internet, and phone bills"
        )
        
        # Groceries
        groceries = st.number_input(
            "Groceries (Food & Household)",
            min_value=0.0,
            value=800.0,
            step=50.0,
            help="Monthly spending on food and household items"
        )
    
    with col2:
        # Fuel/Transport
        transport = st.number_input(
            "Fuel/Transport (Fuel, Public Transit, Car Maintenance)",
            min_value=0.0,
            value=400.0,
            step=50.0,
            help="Includes fuel, public transportation, and car maintenance"
        )
        
        # Miscellaneous Expenses
        misc_expenses = st.number_input(
            "Miscellaneous Expenses (Entertainment, Dining, Shopping)",
            min_value=0.0,
            value=600.0,
            step=50.0,
            help="Includes entertainment, dining out, shopping, and other discretionary spending"
        )

# Add spacing
st.markdown("---")

# -----------------------------------------------
# 5. ANALYSIS BUTTON & CALCULATIONS
# -----------------------------------------------
# Initialize session state to store results
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False

# Centered button using columns
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    analyze_clicked = st.button("Analyze My Budget", use_container_width=True)

if analyze_clicked:
    st.session_state.analysis_done = True
    # Perform calculations
    total_expenses = utility_bills + groceries + transport + misc_expenses
    net_savings = total_income - total_expenses
    savings_percentage = (net_savings / total_income * 100) if total_income > 0 else 0
    
    # Store in session state for persistence
    st.session_state.total_expenses = total_expenses
    st.session_state.net_savings = net_savings
    st.session_state.savings_percentage = savings_percentage
    st.session_state.total_income = total_income

# -----------------------------------------------
# 6. DISPLAY RESULTS (If analysis has been performed)
# -----------------------------------------------
if st.session_state.analysis_done:
    # Retrieve values from session state
    total_expenses = st.session_state.total_expenses
    net_savings = st.session_state.net_savings
    savings_percentage = st.session_state.savings_percentage
    total_income = st.session_state.total_income
    
    # -----------------------------------------------
    # 6a. METRIC DISPLAY (Key Financial Numbers)
    # -----------------------------------------------
    st.subheader("Financial Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-container">
                <h4 style="margin:0; color:#2c3e50;">Total Income</h4>
                <p style="font-size:1.5rem; font-weight:bold; margin:0; color:#28a745;">PKR{total_income:,.2f}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-container">
                <h4 style="margin:0; color:#2c3e50;">Total Expenses</h4>
                <p style="font-size:1.5rem; font-weight:bold; margin:0; color:#dc3545;">PKR{total_expenses:,.2f}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        savings_color = "#28a745" if net_savings >= 0 else "#dc3545"
        st.markdown(f"""
            <div class="metric-container">
                <h4 style="margin:0; color:#2c3e50;">Net Savings</h4>
                <p style="font-size:1.5rem; font-weight:bold; margin:0; color:{savings_color};">PKR{net_savings:,.2f}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-container">
                <h4 style="margin:0; color:#2c3e50;">Savings Rate</h4>
                <p style="font-size:1.5rem; font-weight:bold; margin:0; color:#17a2b8;">{savings_percentage:.1f}%</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # -----------------------------------------------
    # 6b. AI ADVISOR LOGIC (Smart Recommendations)
    # -----------------------------------------------
    st.subheader("AI Advisor Recommendation")
    
    if net_savings > 0 and savings_percentage >= 20:
        st.markdown(f"""
            <div class="success-box">
                <strong>Excellent Savings!</strong><br>
                Your savings are excellent ({savings_percentage:.1f}% of income). 
                You have <strong>PKR{net_savings:,.2f}</strong> in surplus.<br>
                <strong>Tip:</strong> Consider investing this amount in diversified mutual funds, 
                real estate, or a retirement account to build long-term wealth.
            </div>
        """, unsafe_allow_html=True)
    
    elif net_savings > 0 and savings_percentage < 20:
        st.markdown(f"""
            <div class="info-box">
                <strong>Moderate Savings</strong><br>
                You're saving <strong>{savings_percentage:.1f}%</strong> of your income 
                (PKR{net_savings:,.2f}).<br>
                <strong>Tip:</strong> Try to increase your savings rate to 20% by 
                reducing discretionary expenses. Consider creating a detailed budget 
                to track every PKR.
            </div>
        """, unsafe_allow_html=True)
    
    else:  # net_savings <= 0 (overspending)
        st.markdown(f"""
            <div class="warning-box">
                <strong>Alert! Overspending Detected</strong><br>
                You're spending <strong>PKR{abs(net_savings):,.2f}</strong> more than your income.<br>
                <strong>Actionable Advice:</strong> 
                Try cutting down on Miscellaneous expenses by 15%. 
                Review your Utility Bills and Groceries for potential savings 
                (e.g., switching to energy-efficient appliances, meal planning).<br>
                <strong>Recommended:</strong> Create a zero-based budget where 
                every PKR has a purpose.
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # -----------------------------------------------
    # 6c. STUNNING VISUALIZATIONS (Charts)
    # -----------------------------------------------
    st.subheader("Spending Breakdown Visualization")
    
    # Prepare data for charts
    expense_categories = ['Utility Bills', 'Groceries', 'Fuel/Transport', 'Miscellaneous']
    expense_values = [utility_bills, groceries, transport, misc_expenses]
    
    # Create two columns for charts
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # PIE CHART
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
        explode = (0.05, 0.05, 0.05, 0.05)
        
        # Filter out zero values for better visualization
        filtered_data = [(cat, val) for cat, val in zip(expense_categories, expense_values) if val > 0]
        if filtered_data:
            cats, vals = zip(*filtered_data)
            wedges, texts, autotexts = ax1.pie(
                vals, 
                labels=cats, 
                autopct='%1.1f%%',
                startangle=90,
                colors=colors[:len(cats)],
                explode=explode[:len(cats)],
                shadow=True,
                textprops={'fontsize': 10, 'fontweight': 'bold'}
            )
            ax1.set_title('Expense Distribution', fontsize=14, fontweight='bold', pad=20)
            plt.axis('equal')
        else:
            ax1.text(0.5, 0.5, 'No expenses recorded', 
                    horizontalalignment='center', 
                    verticalalignment='center',
                    transform=ax1.transAxes,
                    fontsize=14)
            ax1.set_title('Expense Distribution', fontsize=14, fontweight='bold', pad=20)
        
        st.pyplot(fig1)
    
    with chart_col2:
        # BAR CHART
        fig2, ax2 = plt.subplots(figsize=(8, 6))
        
        # Filter out zero values for cleaner chart
        if any(expense_values):
            bars = ax2.bar(expense_categories, expense_values, 
                          color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'],
                          edgecolor='black',
                          linewidth=1,
                          alpha=0.8)
            
            # Add value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax2.text(bar.get_x() + bar.get_width()/2., height,
                            f'PKR{height:,.0f}',
                            ha='center', va='bottom',
                            fontsize=10, fontweight='bold')
            
            ax2.set_ylabel('Amount (PKR)', fontsize=12, fontweight='bold')
            ax2.set_title('Expense Comparison', fontsize=14, fontweight='bold', pad=20)
            ax2.tick_params(axis='x', rotation=15)
            ax2.grid(axis='y', alpha=0.3, linestyle='--')
            
            # Add a horizontal line for average expense
            avg_expense = np.mean(expense_values) if len(expense_values) > 0 else 0
            if avg_expense > 0:
                ax2.axhline(y=avg_expense, color='red', linestyle='--', 
                           alpha=0.5, label=f'Average: PKR{avg_expense:,.0f}')
                ax2.legend()
        else:
            ax2.text(0.5, 0.5, 'No expenses to display', 
                    horizontalalignment='center', 
                    verticalalignment='center',
                    transform=ax2.transAxes,
                    fontsize=14)
            ax2.set_title('Expense Comparison', fontsize=14, fontweight='bold', pad=20)
        
        st.pyplot(fig2)
    
    # -----------------------------------------------
    # 6d. EXPENSE DATA TABLE (For detailed review)
    # -----------------------------------------------
    with st.expander("View Detailed Expense Breakdown"):
        # Create a DataFrame for table display
        expense_data = {
            'Category': expense_categories,
            'Amount (PKR)': expense_values
        }
        df = pd.DataFrame(expense_data)
        df['Percentage of Income'] = (df['Amount (PKR)'] / total_income * 100).round(1).astype(str) + '%'
        
        # Style the DataFrame
        st.dataframe(
            df,
            column_config={
                "Category": "Expense Category",
                "Amount (PKR)": st.column_config.NumberColumn(
                    "Amount (PKR)",
                    format="PKR%.2f"
                ),
                "Percentage of Income": "Percentage of Income"
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Display total summary
        st.caption(f"""
            **Summary:**
            - Total Income: PKR{total_income:,.2f}
            - Total Expenses: PKR{total_expenses:,.2f}
            - Net Savings: PKR{net_savings:,.2f}
            - Savings Rate: {savings_percentage:.1f}%
        """)

# -----------------------------------------------
# 7. FOOTER WITH TIPS
# -----------------------------------------------
st.markdown("---")
st.caption("""
    **Pro Tips:** 
    - Review your budget monthly to track progress.
    - Aim to save at least 20% of your income.
    - Consider using the 50/30/20 rule: 50% needs, 30% wants, 20% savings.
    - Emergency fund: Save 3-6 months of expenses.
""")

# -----------------------------------------------
# END OF APP
# -----------------------------------------------
