# your_app/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, JsonResponse
from django.utils.html import format_html
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns  # <-- IMPORT SEABORN
import io
import base64
import json
import numpy as np

# (create_preview_table and other helpers remain the same)
def create_preview_table(df):
    """
    Creates a combined HTML table with the head, a separator, and the tail.
    Now includes data-column-name attributes in the header for JS interactivity.
    """
    if len(df) <= 11:
        return df.to_html(classes='dataframe', border=0, justify='left', index=True)
    
    head = df.head(5)
    tail = df.tail(5)

    head_html_body = head.to_html(header=False, index=True, border=0).split('<tbody>')[1].split('</tbody>')[0]
    tail_html_body = tail.to_html(header=False, index=True, border=0).split('<tbody>')[1].split('</tbody>')[0]
    
    header_row_cells = f'<th data-column-name="{df.index.name or "index"}"></th>' 
    header_row_cells += ''.join(f'<th data-column-name="{col}">{col}</th>' for col in df.columns)
    full_header = f'<thead><tr>{header_row_cells}</tr></thead>'
    
    num_columns = len(df.columns) + 1
    separator_row = f'<tr id="load-more-row" class="separator-row"><td colspan="{num_columns}"><button id="load-more-btn" class="font-bold text-indigo-600 hover:text-indigo-800 transition-colors">... Load 10 More ...</button></td></tr>'
    
    combined_html = format_html(
        '<table class="dataframe">{}<tbody id="dataframe-body">{} {} {}</tbody></table>',
        format_html(full_header),
        format_html(head_html_body),
        format_html(separator_row),
        format_html(tail_html_body)
    )
    return combined_html, num_columns

def get_column_stats(df):
    stats = {}
    numeric_cols = df.select_dtypes(include=np.number).columns
    desc = df.describe(include='all')
    for col in df.columns:
        stat_list = []
        if col in numeric_cols:
            stat_list.append(f"<b>Type:</b> {df[col].dtype}")
            stat_list.append(f"<b>Mean:</b> {desc[col]['mean']:.2f}")
            stat_list.append(f"<b>Std Dev:</b> {desc[col]['std']:.2f}")
            stat_list.append(f"<b>Min:</b> {desc[col]['min']:.2f}")
            stat_list.append(f"<b>Max:</b> {desc[col]['max']:.2f}")
            stat_list.append(f"<b>Missing:</b> {df[col].isnull().sum()}")
        else: 
            stat_list.append(f"<b>Type:</b> {df[col].dtype}")
            stat_list.append(f"<b>Unique Values:</b> {desc[col]['unique']}")
            stat_list.append(f"<b>Top Value:</b> {desc[col]['top']}")
            stat_list.append(f"<b>Frequency:</b> {desc[col]['freq']}")
            stat_list.append(f"<b>Missing:</b> {df[col].isnull().sum()}")
        stats[col] = "<br>".join(stat_list)
    stats[df.index.name or 'index'] = f"<b>Type:</b> Index<br><b>Entries:</b> {len(df.index)}"
    return stats

# --- NEW HELPER FUNCTION FOR A BEAUTIFUL SUMMARY ---
def generate_dataset_summary(df):
    """
    Generates a dictionary of structured data for the new UI summary component.
    """
    total_rows = len(df)
    total_cols = len(df.columns)
    
    # Memory usage formatted nicely
    mem_usage_bytes = df.memory_usage(deep=True).sum()
    if mem_usage_bytes < 1024**2:
        mem_usage = f"{mem_usage_bytes / 1024:.2f} KB"
    else:
        mem_usage = f"{mem_usage_bytes / (1024**2):.2f} MB"
        
    total_missing = df.isnull().sum().sum()
    
    # Detailed column information
    column_details = []
    for col in df.columns:
        non_null_count = df[col].count()
        percent_filled = (non_null_count / total_rows) * 100 if total_rows > 0 else 0
        column_details.append({
            'name': col,
            'dtype': str(df[col].dtype),
            'non_null_count': non_null_count,
            'percent_filled': round(percent_filled, 2),
        })
        
    summary = {
        'total_rows': total_rows,
        'total_cols': total_cols,
        'memory_usage': mem_usage,
        'total_missing_vals': total_missing,
        'duplicate_rows': df.duplicated().sum(),
        'column_details': column_details,
        'numeric_cols_count': len(df.select_dtypes(include=np.number).columns),
        'categorical_cols_count': len(df.select_dtypes(include=['object', 'category']).columns),
    }
    return summary


