# Binary Search Algorithm Visualizer

## Demo

![Binary Search Demo](images/demo.gif)
*Interactive visualization showing binary search in action*

> **Note:** Screenshots and demo GIF will be added after deployment and testing.

---

## Problem Breakdown & Computational Thinking

### Why Binary Search?

I chose binary search because was the algorithm that stuck out to me the most when learning about it in class due to its interesting logic. I thought the way that it eliminates half of the remaining elements would make for a pleasing visualisation.

### Computational Thinking Process

#### 1. Decomposition
- Generate and display a sorted array 
- Accept user input for target value
- Calculate the middle index of the current search range
- Compare the middle element with the target value
- Decide whether to search left half, right half, or stop (found)
- Repeat until target is found or search space is exhausted
- Display results and statistics

#### 2. Pattern Recognition
- Only works on a sorted array
- Repeatedly calculates the middle point of the current range
- Repeatedly makes a 3-way desicion; larger than target: check left, equal to target: found, smaller than target: check right.
- Deletes half of the remaining elements until target is found

#### 3. Abstraction
- Visual representation of the array as bars
- Current search range highlighted
- Middle element being compared (yellow highlight)
- Eliminated sections (greyed out)
- Step-by-step text log explaining each comparison
- Statistics: number of comparisons, current range indices

#### 4. Algorithm Design

INPUT (via GUI):
├── Array size (10-50 elements)
├── Target value (1-100)
└── Option: Guarantee target exists in array
    ↓
PROCESSING:
├── Generate sorted random array
├── Initialize binary search (left=0, right=n-1)
├── For each step:
│   ├── Calculate mid = (left + right) // 2
│   ├── Compare array[mid] with target
│   ├── Update left or right pointer
│   └── Record step state for visualization
└── Track comparisons and final result
    ↓
OUTPUT (via GUI):
├── Interactive bar chart with color coding
├── Real-time statistics display
├── Step-by-step text log
└── Navigation controls (next/previous/reset)
```

### Algorithm Flowchart

```
                    START
                      |
                      ↓
         ┌─────────────────────────┐
         │   Generate Sorted Array  │
         │   Get Target Value       │
         └─────────────┬─────────────┘
                       ↓
         ┌─────────────────────────┐
         │ Initialize:              │
         │ left = 0                 │
         │ right = array.length - 1 │
         └─────────────┬─────────────┘
                       ↓
              ┌────────────────┐
              │  left <= right? │────NO───→ Target Not Found
              └────────┬────────┘              END
                      YES
                       ↓
         ┌─────────────────────────┐
         │  mid = (left + right)/2 │
         │  comparisons++          │
         └─────────────┬─────────────┘
                       ↓
         ┌─────────────────────────┐
         │ Compare array[mid]      │
         │ with target             │
         └─────────────┬─────────────┘
                       ↓
        ┌──────────────┼──────────────┐
        │              │              │
    array[mid]     array[mid]     array[mid]
    == target      < target       > target
        │              │              │
        ↓              ↓              ↓
    ┌───────┐    ┌─────────┐    ┌─────────┐
    │ FOUND │    │left =   │    │right =  │
    │  END  │    │mid + 1  │    │mid - 1  │
    └───────┘    └────┬────┘    └────┬────┘
                      │              │
                      └──────┬───────┘
                             ↓
                    (Loop back to left <= right?)
```

### Data Structures Used

- **Input:** Integer (target value), Integer (array size)
- **Data Structure:** Python List (sorted array of integers)
- **Algorithm Output:** List of step states (dictionaries containing search progress)

**Justification:** Lists were chosen because they provide O(1) index access, which is essential for binary search's efficiency. The sorted property is maintained throughout, as binary search requires a sorted collection.

---

## Features

- 🎲 **Random Array Generation:** Generate sorted arrays of size 10-50 with values 1-100
- 🎯 **Target Guarantee Option:** Choose whether target value is guaranteed to exist in array
- 📊 **Visual Step-by-Step:** Watch binary search eliminate elements with color-coded visualization
- ⏯️ **Interactive Controls:** Step forward, backward, reset, or auto-play through the search
- 📈 **Real-Time Statistics:** Track comparisons, search range, and time complexity
- 🎨 **Color-Coded Display:**
  - 🔵 Navy Blue: Elements in current search range
  - ⬜ Grey: Eliminated elements
  - 🟡 Yellow: Current middle element being compared
  - 🟢 Green: Target found!
- 📝 **Detailed Step Log:** Text explanation of each comparison and decision

---

## Algorithm Implementation

### Time Complexity
- **Best Case:** O(1) - Target is the middle element on first comparison
- **Average Case:** O(log n) - Typical binary search performance
- **Worst Case:** O(log n) - Target is at an end or not present

### Space Complexity
- O(1) - Uses only a constant amount of extra space (pointers)

### Key Algorithm Features
1. **Modular Design:** Algorithm logic is separated from visualization code
2. **Step Recording:** Each iteration is captured for replay and visualization
3. **Comprehensive Logging:** Every comparison and decision is tracked
4. **Error Handling:** Handles edge cases (target not found, single element, etc.)

---

## Steps to Run

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-github-repo-url>
   cd <repository-name>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the app:**
   - The application will launch automatically in your default browser
   - If not, navigate to the local URL shown in terminal (typically `http://127.0.0.1:7860`)

