<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/RomainLefeuvre/SamplingMiningWorflowDSL">
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
        <li><a href="#key-features">Key Features</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#template-repository">Template Repository</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
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
        ├── metadata/                               # Metadata system
        │   └── ...                                  # Boolean, date, string metadata types
        ├── operator/                               # Workflow operators
        │   ├── clustering/                         # Clustering operators
        │   ├── selection/                          # Selection operators (filter/sampling)
        │   └── set_algebra/                        # Set algebra operations
        └── test/                                   # Test files and examples
            └── ...                                  # JSON test data and workflow examples
```



## Getting Started

### Prerequisites

Before using this DSL, ensure you have Python 3.8+ installed on your system.

Recommended: install and use [`uv`](https://github.com/astral-sh/uv) 

### Starting from scratch

1. ```uv init```
2. ```uv pip install https://github.com/RomainLefeuvre/samplingMiningWorkflowDSL.git```   

you can also use the published version on pypi
1. ```pip install sampling-mining-workflows-dsl```

### Template Repository

A complete template with examples is available at:
```
git@github.com:RomainLefeuvre/msr_papers_sampling_workflows.git
```

Clone the template to get started quickly:
```bash
git clone https://github.com/RomainLefeuvre/SamplinMiningWorkflowDSLTemplate.git
```


### Dev environment installation
If you want to contribute to this repository, you can clone and setup locally this project :

1. Clone this repository:
   ```bash
   git clone https://github.com/RomainLefeuvre/SamplingMiningWorflowDSL.git
   cd SamplingMiningWorflowDSL
   ```

2. (Recommended) Install dependencies with `uv`:
  ```bash
  uv sync
  ```

3. Activate the virtual environment created by `uv`:
  ```bash
  source .venv/bin/activate
  ```




<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Usage

### Basic Workflow Example

```python
from sampling_mining_workflows_dsl.WorkflowBuilder import WorkflowBuilder
from sampling_mining_workflows_dsl.element.loader.LoaderFactory import LoaderFactory
from sampling_mining_workflows_dsl.element.writer.WriterFactory import WritterFactory
from sampling_mining_workflows_dsl.metadata.Metadata import Metadata

# Define metadata for your data
id_metadata = Metadata.of_string("id")
language_metadata = Metadata.of_string("language")
commit_count_metadata = Metadata.of_integer("commitNb")

# Create loaders and writers
json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer

# Create a basic sampling workflow
workflow = (
    WorkflowBuilder()
    .input(json_loader("input_data.json", id_metadata, commit_count_metadata, language_metadata))
    .filter_operator("commitNb > 1000")
    .random_selection_operator(50)
    .output(json_writer("output_data.json"))
)

# Execute the workflow
results = workflow.execute_workflow()
```

<!-- LICENSE -->
## License

Distributed under the GNU General Public License v3.0. See `LICENSE` for more information.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

<p align="right">(<a href="#readme-top">back to top</a>)</p>









<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/RomainLefeuvre/SamplingMiningWorflowDSL.svg?style=for-the-badge
[contributors-url]: https://github.com/RomainLefeuvre/SamplingMiningWorflowDSL/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/RomainLefeuvre/SamplingMiningWorflowDSL.svg?style=for-the-badge
[forks-url]: https://github.com/RomainLefeuvre/SamplingMiningWorflowDSL/network/members
[stars-shield]: https://img.shields.io/github/stars/RomainLefeuvre/SamplingMiningWorflowDSL.svg?style=for-the-badge
[stars-url]: https://github.com/RomainLefeuvre/SamplingMiningWorflowDSL/stargazers
[issues-shield]: https://img.shields.io/github/issues/RomainLefeuvre/SamplingMiningWorflowDSL.svg?style=for-the-badge
[issues-url]: https://github.com/RomainLefeuvre/SamplingMiningWorflowDSL/issues
[license-shield]: https://img.shields.io/github/license/RomainLefeuvre/SamplingMiningWorflowDSL.svg?style=for-the-badge
[license-url]: https://github.com/RomainLefeuvre/SamplingMiningWorflowDSL/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