def index(request):
    request.session.flush()
    return render(request, "index.html")

def upload_csv(request):
    """
    Handles CSV upload, generates rich analytics, and renders the analysis page.
    """
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            return HttpResponseBadRequest("Invalid file type. Please upload a CSV file.")

        try:
            csv_data = csv_file.read().decode('utf-8')
            request.session['csv_data'] = csv_data
            request.session['csv_filename'] = csv_file.name
            
            df = pd.read_csv(io.StringIO(csv_data))
            request.session['total_rows'] = len(df)

            # --- GENERATE NEW SUMMARY INFO ---
            dataset_summary = generate_dataset_summary(df) # <-- USE THE NEW HELPER
            describe_html = df.describe(include=np.number).to_html(classes='dataframe', border=0, justify='left')
            column_stats = get_column_stats(df)
            combined_html, num_columns = create_preview_table(df)

            numeric_columns = df.select_dtypes(include='number').columns.tolist()
            all_columns = df.columns.tolist()
            
            context = {
                'filename': csv_file.name,
                # New context variable for the summary card
                'summary': dataset_summary,
                # Existing variables
                'describe_html': describe_html,
                'total_rows': len(df),
                'column_stats_json': json.dumps(column_stats),
                'combined_table_html': combined_html,
                'numeric_columns_json': json.dumps(numeric_columns),
                'all_columns_json': json.dumps(all_columns),
            }
            return render(request, 'analysis.html', context)

        except Exception as e:
            return HttpResponseBadRequest(f"Error processing file: {e}. Please ensure it is a valid CSV.")

    return redirect('index')

# The `load_more_rows` and `generate_plot` views remain exactly the same.
# ... (include them here)
def load_more_rows(request):
    # ... same as before
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    csv_data = request.session.get('csv_data')
    if not csv_data:
        return JsonResponse({'error': 'Session expired. Please upload file again.'}, status=404)
    try:
        offset = int(request.POST.get('offset', 5))
        df = pd.read_csv(io.StringIO(csv_data))
        more_rows_df = df.iloc[offset:offset+10]
        if more_rows_df.empty:
            return JsonResponse({'html': '', 'end_of_data': True})
        html_rows = more_rows_df.to_html(header=False, index=True, border=0)
        body_content = html_rows.split('<tbody>')[1].split('</tbody>')[0]
        return JsonResponse({'html': body_content, 'end_of_data': False})
    except Exception as e:
        return JsonResponse({'error': f'Failed to load rows: {e}'}, status=500)

# your_app/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, JsonResponse
from django.utils.html import format_html
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns  # <-- IMPORT SEABORN
import io
import base64
import json
import numpy as np

# --- All other functions (index, upload_csv, helpers) remain the same ---
# ... (create_preview_table, get_column_stats, generate_dataset_summary, index, upload_csv, load_more_rows) ...