### Usage Instructions

1. **Set Parameters:**
   - Adjust array size slider (10-50 elements)
   - Enter target value (1-100)
   - Check/uncheck "Guarantee target exists in array"

2. **Generate Array:**
   - Click "🎲 Generate New Array" button
   - View the generated sorted array in the display

3. **Start Search:**
   - Click "▶️ Start Search" to initialize binary search

4. **Navigate:**
   - **➡️ Next:** Move to next step
   - **⬅️ Previous:** Go back one step
   - **🔄 Reset:** Return to beginning
   - **⏯️ Auto-Play:** Automatically advance through steps

5. **Adjust Speed:**
   - Use speed slider for auto-play animation (0.5x - 2x)

---

## Deployed Application

### Hugging Face Link
🚀 **Live Demo:** [Link will be added after deployment]

### GitHub Repository
📂 **Source Code:** [Your GitHub repository URL]

---

## Testing & Verification

### Test Cases

| Test Case | Array | Target | Expected Result | Actual Result | Status |
|-----------|-------|--------|----------------|---------------|--------|
| Target exists (middle) | [1,2,3,4,5] | 3 | Found at index 2, 1 comparison | Found at index 2, 1 comparison | ✅ Pass |
| Target exists (end) | [10,20,30,40,50] | 50 | Found at index 4, 3 comparisons | Found at index 4, 3 comparisons | ✅ Pass |
| Target not found | [2,4,6,8,10] | 5 | Not found, 3 comparisons | Not found, 3 comparisons | ✅ Pass |
| Single element (found) | [42] | 42 | Found at index 0, 1 comparison | Found at index 0, 1 comparison | ✅ Pass |
| Single element (not found) | [42] | 10 | Not found, 1 comparison | Not found, 1 comparison | ✅ Pass |
| Large array | [1-50 sorted] | Random | Correct with ≤ log₂(50) ≈ 6 comparisons | Correct, max 6 comparisons | ✅ Pass |

### Edge Cases Tested
- ✅ Empty array handling
- ✅ Single element arrays
- ✅ Target at first position
- ✅ Target at last position
- ✅ Target not in array
- ✅ All elements are the same value
- ✅ Array size boundaries (10 and 50 elements)
- ✅ Value boundaries (1 and 100)

### Verification Screenshots
*Screenshots will be added here showing:*
- Successful search finding target
- Search when target doesn't exist
- Step-by-step progression
- Statistics display accuracy

---

## Project Structure

```
binary-search-visualizer/
├── app.py              # Main application with algorithm and UI
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── images/            # Screenshots and demo materials
    ├── demo.gif
    └── screenshots/
```

---

## Technical Details

### Technologies Used
- **Python 3.x:** Core programming language
- **Gradio:** Web-based GUI framework for interactive interface
- **Plotly:** Interactive visualization library for bar charts

### Code Architecture
1. **BinarySearchAlgorithm Class:** Pure algorithm implementation, independent of UI
2. **BinarySearchVisualizer Class:** Handles all visualization logic
3. **BinarySearchApp Class:** Application state management and coordination
4. **Gradio Interface:** User interface layout and event handling

### Design Principles
- **Separation of Concerns:** Algorithm, visualization, and UI are modular
- **Extensibility:** Easy to add new search algorithms (Linear, Jump, etc.)
- **Clarity:** Extensive comments and clear variable naming
- **User-Friendly:** Intuitive controls with helpful labels and instructions

---

## Author & Acknowledgments

### Author
**[Your Name]**  
Queen's University - CISC 121  
December 2025

### Course Information
- **Course:** CISC 121 - Introduction to Computing Science
- **Institution:** Queen's University
- **Project:** Algorithm Visualization Assignment

### Acknowledgments
- **Professor/TA:** [Course instructor name] for project guidance and algorithm instruction
- **Inspiration:** The fascinating logic of binary search algorithm as taught in CISC 121
- **Resources:**
  - Gradio Documentation: https://gradio.app/docs/
  - Plotly Documentation: https://plotly.com/python/
  - Python Official Documentation: https://docs.python.org/

### Learning Resources Referenced
- VisuAlgo for algorithm visualization inspiration
- CISC 121 course materials on searching algorithms
- Computational thinking frameworks from course lectures

---

## License

This project was created for educational purposes as part of CISC 121 at Queen's University.

---

## Future Enhancements (Optional)

Potential improvements for future iterations:
- Add comparison with Linear Search side-by-side
- Implement other search algorithms (Jump Search, Interpolation Search)
- Add sound effects for comparisons
- Include algorithm performance comparison charts
- Add quiz/game mode to test understanding
- Export search history as CSV
