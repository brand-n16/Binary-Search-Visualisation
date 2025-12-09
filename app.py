import gradio as gr
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random
import io
from PIL import Image

# ============================================================================
# ALGORITHM CLASS - Isolated binary search logic
# ============================================================================

class BinarySearchAlgorithm:
    """
    Binary Search algorithm implementation that generates step-by-step states
    for visualization purposes. This class is independent of the UI.
    """
    
    def __init__(self, array, target):
        """
        Initialize the binary search algorithm.
        
        Args:
            array: Sorted list of integers
            target: Integer value to search for
        """
        self.array = array
        self.target = target
        self.steps = []  # Will store each step's state
        self.comparisons = 0
        self.found = False
        self.found_index = -1
        
    def execute(self):
        """
        Execute binary search and record each step.
        
        Returns:
            List of step dictionaries containing state information
        """
        left = 0
        right = len(self.array) - 1
        
        # Initial state
        self.steps.append({
            'left': left,
            'right': right,
            'mid': None,
            'comparison': None,
            'message': f"Starting search for {self.target} in array of size {len(self.array)}",
            'status': 'searching'
        })
        
        while left <= right:
            mid = (left + right) // 2
            mid_value = self.array[mid]
            self.comparisons += 1
            
            # Record comparison step
            if mid_value == self.target:
                self.found = True
                self.found_index = mid
                self.steps.append({
                    'left': left,
                    'right': right,
                    'mid': mid,
                    'comparison': 'equal',
                    'message': f"Step {self.comparisons}: Found! Array[{mid}] = {mid_value} equals target {self.target}",
                    'status': 'found'
                })
                break
            elif mid_value < self.target:
                self.steps.append({
                    'left': left,
                    'right': right,
                    'mid': mid,
                    'comparison': 'less',
                    'message': f"Step {self.comparisons}: Array[{mid}] = {mid_value} < {self.target}. Searching right half.",
                    'status': 'searching'
                })
                left = mid + 1
            else:
                self.steps.append({
                    'left': left,
                    'right': right,
                    'mid': mid,
                    'comparison': 'greater',
                    'message': f"Step {self.comparisons}: Array[{mid}] = {mid_value} > {self.target}. Searching left half.",
                    'status': 'searching'
                })
                right = mid - 1
        
        # If not found
        if not self.found:
            self.steps.append({
                'left': left,
                'right': right,
                'mid': None,
                'comparison': None,
                'message': f"Search complete: {self.target} not found in array after {self.comparisons} comparisons",
                'status': 'not_found'
            })
        
        return self.steps

# ============================================================================
# VISUALIZATION ENGINE - Separated from algorithm logic using Matplotlib
# ============================================================================

