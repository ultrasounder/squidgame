import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Generate synthetic ISP data
def generate_synthetic_data(days=30):
    # Generate timestamp index
    dates = pd.date_range(
        start=datetime.now() - timedelta(days=days),
        end=datetime.now(),
        freq='5min'
    )
    
    # Create base DataFrame
    df = pd.DataFrame(index=dates)
    
    # Add traffic patterns with daily and weekly seasonality
    hourly_pattern = np.sin(np.pi * df.index.hour / 24) + 1
    weekly_pattern = 1 - (0.3 * (df.index.dayofweek // 5))  # Lower traffic on weekends
    
    # Generate traffic data - Fixed the clip issue
    base_traffic = np.array(50 +  # Base traffic
        30 * hourly_pattern +  # Daily pattern
        10 * weekly_pattern +  # Weekly pattern
        5 * np.random.normal(0, 1, len(df)))  # Random noise
    
    df['traffic_gbps'] = np.clip(base_traffic, 0, None)
    
    # Generate cache performance metrics
    df['cache_hit_rate'] = 0.95 + 0.03 * np.random.random(len(df))
    df['response_time_ms'] = 15 + 5 * np.random.random(len(df))
    
    # Calculate derived metrics
    df['transit_savings_gbps'] = df['traffic_gbps'] * df['cache_hit_rate']
    df['cost_savings'] = df['transit_savings_gbps'] * 0.02  # Assume $0.02 per GB transit cost
    
    return df

# Calculate key metrics
def calculate_metrics(df):
    metrics = {
        'peak_traffic': df['traffic_gbps'].max(),
        'p95_traffic': df['traffic_gbps'].quantile(0.95),
        'avg_cache_hit': df['cache_hit_rate'].mean(),
        'total_savings': df['cost_savings'].sum(),
        'avg_response': df['response_time_ms'].mean()
    }
    return metrics

# Create visualizations
def create_dashboard(df):
    # Create subplot figure
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            'Traffic Pattern', 'Cache Hit Rate',
            'Response Time', 'Cost Savings',
            'Traffic Distribution', 'Daily Pattern'
        )
    )
    
    # Traffic pattern
    fig.add_trace(
        go.Scatter(x=df.index, y=df['traffic_gbps'],
                  name='Traffic', line_color='#e50914'),
        row=1, col=1
    )
    
    # Cache hit rate
    fig.add_trace(
        go.Scatter(x=df.index, y=df['cache_hit_rate'],
                  name='Cache Hits', line_color='#3b82f6'),
        row=1, col=2
    )
    
    # Response time
    fig.add_trace(
        go.Scatter(x=df.index, y=df['response_time_ms'],
                  name='Response Time', line_color='#10b981'),
        row=2, col=1
    )
    
    # Cost savings
    fig.add_trace(
        go.Scatter(x=df.index, y=df['cost_savings'].cumsum(),
                  name='Cumulative Savings', line_color='#8b5cf6'),
        row=2, col=2
    )
    
    # Traffic distribution
    fig.add_trace(
        go.Histogram(x=df['traffic_gbps'], nbinsx=50,
                    name='Traffic Dist', marker_color='#e50914'),
        row=3, col=1
    )
    
    # Daily pattern
    daily_pattern = df.groupby(df.index.hour)['traffic_gbps'].mean()
    fig.add_trace(
        go.Scatter(x=daily_pattern.index, y=daily_pattern.values,
                  name='Daily Pattern', line_color='#3b82f6'),
        row=3, col=2
    )
    
    # Update layout
    fig.update_layout(
        height=1200,
        title_text='ISP Network Analytics Dashboard',
        showlegend=False
    )
    
    return fig

# Main execution
if __name__ == "__main__":
    # Generate data
    df = generate_synthetic_data()
    
    # Calculate metrics
    metrics = calculate_metrics(df)
    
    # Create dashboard
    fig = create_dashboard(df)
    
    # Save metrics to CSV
    pd.DataFrame([metrics]).to_csv('isp_metrics.csv')
    
    # Save dashboard
    fig.write_html('isp_dashboard.html')