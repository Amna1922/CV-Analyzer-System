# cv_analyzer_gui.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os
from cv_analyzer_enhanced import EnhancedCVAnalyzer

class CVAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced CV Analyzer")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        self.analyzer = EnhancedCVAnalyzer()
        self.current_results = None
        self.performance_df = None
        
        self.setup_gui()
    
    def setup_gui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = tk.Label(main_frame, text="Enhanced CV Analyzer", 
                              font=('Arial', 16, 'bold'), 
                              bg='#f0f0f0', fg='#2c3e50')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        # CV Directory selection
        ttk.Label(file_frame, text="CV Directory:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.cv_dir_var = tk.StringVar(value="data/cvs")
        ttk.Entry(file_frame, textvariable=self.cv_dir_var, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E))
        ttk.Button(file_frame, text="Browse", command=self.browse_cv_dir).grid(row=0, column=2, padx=(10, 0))
        
        # Job Description selection
        ttk.Label(file_frame, text="Job Description:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.job_file_var = tk.StringVar(value="data/job_descriptions/job_data_scientist.txt")
        ttk.Entry(file_frame, textvariable=self.job_file_var, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(10, 0))
        ttk.Button(file_frame, text="Browse", command=self.browse_job_file).grid(row=1, column=2, padx=(10, 0), pady=(10, 0))
        
        # Algorithm selection
        ttk.Label(file_frame, text="Algorithm:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.algorithm_var = tk.StringVar(value="KMP")
        algorithm_combo = ttk.Combobox(file_frame, textvariable=self.algorithm_var, 
                                      values=["Brute Force", "KMP", "Rabin-Karp"], 
                                      state="readonly", width=47)
        algorithm_combo.grid(row=2, column=1, sticky=tk.W, pady=(10, 0))
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=(0, 20))
        
        ttk.Button(button_frame, text="Analyze CVs", 
                  command=self.analyze_cvs, style='Accent.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Compare Algorithms", 
                  command=self.compare_algorithms).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Performance Analysis", 
                  command=self.performance_analysis).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Generate Report", 
                  command=self.generate_report).pack(side=tk.LEFT)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Results tab
        self.results_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.results_frame, text="Results")
        
        # Comparison tab
        self.comparison_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.comparison_frame, text="Algorithm Comparison")
        
        # Performance tab
        self.performance_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.performance_frame, text="Performance")
        
        # Visualization tab
        self.viz_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.viz_frame, text="Visualizations")
        
        # Configure main frame grid
        main_frame.rowconfigure(3, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Initialize results display
        self.setup_results_tab()
        self.setup_comparison_tab()
        self.setup_performance_tab()
        self.setup_visualization_tab()
    
    def setup_results_tab(self):
        # Results summary
        summary_frame = ttk.LabelFrame(self.results_frame, text="Analysis Summary", padding="10")
        summary_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.summary_text = scrolledtext.ScrolledText(summary_frame, height=8, width=100)
        self.summary_text.pack(fill=tk.X)
        
        # Candidate ranking
        ranking_frame = ttk.LabelFrame(self.results_frame, text="Candidate Ranking", padding="10")
        ranking_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for candidate results
        columns = ('Rank', 'CV File', 'Score', 'Matches', 'Time', 'Comparisons')
        self.results_tree = ttk.Treeview(ranking_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=100)
        
        self.results_tree.column('CV File', width=200)
        self.results_tree.column('Rank', width=60)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(ranking_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_comparison_tab(self):
        # Algorithm comparison frame
        comp_frame = ttk.Frame(self.comparison_frame)
        comp_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for algorithm comparison
        columns = ('Algorithm', 'Score (%)', 'Matches', 'Time (ms)', 'Comparisons', 'Matched Keywords')
        self.comp_tree = ttk.Treeview(comp_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.comp_tree.heading(col, text=col)
            self.comp_tree.column(col, width=120)
        
        self.comp_tree.column('Matched Keywords', width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(comp_frame, orient=tk.VERTICAL, command=self.comp_tree.yview)
        self.comp_tree.configure(yscrollcommand=scrollbar.set)
        
        self.comp_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_performance_tab(self):
        # Performance metrics frame
        perf_frame = ttk.Frame(self.performance_frame)
        perf_frame.pack(fill=tk.BOTH, expand=True)
        
        self.perf_text = scrolledtext.ScrolledText(perf_frame, height=20, width=100)
        self.perf_text.pack(fill=tk.BOTH, expand=True)
    
    def setup_visualization_tab(self):
        # Visualization frame
        viz_frame = ttk.Frame(self.viz_frame)
        viz_frame.pack(fill=tk.BOTH, expand=True)
        
        self.viz_text = tk.Label(viz_frame, text="Visualizations will appear here after analysis", 
                                font=('Arial', 12), fg='gray')
        self.viz_text.pack(expand=True)
        
        self.canvas_frame = ttk.Frame(viz_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
    
    def browse_cv_dir(self):
        directory = filedialog.askdirectory(initialdir="data/cvs")
        if directory:
            self.cv_dir_var.set(directory)
    
    def browse_job_file(self):
        filename = filedialog.askopenfilename(
            initialdir="data/job_descriptions",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.job_file_var.set(filename)
    
    def analyze_cvs(self):
        try:
            cv_directory = self.cv_dir_var.get()
            job_file = self.job_file_var.get()
            algorithm = self.algorithm_var.get()
            
            if not os.path.exists(cv_directory):
                messagebox.showerror("Error", "CV directory does not exist!")
                return
            
            if not os.path.exists(job_file):
                messagebox.showerror("Error", "Job description file does not exist!")
                return
            
            # Clear previous results
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)
            self.summary_text.delete(1.0, tk.END)
            
            # Perform analysis
            self.current_results = self.analyzer.analyze_multiple_cvs(cv_directory, job_file, algorithm)
            
            if 'error' in self.current_results:
                messagebox.showerror("Error", self.current_results['error'])
                return
            
            # Display summary
            summary = f"Job Description: {self.current_results['job_description']}\n"
            summary += f"Algorithm: {self.current_results['algorithm']}\n"
            summary += f"Total CVs Analyzed: {self.current_results['total_cvs_analyzed']}\n"
            summary += f"Keywords: {', '.join(self.current_results['keywords'][:5])}"
            if len(self.current_results['keywords']) > 5:
                summary += f"... (and {len(self.current_results['keywords']) - 5} more)"
            
            self.summary_text.insert(tk.END, summary)
            
            # Display candidate ranking
            for i, result in enumerate(self.current_results['results'], 1):
                self.results_tree.insert('', 'end', values=(
                    i,
                    result['cv_file'],
                    f"{result['score']:.1f}%",
                    f"{result['matched_count']}/{result['total_keywords']}",
                    f"{result['execution_time_ms']:.2f}ms",
                    result['total_comparisons']
                ))
            
            messagebox.showinfo("Success", f"Analysis completed! {len(self.current_results['results'])} CVs analyzed.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
    
    def compare_algorithms(self):
        try:
            cv_directory = self.cv_dir_var.get()
            job_file = self.job_file_var.get()
            
            cv_files = [f for f in os.listdir(cv_directory) if f.lower().endswith('.docx')]
            if not cv_files:
                messagebox.showerror("Error", "No .docx files found in CV directory!")
                return
            
            test_cv = os.path.join(cv_directory, cv_files[0])
            
            # Clear previous comparison
            for item in self.comp_tree.get_children():
                self.comp_tree.delete(item)
            
            # Perform comparison
            comparison_df = self.analyzer.compare_algorithms_single_cv(test_cv, job_file)
            
            # Display results
            for _, row in comparison_df.iterrows():
                matched_keywords = ', '.join(row['Matched Keywords'][:3])
                if len(row['Matched Keywords']) > 3:
                    matched_keywords += '...'
                
                self.comp_tree.insert('', 'end', values=(
                    row['Algorithm'],
                    row['Score (%)'],
                    row['Matches'],
                    row['Time (ms)'],
                    row['Comparisons'],
                    matched_keywords
                ))
            
            self.notebook.select(1)  # Switch to comparison tab
            messagebox.showinfo("Success", "Algorithm comparison completed!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Comparison failed: {str(e)}")
    
    def performance_analysis(self):
        try:
            cv_directory = self.cv_dir_var.get()
            job_file = self.job_file_var.get()
            
            # Clear previous performance data
            self.perf_text.delete(1.0, tk.END)
            
            # Perform performance analysis
            self.performance_df = self.analyzer.performance_analysis(cv_directory, job_file)
            
            if isinstance(self.performance_df, dict) and 'error' in self.performance_df:
                messagebox.showerror("Error", self.performance_df['error'])
                return
            
            # Display performance summary
            self.perf_text.insert(tk.END, "PERFORMANCE ANALYSIS SUMMARY\n")
            self.perf_text.insert(tk.END, "=" * 50 + "\n\n")
            
            # Algorithm performance
            algo_summary = self.performance_df.groupby('Algorithm').agg({
                'Score_Percentage': 'mean',
                'Execution_Time_ms': 'mean',
                'Comparisons': 'mean'
            }).round(2)
            
            self.perf_text.insert(tk.END, "Algorithm Performance:\n")
            self.perf_text.insert(tk.END, str(algo_summary) + "\n\n")
            
            # File size impact
            size_impact = self.performance_df[self.performance_df['Test_Type'] == 'File_Size']
            if not size_impact.empty:
                size_summary = size_impact.groupby(['Size_Category', 'Algorithm'])['Execution_Time_ms'].mean().unstack()
                self.perf_text.insert(tk.END, "\nFile Size Impact on Execution Time (ms):\n")
                self.perf_text.insert(tk.END, str(size_summary) + "\n")
            
            self.notebook.select(2)  # Switch to performance tab
            messagebox.showinfo("Success", "Performance analysis completed!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Performance analysis failed: {str(e)}")
    
    def generate_report(self):
        try:
            if self.current_results is None or self.performance_df is None:
                messagebox.showwarning("Warning", "Please run analysis first!")
                return
            
            # Generate comprehensive report
            self.analyzer.generate_comprehensive_report(self.current_results, self.performance_df)
            
            # Create visualizations
            self.display_visualizations()
            
            messagebox.showinfo("Success", "Comprehensive report generated!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Report generation failed: {str(e)}")
    
    def display_visualizations(self):
        # Clear previous visualizations
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        
        try:
            # Create visualizations
            self.analyzer.create_visualizations(self.performance_df)
            
            # Display the generated image
            if os.path.exists('data/results/performance_visualizations.png'):
                import matplotlib.image as mpimg
                
                fig, ax = plt.subplots(figsize=(10, 8))
                img = mpimg.imread('data/results/performance_visualizations.png')
                ax.imshow(img)
                ax.axis('off')  # Hide axes
                
                # Embed in tkinter
                canvas = FigureCanvasTkAgg(fig, self.canvas_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
                self.notebook.select(3)  # Switch to visualization tab
                
        except Exception as e:
            self.viz_text.config(text=f"Error creating visualizations: {str(e)}")

def main():
    root = tk.Tk()
    app = CVAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()