class BinarySearchVisualizer:
    """
    Handles visualization of binary search steps using Matplotlib.
    This is independent of the algorithm implementation.
    """
    
    def __init__(self):
        self.colors = {
            'default': '#1f3a93',      # Navy blue for regular elements
            'eliminated': '#d3d3d3',    # Grey for eliminated sections
            'current': '#ffd700',       # Yellow for current middle element
            'found': '#32cd32'          # Green for found target
        }
    
    def create_bar_chart(self, array, step_data):
        """
        Create a Matplotlib bar chart showing the current search state.
        
        Args:
            array: The sorted array being searched
            step_data: Dictionary containing current step information
            
        Returns:
            PIL Image object
        """
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Determine color for each bar based on current step
        colors = []
        for i in range(len(array)):
            if step_data['status'] == 'found' and i == step_data['mid']:
                colors.append(self.colors['found'])  # Target found
            elif step_data['mid'] is not None and i == step_data['mid']:
                colors.append(self.colors['current'])  # Current middle element
            elif step_data['left'] is not None and step_data['right'] is not None:
                if i < step_data['left'] or i > step_data['right']:
                    colors.append(self.colors['eliminated'])  # Outside search range
                else:
                    colors.append(self.colors['default'])  # In search range
            else:
                colors.append(self.colors['default'])
        
        # Create bars
        indices = list(range(len(array)))
        bars = ax.bar(indices, array, color=colors, edgecolor='black', linewidth=1.5)
        
        # Add value labels on top of bars
        for i, (bar, value) in enumerate(zip(bars, array)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{value}',
                   ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # Customize plot
        status_title = step_data['status'].replace('_', ' ').title()
        ax.set_title(f'Binary Search Visualization - {status_title}', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Array Index', fontsize=12, fontweight='bold')
        ax.set_ylabel('Value', fontsize=12, fontweight='bold')
        ax.set_xticks(indices)
        ax.set_xticklabels(indices)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Set y-axis limits with some padding
        if array:
            ax.set_ylim(0, max(array) * 1.15)
        
        # Add legend
        legend_elements = [
            mpatches.Patch(color=self.colors['default'], label='In Search Range'),
            mpatches.Patch(color=self.colors['eliminated'], label='Eliminated'),
            mpatches.Patch(color=self.colors['current'], label='Current Middle'),
            mpatches.Patch(color=self.colors['found'], label='Target Found')
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
        
        plt.tight_layout()
        
        # Convert to PIL Image
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img = Image.open(buf)
        plt.close(fig)
        
        return img

# ============================================================================
# GRADIO APPLICATION - UI and State Management
# ============================================================================

class BinarySearchApp:
    """
    Main application class that manages the Gradio interface and coordinates
    between the algorithm and visualization components.
    """
    
    def __init__(self):
        self.current_array = []
        self.current_target = None
        self.algorithm = None
        self.visualizer = BinarySearchVisualizer()
        self.current_step = 0
        self.all_steps = []
        self.is_playing = False
        
    def generate_array(self, size, guarantee_target, target_value):
        """
        Generate a sorted random array.
        
        Args:
            size: Number of elements in array
            guarantee_target: Boolean - if True, ensure target is in array
            target_value: The target value to search for
            
        Returns:
            Tuple: (array, status_message)
        """
        # Generate sorted random array
        self.current_array = sorted(random.sample(range(1, 101), int(size)))
        
        # If guarantee_target is True, replace a random element with target
        if guarantee_target and int(target_value) not in self.current_array:
            random_index = random.randint(0, int(size) - 1)
            self.current_array[random_index] = int(target_value)
            self.current_array.sort()  # Re-sort after insertion
        
        return self.current_array, f"Generated sorted array of size {int(size)}"
    
    def initialize_search(self, array, target):
        """
        Initialize a new search with the given array and target.
        
        Args:
            array: Sorted array to search
            target: Target value to find
            
        Returns:
            Tuple: (image, stats_text, log_text, step_info)
        """
        if not array:
            return None, "Please generate an array first", "", "Step 0 of 0"
        
        self.current_target = int(target)
        self.algorithm = BinarySearchAlgorithm(array, int(target))
        self.all_steps = self.algorithm.execute()
        self.current_step = 0
        
        # Display initial state
        return self.display_current_step()
    
    def display_current_step(self):
        """
        Display the current step of the search.
        
        Returns:
            Tuple: (image, stats_text, log_text, step_info)
        """
        if not self.all_steps:
            return None, "No search initialized", "", "Step 0 of 0"
        
        step_data = self.all_steps[self.current_step]
        
        # Create visualization
        img = self.visualizer.create_bar_chart(self.current_array, step_data)
        
        # Create statistics text
        stats = f"""**Statistics:**
- Comparisons so far: {self.current_step}
- Current search range: [{step_data.get('left', 'N/A')}, {step_data.get('right', 'N/A')}]
- Time Complexity: O(log n)
- Array size (n): {len(self.current_array)}
"""
        
        # Create step log (show all steps up to current)
        log_lines = []
        for i in range(self.current_step + 1):
            log_lines.append(self.all_steps[i]['message'])
        log_text = "\n".join(log_lines)
        
        # Step counter
        step_info = f"Step {self.current_step + 1} of {len(self.all_steps)}"
        
        return img, stats, log_text, step_info
    
    def next_step(self):
        """Move to next step in the search."""
        if self.current_step < len(self.all_steps) - 1:
            self.current_step += 1
        else:
            self.is_playing = False  # Stop auto-play at end
        return self.display_current_step()
    
    def previous_step(self):
        """Move to previous step in the search."""
        if self.current_step > 0:
            self.current_step -= 1
        return self.display_current_step()
    
    def reset_search(self):
        """Reset to the beginning of the current search."""
        self.current_step = 0
        if self.all_steps:
            return self.display_current_step()
        return None, "No search to reset", "", "Step 0 of 0"
    
    def toggle_auto_play(self):
        """Toggle auto-play on/off."""
        self.is_playing = not self.is_playing
        return "Stop Auto-Play" if self.is_playing else "Start Auto-Play"
    
    def auto_play_step(self):
        """Execute one step of auto-play and return whether to continue."""
        if not self.is_playing:
            return self.display_current_step() + (False,)
        
        if self.current_step < len(self.all_steps) - 1:
            self.current_step += 1
            result = self.display_current_step()
            return result + (True,)  # Continue playing
        else:
            self.is_playing = False
            result = self.display_current_step()
            return result + (False,)  # Stop playing

# ============================================================================
# GRADIO INTERFACE SETUP
# ============================================================================

def create_interface():
    """Create and configure the Gradio interface."""
    
    app = BinarySearchApp()
    
    with gr.Blocks(title="Binary Search Visualizer") as interface:
        gr.Markdown("""
        # Binary Search Algorithm Visualizer
        Interactive step-by-step visualization of the Binary Search algorithm
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Controls")
                
                # Array generation controls
                array_size = gr.Slider(
                    minimum=10, 
                    maximum=50, 
                    value=20, 
                    step=1, 
                    label="Array Size"
                )
                
                target_input = gr.Number(
                    value=50, 
                    label="Target Value to Search",
                    minimum=1,
                    maximum=100
                )
                
                guarantee_target = gr.Checkbox(
                    label="Guarantee target exists in array",
                    value=True
                )
                
                generate_btn = gr.Button("Generate New Array", variant="primary")
                
                array_display = gr.JSON(label="Current Array", value=[])
                
                gr.Markdown("---")
                
                # Search controls
                start_search_btn = gr.Button("Start Search", variant="primary")
                
                with gr.Row():
                    prev_btn = gr.Button("Previous")
                    next_btn = gr.Button("Next")
                
                reset_btn = gr.Button("Reset")
                
                speed_slider = gr.Slider(
                    minimum=0.5,
                    maximum=2.0,
                    value=1.0,
                    step=0.5,
                    label="Animation Speed",
                    info="Speed multiplier for auto-play"
                )
                
                auto_play_btn = gr.Button("Auto-Play to End")
                
            with gr.Column(scale=2):
                gr.Markdown("### Visualization")
                
                step_counter = gr.Textbox(
                    label="Progress",
                    value="Step 0 of 0",
                    interactive=False
                )
                
                plot_output = gr.Image(label="Binary Search State", type="pil")
                
                stats_output = gr.Markdown("**Statistics:** No search running")
                
                gr.Markdown("### Step-by-Step Log")
                log_output = gr.Textbox(
                    label="Search Log",
                    lines=8,
                    max_lines=15,
                    interactive=False
                )
        
        # Event handlers
        def generate_array_handler(size, guarantee, target):
            array, message = app.generate_array(size, guarantee, target)
            return array, message
        
        generate_btn.click(
            fn=generate_array_handler,
            inputs=[array_size, guarantee_target, target_input],
            outputs=[array_display, stats_output]
        )
        
        start_search_btn.click(
            fn=lambda target: app.initialize_search(app.current_array, target),
            inputs=[target_input],
            outputs=[plot_output, stats_output, log_output, step_counter]
        )
        
        # Update target value when changed
        target_input.change(
            fn=lambda t: setattr(app, 'current_target', int(t)) or t,
            inputs=[target_input],
            outputs=[]
        )
        
        next_btn.click(
            fn=app.next_step,
            inputs=[],
            outputs=[plot_output, stats_output, log_output, step_counter]
        )
        
        prev_btn.click(
            fn=app.previous_step,
            inputs=[],
            outputs=[plot_output, stats_output, log_output, step_counter]
        )
        
        reset_btn.click(
            fn=app.reset_search,
            inputs=[],
            outputs=[plot_output, stats_output, log_output, step_counter]
        )
        
        # Auto-play functionality - simpler approach
        def run_auto_play(speed):
            """Run through all remaining steps automatically."""
            import time
            results = []
            while app.all_steps and app.current_step < len(app.all_steps) - 1:
                app.current_step += 1
                time.sleep(1.0 / speed)
                yield app.display_current_step()
            
            # Final state
            yield app.display_current_step()
        
        auto_play_btn.click(
            fn=run_auto_play,
            inputs=[speed_slider],
            outputs=[plot_output, stats_output, log_output, step_counter]
        )
    
    return interface

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    interface = create_interface()
    interface.launch()