def generate_plot(request):
    """
    Generates a plot using data from the session and returns it as a Base64 image.
    NOW WITH MORE PLOT TYPES!
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    csv_data = request.session.get('csv_data')
    if not csv_data:
        return JsonResponse({'error': 'Session expired. Please upload file again.'}, status=404)

    try:
        df = pd.read_csv(io.StringIO(csv_data))
        plot_type = request.POST.get('plot_type')
        
        # Use a consistent, professional style
        sns.set_theme(style="whitegrid")
        fig, ax = plt.subplots(figsize=(10, 6))

        # --- SINGLE NUMERIC COLUMN PLOTS ---
        if plot_type in ['histogram', 'boxplot', 'kde']:
            col = request.POST.get('col')
            if not col: return JsonResponse({'error': 'Column not specified.'}, status=400)
            
            if plot_type == 'histogram':
                sns.histplot(data=df, x=col, bins=20, ax=ax, color='skyblue')
                ax.set_title(f'Histogram of {col}', fontsize=16)
            
            elif plot_type == 'boxplot':
                sns.boxplot(data=df, y=col, ax=ax, color='lightgreen')
                ax.set_title(f'Box Plot of {col}', fontsize=16)
            
            elif plot_type == 'kde':
                sns.kdeplot(data=df, x=col, fill=True, ax=ax, color='coral')
                ax.set_title(f'Kernel Density Estimate of {col}', fontsize=16)

        # --- SINGLE CATEGORICAL COLUMN PLOTS ---
        elif plot_type == 'pie':
            col = request.POST.get('col')
            if not col: return JsonResponse({'error': 'Column not specified.'}, status=400)

            value_counts = df[col].value_counts()
            data_to_plot = value_counts
            # For pie charts, group smaller slices into 'Other' for readability
            if len(value_counts) > 9:
                top_9 = value_counts.nlargest(9)
                other_sum = value_counts.iloc[9:].sum()
                if other_sum > 0:
                    top_9['Other'] = other_sum
                data_to_plot = top_9

            ax.pie(data_to_plot, labels=data_to_plot.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
            ax.set_title(f'Pie Chart for {col}', fontsize=16)
            ax.axis('equal')

        # --- TWO NUMERIC COLUMN PLOTS ---
        elif plot_type in ['line', 'scatter', 'area', 'stem', 'hexbin']:
            x_col, y_col = request.POST.get('x_col'), request.POST.get('y_col')
            if not x_col or not y_col: return JsonResponse({'error': 'X and Y columns not specified.'}, status=400)

            if plot_type == 'line':
                sns.lineplot(data=df, x=x_col, y=y_col, marker='o', ax=ax, color='teal')
                ax.set_title(f'Line Plot of {y_col} vs {x_col}', fontsize=16)
            
            elif plot_type == 'scatter':
                sns.scatterplot(data=df, x=x_col, y=y_col, alpha=0.6, ax=ax, color='tomato')
                ax.set_title(f'Scatter Plot of {y_col} vs {x_col}', fontsize=16)

            elif plot_type == 'hexbin':
                hb = ax.hexbin(df[x_col], df[y_col], gridsize=30, cmap='inferno', mincnt=1)
                fig.colorbar(hb, ax=ax, label='Count in Bin')
                ax.set_title(f'Hexbin Density Plot of {y_col} vs {x_col}', fontsize=16)

            # These are less common, using Matplotlib directly is fine
            elif plot_type == 'area':
                ax.fill_between(df[x_col], df[y_col], color="skyblue", alpha=0.4)
                ax.plot(df[x_col], df[y_col], color="Slateblue", alpha=0.6)
                ax.set_title(f'Area Plot of {y_col} vs {x_col}', fontsize=16)
            
            elif plot_type == 'stem':
                ax.stem(df[x_col], df[y_col], linefmt='grey', markerfmt='D', bottom=0)
                ax.set_title(f'Stem Plot of {y_col} vs {x_col}', fontsize=16)

            ax.set_xlabel(x_col, fontsize=12); ax.set_ylabel(y_col, fontsize=12)
            plt.xticks(rotation=45, ha='right')

        # --- CATEGORICAL vs NUMERIC PLOTS ---
        elif plot_type in ['bar', 'violinplot']:
            x_col, y_col = request.POST.get('x_col'), request.POST.get('y_col')
            if not x_col or not y_col: return JsonResponse({'error': 'Categorical and Numeric columns not specified.'}, status=400)

            if plot_type == 'bar':
                orientation = request.POST.get('bar_orientation', 'vertical')
                if orientation == 'vertical':
                    sns.barplot(data=df, x=x_col, y=y_col, ax=ax, palette='viridis')
                    ax.set_xlabel(x_col, fontsize=12); ax.set_ylabel(y_col, fontsize=12)
                    plt.xticks(rotation=45, ha='right')
                else: # Horizontal
                    sns.barplot(data=df, x=y_col, y=x_col, ax=ax, palette='viridis', orient='h')
                    ax.set_xlabel(y_col, fontsize=12); ax.set_ylabel(x_col, fontsize=12)
                ax.set_title(f'Bar Plot of {y_col} by {x_col}', fontsize=16)

            elif plot_type == 'violinplot':
                sns.violinplot(data=df, x=x_col, y=y_col, ax=ax, palette='muted')
                ax.set_title(f'Violin Plot of {y_col} by {x_col}', fontsize=16)
                plt.xticks(rotation=45, ha='right')
                
        else:
            return JsonResponse({'error': f'Invalid or unknown plot type: {plot_type}'}, status=400)
            
        fig.tight_layout()
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=120) # Increase DPI for better quality
        plt.close(fig)
        buf.seek(0)
        
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return JsonResponse({'image_base64': image_base64})

    except Exception as e:
        # Provide more specific error messages
        import traceback
        traceback.print_exc()
        if isinstance(e, KeyError):
            return JsonResponse({'error': f'Plot generation failed. Column not found: {e}. Please check your selections.'}, status=500)
        return JsonResponse({'error': f'An unexpected error occurred during plot generation: {e}'}, status=500)