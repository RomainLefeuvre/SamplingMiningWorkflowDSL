<a id="readme-top"></a>




<!-- PROJECT LOGO -->
<br />
<div align="center">
    <img src=".logo.png" alt="Logo" width="300" height="300">
  </a>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-repository">About The Repository</a>
      <ul>
        <li><a href="#project-structure">Project Structure</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
  
  </ol>
</details>



## About The Repository

This repository provides a Python internal DSL (Domain Specific Language) to model sampling workflows for MSR (Mining Software Repositories) studies. The DSL offers a structured and intuitive approach to define, execute, and analyze complex data sampling and processing workflows commonly used in software engineering research.

### Project Structure

```
PythonWorkflowDSL/
├── pyproject.toml                                    # Python package configuration
├── README.md                                         # Project documentation
└── src/
    └── sampling_mining_workflows_dsl/               # Main DSL package
        ├── __init__.py                              # Package initialization
        ├── CompleteWorkflow.py                      # Complete workflow implementation
        ├── toolbox.py                               # Utility functions and tools
        ├── Workflow.py                              # Core workflow class
        ├── WorkflowBuilder.py                       # Builder pattern for workflows
        ├── analysis/                                # Statistical analysis modules
        │   └── ...                                  # Chi-square, coverage, distribution analysis
        ├── constraint/                              # Constraint system
        │   └── ...                                  # Boolean constraints and comparators
        ├── element/                                 # Data element management
        │   ├── loader/                             # Data loader implementations
        │   └── writer/                             # Data writer implementations
        ├── exec_visualizer/                        # Execution visualization
        │   └── ...                                  # Local server and visualization tools
        ├── swh/                                    # Software heritage integration
        │   └── ...                                  # SEART data loader and metadata
        ├── metadata/                               # Metadata system
        │   └── ...                                  # Boolean, date, string metadata types
        ├── operator/                               # Workflow operators
        │   ├── clustering/                         # Clustering operators
        │   ├── selection/                          # Selection operators (filter/sampling)
        │   └── set_algebra/                        # Set algebra operations
       
```



## Getting Started

### Prerequisites

Before using this DSL, ensure you have Python 3.8+ installed on your system.

### Installation

1. Clone this repository:
   ```bash
   git clone ...
   cd SamplingMiningWorkflowDSL
   ```

2. Install the DSL package (dependencies will be installed automatically):
   ```bash
   pip install .
   ```

3. Install in development mode (optional):
   ```bash
   pip install -e .
   ```


<p align="right">(<a href="#readme-top">back to top</a>)</p>


